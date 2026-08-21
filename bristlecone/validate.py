"""Fail-closed validator — the conformance contract of spec §6.

Fails on: required-core violations, the closed status vocabulary, ID grammar,
dangling links, duplicate IDs. Honors must-ignore for everything else: unknown
keys, unknown body sections, and unknown record types pass untouched.

Strict mode adds one check (spec §3.1): a position carrying a ``lane`` key is
tool-filled and must be fully attributed (``vendor``, ``model``, ``route``).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from . import records

STATUS_VOCAB = frozenset({"open", "decided", "unresolved", "superseded", "withdrawn"})
OUTCOME_REQUIRED = ("decision", "decided_by", "decided_date")
LANE_REQUIRED = ("vendor", "model", "route")

# Required front-matter cores per known type (spec §3). Unknown types get no
# type-specific checks — must-ignore.
REQUIRED_CORE = {
    "deliberation": ("date", "question", "status"),
    "handoff": ("date", "from"),
    "succession": ("date", "from"),
}


@dataclass(frozen=True)
class Finding:
    """One validation failure: which record, a stable code, and a message."""

    record: str
    code: str
    message: str


def validate_tree(root: Path, strict: bool = False) -> list[Finding]:
    """Validate every record under ``root``; links resolve within that tree."""
    return validate_files(records.scan_tree(root), strict=strict)


def validate_files(paths: list[Path], strict: bool = False) -> list[Finding]:
    """Validate the given files as one corpus (link targets = the given set)."""
    known_ids = {p.stem for p in paths}
    findings = [
        Finding(stem, "duplicate-id", f"{stem}: ID appears {n} times in the corpus")
        for stem, n in sorted(Counter(p.stem for p in paths).items())
        if n > 1
    ]
    for path in paths:
        findings.extend(validate_file(path, known_ids, strict=strict))
    return findings


def validate_file(path: Path, known_ids: set[str], strict: bool = False) -> list[Finding]:
    try:
        record = records.load_file(path)
    except records.RecordParseError as exc:
        return [Finding(path.stem, "parse-error", str(exc))]
    return validate_record(record, known_ids, strict=strict)


def validate_record(
    record: records.Record, known_ids: set[str], strict: bool = False
) -> list[Finding]:
    findings: list[Finding] = []
    if not records.ID_RE.match(record.id):
        findings.append(
            Finding(
                record.id,
                "id-grammar",
                f"'{record.id}' is not a legal ID (lowercase alphanumerics and hyphens)",
            )
        )
    _check_required_core(record, findings)
    _check_links(record, known_ids, findings)
    if record.front.get("type") == "deliberation":
        _check_deliberation(record, findings, strict=strict)
    return findings


def _check_required_core(record: records.Record, findings: list[Finding]) -> None:
    rtype = record.front.get("type")
    if rtype is None:
        _missing(record, "type", findings)
        return
    for key in REQUIRED_CORE.get(rtype, ()):
        if key not in record.front:
            _missing(record, key, findings)


def _check_deliberation(record: records.Record, findings: list[Finding], strict: bool) -> None:
    _check_status(record, findings)
    for i, position in enumerate(record.front.get("positions", [])):
        _check_position(record, i, position, findings, strict=strict)
    outcome = record.front.get("outcome")
    if outcome is not None:
        for key in OUTCOME_REQUIRED:
            if key not in outcome:
                _missing(record, f"outcome.{key}", findings)


def _check_status(record: records.Record, findings: list[Finding]) -> None:
    status = record.front.get("status")
    if status is not None and status not in STATUS_VOCAB:
        findings.append(
            Finding(
                record.id,
                "status-vocab",
                f"status '{status}' is not one of: {', '.join(sorted(STATUS_VOCAB))}",
            )
        )


def _check_position(
    record: records.Record, i: int, position: dict, findings: list[Finding], strict: bool
) -> None:
    if "by" not in position:
        _missing(record, f"positions[{i}].by", findings)
    if not strict or "lane" not in position:
        return
    for key in LANE_REQUIRED:
        if key not in position:
            findings.append(
                Finding(
                    record.id,
                    "lane-attribution",
                    f"positions[{i}] has lane '{position['lane']}' (tool-filled) "
                    f"but no '{key}' — tool-filled implies fully attributed",
                )
            )


def _check_links(record: records.Record, known_ids: set[str], findings: list[Finding]) -> None:
    for key in records.LINK_KEYS:
        for target in record.front.get(key, []):
            if target not in known_ids:
                findings.append(
                    Finding(
                        record.id,
                        "dangling-link",
                        f"{key} names '{target}', which exists nowhere in the corpus",
                    )
                )


def _missing(record: records.Record, field: str, findings: list[Finding]) -> None:
    findings.append(
        Finding(record.id, "missing-required", f"required field '{field}' is absent")
    )
