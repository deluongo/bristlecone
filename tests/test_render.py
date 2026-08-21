"""Renderer tests — the spec §6 renderer contract: lenient by default (a
malformed file renders as raw text behind a warning banner, never a crash),
dissent computed and presented first-class and unedited, full attribution
displayed, and the model-output disclaimer on every page."""

import html
from pathlib import Path

from bristlecone import render
from bristlecone.__main__ import main

REPO = Path(__file__).resolve().parent.parent
VALID = REPO / "spec" / "examples" / "valid"
INVALID = REPO / "spec" / "examples" / "invalid"
RECORDS = REPO / "records"

CANONICAL = "2026-01-15-canonical-deliberation"


def rendered(tmp_path: Path, root: Path) -> tuple[Path, list[Path]]:
    out = tmp_path / "site"
    return out, render.render_tree(root, out)


def dissent_panel(page: str) -> str:
    start = page.index('<section class="dissent">')
    return page[start : page.index("</section>", start)]


def test_render_tree_writes_index_plus_one_page_per_record(tmp_path: Path) -> None:
    out, written = rendered(tmp_path, VALID)
    assert {p.name for p in written} == {
        "index.html",
        f"{CANONICAL}.html",
        "2026-01-16-example-handoff.html",
        "2026-01-17-example-succession.html",
    }
    assert all(p.exists() for p in written)


def test_index_lists_records_newest_first_with_status_and_subject(tmp_path: Path) -> None:
    out, _ = rendered(tmp_path, VALID)
    index = (out / "index.html").read_text(encoding="utf-8")
    assert f'href="{CANONICAL}.html"' in index
    assert "decided" in index
    assert "tabs or spaces" in index
    assert index.index("2026-01-17-example-succession") < index.index(CANONICAL)
    assert render.DISCLAIMER in index


def test_dissent_is_computed_and_presented_unedited(tmp_path: Path) -> None:
    out, _ = rendered(tmp_path, VALID)
    panel = dissent_panel((out / f"{CANONICAL}.html").read_text(encoding="utf-8"))
    assert "other-model-large via vendor CLI" in panel  # the dissenter, display attribution
    assert "tabs" in panel  # its stance
    assert "Tabs encode intent, not appearance" in panel  # its body section, unedited
    assert "example-model-9b" not in panel  # agreeing positions stay out of the panel


def test_no_dissent_panel_without_an_outcome(tmp_path: Path) -> None:
    out, _ = rendered(tmp_path, VALID)
    page = (out / "2026-01-16-example-handoff.html").read_text(encoding="utf-8")
    assert '<section class="dissent">' not in page


def test_attribution_and_disclaimer_on_record_pages(tmp_path: Path) -> None:
    out, _ = rendered(tmp_path, VALID)
    page = (out / f"{CANONICAL}.html").read_text(encoding="utf-8")
    for fragment in ("exampleco", "example-model-9b", "9b-2026-01", "temperature=0.2"):
        assert fragment in page
    assert render.DISCLAIMER in page


def test_outcome_box_shows_decision_with_option_label(tmp_path: Path) -> None:
    out, _ = rendered(tmp_path, VALID)
    page = (out / f"{CANONICAL}.html").read_text(encoding="utf-8")
    assert "Space characters" in page
    assert "a. human" in page


def test_resolvable_link_becomes_anchor(tmp_path: Path) -> None:
    out, _ = rendered(tmp_path, VALID)
    page = (out / f"{CANONICAL}.html").read_text(encoding="utf-8")
    assert '<a href="2026-01-16-example-handoff.html">' in page


def test_dangling_link_is_marked_broken_not_fatal(tmp_path: Path) -> None:
    out, _ = rendered(tmp_path, INVALID)
    page = (out / "dangling-link.html").read_text(encoding="utf-8")
    assert 'class="broken-link"' in page
    assert "2099-12-31-record-that-does-not-exist" in page


def test_malformed_record_renders_raw_with_warning_banner(tmp_path: Path) -> None:
    out, _ = rendered(tmp_path, INVALID)  # must not raise
    page = (out / "broken-toml.html").read_text(encoding="utf-8")
    raw = (INVALID / "broken-toml.md").read_text(encoding="utf-8")
    assert 'class="warning"' in page
    assert html.escape(raw) in page  # the whole file, escaped, as raw text
    index = (out / "index.html").read_text(encoding="utf-8")
    assert 'href="broken-toml.html"' in index


def test_wrong_shapes_in_front_matter_never_crash(tmp_path: Path) -> None:
    tree = tmp_path / "tree"
    tree.mkdir()
    (tree / "wrong-shapes.md").write_text(
        '+++\ntype = "deliberation"\ndate = 2026-01-01\nquestion = "shapes"\n'
        'status = "open"\ntags = "not-a-list"\npositions = "not-a-list"\n'
        'outcome = "not-a-table"\n+++\n\nbody\n',
        encoding="utf-8",
    )
    (tree / "unmatched-dissenter.md").write_text(
        '+++\ntype = "deliberation"\ndate = 2026-01-02\nquestion = "q"\nstatus = "decided"\n\n'
        '[[positions]]\nby = "hand-writer"\n\n'
        '[[positions]]\nby = "nobody in the body"\nstance = "b"\n\n'
        '[outcome]\ndecision = "a"\ndecided_by = "x"\ndecided_date = 2026-01-03\n+++\n\nbody\n',
        encoding="utf-8",
    )
    out, written = rendered(tmp_path, tree)
    assert len(written) == 3
    shapes = (out / "wrong-shapes.html").read_text(encoding="utf-8")
    assert "shapes" in shapes
    assert '<section class="dissent">' not in shapes
    dissenter = (out / "unmatched-dissenter.html").read_text(encoding="utf-8")
    assert "nobody in the body" in dissent_panel(dissenter)


def test_real_archive_renders_with_operator_dissent_first_class(tmp_path: Path) -> None:
    out, written = rendered(tmp_path, RECORDS)
    assert len(written) == 10  # index + the 9 founding records
    treasury = (out / "2026-08-20-treasury-allocation.html").read_text(encoding="utf-8")
    panel = dissent_panel(treasury)
    assert "deluongo (human operator)" in panel
    assert "People will give you bitcoin" in panel  # the operator's words, unedited


def test_cli_render_exit_contract(tmp_path: Path) -> None:
    out = tmp_path / "site"
    assert main(["render", str(VALID), "--out", str(out)]) == 0
    assert (out / "index.html").exists()
    assert main(["render", str(tmp_path / "missing"), "--out", str(out)]) == 2
