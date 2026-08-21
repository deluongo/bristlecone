"""Git-backed enforcement of spec §4 — the only module that shells out.

Two jobs. ``check_range`` proves append-only semantics across a commit range:
deletions and renames under ``records/`` always fail; a record whose pre-change
version was frozen (terminal status, or any handoff/succession) admits only the
permitted edits — appending to ``superseded_by`` and moving ``status`` to
``superseded``/``withdrawn``. ``first_commit_stamps`` finds each record's
first-introduced commit for rendered pages.

Interpretive pins, chosen fail-closed and fixed by the test suite:

- A rename that keeps the filename (a move between subdirectories) is legal —
  spec §2 says moving a file does not change its ID; §4's rename ban is read as
  banning ID changes. Content changes during a move still face the frozen check.
- Legality of a frozen edit is judged semantically (parsed front matter equal
  outside the two permitted keys, body byte-identical), so reflowing TOML
  whitespace is tolerated but no wording change is.
- If the pre-change version does not parse, its frozen state is unknowable, so
  the modification fails closed (``frozen-indeterminate``).
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from . import records
from .validate import Finding

TERMINAL_STATUSES = frozenset({"decided", "unresolved", "superseded", "withdrawn"})
ALWAYS_FROZEN_TYPES = frozenset({"handoff", "succession"})
PERMITTED_KEYS = ("superseded_by", "status")


class GitError(RuntimeError):
    """git failed or the range is malformed — an environment error, exit 2."""


@dataclass(frozen=True)
class Stamp:
    """One commit reference for display: abbreviated SHA + author date."""

    sha: str
    date: str


def check_range(repo: Path, range_spec: str) -> list[Finding]:
    """Append-only findings for ``records/`` changes across the range.

    Accepts ``BASE..HEAD`` (exact endpoints) or ``BASE...HEAD`` (from the
    merge base, the pull-request shape).
    """
    base, head = _resolve_range(repo, range_spec)
    out = _git(repo, "diff", "--name-status", "-z", "-M", base, head, "--", "records/")
    findings: list[Finding] = []
    for code, old_path, new_path in _parse_name_status(out):
        findings.extend(_check_change(repo, base, head, code, old_path, new_path))
    return findings


def first_commit_stamps(repo: Path, paths: list[Path]) -> dict[str, Stamp]:
    """Record ID -> first-introduced commit (spec §4 page stamps). ``--follow``
    keeps a record's original stamp across subdirectory moves. Uncommitted
    files get no entry."""
    stamps: dict[str, Stamp] = {}
    for path in paths:
        # Absolute pathspec: ``git -C repo`` moves the cwd, which would strand a
        # caller's relative paths (the CLI passes the records dir itself as repo).
        out = _git(
            repo, "log", "--follow", "--diff-filter=A", "--format=%h %as", "--", str(path.resolve())
        ).splitlines()
        if out:
            sha, date = out[-1].split(" ", 1)
            stamps[path.stem] = Stamp(sha=sha, date=date)
    return stamps


def head_commit(repo: Path) -> Stamp:
    """The commit the site is built from, for the index footer."""
    sha, date = _git(repo, "log", "-1", "--format=%h %as").strip().split(" ", 1)
    return Stamp(sha=sha, date=date)


def _resolve_range(repo: Path, range_spec: str) -> tuple[str, str]:
    dots = "..." if "..." in range_spec else ".."
    base, _, head = range_spec.partition(dots)
    if not base or not head:
        raise GitError(f"range must be BASE..HEAD or BASE...HEAD, got '{range_spec}'")
    if dots == "...":
        base = _git(repo, "merge-base", base, head).strip()
    return base, head


def _parse_name_status(out: str) -> list[tuple[str, str, str]]:
    tokens = out.split("\0")
    entries: list[tuple[str, str, str]] = []
    i = 0
    while i < len(tokens):
        if not tokens[i]:
            i += 1
            continue
        code = tokens[i][0]
        if code in "RC":
            entries.append((code, tokens[i + 1], tokens[i + 2]))
            i += 3
        else:
            entries.append((code, tokens[i + 1], tokens[i + 1]))
            i += 2
    return entries


def _check_change(
    repo: Path, base: str, head: str, code: str, old_path: str, new_path: str
) -> list[Finding]:
    stem = PurePosixPath(new_path).stem
    if code == "D":
        return [Finding(stem, "record-deleted", f"'{old_path}' deleted — records/ is append-only")]
    if code == "R" and PurePosixPath(old_path).name != PurePosixPath(new_path).name:
        return [
            Finding(
                stem,
                "record-renamed",
                f"'{old_path}' renamed to '{new_path}' — a record's ID never changes (spec §2)",
            )
        ]
    if code in "AC" or not new_path.endswith(".md"):
        return []
    return _check_modified(repo, base, head, old_path, new_path)


def _check_modified(
    repo: Path, base: str, head: str, old_path: str, new_path: str
) -> list[Finding]:
    stem = PurePosixPath(new_path).stem
    try:
        old = records.parse_text(_git(repo, "show", f"{base}:{old_path}"), record_id=stem)
    except records.RecordParseError:
        return [
            Finding(
                stem,
                "frozen-indeterminate",
                "the pre-change version does not parse, so its frozen state is unknowable — "
                "failing closed (spec §4)",
            )
        ]
    if not _is_frozen(old.front):
        return []
    try:
        new = records.parse_text(_git(repo, "show", f"{head}:{new_path}"), record_id=stem)
    except records.RecordParseError:
        return [
            Finding(stem, "frozen-edit", "frozen record modified into a file that no longer parses")
        ]
    return _frozen_edit_findings(old, new)


def _is_frozen(front: dict) -> bool:
    return (
        front.get("type") in ALWAYS_FROZEN_TYPES or front.get("status") in TERMINAL_STATUSES
    )


def _frozen_edit_findings(old: records.Record, new: records.Record) -> list[Finding]:
    findings: list[Finding] = []
    if new.body != old.body:
        findings.append(
            Finding(
                new.id,
                "frozen-edit",
                "body changed on a frozen record — testimony stands (spec §4)",
            )
        )
    if _without_permitted(new.front) != _without_permitted(old.front):
        findings.append(
            Finding(
                new.id,
                "frozen-edit",
                "front matter changed beyond superseded_by/status on a frozen record (spec §4)",
            )
        )
    old_links = old.front.get("superseded_by", [])
    if new.front.get("superseded_by", [])[: len(old_links)] != old_links:
        findings.append(
            Finding(
                new.id, "frozen-edit", "superseded_by on a frozen record may only be appended to"
            )
        )
    new_status = new.front.get("status")
    if new_status != old.front.get("status") and new_status not in ("superseded", "withdrawn"):
        findings.append(
            Finding(
                new.id,
                "frozen-edit",
                "status on a frozen record may only move to superseded/withdrawn, "
                f"not '{new_status}'",
            )
        )
    return findings


def _without_permitted(front: dict) -> dict:
    return {k: v for k, v in front.items() if k not in PERMITTED_KEYS}


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=False
    )
    if proc.returncode != 0:
        raise GitError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout
