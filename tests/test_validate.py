"""Validator tests keyed to the fixture matrix in spec/examples/README.md.

Every row there is a test case: the 3 valid fixtures pass a fail-closed
validator; each invalid fixture fails for EXACTLY its labeled reason (a failure
for any other reason is itself a test failure). missing-lane-attribution fails
only under --strict.

Interpretive note (pinned by the matrix): the enforced ID grammar is the
character rule — lowercase alphanumerics and hyphens — because the invalid
fixtures' own filenames carry no YYYY-MM-DD- prefix yet must not fail for it.
The date prefix is convention (spec §2 "Convention:"), not validated.
"""

from pathlib import Path

import pytest

from bristlecone import validate
from bristlecone.__main__ import main

EXAMPLES = Path(__file__).resolve().parent.parent / "spec" / "examples"
VALID = EXAMPLES / "valid"
INVALID = EXAMPLES / "invalid"

# fixture stem -> (expected finding code, required message substring)
INVALID_MATRIX = {
    "broken-toml": ("parse-error", "TOML"),
    "missing-required-question": ("missing-required", "question"),
    "bad-status-vocab": ("status-vocab", "finalized"),
    "dangling-link": ("dangling-link", "2099-12-31-record-that-does-not-exist"),
    "Bad_ID_Grammar": ("id-grammar", "Bad_ID_Grammar"),
    "outcome-missing-decided-by": ("missing-required", "outcome.decided_by"),
}
STRICT_ONLY = {"missing-lane-attribution": ("lane-attribution", "example-lane")}


def findings_by_record(root: Path, strict: bool = False) -> dict[str, list[validate.Finding]]:
    grouped: dict[str, list[validate.Finding]] = {}
    for f in validate.validate_tree(root, strict=strict):
        grouped.setdefault(f.record, []).append(f)
    return grouped


def test_valid_tree_passes_default_and_strict() -> None:
    assert validate.validate_tree(VALID) == []
    assert validate.validate_tree(VALID, strict=True) == []


@pytest.mark.parametrize(
    ("stem", "expected"), sorted(INVALID_MATRIX.items()), ids=sorted(INVALID_MATRIX)
)
def test_invalid_fixture_fails_for_exactly_the_labeled_reason(
    stem: str, expected: tuple[str, str]
) -> None:
    code, substring = expected
    grouped = findings_by_record(INVALID)
    findings = grouped.get(stem, [])
    assert findings, f"{stem} produced no findings"
    assert {f.code for f in findings} == {code}, findings
    assert any(substring in f.message for f in findings), findings


def test_lane_attribution_passes_default_fails_strict_only() -> None:
    default = findings_by_record(INVALID)
    assert "missing-lane-attribution" not in default
    strict = findings_by_record(INVALID, strict=True)
    findings = strict["missing-lane-attribution"]
    assert {f.code for f in findings} == {"lane-attribution"}, findings
    # strict adds nothing else anywhere in the invalid tree
    for stem, (code, _) in INVALID_MATRIX.items():
        assert {f.code for f in strict[stem]} == {code}


def test_no_invalid_fixture_fails_for_an_unlabeled_reason() -> None:
    grouped = findings_by_record(INVALID, strict=True)
    labeled = set(INVALID_MATRIX) | set(STRICT_ONLY)
    assert set(grouped) == labeled


def test_position_missing_by_is_required_core(tmp_path: Path) -> None:
    (tmp_path / "2026-01-01-no-by.md").write_text(
        '+++\ntype = "deliberation"\ndate = 2026-01-01\nquestion = "q?"\nstatus = "open"\n'
        "[[positions]]\nstance = \"abstain\"\n+++\n\nbody\n",
        encoding="utf-8",
    )
    findings = validate.validate_tree(tmp_path)
    assert {f.code for f in findings} == {"missing-required"}
    assert any("positions[0].by" in f.message for f in findings)


def test_duplicate_ids_across_subdirectories_fail(tmp_path: Path) -> None:
    record = '+++\ntype = "handoff"\ndate = 2026-01-01\nfrom = "someone"\n+++\n\nbody\n'
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    (tmp_path / "a" / "2026-01-01-dup.md").write_text(record, encoding="utf-8")
    (tmp_path / "b" / "2026-01-01-dup.md").write_text(record, encoding="utf-8")
    findings = validate.validate_tree(tmp_path)
    assert {f.code for f in findings} == {"duplicate-id"}


def test_unknown_type_passes_by_must_ignore(tmp_path: Path) -> None:
    (tmp_path / "2026-01-01-future.md").write_text(
        '+++\ntype = "sometype-from-v9"\ndate = 2026-01-01\n+++\n\nbody\n', encoding="utf-8"
    )
    assert validate.validate_tree(tmp_path, strict=True) == []


def test_missing_type_fails(tmp_path: Path) -> None:
    (tmp_path / "2026-01-01-untyped.md").write_text(
        "+++\ndate = 2026-01-01\n+++\n\nbody\n", encoding="utf-8"
    )
    findings = validate.validate_tree(tmp_path)
    assert {f.code for f in findings} == {"missing-required"}
    assert any("type" in f.message for f in findings)


def test_links_resolve_across_subdirectories(tmp_path: Path) -> None:
    (tmp_path / "deep").mkdir()
    (tmp_path / "2026-01-01-one.md").write_text(
        '+++\ntype = "handoff"\ndate = 2026-01-01\nfrom = "x"\n'
        'relates_to = ["2026-01-02-two"]\n+++\n\nbody\n',
        encoding="utf-8",
    )
    (tmp_path / "deep" / "2026-01-02-two.md").write_text(
        '+++\ntype = "handoff"\ndate = 2026-01-02\nfrom = "y"\n+++\n\nbody\n', encoding="utf-8"
    )
    assert validate.validate_tree(tmp_path) == []


# --- CLI exit-code contract: 0 = valid, 1 = findings, 2 = usage/path error ---


def test_cli_valid_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["validate", str(VALID)]) == 0
    assert "OK" in capsys.readouterr().out


def test_cli_invalid_exits_one(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["validate", str(INVALID)]) == 1
    out = capsys.readouterr().out
    assert "status-vocab" in out


def test_cli_strict_flag(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["validate", "--strict", str(INVALID / "missing-lane-attribution.md")]) == 1
    assert main(["validate", str(INVALID / "missing-lane-attribution.md")]) == 0


def test_cli_missing_path_exits_two(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["validate", str(EXAMPLES / "does-not-exist")]) == 2


def test_cli_single_file_corpus_is_the_given_set() -> None:
    # a lone file that cites a record outside the given paths is dangling
    assert main(["validate", str(INVALID / "dangling-link.md")]) == 1
