"""Scrub — the filter every byte of lane I/O passes through before it may
land in a tracked file (KEY-HANDLING.md §5; ask-lane-architecture design pin:
scrub wraps transport, it never lives inside a transport kind).

Two filter families:

- **Secret shapes**: known credential grammars (vendor key prefixes, age
  identities, bearer tokens) plus a high-entropy-blob rule for keys with no
  recognizable prefix. The blob rule requires mixed case AND a digit, so the
  hex the archive legitimately traffics in (git commit SHAs, sha256
  fingerprints) never trips it.
- **Denylist**: literal private-context terms from a local, gitignored file —
  the same list ship.sh greps; matching is case-insensitive to mirror its
  ``grep -iF``.

Replacements are ``[SCRUBBED:<code>]`` markers. Hit reports carry pattern
codes only, never matched text — a scrub report that quoted the secret would
itself be a leak. Scrubbing is idempotent: markers contain nothing that
matches any filter.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

# Known credential grammars, most specific first. Codes are stable identifiers
# safe to publish; patterns are anchored on word boundaries so prose survives.
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    # The age pattern is split so the hygiene grep (ship.sh/CI) never sees a
    # contiguous credential shape in this file's own source.
    ("secret:age-identity", re.compile(r"\bAGE-SECRET" r"-KEY-1[A-Z0-9]{40,}\b")),
    ("secret:openai-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("secret:github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("secret:aws-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("secret:bearer", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}")),
)

# Candidate tokens for the entropy rule: long unbroken runs of base64-ish
# characters. Dots and colons break tokens, so URLs and hashes-with-context
# split into short harmless pieces.
_BLOB_CANDIDATE = re.compile(r"[A-Za-z0-9+/=_-]{32,}")
_BLOB_ENTROPY_BITS = 4.0

_MARKER = "[SCRUBBED:{code}]"


@dataclass(frozen=True)
class ScrubResult:
    """Scrubbed text plus the codes (never the text) of what fired."""

    text: str
    hits: tuple[str, ...]


def load_denylist(path: Path) -> tuple[str, ...]:
    """Read literal terms from a local denylist file; absent file = no terms.

    Blank lines and ``#`` comments are skipped; terms are stripped.
    """
    if not path.is_file():
        return ()
    lines = (line.strip() for line in path.read_text().splitlines())
    return tuple(line for line in lines if line and not line.startswith("#"))


def scrub(text: str, denylist: tuple[str, ...] = ()) -> ScrubResult:
    """Replace secret shapes and denylist literals with [SCRUBBED:*] markers."""
    hits: list[str] = []
    for code, pattern in SECRET_PATTERNS:
        text = _replace(pattern, text, code, hits)
    text = _scrub_entropy_blobs(text, hits)
    for term in denylist:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        text = _replace(pattern, text, "denylist", hits)
    return ScrubResult(text=text, hits=tuple(hits))


def _replace(pattern: re.Pattern[str], text: str, code: str, hits: list[str]) -> str:
    text, count = pattern.subn(_MARKER.format(code=code), text)
    hits.extend([code] * count)
    return text


def _scrub_entropy_blobs(text: str, hits: list[str]) -> str:
    def judge(match: re.Match[str]) -> str:
        token = match.group(0)
        if not _looks_like_secret(token):
            return token
        hits.append("secret:entropy")
        return _MARKER.format(code="secret:entropy")

    return _BLOB_CANDIDATE.sub(judge, text)


def _looks_like_secret(token: str) -> bool:
    """Mixed case + digit + high Shannon entropy; plain hex and words never qualify."""
    if not (
        any(c.islower() for c in token)
        and any(c.isupper() for c in token)
        and any(c.isdigit() for c in token)
    ):
        return False
    return _shannon_bits(token) >= _BLOB_ENTROPY_BITS


def _shannon_bits(token: str) -> float:
    counts = Counter(token)
    total = len(token)
    return -sum((n / total) * math.log2(n / total) for n in counts.values())
