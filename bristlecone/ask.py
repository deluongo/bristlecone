"""Ask orchestrator — fan one open record's question out to configured lanes
and fill attributed positions back in. Pipeline order is the design pin from
records/2026-08-21-ask-lane-architecture.md (gpt lane, adopted verbatim):

    build prompt -> outbound scrub gate -> transport -> parse/validate ->
    at most one repair reprompt (through the same outbound gate) ->
    inbound scrub -> commit attributed positions

Boundary discipline (pins fixed by tests):

- **Never creates or decides a record.** Ask edits exactly one existing
  ``deliberation`` record with ``status = "open"`` (spec §4: open records are
  freely editable) and only ever APPENDS ``[[positions]]`` stanzas and
  ``## Position:`` body sections. It never touches ``[outcome]`` or ``status``.
- **Outbound gate is fail-closed**: if the built prompt trips any scrub filter
  (secret shape or private-context denylist), nothing is dispatched to any
  lane — the block report carries pattern codes only, never matched text.
- **Inbound scrub before commit**: raw lane output stays in memory; every byte
  that lands in the record has passed :func:`bristlecone.scrub.scrub`.
- **Independence**: the prompt carries the record's question, options, and
  ``## Context`` section only — never other lanes' positions.
- **Capture honesty (spec §3.1)**: failed lanes are recorded as failed in
  ``gathered`` — no stance, nothing fabricated, no silent resampling. A reply
  that fails the format after its one repair is preserved unedited (scrubbed)
  in the body. Stance case-normalization is noted in ``gathered``.
- Metering is not handled here: metered lanes decline at the gate inside
  ``lanes.run`` while KEY-HANDLING is unapproved; keyed transport and its
  spend caps live only in the operator-pinned client (KEY-HANDLING.md §3).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from . import lanes as _lanes
from . import records, scrub
from .laneconfig import Lane

REPAIR_SUFFIX = (
    "\n\nYour previous reply did not follow the required format. Reply again, "
    "following the format exactly, beginning with the STANCE: line."
)

_STANCE_RE = re.compile(r"^STANCE:\s*(.+?)\s*$", re.MULTILINE)
_CONTEXT_RE = re.compile(r"^## Context\s*\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
_RUNNABLE = frozenset({"ok", "dry-run"})


class AskError(Exception):
    """The record cannot support an ask (wrong type/status/shape) — usage-class."""


class OutboundBlocked(Exception):
    """The outbound gate fired: nothing was dispatched. Carries codes only."""

    def __init__(self, hits: tuple[str, ...]):
        super().__init__(f"outbound scrub gate: {', '.join(sorted(set(hits)))}")
        self.hits = hits


@dataclass(frozen=True)
class LaneReport:
    """One lane's outcome: filled[:repaired] | declined:* | failed:*."""

    lane: str
    status: str
    stance: str | None
    hits: tuple[str, ...]  # inbound scrub codes (never matched text)


@dataclass(frozen=True)
class AskResult:
    """Per-lane reports plus the assembled (re-parse-verified) record text."""

    reports: tuple[LaneReport, ...]
    text: str

    @property
    def all_filled(self) -> bool:
        return all(r.status.startswith("filled") for r in self.reports)


def run_ask(
    record: records.Record,
    lane_list: tuple[Lane, ...],
    denylist: tuple[str, ...] = (),
    *,
    dry_run: bool = False,
) -> AskResult:
    """Fan out to every lane and assemble the updated record text in memory.

    Writes nothing — the caller decides where (and whether) the text lands.
    Raises AskError for an un-askable record, OutboundBlocked from the gate.
    """
    option_ids = _askable_option_ids(record)
    prompt = build_prompt(record)
    _gate_outbound(prompt, denylist)
    taken = {p.get("label") for p in record.front.get("positions", [])}
    reports, stanzas, sections = [], [], []
    for lane in lane_list:
        report, stanza, section = _ask_lane(lane, prompt, option_ids, denylist, dry_run, taken)
        reports.append(report)
        stanzas.append(stanza)
        sections.append(section)
    text = _updated_text(record, stanzas, sections)
    return AskResult(reports=tuple(reports), text=text)


def build_prompt(record: records.Record) -> str:
    """Question + options + Context section only — independence by construction."""
    lines = [
        "You are one lane in a multi-model deliberation. Answer independently;",
        "you are not shown any other lane's position.",
        "",
        f"QUESTION: {record.front['question']}",
        "",
        "OPTIONS:",
    ]
    lines += [f"- {opt['id']}: {opt.get('label', '')}" for opt in record.front["options"]]
    context = _CONTEXT_RE.search(record.body)
    if context and context.group(1).strip():
        lines += ["", "CONTEXT:", "", context.group(1).strip()]
    lines += [
        "",
        "Reply in exactly this format:",
        "STANCE: <one option id from the list, or abstain>",
        "SUMMARY: <one sentence>",
        "ARGUMENTS: <your reasoning>",
    ]
    return "\n".join(lines)


def _askable_option_ids(record: records.Record) -> frozenset[str]:
    front = record.front
    if front.get("type") != "deliberation":
        raise AskError(f"{record.id}: ask fills deliberation records only")
    if front.get("status") != "open":
        raise AskError(
            f"{record.id}: status is {front.get('status')!r} — ask edits open records "
            "only; it never touches terminal records or decides one (spec §4)"
        )
    if not isinstance(front.get("question"), str) or not front["question"]:
        raise AskError(f"{record.id}: ask needs a non-empty question string")
    return _option_ids(record)


def _option_ids(record: records.Record) -> frozenset[str]:
    options = record.front.get("options")
    well_formed = isinstance(options, list) and all(
        isinstance(o, dict) and isinstance(o.get("id"), str) for o in options
    )
    if not options or not well_formed:
        raise AskError(f"{record.id}: ask needs a non-empty options list with string ids")
    return frozenset(o["id"] for o in options)


def _gate_outbound(prompt: str, denylist: tuple[str, ...]) -> None:
    hits = scrub.scrub(prompt, denylist).hits
    if hits:
        raise OutboundBlocked(hits)


def _ask_lane(
    lane: Lane,
    prompt: str,
    option_ids: frozenset[str],
    denylist: tuple[str, ...],
    dry_run: bool,
    taken: set,
) -> tuple[LaneReport, str | None, str | None]:
    if lane.name in taken:
        return LaneReport(lane.name, "declined:duplicate-label", None, ()), None, None
    result = _lanes.run(lane, prompt, dry_run=dry_run)
    repaired = False
    if result.status in _RUNNABLE and _parse_stance(result.text, option_ids)[0] is None:
        repair = prompt + REPAIR_SUFFIX
        _gate_outbound(repair, denylist)
        result = _lanes.run(lane, repair, dry_run=dry_run)
        repaired = True
    return _commit(lane, result, option_ids, denylist, dry_run=dry_run, repaired=repaired)


def _commit(
    lane: Lane,
    result: _lanes.LaneResult,
    option_ids: frozenset[str],
    denylist: tuple[str, ...],
    *,
    dry_run: bool,
    repaired: bool,
) -> tuple[LaneReport, str | None, str | None]:
    if result.status == "declined:gate":
        return LaneReport(lane.name, result.status, None, ()), None, None
    if result.status not in _RUNNABLE:
        gathered = f"bristlecone ask: {result.status} — lane failed; nothing fabricated"
        stanza = _toml_position(_position(lane, None, gathered))
        return LaneReport(lane.name, result.status, None, ()), stanza, None
    clean = scrub.scrub(result.text, denylist)
    stance, normalized = _parse_stance(clean.text, option_ids)
    if stance is None:
        return _commit_format_failure(lane, clean)
    gathered = _gathered(dry_run=dry_run, repaired=repaired, normalized=normalized)
    stanza = _toml_position(_position(lane, stance, gathered))
    status = "filled:repaired" if repaired else "filled"
    report = LaneReport(lane.name, status, stance, clean.hits)
    return report, stanza, _section(lane.name, clean.text)


def _commit_format_failure(
    lane: Lane, clean: scrub.ScrubResult
) -> tuple[LaneReport, str, str]:
    gathered = (
        "bristlecone ask: reply failed the required format after one repair "
        "reprompt; capture preserved unedited (scrubbed), not resampled"
    )
    section = _section(
        lane.name,
        clean.text,
        note="capture failed the required reply format; preserved unedited, not resampled",
    )
    stanza = _toml_position(_position(lane, None, gathered))
    return LaneReport(lane.name, "failed:format", None, clean.hits), stanza, section


def _parse_stance(text: str, option_ids: frozenset[str]) -> tuple[str | None, bool]:
    match = _STANCE_RE.search(text)
    if not match:
        return None, False
    raw = match.group(1).strip("`'\".")
    token = raw.lower()
    if token in option_ids or token == "abstain":
        return token, token != raw
    return None, False


def _gathered(*, dry_run: bool, repaired: bool, normalized: bool) -> str:
    base = (
        "bristlecone ask --dry-run: deterministic fixture; no transport touched"
        if dry_run
        else "bristlecone ask: single call, provider-default params"
    )
    if repaired:
        base += "; one format-repair reprompt"
    if normalized:
        base += "; stance case-normalized to the option id"
    return base


def _position(lane: Lane, stance: str | None, gathered: str) -> dict:
    position = {"label": lane.name, "by": f"{lane.model} via {lane.name} ({lane.route})"}
    if stance is not None:
        position["stance"] = stance
    position |= {
        "vendor": lane.vendor,
        "model": lane.model,
        "route": lane.route,
        "lane": lane.name,
        "gathered": gathered,
    }
    return position


def _toml_position(position: dict) -> str:
    # json.dumps escapes are a subset of TOML basic-string escapes, so every
    # value emitted here is a legal TOML string; the reparse in _updated_text
    # is the fail-closed check on that claim.
    lines = ["", "[[positions]]"]
    lines += [f"{key} = {json.dumps(value)}" for key, value in position.items()]
    return "\n".join(lines) + "\n"


def _section(label: str, text: str, note: str | None = None) -> str:
    parts = [f"\n## Position: {label}\n"]
    if note:
        parts.append(f"\n*({note})*\n")
    if text.strip():
        parts.append(f"\n{text.strip()}\n")
    return "".join(parts)


def _updated_text(
    record: records.Record, stanzas: list[str | None], sections: list[str | None]
) -> str:
    front_text = record.front_text
    if front_text and not front_text.endswith("\n"):
        front_text += "\n"
    front_text += "".join(s for s in stanzas if s)
    body = record.body.rstrip("\n") + "\n" + "".join(s for s in sections if s)
    text = records.serialize(
        records.Record(id=record.id, front=record.front, front_text=front_text, body=body)
    )
    records.parse_text(text, record.id)  # fail-closed: never emit an unparseable record
    return text
