"""Tests for gitio — spec §4 append-only enforcement and commit stamps.

Every test builds a real throwaway git repository, because the unit under test
IS the git behavior: the red-team test runs the exact command CI runs and
proves an illegal edit to a decided record is blocked.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

from bristlecone import gitio, records
from bristlecone.__main__ import main

DECIDED = """\
+++
type = "deliberation"
date = 2026-08-20
question = "Pick a name"
status = "decided"

[[positions]]
by = "model-a"
stance = "yes"

[outcome]
decision = "yes"
decided_by = "operator"
decided_date = 2026-08-20
+++

## Context

Decided; frozen per spec §4.
"""

OPEN = """\
+++
type = "deliberation"
date = 2026-08-20
question = "Still deliberating"
status = "open"
+++

## Context

Open; edit freely.
"""

HANDOFF = """\
+++
type = "handoff"
date = 2026-08-20
from = "model-a"
+++

## State of work

Done.
"""


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), "-c", "commit.gpgsign=false", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout


def write_record(repo: Path, name: str, text: str) -> Path:
    path = repo / "records" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def commit_all(repo: Path, message: str) -> None:
    git(repo, "add", "-A")
    git(repo, "commit", "-m", message)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-b", "main")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "config", "user.name", "test")
    write_record(tmp_path, "2026-08-20-name.md", DECIDED)
    write_record(tmp_path, "2026-08-20-open.md", OPEN)
    write_record(tmp_path, "2026-08-20-handoff.md", HANDOFF)
    commit_all(tmp_path, "founding")
    return tmp_path


def check(repo: Path, range_spec: str = "HEAD~1..HEAD") -> list:
    return gitio.check_range(repo, range_spec)


# --- legal changes ---------------------------------------------------------


def test_new_record_passes(repo: Path) -> None:
    write_record(repo, "2026-08-21-new.md", OPEN)
    commit_all(repo, "add record")
    assert check(repo) == []


def test_superseded_by_added_when_absent(repo: Path) -> None:
    text = DECIDED.replace(
        'status = "decided"', 'status = "decided"\nsuperseded_by = ["2026-08-20-open"]'
    )
    write_record(repo, "2026-08-20-name.md", text)
    commit_all(repo, "link successor")
    assert check(repo) == []


def test_superseded_by_appended_to_existing(repo: Path) -> None:
    base = DECIDED.replace('status = "decided"', 'status = "decided"\nsuperseded_by = ["a"]')
    write_record(repo, "2026-08-20-name.md", base)
    commit_all(repo, "first successor")
    write_record(
        repo,
        "2026-08-20-name.md",
        base.replace('superseded_by = ["a"]', 'superseded_by = ["a", "b"]'),
    )
    commit_all(repo, "second successor")
    assert check(repo) == []


def test_status_to_superseded(repo: Path) -> None:
    write_record(
        repo, "2026-08-20-name.md", DECIDED.replace('status = "decided"', 'status = "superseded"')
    )
    commit_all(repo, "supersede")
    assert check(repo) == []


def test_status_to_withdrawn_with_append(repo: Path) -> None:
    text = DECIDED.replace(
        'status = "decided"', 'status = "withdrawn"\nsuperseded_by = ["2026-08-20-open"]'
    )
    write_record(repo, "2026-08-20-name.md", text)
    commit_all(repo, "withdraw + link")
    assert check(repo) == []


def test_open_record_edits_freely(repo: Path) -> None:
    write_record(repo, "2026-08-20-open.md", OPEN.replace("Open; edit freely.", "Rewritten."))
    commit_all(repo, "rework open record")
    assert check(repo) == []


def test_subdirectory_move_same_stem_allowed(repo: Path) -> None:
    (repo / "records" / "founding").mkdir()
    git(repo, "mv", "records/2026-08-20-name.md", "records/founding/2026-08-20-name.md")
    commit_all(repo, "reorganize")
    assert check(repo) == []


# --- illegal changes -------------------------------------------------------


def test_red_team_decided_body_edit_blocked_by_ci_command(repo: Path, capsys) -> None:
    """THE red-team drill: branch off, rewrite a decided record's body, and run
    the exact invocation ci.yml runs. It must block (exit 1)."""
    git(repo, "checkout", "-b", "red-team")
    write_record(
        repo,
        "2026-08-20-name.md",
        DECIDED.replace("Decided; frozen per spec §4.", "History now reads better."),
    )
    commit_all(repo, "improve the record")
    exit_code = main(["validate", "--repo", str(repo), "--git-range", "main...red-team"])
    assert exit_code == 1
    assert "frozen-edit" in capsys.readouterr().out


def test_front_matter_change_blocked(repo: Path) -> None:
    write_record(
        repo, "2026-08-20-name.md", DECIDED.replace('question = "Pick a name"', 'question = "?"')
    )
    commit_all(repo, "reword question")
    findings = check(repo)
    assert [f.code for f in findings] == ["frozen-edit"]
    assert "front matter" in findings[0].message


def test_superseded_by_truncation_blocked(repo: Path) -> None:
    base = DECIDED.replace('status = "decided"', 'status = "decided"\nsuperseded_by = ["a", "b"]')
    write_record(repo, "2026-08-20-name.md", base)
    commit_all(repo, "two successors")
    write_record(
        repo,
        "2026-08-20-name.md",
        base.replace('superseded_by = ["a", "b"]', 'superseded_by = ["b"]'),
    )
    commit_all(repo, "drop one")
    assert [f.code for f in check(repo)] == ["frozen-edit"]


def test_status_regression_blocked(repo: Path) -> None:
    write_record(
        repo, "2026-08-20-name.md", DECIDED.replace('status = "decided"', 'status = "open"')
    )
    commit_all(repo, "reopen")
    findings = check(repo)
    assert [f.code for f in findings] == ["frozen-edit"]
    assert "status" in findings[0].message


def test_deletion_blocked(repo: Path) -> None:
    git(repo, "rm", "records/2026-08-20-open.md")
    commit_all(repo, "delete")
    assert [f.code for f in check(repo)] == ["record-deleted"]


def test_rename_blocked(repo: Path) -> None:
    git(repo, "mv", "records/2026-08-20-name.md", "records/2026-08-20-renamed.md")
    commit_all(repo, "rename")
    assert [f.code for f in check(repo)] == ["record-renamed"]


def test_handoff_edit_blocked(repo: Path) -> None:
    write_record(repo, "2026-08-20-handoff.md", HANDOFF.replace("Done.", "Not done."))
    commit_all(repo, "amend handoff")
    assert [f.code for f in check(repo)] == ["frozen-edit"]


def test_unparseable_old_version_fails_closed(repo: Path) -> None:
    write_record(repo, "broken.md", "no fences at all\n")
    commit_all(repo, "add broken")
    write_record(repo, "broken.md", "still no fences\n")
    commit_all(repo, "edit broken")
    assert [f.code for f in check(repo)] == ["frozen-indeterminate"]


def test_frozen_made_unparseable_blocked(repo: Path) -> None:
    write_record(repo, "2026-08-20-name.md", "+++\nnot toml ===\n")
    commit_all(repo, "corrupt")
    assert [f.code for f in check(repo)] == ["frozen-edit"]


def test_changes_outside_records_ignored(repo: Path) -> None:
    (repo / "README.md").write_text("anything\n", encoding="utf-8")
    commit_all(repo, "readme")
    assert check(repo) == []


# --- ranges ----------------------------------------------------------------


def test_three_dot_uses_merge_base(repo: Path) -> None:
    git(repo, "checkout", "-b", "side")
    write_record(repo, "2026-08-21-side.md", OPEN)
    commit_all(repo, "side work")
    git(repo, "checkout", "main")
    write_record(repo, "2026-08-21-main-moved.md", OPEN)
    commit_all(repo, "main advances")
    assert gitio.check_range(repo, "main...side") == []


def test_range_without_dots_rejected(repo: Path) -> None:
    with pytest.raises(gitio.GitError, match="BASE..HEAD"):
        gitio.check_range(repo, "main")


def test_range_with_empty_side_rejected(repo: Path) -> None:
    with pytest.raises(gitio.GitError, match="BASE..HEAD"):
        gitio.check_range(repo, "..main")


def test_git_failure_raises(tmp_path: Path) -> None:
    with pytest.raises(gitio.GitError):
        gitio.check_range(tmp_path, "a..b")


# --- stamps ----------------------------------------------------------------


def test_first_commit_stamps(repo: Path) -> None:
    paths = records.scan_tree(repo / "records")
    stamps = gitio.first_commit_stamps(repo, paths)
    first_sha = git(repo, "log", "--format=%h", "--reverse").splitlines()[0]
    assert stamps["2026-08-20-name"].sha == first_sha
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamps["2026-08-20-name"].date)


def test_stamps_follow_subdirectory_moves(repo: Path) -> None:
    original = gitio.first_commit_stamps(repo, records.scan_tree(repo / "records"))
    (repo / "records" / "founding").mkdir()
    git(repo, "mv", "records/2026-08-20-name.md", "records/founding/2026-08-20-name.md")
    commit_all(repo, "reorganize")
    moved = gitio.first_commit_stamps(repo, records.scan_tree(repo / "records"))
    assert moved["2026-08-20-name"] == original["2026-08-20-name"]


def test_uncommitted_record_has_no_stamp(repo: Path) -> None:
    write_record(repo, "2026-08-21-uncommitted.md", OPEN)
    stamps = gitio.first_commit_stamps(repo, records.scan_tree(repo / "records"))
    assert "2026-08-21-uncommitted" not in stamps


def test_head_commit(repo: Path) -> None:
    stamp = gitio.head_commit(repo)
    assert stamp.sha == git(repo, "log", "-1", "--format=%h").strip()


# --- CLI wiring ------------------------------------------------------------


def test_cli_git_range_legal_change_exits_zero(repo: Path, capsys) -> None:
    write_record(repo, "2026-08-21-new.md", OPEN)
    commit_all(repo, "add record")
    assert main(["validate", "--repo", str(repo), "--git-range", "HEAD~1..HEAD"]) == 0
    assert "append-only" in capsys.readouterr().out


def test_cli_git_range_rejects_paths(repo: Path, capsys) -> None:
    assert main(["validate", "--git-range", "a..b", str(repo / "records")]) == 2


def test_cli_validate_requires_paths_or_range(capsys) -> None:
    assert main(["validate"]) == 2


def test_cli_git_range_outside_repo_exits_two(tmp_path: Path, capsys) -> None:
    assert main(["validate", "--repo", str(tmp_path), "--git-range", "a..b"]) == 2
    assert "bristlecone:" in capsys.readouterr().err


def test_cli_render_stamps(repo: Path, tmp_path: Path, capsys) -> None:
    out = tmp_path / "site"
    assert main(["render", str(repo / "records"), "-o", str(out), "--stamps"]) == 0
    page = (out / "2026-08-20-name.html").read_text(encoding="utf-8")
    head = gitio.head_commit(repo)
    assert head.sha in page
    index = (out / "index.html").read_text(encoding="utf-8")
    assert head.sha in index


def test_cli_render_stamps_with_relative_records_dir(repo: Path, monkeypatch, capsys) -> None:
    """Regression: a relative RECORDS_DIR must still stamp (git -C moves the cwd,
    so pathspecs have to be absolute)."""
    monkeypatch.chdir(repo)
    assert main(["render", "records", "-o", "site", "--stamps"]) == 0
    page = (repo / "site" / "2026-08-20-name.html").read_text(encoding="utf-8")
    assert gitio.head_commit(repo).sha in page
    assert "not yet committed" not in page


def test_cli_render_stamps_outside_repo_exits_two(tmp_path: Path, capsys) -> None:
    tree = tmp_path / "records"
    tree.mkdir()
    assert main(["render", str(tree), "-o", str(tmp_path / "site"), "--stamps"]) == 2
