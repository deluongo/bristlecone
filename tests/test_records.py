"""Envelope parse/serialize tests for bristlecone.records (spec §1–§2).

Corpus: spec/examples/ — every parseable fixture must round-trip byte-for-byte
(serialize(parse(text)) == text). broken-toml.md is the only unparseable fixture.
"""

from pathlib import Path

import pytest

from bristlecone import records

EXAMPLES = Path(__file__).resolve().parent.parent / "spec" / "examples"
ALL_FIXTURES = sorted(EXAMPLES.rglob("*.md"))
PARSEABLE = [p for p in ALL_FIXTURES if p.name not in {"README.md", "broken-toml.md"}]


def test_corpus_present() -> None:
    names = {p.name for p in ALL_FIXTURES}
    assert "2026-01-15-canonical-deliberation.md" in names
    assert "broken-toml.md" in names
    assert len(PARSEABLE) == 9


@pytest.mark.parametrize("path", PARSEABLE, ids=lambda p: p.stem)
def test_round_trip_byte_identical(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    rec = records.parse_text(text, record_id=path.stem, path=path)
    assert records.serialize(rec) == text


@pytest.mark.parametrize("path", PARSEABLE, ids=lambda p: p.stem)
def test_reparse_is_stable(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    rec = records.parse_text(text, record_id=path.stem)
    again = records.parse_text(records.serialize(rec), record_id=path.stem)
    assert again.front == rec.front
    assert again.body == rec.body
    assert again.front_text == rec.front_text


def test_id_is_filename_stem_and_front_preserved() -> None:
    path = EXAMPLES / "valid" / "2026-01-15-canonical-deliberation.md"
    rec = records.load_file(path)
    assert rec.id == "2026-01-15-canonical-deliberation"
    assert rec.front["type"] == "deliberation"
    assert rec.front["question"].startswith("Should the example project")
    # must-ignore rule: unknown keys are preserved, not dropped or rejected
    assert rec.front["review_priority"] == "low"
    assert len(rec.front["positions"]) == 3
    assert rec.front["outcome"]["decided_by"] == "a. human"
    assert "## Afterword" in rec.body


def test_missing_opening_fence_raises() -> None:
    with pytest.raises(records.RecordParseError, match="first line"):
        records.parse_text("type = 'x'\n", record_id="no-fence")


def test_missing_closing_fence_raises() -> None:
    with pytest.raises(records.RecordParseError, match="closing"):
        records.parse_text('+++\ntype = "handoff"\n', record_id="no-close")


def test_empty_file_raises() -> None:
    with pytest.raises(records.RecordParseError):
        records.parse_text("", record_id="empty")


def test_broken_toml_error_is_line_numbered_in_file_coordinates() -> None:
    """The unterminated string is on file line 2 (TOML line 1); the error must say line 2."""
    path = EXAMPLES / "invalid" / "broken-toml.md"
    with pytest.raises(records.RecordParseError, match=r"line 2\b") as exc:
        records.load_file(path)
    assert "TOML" in str(exc.value)


def test_load_file_sets_path() -> None:
    path = EXAMPLES / "valid" / "2026-01-16-example-handoff.md"
    rec = records.load_file(path)
    assert rec.path == path
    assert rec.front["from"] == "example-model-9b via localrunner (local)"
