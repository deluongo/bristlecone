"""Minimal markdown → HTML for record bodies (stdlib-only).

Covers the subset record bodies actually use — ATX headings, paragraphs,
unordered/ordered lists, blockquotes, fenced code blocks, inline code, bold,
italic, links — and escapes all HTML. Unrecognized constructs degrade to plain
paragraphs. Link hrefs are restricted to http/https/mailto and relative paths:
a foreign record rendered in lenient mode must never inject script.
"""

from __future__ import annotations

import html
import re

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_ORDERED_RE = re.compile(r"^\d+\.\s+")
_QUOTE_MARK_RE = re.compile(r"^>\s?")
_CODE_SPAN_RE = re.compile(r"`([^`]+)`")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_ITALIC_RE = re.compile(r"\*(.+?)\*")
_STASH_RE = re.compile(r"\x00(\d+)\x00")


def to_html(text: str) -> str:
    """Render a whole body; blocks are emitted one per line."""
    return "\n".join(_block_html(kind, lines) for kind, lines in _blocks(text.split("\n")))


def _blocks(lines: list[str]) -> list[tuple[str, list[str]]]:
    """Group lines into (kind, lines) blocks: code | heading | quote | ul | ol | p."""
    out: list[tuple[str, list[str]]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("```"):
            close = next(
                (j for j in range(i + 1, len(lines)) if lines[j].startswith("```")), len(lines)
            )
            out.append(("code", lines[i + 1 : close]))
            i = close + 1
        elif _HEADING_RE.match(line):
            out.append(("heading", [line]))
            i += 1
        else:
            kind = _line_kind(line)
            j = i + 1
            while j < len(lines) and _continues(kind, lines[j]):
                j += 1
            out.append((kind, lines[i:j]))
            i = j
    return out


def _line_kind(line: str) -> str:
    if line.startswith(">"):
        return "quote"
    if line.startswith(("- ", "* ")):
        return "ul"
    if _ORDERED_RE.match(line):
        return "ol"
    return "p"


def _continues(kind: str, line: str) -> bool:
    return (
        bool(line.strip())
        and not line.startswith("```")
        and not _HEADING_RE.match(line)
        and _line_kind(line) == kind
    )


def _block_html(kind: str, lines: list[str]) -> str:
    if kind == "code":
        return f"<pre><code>{html.escape(chr(10).join(lines))}</code></pre>"
    if kind == "heading":
        match = _HEADING_RE.match(lines[0])
        assert match is not None  # _blocks only labels matching lines as headings
        level = len(match.group(1))
        return f"<h{level}>{_inline(match.group(2))}</h{level}>"
    if kind == "quote":
        inner = _inline("\n".join(_QUOTE_MARK_RE.sub("", line) for line in lines))
        return f"<blockquote><p>{inner}</p></blockquote>"
    if kind in ("ul", "ol"):
        items = "".join(f"<li>{_inline(_strip_marker(kind, line))}</li>" for line in lines)
        return f"<{kind}>{items}</{kind}>"
    return f"<p>{_inline(' '.join(line.strip() for line in lines))}</p>"


def _strip_marker(kind: str, line: str) -> str:
    return line[2:] if kind == "ul" else _ORDERED_RE.sub("", line)


def _inline(text: str) -> str:
    """Escape, then apply inline marks; code spans and links are stashed first
    so later passes cannot reformat their contents."""
    stash: list[str] = []

    def keep(fragment: str) -> str:
        stash.append(fragment)
        return f"\x00{len(stash) - 1}\x00"

    out = html.escape(text)
    out = _CODE_SPAN_RE.sub(lambda m: keep(f"<code>{m.group(1)}</code>"), out)
    out = _LINK_RE.sub(lambda m: keep(_link_html(m.group(1), m.group(2))), out)
    out = _BOLD_RE.sub(r"<strong>\1</strong>", out)
    out = _ITALIC_RE.sub(r"<em>\1</em>", out)
    return _STASH_RE.sub(lambda m: stash[int(m.group(1))], out)


def _link_html(label: str, href: str) -> str:
    # href arrives already HTML-escaped (quotes included), so it cannot break
    # out of the attribute; unsafe schemes degrade to the bare label.
    return f'<a href="{href}">{label}</a>' if _safe_href(href) else label


def _safe_href(href: str) -> bool:
    first_segment = href.split("/", 1)[0]
    if ":" not in first_segment:
        return True  # relative path
    return first_segment.split(":", 1)[0].lower() in ("http", "https", "mailto")
