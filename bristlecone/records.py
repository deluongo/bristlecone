"""Parse and serialize record files — the envelope grammar of spec §1–§2.

A record is one file: TOML front matter between `+++` fences, then a markdown
body. Parsing is lossless: the raw front-matter text is kept alongside the
parsed table, so ``serialize(parse_text(text, ...)) == text`` byte-for-byte for
any canonical file (LF line endings, fence lines exactly ``+++``). Records are
testimony — this module never rewrites what was written.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

FENCE = "+++"

#: Link-holding front-matter keys (spec §2); values are lists of record IDs.
LINK_KEYS = ("supersedes", "superseded_by", "relates_to", "cites")

#: Enforced ID grammar: lowercase alphanumerics in hyphen-separated runs.
#: The `YYYY-MM-DD-` prefix is convention (spec §2 says "Convention:"), not
#: enforced — the fixture matrix pins this: invalid-fixture filenames carry no
#: date prefix yet must fail only for their labeled defect.
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# The first front-matter line is file line 2 (line 1 is the opening fence).
_TOML_LINE_OFFSET = 1
_LINE_REF_RE = re.compile(r"\(at line (\d+),")


class RecordParseError(ValueError):
    """The file violates the envelope grammar or its front matter is not TOML."""


@dataclass(frozen=True)
class Record:
    """One parsed record. ``id`` is the filename stem; ``front`` is the parsed
    TOML table with unknown keys preserved (must-ignore rule)."""

    id: str
    front: dict
    front_text: str
    body: str
    path: Path | None = None


def parse_text(text: str, record_id: str, path: Path | None = None) -> Record:
    """Split the envelope and parse the front matter. Raises RecordParseError
    with file-coordinate line numbers on TOML failures."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != FENCE:
        raise RecordParseError(f"{record_id}: first line must be '{FENCE}'")
    close = next(
        (i for i, line in enumerate(lines[1:], start=1) if line.rstrip("\r\n") == FENCE),
        None,
    )
    if close is None:
        raise RecordParseError(f"{record_id}: closing '{FENCE}' fence not found")
    front_text = "".join(lines[1:close])
    body = "".join(lines[close + 1 :])
    try:
        front = tomllib.loads(front_text)
    except tomllib.TOMLDecodeError as exc:
        raise RecordParseError(
            f"{record_id}: front matter is not valid TOML: {_to_file_coordinates(str(exc))}"
        ) from exc
    return Record(id=record_id, front=front, front_text=front_text, body=body, path=path)


def load_file(path: Path) -> Record:
    """Parse one record file; its ID is the filename stem."""
    return parse_text(path.read_text(encoding="utf-8"), record_id=path.stem, path=path)


def serialize(record: Record) -> str:
    """Reassemble the canonical file text. Inverse of parse_text by construction."""
    return f"{FENCE}\n{record.front_text}{FENCE}\n{record.body}"


def scan_tree(root: Path) -> list[Path]:
    """All record files under ``root``, any depth, in stable order (spec §2)."""
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def _to_file_coordinates(message: str) -> str:
    """Shift tomllib's line references so they point at lines of the whole file
    (the fixture contract asks for a line-numbered error in file terms)."""

    def shift(match: re.Match[str]) -> str:
        return f"(at line {int(match.group(1)) + _TOML_LINE_OFFSET},"

    return _LINE_REF_RE.sub(shift, message)
