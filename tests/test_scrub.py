"""Tests for scrub — the filter every byte of lane I/O passes through before
it may land in a tracked file (KEY-HANDLING.md §5; ask-lane-architecture pins).

The two families: secret-shape patterns (credential shapes + high-entropy
blobs) and the local private-context denylist (gitignored; mirrored from
ship.sh's gate). Hit reports carry pattern codes only — a scrub report that
quoted the matched secret would itself be a leak.
"""

from __future__ import annotations

from pathlib import Path

from bristlecone import scrub

# Test-only fabricated credential shapes — never real keys.
FAKE_OPENAI = "sk-" + "a1B2" * 12
FAKE_GITHUB = "ghp_" + "A" * 36
FAKE_AWS = "AKIA" + "J" * 16
FAKE_AGE = "AGE-SECRET" + "-KEY-1" + "Q" * 58  # split so the hygiene grep never matches source
FAKE_BEARER = "Bearer abc123DEF456ghi789JKL012mno345PQR678"


class TestSecretShapes:
    def test_openai_style_key_scrubbed(self):
        result = scrub.scrub(f"the key is {FAKE_OPENAI} ok")
        assert FAKE_OPENAI not in result.text
        assert "[SCRUBBED:" in result.text
        assert result.hits

    def test_github_token_scrubbed(self):
        result = scrub.scrub(f"token {FAKE_GITHUB}")
        assert FAKE_GITHUB not in result.text

    def test_aws_key_scrubbed(self):
        result = scrub.scrub(f"aws {FAKE_AWS}")
        assert FAKE_AWS not in result.text

    def test_age_secret_key_scrubbed(self):
        result = scrub.scrub(f"identity: {FAKE_AGE}")
        assert FAKE_AGE not in result.text

    def test_bearer_token_scrubbed(self):
        result = scrub.scrub(f"Authorization: {FAKE_BEARER}")
        assert FAKE_BEARER.split()[1] not in result.text

    def test_high_entropy_base64_blob_scrubbed(self):
        blob = "dGhpc0lzQVZlcnlTZWNyZXRCbG9iMTIzNDU2Nzg5MEFCQ0RFRmdoaWprbA"
        result = scrub.scrub(f"payload {blob} end")
        assert blob not in result.text

    def test_multiple_occurrences_all_scrubbed(self):
        result = scrub.scrub(f"{FAKE_GITHUB} and again {FAKE_GITHUB}")
        assert FAKE_GITHUB not in result.text


class TestFalsePositives:
    """Legit archive content must pass untouched — commit hashes above all."""

    def test_git_sha_untouched(self):
        sha = "dd793bd0aa11bb22cc33dd44ee55ff6677889900"
        result = scrub.scrub(f"first introduced in {sha}")
        assert result.text == f"first introduced in {sha}"
        assert not result.hits

    def test_sha256_hex_untouched(self):
        digest = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert scrub.scrub(digest).text == digest

    def test_ordinary_prose_untouched(self):
        prose = "The maintainer decided sops-exec-env-pinned after two rounds."
        result = scrub.scrub(prose)
        assert result.text == prose
        assert not result.hits

    def test_long_english_word_run_untouched(self):
        text = "Supercalifragilisticexpialidocious is not a credential"
        assert scrub.scrub(text).text == text

    def test_markdown_url_untouched(self):
        text = "see https://deluongo.github.io/bristlecone/ for the site"
        assert scrub.scrub(text).text == text


class TestDenylist:
    def test_denylist_literal_scrubbed(self):
        result = scrub.scrub("mentions ProjectHush here", denylist=("ProjectHush",))
        assert "ProjectHush" not in result.text
        assert "denylist" in "".join(result.hits)

    def test_denylist_case_insensitive(self):
        result = scrub.scrub("mentions PROJECTHUSH here", denylist=("projecthush",))
        assert "PROJECTHUSH" not in result.text

    def test_marker_never_contains_the_literal(self):
        result = scrub.scrub("x SecretName y", denylist=("SecretName",))
        assert "SecretName" not in result.text

    def test_hits_never_contain_matched_text(self):
        result = scrub.scrub(f"k={FAKE_OPENAI} n=ProjectHush", denylist=("ProjectHush",))
        joined = "".join(result.hits)
        assert FAKE_OPENAI not in joined
        assert "ProjectHush" not in joined


class TestLoadDenylist:
    def test_missing_file_is_empty(self, tmp_path: Path):
        assert scrub.load_denylist(tmp_path / "absent.txt") == ()

    def test_blank_lines_and_comments_skipped(self, tmp_path: Path):
        listing = tmp_path / "deny.txt"
        listing.write_text("# comment\n\nTermOne\n  TermTwo  \n")
        assert scrub.load_denylist(listing) == ("TermOne", "TermTwo")


class TestIdempotence:
    def test_scrubbing_scrubbed_text_is_stable(self):
        once = scrub.scrub(f"key {FAKE_OPENAI}", denylist=("ProjectHush",))
        twice = scrub.scrub(once.text, denylist=("ProjectHush",))
        assert twice.text == once.text
        assert not twice.hits
