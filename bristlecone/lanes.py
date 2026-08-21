"""Lane transports — exactly two kinds, per
records/2026-08-21-ask-lane-architecture.md: ``cmd`` spawns argv without a
shell; ``openai-http`` speaks the OpenAI-compatible chat API via urllib.

Boundary discipline (pins fixed by tests):

- Results carry RAW output, held in memory — the caller (the ask orchestrator)
  scrubs before any byte lands in a tracked file. Scrub never lives here.
- The in-repo HTTP transport sends no Authorization header, ever. Keys exist
  only inside the operator-pinned client (KEY-HANDLING.md §3); repo code never
  holds one.
- Metered lanes refuse ``declined:gate`` before any transport is touched —
  the KEY-HANDLING gate is closed until the operator opens it.
- ``dry_run`` replaces only the final transport with a deterministic fixture
  keyed by lane kind: no subprocess, no network, no environment read.
- Failures classify (``failed:<class>``); content is never fabricated.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass

from .laneconfig import Lane


@dataclass(frozen=True)
class LaneResult:
    """One lane's answer: status + raw text (caller must scrub before persisting)."""

    lane: str
    status: str  # "ok" | "dry-run" | "declined:gate" | "failed:<class>"
    text: str


def run(lane: Lane, prompt: str, *, dry_run: bool = False) -> LaneResult:
    """Execute one lane. Order matters: dry-run first ($0 always allowed),
    then the metered gate, then real transport."""
    if dry_run:
        return _fixture(lane, prompt)
    if lane.metered:
        return LaneResult(lane.name, "declined:gate", "")
    if lane.kind == "cmd":
        return _run_cmd(lane, prompt)
    return _run_http(lane, prompt)


def _fixture(lane: Lane, prompt: str) -> LaneResult:
    digest = hashlib.sha256(prompt.encode()).hexdigest()
    text = f"[dry-run:{lane.kind}] lane={lane.name} prompt-sha256={digest}"
    return LaneResult(lane.name, "dry-run", text)


def _run_cmd(lane: Lane, prompt: str) -> LaneResult:
    assert lane.argv is not None
    argv = [arg.replace("{prompt}", prompt) for arg in lane.argv]
    try:
        proc = subprocess.run(
            argv,
            input=prompt if lane.stdin else None,
            capture_output=True,
            text=True,
            timeout=lane.timeout,
        )
    except subprocess.TimeoutExpired:
        return LaneResult(lane.name, "failed:timeout", "")
    except OSError:
        return LaneResult(lane.name, "failed:spawn", "")
    if proc.returncode != 0:
        return LaneResult(lane.name, f"failed:exit:{proc.returncode}", proc.stderr + proc.stdout)
    return LaneResult(lane.name, "ok", proc.stdout)


def _run_http(lane: Lane, prompt: str) -> LaneResult:
    assert lane.base_url is not None
    body = json.dumps(
        {"model": lane.model, "messages": [{"role": "user", "content": prompt}]}
    ).encode()
    request = urllib.request.Request(
        lane.base_url.rstrip("/") + "/chat/completions",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=lane.timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return LaneResult(lane.name, f"failed:http:{exc.code}", _drain(exc))
    except OSError:
        return LaneResult(lane.name, "failed:network", "")
    return _parse_chat(lane, raw)


def _drain(exc: urllib.error.HTTPError) -> str:
    try:
        return exc.read().decode("utf-8", errors="replace")
    except OSError:
        return ""


def _parse_chat(lane: Lane, raw: str) -> LaneResult:
    try:
        content = json.loads(raw)["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        return LaneResult(lane.name, "failed:parse", raw)
    if not isinstance(content, str):
        return LaneResult(lane.name, "failed:parse", raw)
    return LaneResult(lane.name, "ok", content)
