"""Tests for lanes — the two transports and their pins from
records/2026-08-21-ask-lane-architecture.md and KEY-HANDLING.md.

Load-bearing pins, each fixed by a test here:
- metered lanes refuse `declined:gate` while the KEY-HANDLING gate is closed;
- `--dry-run` replaces only the final transport: deterministic fixtures keyed
  by kind, and provably NO subprocess spawn, network call, or secret lookup;
- the in-repo `openai-http` transport NEVER sends an Authorization header —
  keys exist only inside the operator-pinned client, never repo code;
- `cmd` spawns argv without a shell, so metacharacters in prompts stay inert;
- failures are classified (`failed:<class>`), never fabricated content.
"""

from __future__ import annotations

import http.server
import json
import subprocess
import sys
import threading
import urllib.request
from pathlib import Path

import pytest

from bristlecone import laneconfig, lanes
from bristlecone.__main__ import main


def cmd_lane(argv: list[str], *, stdin: bool = False, timeout: float = 30.0) -> laneconfig.Lane:
    return laneconfig.Lane(
        name="test-cmd", kind="cmd", vendor="v", model="m", route="local",
        metered=False, timeout=timeout, argv=tuple(argv), stdin=stdin, base_url=None,
    )


def http_lane(base_url: str, *, metered: bool = False) -> laneconfig.Lane:
    return laneconfig.Lane(
        name="test-http", kind="openai-http", vendor="v", model="m", route="local",
        metered=metered, timeout=10.0, argv=None, stdin=False, base_url=base_url,
    )


ECHO = [sys.executable, "-c", "import sys; print('echo:' + sys.argv[1])", "{prompt}"]


class TestCmdTransport:
    def test_success(self):
        result = lanes.run(cmd_lane(ECHO), "hello")
        assert result.status == "ok"
        assert result.text.strip() == "echo:hello"

    def test_stdin_mode(self):
        lane = cmd_lane(
            [sys.executable, "-c", "import sys; print('got:' + sys.stdin.read())"], stdin=True
        )
        result = lanes.run(lane, "piped")
        assert result.status == "ok"
        assert result.text.strip() == "got:piped"

    def test_metacharacters_stay_inert(self):
        result = lanes.run(cmd_lane(ECHO), "x; touch /tmp/pwned && $(whoami) `id`")
        assert result.status == "ok"
        assert result.text.strip() == "echo:x; touch /tmp/pwned && $(whoami) `id`"

    def test_nonzero_exit_classified(self):
        lane = cmd_lane(
            [sys.executable, "-c", "import sys; sys.stderr.write('boom'); sys.exit(3)", "{prompt}"]
        )
        result = lanes.run(lane, "p")
        assert result.status == "failed:exit:3"
        assert "boom" in result.text  # raw stderr stays in memory for the caller to scrub

    def test_timeout_classified(self):
        lane = cmd_lane(
            [sys.executable, "-c", "import time; time.sleep(30)", "{prompt}"], timeout=0.5
        )
        assert lanes.run(lane, "p").status == "failed:timeout"

    def test_missing_binary_classified(self):
        result = lanes.run(cmd_lane(["definitely-not-a-real-binary-xyz", "{prompt}"]), "p")
        assert result.status == "failed:spawn"


class _Handler(http.server.BaseHTTPRequestHandler):
    response_code = 200
    response_body = b""
    seen_headers: list[dict] = []
    seen_bodies: list[dict] = []

    def do_POST(self):
        cls = type(self)
        cls.seen_headers.append(dict(self.headers))
        body = self.rfile.read(int(self.headers["Content-Length"]))
        cls.seen_bodies.append(json.loads(body))
        self.send_response(cls.response_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(cls.response_body)

    def log_message(self, *args):
        pass


@pytest.fixture
def server():
    class Handler(_Handler):
        seen_headers = []
        seen_bodies = []

    httpd = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield Handler, f"http://127.0.0.1:{httpd.server_address[1]}/v1"
    httpd.shutdown()


def ok_payload(content: str) -> bytes:
    return json.dumps({"choices": [{"message": {"content": content}}]}).encode()


class TestHttpTransport:
    def test_success(self, server):
        handler, base_url = server
        handler.response_body = ok_payload("the answer")
        result = lanes.run(http_lane(base_url), "the question")
        assert result.status == "ok"
        assert result.text == "the answer"

    def test_request_shape(self, server):
        handler, base_url = server
        handler.response_body = ok_payload("x")
        lanes.run(http_lane(base_url), "prompt-text")
        body = handler.seen_bodies[0]
        assert body["model"] == "m"
        assert body["messages"] == [{"role": "user", "content": "prompt-text"}]

    def test_never_sends_authorization_header(self, server):
        handler, base_url = server
        handler.response_body = ok_payload("x")
        lanes.run(http_lane(base_url), "p")
        sent = {k.lower() for k in handler.seen_headers[0]}
        assert "authorization" not in sent
        assert not any("key" in k or "token" in k for k in sent)

    def test_http_error_classified(self, server):
        handler, base_url = server
        handler.response_code = 500
        assert lanes.run(http_lane(base_url), "p").status == "failed:http:500"

    def test_bad_payload_classified(self, server):
        handler, base_url = server
        handler.response_body = b"not json"
        assert lanes.run(http_lane(base_url), "p").status == "failed:parse"

    def test_missing_content_classified(self, server):
        handler, base_url = server
        handler.response_body = json.dumps({"choices": []}).encode()
        assert lanes.run(http_lane(base_url), "p").status == "failed:parse"

    def test_non_string_content_classified(self, server):
        handler, base_url = server
        handler.response_body = json.dumps({"choices": [{"message": {"content": 5}}]}).encode()
        assert lanes.run(http_lane(base_url), "p").status == "failed:parse"

    def test_error_body_that_cannot_be_read_drains_empty(self):
        class BrokenBody:
            def read(self):
                raise OSError("connection died mid-body")

        assert lanes._drain(BrokenBody()) == ""

    def test_connection_refused_classified(self):
        result = lanes.run(http_lane("http://127.0.0.1:9/v1"), "p")
        assert result.status == "failed:network"


class TestMeteredGate:
    def test_metered_lane_refuses_real_run(self, server):
        handler, base_url = server
        result = lanes.run(http_lane(base_url, metered=True), "p")
        assert result.status == "declined:gate"
        assert handler.seen_bodies == []  # nothing left the machine

    def test_decline_happens_before_any_transport(self, monkeypatch):
        monkeypatch.setattr(urllib.request, "urlopen", _forbid("network"))
        monkeypatch.setattr(subprocess, "run", _forbid("subprocess"))
        result = lanes.run(http_lane("https://api.deepseek.com/v1", metered=True), "p")
        assert result.status == "declined:gate"


def _forbid(what: str):
    def guard(*args, **kwargs):
        raise AssertionError(f"{what} reached during a run that must not touch it")

    return guard


class TestDryRun:
    def test_deterministic(self):
        first = lanes.run(cmd_lane(ECHO), "same prompt", dry_run=True)
        second = lanes.run(cmd_lane(ECHO), "same prompt", dry_run=True)
        assert first.status == "dry-run"
        assert first.text == second.text

    def test_fixtures_keyed_by_kind(self, server):
        _, base_url = server
        by_cmd = lanes.run(cmd_lane(ECHO), "p", dry_run=True)
        by_http = lanes.run(http_lane(base_url), "p", dry_run=True)
        assert by_cmd.text != by_http.text
        assert "cmd" in by_cmd.text and "openai-http" in by_http.text

    def test_no_spawn_no_network_no_secret_lookup(self, monkeypatch):
        monkeypatch.setattr(subprocess, "run", _forbid("subprocess"))
        monkeypatch.setattr(subprocess, "Popen", _forbid("subprocess"))
        monkeypatch.setattr(urllib.request, "urlopen", _forbid("network"))
        import os

        monkeypatch.setattr(os, "environ", _Trap())
        for lane in (cmd_lane(ECHO), http_lane("http://localhost:1/v1")):
            assert lanes.run(lane, "p", dry_run=True).status == "dry-run"

    def test_metered_lane_dry_runs_at_zero_dollars(self, monkeypatch):
        monkeypatch.setattr(urllib.request, "urlopen", _forbid("network"))
        lane = http_lane("https://api.deepseek.com/v1", metered=True)
        assert lanes.run(lane, "p", dry_run=True).status == "dry-run"


class _Trap(dict):
    def __getitem__(self, key):
        raise AssertionError("environment read during dry-run")

    def get(self, key, default=None):
        raise AssertionError("environment read during dry-run")


class TestLanesCli:
    def test_valid_config_lists_lanes(self, tmp_path: Path, capsys):
        config = tmp_path / "lanes.toml"
        config.write_text(
            '[lane.x]\nkind = "cmd"\nvendor = "v"\nmodel = "m"\nroute = "r"\n'
            'argv = ["c", "{prompt}"]\n'
        )
        assert main(["lanes", "--config", str(config)]) == 0
        out = capsys.readouterr().out
        assert "x" in out and "cmd" in out

    def test_metered_lane_shows_gate(self, capsys):
        assert main(["lanes", "--config", "lanes.toml"]) == 0
        assert "declined:gate" in capsys.readouterr().out

    def test_invalid_config_exits_1(self, tmp_path: Path, capsys):
        config = tmp_path / "lanes.toml"
        config.write_text('[lane.x]\nkind = "smoke-signal"\n')
        assert main(["lanes", "--config", str(config)]) == 1
        assert "kind" in capsys.readouterr().err

    def test_missing_config_exits_2(self, tmp_path: Path):
        assert main(["lanes", "--config", str(tmp_path / "absent.toml")]) == 2
