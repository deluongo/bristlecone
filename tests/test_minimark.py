"""minimark covers the markdown subset record bodies actually use; all HTML is
escaped, and unsafe link schemes degrade to text — a foreign record rendered in
lenient mode must never inject script."""

from bristlecone.minimark import to_html


def test_heading_levels() -> None:
    assert to_html("## Context") == "<h2>Context</h2>"
    assert to_html("###### Deep") == "<h6>Deep</h6>"


def test_seven_hashes_is_not_a_heading() -> None:
    assert to_html("####### nope") == "<p>####### nope</p>"


def test_paragraph_joins_lines_and_applies_inline_marks() -> None:
    assert to_html("one *two*\n**three**") == "<p>one <em>two</em> <strong>three</strong></p>"


def test_document_blocks_are_separated() -> None:
    assert to_html("## H\n\npara") == "<h2>H</h2>\n<p>para</p>"


def test_code_span_contents_are_protected_from_inline_marks() -> None:
    assert to_html("`**not bold**`") == "<p><code>**not bold**</code></p>"


def test_html_is_escaped_everywhere() -> None:
    assert to_html("<b>hi</b>") == "<p>&lt;b&gt;hi&lt;/b&gt;</p>"
    assert to_html("```\n<script>\n```") == "<pre><code>&lt;script&gt;</code></pre>"


def test_fenced_code_block_keeps_blank_lines_and_markers() -> None:
    assert to_html("```\na\n\n- b\n```") == "<pre><code>a\n\n- b</code></pre>"


def test_unterminated_fence_swallows_rest_without_crashing() -> None:
    assert to_html("```\ncode to the end") == "<pre><code>code to the end</code></pre>"


def test_blockquote_with_inline_marks() -> None:
    assert (
        to_html("> quoted *words*\n> more")
        == "<blockquote><p>quoted <em>words</em>\nmore</p></blockquote>"
    )


def test_unordered_and_ordered_lists() -> None:
    assert to_html("- a\n- b") == "<ul><li>a</li><li>b</li></ul>"
    assert to_html("1. a\n2. b") == "<ol><li>a</li><li>b</li></ol>"


def test_safe_absolute_and_relative_links_render_anchors() -> None:
    assert (
        to_html("[site](https://example.org)")
        == '<p><a href="https://example.org">site</a></p>'
    )
    assert to_html("[rec](2026-01-15-x.html)") == '<p><a href="2026-01-15-x.html">rec</a></p>'


def test_unsafe_link_scheme_degrades_to_text() -> None:
    assert to_html("[x](javascript:doevil)") == "<p>x</p>"


def test_empty_input_renders_empty() -> None:
    assert to_html("") == ""
