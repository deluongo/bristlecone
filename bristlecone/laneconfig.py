"""Lane config — hand-editable TOML stanzas over exactly two transport kinds
(records/2026-08-21-ask-lane-architecture.md: lanes are DATA, not code).

Fail-closed on purpose, unlike the record validator's must-ignore: a config
typo like ``metred = true`` silently un-metering a lane is precisely the
failure mode the metering design cannot afford, so unknown keys and unknown
kinds are errors.

Interpretive pin, fixed by tests: a keyless ``openai-http`` lane must point at
a loopback host. The only keyless HTTP lane in the required matrix is ollama's
localhost endpoint; any remote endpoint is metered/BYOK territory, and keyed
transport runs only from the operator-pinned client (KEY-HANDLING.md §3).
Metered lanes may name remote hosts — they refuse at the gate anyway.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_TIMEOUT = 120.0
KINDS = frozenset({"cmd", "openai-http"})
ATTRIBUTION = ("vendor", "model", "route")  # spec §3.1 needs these on every position
_COMMON_KEYS = frozenset({"kind", "vendor", "model", "route", "metered", "timeout"})
_KIND_KEYS = {
    "cmd": _COMMON_KEYS | {"argv", "stdin"},
    "openai-http": _COMMON_KEYS | {"base_url"},
}
_LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})


class ConfigError(Exception):
    """Any reason the lane config cannot be trusted as written."""


@dataclass(frozen=True)
class Lane:
    """One configured lane: attribution + transport parameters for its kind."""

    name: str
    kind: str
    vendor: str
    model: str
    route: str
    metered: bool
    timeout: float
    argv: tuple[str, ...] | None
    stdin: bool
    base_url: str | None


def load(path: Path) -> tuple[Lane, ...]:
    """Parse and validate a lanes.toml; raise ConfigError on any defect."""
    try:
        data = tomllib.loads(path.read_text())
    except OSError as exc:
        raise ConfigError(f"cannot read {path}: {exc}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"{path}: invalid TOML: {exc}") from exc
    tables = data.get("lane")
    if not isinstance(tables, dict) or not tables:
        raise ConfigError(f"{path}: no [lane.<name>] tables")
    return tuple(_parse_lane(name, table) for name, table in tables.items())


def _parse_lane(name: str, table: object) -> Lane:
    kind = _checked_kind(name, table)
    _check_attribution(name, table)
    metered = _typed(name, table, "metered", bool, default=False)
    argv, stdin = _parse_cmd(name, table) if kind == "cmd" else (None, False)
    base_url = _parse_http(name, table, metered) if kind == "openai-http" else None
    return Lane(
        name=name, kind=kind, vendor=table["vendor"], model=table["model"], route=table["route"],
        metered=metered, timeout=_parse_timeout(name, table), argv=argv, stdin=stdin,
        base_url=base_url,
    )


def _checked_kind(name: str, table: object) -> str:
    if not isinstance(table, dict):
        raise ConfigError(f"lane {name}: not a table")
    kind = table.get("kind")
    if kind not in KINDS:
        raise ConfigError(f"lane {name}: unknown kind {kind!r} (must be one of {sorted(KINDS)})")
    unknown = set(table) - _KIND_KEYS[kind]
    if unknown:
        raise ConfigError(f"lane {name}: unknown key(s) {sorted(unknown)} for kind {kind}")
    return kind


def _check_attribution(name: str, table: dict) -> None:
    for key in ATTRIBUTION:
        if not isinstance(table.get(key), str) or not table[key]:
            raise ConfigError(f"lane {name}: missing attribution key {key!r}")


def _parse_timeout(name: str, table: dict) -> float:
    timeout = float(_typed(name, table, "timeout", (int, float), default=DEFAULT_TIMEOUT))
    if timeout <= 0:
        raise ConfigError(f"lane {name}: timeout must be positive")
    return timeout


def _typed(name: str, table: dict, key: str, types: type | tuple, *, default: object) -> object:
    value = table.get(key, default)
    if not isinstance(value, types) or isinstance(value, bool) != (types is bool):
        raise ConfigError(f"lane {name}: {key} has wrong type")
    return value


def _parse_cmd(name: str, table: dict) -> tuple[tuple[str, ...], bool]:
    argv = _checked_argv(name, table)
    stdin = _typed(name, table, "stdin", bool, default=False)
    placeholders = sum(arg.count("{prompt}") for arg in argv)
    if stdin and placeholders:
        raise ConfigError(f"lane {name}: stdin = true conflicts with a {{prompt}} placeholder")
    if not stdin and placeholders != 1:
        raise ConfigError(
            f"lane {name}: argv needs exactly one {{prompt}} placeholder (or stdin = true)"
        )
    return tuple(argv), stdin


def _checked_argv(name: str, table: dict) -> list[str]:
    argv = table.get("argv")
    if (
        not isinstance(argv, list)
        or not argv
        or not all(isinstance(arg, str) for arg in argv)
    ):
        raise ConfigError(f"lane {name}: cmd lanes need argv, a non-empty list of strings")
    return argv


def _parse_http(name: str, table: dict, metered: bool) -> str:
    base_url = table.get("base_url")
    if not isinstance(base_url, str) or urlparse(base_url).scheme not in {"http", "https"}:
        raise ConfigError(f"lane {name}: openai-http lanes need an http(s) base_url")
    host = urlparse(base_url).hostname or ""
    if not metered and host not in _LOOPBACK_HOSTS:
        raise ConfigError(
            f"lane {name}: keyless openai-http lanes must target a loopback host; "
            f"remote endpoints are metered/BYOK territory (KEY-HANDLING.md §3)"
        )
    return base_url
