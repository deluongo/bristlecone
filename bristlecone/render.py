"""Lenient static-site renderer — the spec §6 renderer contract.

Emits ``index.html`` plus one page per record file. Dissent is computed, never
declared (spec §3.1): every position whose stance differs from the outcome's
decision is presented first-class and unedited in a panel of its own. A file
that fails to parse renders as raw text behind a warning banner — a foreign
record never crashes the site. Broken links are marked, not fatal. Commit
stamps (spec §4) arrive with the Pages deploy in M1-S3.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from . import minimark, records

DISCLAIMER = (
    "Positions in these records are a model's output under the recorded parameters — "
    "not a vendor's official view."
)

_CSS = (
    "body{font-family:system-ui,sans-serif;line-height:1.55;max-width:46rem;"
    "margin:2rem auto;padding:0 1rem;color:#222;background:#fff}"
    "a{color:#0b5394}h1{line-height:1.2}"
    ".meta{color:#666}"
    "pre{background:#f5f5f5;padding:.75rem;overflow-x:auto}"
    "code{background:#f5f5f5;padding:0 .2rem}"
    "blockquote{border-left:3px solid #ccc;margin:0.5rem 0;padding-left:1rem;color:#444}"
    "section{margin:1.5rem 0}"
    ".dissent{border-left:4px solid #b45309;background:#fff8eb;padding:.25rem 1rem}"
    ".outcome{border-left:4px solid #0b5394;background:#f0f6fb;padding:.25rem 1rem}"
    ".warning{border-left:4px solid #b91c1c;background:#fef2f2;padding:.5rem 1rem}"
    ".badge{background:#b45309;color:#fff;padding:0 .4rem;border-radius:.5rem;font-size:.8em}"
    ".broken-link{color:#b91c1c;text-decoration:line-through}"
    "table{border-collapse:collapse;width:100%}"
    "td,th{text-align:left;padding:.3rem .6rem;border-bottom:1px solid #eee;vertical-align:top}"
    "dl{display:grid;grid-template-columns:max-content 1fr;gap:.1rem .8rem;margin:.3rem 0}"
    "dt{color:#666}dd{margin:0}"
    "footer{margin-top:2rem;border-top:1px solid #eee;color:#666;font-size:.9em}"
)

_ATTRIBUTION_KEYS = ("stance", "vendor", "model", "model_version", "route", "lane", "gathered")


def render_tree(root: Path, out_dir: Path) -> list[Path]:
    """Render every record under ``root`` into ``out_dir``; returns written paths
    (index first). Never raises on record content — lenient by contract."""
    paths = records.scan_tree(root)
    known_ids = {p.stem for p in paths}
    out_dir.mkdir(parents=True, exist_ok=True)
    entries: list[tuple[str, dict | None]] = []
    written: list[Path] = []
    for path in paths:
        try:
            record = records.load_file(path)
            page = _record_page(record, known_ids)
            entries.append((record.id, record.front))
        except records.RecordParseError as exc:
            page = _malformed_page(path.stem, str(exc), path.read_text(encoding="utf-8"))
            entries.append((path.stem, None))
        target = out_dir / f"{path.stem}.html"
        target.write_text(page, encoding="utf-8")
        written.append(target)
    index = out_dir / "index.html"
    index.write_text(_index_page(entries), encoding="utf-8")
    return [index, *written]


def _record_page(record: records.Record, known_ids: set[str]) -> str:
    front = record.front
    title = front.get("question") or front.get("re") or front.get("occasion") or record.id
    parts = [
        '<p class="crumb"><a href="index.html">&larr; index</a></p>',
        f"<h1>{_text(title)}</h1>",
        _headline_meta(record.id, front),
        _links_html(front, known_ids),
        _outcome_html(front),
        _positions_html(front),
        _dissent_html(record),
        f'<article class="body">{minimark.to_html(record.body)}</article>',
        _footer(),
    ]
    return _page(record.id, "\n".join(p for p in parts if p))


def _malformed_page(stem: str, message: str, raw: str) -> str:
    body = "\n".join(
        (
            '<p class="crumb"><a href="index.html">&larr; index</a></p>',
            f"<h1>{_text(stem)}</h1>",
            f'<div class="warning">This file does not parse as a record ({_text(message)}). '
            "Shown unmodified as raw text — lenient mode, spec §6.</div>",
            f"<pre>{html.escape(raw)}</pre>",
            _footer(),
        )
    )
    return _page(stem, body)


def _index_page(entries: list[tuple[str, dict | None]]) -> str:
    newest_first = sorted(entries, key=lambda e: e[0], reverse=True)
    rows = [_index_row(rid, front) for rid, front in newest_first]
    table = (
        "<table><thead><tr><th>record</th><th>type</th><th>status</th><th>subject</th></tr>"
        f"</thead><tbody>{''.join(rows)}</tbody></table>"
    )
    body = f"<h1>Bristlecone — deliberation archive</h1>\n{table}\n{_footer()}"
    return _page("Bristlecone archive", body)


def _index_row(record_id: str, front: dict | None) -> str:
    link = f'<a href="{_text(record_id)}.html">{_text(record_id)}</a>'
    if front is None:
        cells = (link, '<span class="broken-link">unparseable</span>', "", "raw text, see page")
    else:
        subject = front.get("question") or front.get("re") or front.get("occasion") or ""
        cells = (link, _text(front.get("type", "")), _text(front.get("status", "")), _text(subject))
    return "<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>"


def _headline_meta(record_id: str, front: dict) -> str:
    bits = [record_id, front.get("type"), front.get("status"), front.get("date")]
    if front.get("class"):
        bits.append(f"Class {front['class']}")
    bits.extend(f"#{tag}" for tag in _as_list(front, "tags"))
    return '<p class="meta">' + " · ".join(_text(b) for b in bits if b) + "</p>"


def _links_html(front: dict, known_ids: set[str]) -> str:
    rows = [
        f"{key} → {_link_or_broken(str(target), known_ids)}"
        for key in records.LINK_KEYS
        for target in _as_list(front, key)
    ]
    return '<p class="links">' + "<br>".join(rows) + "</p>" if rows else ""


def _link_or_broken(target: str, known_ids: set[str]) -> str:
    if target in known_ids:
        return f'<a href="{_text(target)}.html">{_text(target)}</a>'
    return f'<span class="broken-link" title="not in this archive">{_text(target)}</span>'


def _outcome_html(front: dict) -> str:
    outcome = front.get("outcome")
    if not isinstance(outcome, dict):
        return ""
    label = _option_label(front, outcome.get("decision"))
    decision = _text(outcome.get("decision", "?")) + (f" — {_text(label)}" if label else "")
    rows = [f"<strong>Decision:</strong> {decision}"]
    rows.extend(
        f"<strong>{key.replace('_', ' ').capitalize()}:</strong> {_text(outcome[key])}"
        for key in ("decided_by", "decided_date", "authority", "rationale")
        if key in outcome
    )
    return '<section class="outcome"><h2>Outcome</h2><p>' + "<br>".join(rows) + "</p></section>"


def _option_label(front: dict, decision: object) -> str | None:
    for option in _as_list(front, "options"):
        if isinstance(option, dict) and option.get("id") == decision:
            return option.get("label")
    return None


def _positions_html(front: dict) -> str:
    positions = [p for p in _as_list(front, "positions") if isinstance(p, dict)]
    if not positions:
        return ""
    decision = _decision(front)
    items = "".join(_position_item(p, decision) for p in positions)
    return f'<section class="positions"><h2>Positions</h2>{items}</section>'


def _position_item(position: dict, decision: object) -> str:
    badge = ' <span class="badge">dissent</span>' if _is_dissent(position, decision) else ""
    return (
        '<article class="position">'
        f'<p><strong>{_text(position.get("by", "?"))}</strong>{badge}</p>'
        f"{_attribution(position)}</article>"
    )


def _attribution(position: dict) -> str:
    rows = [
        f"<dt>{key}</dt><dd>{_text(position[key])}</dd>"
        for key in _ATTRIBUTION_KEYS
        if key in position
    ]
    params = position.get("params")
    if isinstance(params, dict):
        rendered = ", ".join(f"{k}={v}" for k, v in params.items())
        rows.append(f"<dt>params</dt><dd>{_text(rendered)}</dd>")
    return f"<dl>{''.join(rows)}</dl>" if rows else ""


def _dissent_html(record: records.Record) -> str:
    decision = _decision(record.front)
    dissent = [
        p
        for p in _as_list(record.front, "positions")
        if isinstance(p, dict) and _is_dissent(p, decision)
    ]
    if not dissent:
        return ""
    blocks = []
    for position in dissent:
        section = _position_section(record.body, position)
        blocks.append(
            '<article class="position">'
            f'<p><strong>{_text(position.get("by", "?"))}</strong> — '
            f"stance: {_text(position.get('stance'))}</p>"
            f"{minimark.to_html(section) if section else ''}</article>"
        )
    return (
        '<section class="dissent"><h2>Dissent</h2>'
        "<p>Computed, not declared: positions whose stance differs from the outcome, "
        "presented unedited.</p>" + "".join(blocks) + "</section>"
    )


def _decision(front: dict) -> object:
    outcome = front.get("outcome")
    return outcome.get("decision") if isinstance(outcome, dict) else None


def _is_dissent(position: dict, decision: object) -> bool:
    return decision is not None and "stance" in position and position["stance"] != decision


def _position_section(body: str, position: dict) -> str:
    """The position's ``## Position: <label-or-by>`` body section, verbatim."""
    for key in ("label", "by"):
        name = position.get(key)
        if not name:
            continue
        pattern = rf"^## Position: {re.escape(str(name))}\s*$(.*?)(?=^## |\Z)"
        match = re.search(pattern, body, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1).strip()
    return ""


def _as_list(front: dict, key: str) -> list:
    value = front.get(key)
    return value if isinstance(value, list) else []


def _text(value: object) -> str:
    return html.escape(str(value))


def _footer() -> str:
    return f"<footer><p>{DISCLAIMER}</p></footer>"


def _page(title: str, body: str) -> str:
    return (
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{_text(title)}</title><style>{_CSS}</style></head>\n"
        f"<body><main>\n{body}\n</main></body></html>\n"
    )
