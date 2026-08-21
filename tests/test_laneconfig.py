"""Tests for laneconfig — hand-editable TOML lane stanzas over exactly two
transport kinds (records/2026-08-21-ask-lane-architecture.md: lanes are DATA).

Fail-closed everywhere: unknown kinds, unknown keys (a typo like `metred`
silently un-metering a lane is the failure mode that matters), missing
attribution. One interpretive pin, fixed here: a keyless `openai-http` lane
must point at loopback — every remote HTTP endpoint is metered/BYOK territory,
which runs only from the operator-pinned client (KEY-HANDLING.md §3).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from bristlecone import laneconfig

VALID = """\
[lane.claude]
kind = "cmd"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
argv = ["claude", "-p", "{prompt}"]

[lane.qwen]
kind = "openai-http"
vendor = "alibaba"
model = "qwen2.5:3b-instruct"
route = "local"
base_url = "http://localhost:11434/v1"

[lane.deepseek]
kind = "openai-http"
vendor = "deepseek"
model = "deepseek-chat"
route = "metered-api"
base_url = "https://api.deepseek.com/v1"
metered = true
"""


def write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "lanes.toml"
    path.write_text(text)
    return path


class TestValidConfig:
    def test_parses_all_lanes(self, tmp_path: Path):
        lanes = laneconfig.load(write(tmp_path, VALID))
        assert [lane.name for lane in lanes] == ["claude", "qwen", "deepseek"]

    def test_cmd_lane_fields(self, tmp_path: Path):
        claude = laneconfig.load(write(tmp_path, VALID))[0]
        assert claude.kind == "cmd"
        assert claude.argv == ("claude", "-p", "{prompt}")
        assert claude.metered is False
        assert claude.stdin is False

    def test_http_lane_fields(self, tmp_path: Path):
        qwen = laneconfig.load(write(tmp_path, VALID))[1]
        assert qwen.kind == "openai-http"
        assert qwen.base_url == "http://localhost:11434/v1"

    def test_metered_flag(self, tmp_path: Path):
        deepseek = laneconfig.load(write(tmp_path, VALID))[2]
        assert deepseek.metered is True

    def test_remote_metered_endpoint_is_legal(self, tmp_path: Path):
        # metered lanes may name a remote host: they refuse at the gate anyway
        assert laneconfig.load(write(tmp_path, VALID))[2].base_url.startswith("https://")

    def test_stdin_mode(self, tmp_path: Path):
        text = """\
[lane.pipe]
kind = "cmd"
vendor = "anthropic"
model = "m"
route = "subscription-cli"
argv = ["some-cli"]
stdin = true
"""
        assert laneconfig.load(write(tmp_path, text))[0].stdin is True

    def test_timeout_default_and_override(self, tmp_path: Path):
        lanes = laneconfig.load(write(tmp_path, VALID + 'timeout = 30\n'))
        assert lanes[0].timeout == laneconfig.DEFAULT_TIMEOUT
        assert lanes[2].timeout == 30

    def test_repo_default_config_is_valid(self):
        lanes = laneconfig.load(Path(__file__).parent.parent / "lanes.toml")
        assert {lane.kind for lane in lanes} <= {"cmd", "openai-http"}
        metered = [lane for lane in lanes if lane.metered]
        assert all(lane.name == "deepseek" for lane in metered)


class TestFailClosed:
    def err(self, tmp_path: Path, text: str) -> str:
        with pytest.raises(laneconfig.ConfigError) as excinfo:
            laneconfig.load(write(tmp_path, text))
        return str(excinfo.value)

    def test_unknown_kind(self, tmp_path: Path):
        msg = self.err(
            tmp_path,
            '[lane.x]\nkind = "grpc"\nvendor = "v"\nmodel = "m"\nroute = "r"\n',
        )
        assert "kind" in msg

    def test_unknown_key_rejected(self, tmp_path: Path):
        msg = self.err(tmp_path, VALID.replace("metered = true", "metred = true"))
        assert "metred" in msg

    def test_cmd_requires_argv(self, tmp_path: Path):
        self.err(tmp_path, '[lane.x]\nkind = "cmd"\nvendor = "v"\nmodel = "m"\nroute = "r"\n')

    def test_cmd_argv_needs_placeholder_or_stdin(self, tmp_path: Path):
        msg = self.err(
            tmp_path,
            '[lane.x]\nkind = "cmd"\nvendor = "v"\nmodel = "m"\nroute = "r"\n'
            'argv = ["cli", "run"]\n',
        )
        assert "{prompt}" in msg

    def test_cmd_placeholder_and_stdin_conflict(self, tmp_path: Path):
        self.err(
            tmp_path,
            '[lane.x]\nkind = "cmd"\nvendor = "v"\nmodel = "m"\nroute = "r"\n'
            'argv = ["cli", "{prompt}"]\nstdin = true\n',
        )

    def test_http_requires_base_url(self, tmp_path: Path):
        self.err(
            tmp_path, '[lane.x]\nkind = "openai-http"\nvendor = "v"\nmodel = "m"\nroute = "r"\n'
        )

    def test_keyless_http_must_be_loopback(self, tmp_path: Path):
        msg = self.err(
            tmp_path,
            '[lane.x]\nkind = "openai-http"\nvendor = "v"\nmodel = "m"\nroute = "r"\n'
            'base_url = "https://api.example.com/v1"\n',
        )
        assert "loopback" in msg

    def test_missing_attribution(self, tmp_path: Path):
        msg = self.err(tmp_path, '[lane.x]\nkind = "cmd"\nargv = ["c", "{prompt}"]\n')
        assert "vendor" in msg

    def test_argv_must_be_strings(self, tmp_path: Path):
        self.err(
            tmp_path,
            '[lane.x]\nkind = "cmd"\nvendor = "v"\nmodel = "m"\nroute = "r"\nargv = [1, 2]\n',
        )

    def test_no_lanes_table(self, tmp_path: Path):
        self.err(tmp_path, 'title = "not a lane config"\n')

    def test_missing_file(self, tmp_path: Path):
        with pytest.raises(laneconfig.ConfigError):
            laneconfig.load(tmp_path / "absent.toml")

    def test_invalid_toml(self, tmp_path: Path):
        with pytest.raises(laneconfig.ConfigError):
            laneconfig.load(write(tmp_path, "[lane.x\n"))

    def test_lane_entry_not_a_table(self, tmp_path: Path):
        self.err(tmp_path, "[lane]\nx = 5\n")

    def test_nonpositive_timeout(self, tmp_path: Path):
        self.err(
            tmp_path,
            '[lane.x]\nkind = "cmd"\nvendor = "v"\nmodel = "m"\nroute = "r"\n'
            'argv = ["c", "{prompt}"]\ntimeout = 0\n',
        )

    def test_metered_wrong_type(self, tmp_path: Path):
        self.err(
            tmp_path,
            '[lane.x]\nkind = "cmd"\nvendor = "v"\nmodel = "m"\nroute = "r"\n'
            'argv = ["c", "{prompt}"]\nmetered = "yes"\n',
        )
