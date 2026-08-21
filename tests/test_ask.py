"""Tests for the ask orchestrator — the pipeline pins from
records/2026-08-21-ask-lane-architecture.md.

Load-bearing pins, each fixed here:
- ask fills positions into an EXISTING open deliberation record only — it
  never creates or decides one, and refuses terminal records;
- the outbound scrub gate is fail-closed: a prompt that trips any filter
  dispatches NOTHING (proven with traps), and the block names codes only;
- every byte landing in the record has passed inbound scrub;
- the repair reprompt fires exactly once, then failure is classified —
  captures are preserved, never fabricated or silently resampled;
- --dry-run runs the whole pipeline with zero subprocess/network/env access
  and never writes the record file;
- the prompt carries question/options/Context only, never other positions.
"""

from __future__ import annotations

import subprocess
import sys
import urllib.request
from pathlib import Path

import pytest

from bristlecone import ask, laneconfig, records, validate
from bristlecone.__main__ import main

RECORD_TEXT = '''+++
type = "deliberation"
date = 2026-08-21
question = "Which color should the shed be?"
status = "open"
options = [
  { id = "red", label = "paint it red" },
  { id = "blue", label = "paint it blue" },
]
+++

## Context

The shed needs painting before winter.

## Position: hand

A hand-written position that must never leak into any lane's prompt.
'''

# Credential-shaped test input, assembled at runtime so the hygiene grep never
# sees a contiguous key shape in this file's source.
FAKE_KEY = "sk-" + "Ab1" * 10
VALID_REPLY = "STANCE: red\\nSUMMARY: fine.\\nARGUMENTS: because."


def make_record(tmp_path: Path, text: str = RECORD_TEXT, name: str = "2026-08-21-shed") -> Path:
    path = tmp_path / f"{name}.md"
    path.write_text(text, encoding="utf-8")
    return path


def load(path: Path) -> records.Record:
    return records.load_file(path)


def reply_lane(name: str, script_body: str) -> laneconfig.Lane:
    """A cmd lane running an inline python script; the prompt arrives on stdin."""
    return laneconfig.Lane(
        name=name, kind="cmd", vendor="v", model=f"model-{name}", route="local",
        metered=False, timeout=30.0,
        argv=(sys.executable, "-c", f"import sys; sys.stdin.read(); {script_body}"),
        stdin=True, base_url=None,
    )


def printing_lane(name: str, reply: str) -> laneconfig.Lane:
    return reply_lane(name, f"print('{reply}')")


def metered_lane(name: str = "paid") -> laneconfig.Lane:
    return laneconfig.Lane(
        name=name, kind="openai-http", vendor="v", model="m", route="metered-api",
        metered=True, timeout=10.0, argv=None, stdin=False,
        base_url="https://example.invalid/v1",
    )


def _forbid(what: str):
    def guard(*args, **kwargs):
        raise AssertionError(f"{what} reached during a run that must not touch it")

    return guard


@pytest.fixture
def no_transport(monkeypatch):
    monkeypatch.setattr(subprocess, "run", _forbid("subprocess"))
    monkeypatch.setattr(subprocess, "Popen", _forbid("subprocess"))
    monkeypatch.setattr(urllib.request, "urlopen", _forbid("network"))


class TestBuildPrompt:
    def test_carries_question_options_context(self, tmp_path):
        prompt = ask.build_prompt(load(make_record(tmp_path)))
        assert "Which color should the shed be?" in prompt
        assert "- red: paint it red" in prompt and "- blue: paint it blue" in prompt
        assert "The shed needs painting before winter." in prompt
        assert "STANCE:" in prompt

    def test_never_carries_other_positions(self, tmp_path):
        prompt = ask.build_prompt(load(make_record(tmp_path)))
        assert "hand-written position" not in prompt
        assert "## Position" not in prompt

    def test_no_context_section_is_fine(self, tmp_path):
        text = RECORD_TEXT.split("## Context")[0] + "Body without headings.\n"
        prompt = ask.build_prompt(load(make_record(tmp_path, text)))
        assert "CONTEXT:" not in prompt


class TestAskableChecks:
    def rec(self, tmp_path, mutate: str, replacement: str) -> records.Record:
        return load(make_record(tmp_path, RECORD_TEXT.replace(mutate, replacement)))

    def test_terminal_status_refused(self, tmp_path):
        record = self.rec(tmp_path, 'status = "open"', 'status = "decided"')
        with pytest.raises(ask.AskError, match="never touches terminal records"):
            ask.run_ask(record, ())

    def test_non_deliberation_refused(self, tmp_path):
        record = self.rec(tmp_path, 'type = "deliberation"', 'type = "handoff"')
        with pytest.raises(ask.AskError, match="deliberation records only"):
            ask.run_ask(record, ())

    def test_missing_question_refused(self, tmp_path):
        record = self.rec(tmp_path, 'question = "Which color should the shed be?"', "")
        with pytest.raises(ask.AskError, match="question"):
            ask.run_ask(record, ())

    def test_missing_options_refused(self, tmp_path):
        text = RECORD_TEXT.replace("options = [", "ignored = [")
        with pytest.raises(ask.AskError, match="options"):
            ask.run_ask(load(make_record(tmp_path, text)), ())


class TestOutboundGate:
    def test_denylist_term_blocks_all_dispatch(self, tmp_path, no_transport):
        record = load(make_record(tmp_path))
        with pytest.raises(ask.OutboundBlocked) as excinfo:
            ask.run_ask(record, (printing_lane("a", VALID_REPLY),), denylist=("shed",))
        assert "denylist" in str(excinfo.value)
        assert "shed" not in str(excinfo.value)  # codes only, never matched text

    def test_secret_shape_in_record_blocks_dispatch(self, tmp_path, no_transport):
        text = RECORD_TEXT.replace("before winter", f"before {FAKE_KEY} winter")
        with pytest.raises(ask.OutboundBlocked) as excinfo:
            ask.run_ask(load(make_record(tmp_path, text)), (printing_lane("a", VALID_REPLY),))
        assert "secret:openai-key" in str(excinfo.value)
        assert FAKE_KEY not in str(excinfo.value)


class TestDryRun:
    def lanes(self):
        return (printing_lane("a", VALID_REPLY), metered_lane())

    def test_full_pipeline_no_transport_no_env(self, tmp_path, no_transport, monkeypatch):
        import os

        monkeypatch.setattr(os, "environ", _EnvTrap())
        result = ask.run_ask(load(make_record(tmp_path)), self.lanes(), dry_run=True)
        assert result.all_filled
        assert [r.stance for r in result.reports] == ["abstain", "abstain"]

    def test_metered_lane_participates_at_zero_dollars(self, tmp_path, no_transport):
        result = ask.run_ask(load(make_record(tmp_path)), (metered_lane(),), dry_run=True)
        assert result.reports[0].status == "filled"

    def test_deterministic(self, tmp_path, no_transport):
        record = load(make_record(tmp_path))
        first = ask.run_ask(record, self.lanes(), dry_run=True)
        second = ask.run_ask(record, self.lanes(), dry_run=True)
        assert first.text == second.text

    def test_assembled_record_is_strict_valid(self, tmp_path, no_transport):
        path = make_record(tmp_path)
        result = ask.run_ask(load(path), self.lanes(), dry_run=True)
        path.write_text(result.text, encoding="utf-8")
        assert validate.validate_file(path, {path.stem}, strict=True) == []
        front = load(path).front
        assert [p["label"] for p in front["positions"]] == ["a", "paid"]
        assert all(p["gathered"].startswith("bristlecone ask --dry-run")
                   for p in front["positions"])


class _EnvTrap(dict):
    def __getitem__(self, key):
        raise AssertionError("environment read during dry-run")

    def get(self, key, default=None):
        raise AssertionError("environment read during dry-run")


class TestRealFill:
    def test_valid_reply_fills_attributed_position(self, tmp_path):
        path = make_record(tmp_path)
        result = ask.run_ask(load(path), (printing_lane("a", VALID_REPLY),))
        assert [r.status for r in result.reports] == ["filled"]
        path.write_text(result.text, encoding="utf-8")
        record = load(path)
        (position,) = record.front["positions"]
        assert position["stance"] == "red"
        assert position["lane"] == "a"
        assert position["by"] == "model-a via a (local)"
        assert "## Position: a" in record.body
        assert "ARGUMENTS: because." in record.body
        assert "hand-written position" in record.body  # existing body preserved

    def test_stance_case_normalization_is_noted(self, tmp_path):
        lane = printing_lane("a", "STANCE: Red\\nSUMMARY: s\\nARGUMENTS: a")
        result = ask.run_ask(load(make_record(tmp_path)), (lane,))
        assert result.reports[0].stance == "red"
        assert "case-normalized" in result.text

    def test_abstain_is_always_legal(self, tmp_path):
        lane = printing_lane("a", "STANCE: abstain\\nSUMMARY: s\\nARGUMENTS: a")
        assert ask.run_ask(load(make_record(tmp_path)), (lane,)).reports[0].stance == "abstain"

    def test_inbound_scrub_before_commit(self, tmp_path):
        lane = reply_lane("a", f"print('STANCE: red\\nSUMMARY: s\\nARGUMENTS: ' + {FAKE_KEY!r})")
        result = ask.run_ask(load(make_record(tmp_path)), (lane,))
        assert result.reports[0].hits == ("secret:openai-key",)
        assert FAKE_KEY not in result.text
        assert "[SCRUBBED:secret:openai-key]" in result.text

    def test_transport_failure_recorded_not_fabricated(self, tmp_path):
        lane = reply_lane("a", "sys.exit(3)")
        result = ask.run_ask(load(make_record(tmp_path)), (lane,))
        assert result.reports[0].status == "failed:exit:3"
        assert not result.all_filled
        record = records.parse_text(result.text, "x")
        (position,) = record.front["positions"]
        assert "stance" not in position
        assert "failed:exit:3" in position["gathered"]
        assert "## Position: a" not in record.body  # no body content to preserve

    def test_metered_lane_declines_and_writes_nothing(self, tmp_path):
        result = ask.run_ask(load(make_record(tmp_path)), (metered_lane(),))
        assert result.reports[0].status == "declined:gate"
        assert "positions" not in records.parse_text(result.text, "x").front

    def test_duplicate_label_never_runs(self, tmp_path, no_transport):
        text = RECORD_TEXT.replace(
            "+++\n\n## Context", '\n[[positions]]\nlabel = "a"\nby = "x"\n+++\n\n## Context'
        )
        result = ask.run_ask(load(make_record(tmp_path, text)), (printing_lane("a", "x"),))
        assert result.reports[0].status == "declined:duplicate-label"


class TestRepair:
    def counting_lane(self, tmp_path: Path, first: str, second: str) -> laneconfig.Lane:
        flag = tmp_path / "called-once"
        body = (
            f"import pathlib; f = pathlib.Path({str(flag)!r}); "
            f"print('{second}') if f.exists() else (f.write_text('x'), print('{first}'))"
        )
        return reply_lane("a", body)

    def test_repair_fires_once_then_fills(self, tmp_path):
        lane = self.counting_lane(tmp_path, "not the format", VALID_REPLY)
        result = ask.run_ask(load(make_record(tmp_path)), (lane,))
        assert result.reports[0].status == "filled:repaired"
        assert result.reports[0].stance == "red"
        assert "one format-repair reprompt" in result.text

    def test_repair_prompt_names_the_defect(self, tmp_path):
        assert "STANCE" in ask.REPAIR_SUFFIX

    def test_unknown_stance_triggers_repair(self, tmp_path):
        lane = self.counting_lane(
            tmp_path, "STANCE: mauve\\nSUMMARY: s\\nARGUMENTS: a", VALID_REPLY
        )
        result = ask.run_ask(load(make_record(tmp_path)), (lane,))
        assert result.reports[0].status == "filled:repaired"

    def test_second_failure_classifies_and_preserves_capture(self, tmp_path):
        lane = printing_lane("a", "still not the format")
        result = ask.run_ask(load(make_record(tmp_path)), (lane,))
        assert result.reports[0].status == "failed:format"
        record = records.parse_text(result.text, "x")
        (position,) = record.front["positions"]
        assert "stance" not in position
        assert "not resampled" in position["gathered"]
        assert "still not the format" in record.body  # capture preserved unedited


class TestUpdatedText:
    def test_unterminated_front_text_gains_newline_before_append(self):
        # Parsed records always carry a newline-terminated front_text; this
        # guards Records constructed programmatically without one.
        record = records.Record(
            id="x", front={}, front_text='type = "deliberation"', body="body\n"
        )
        text = ask._updated_text(record, ['\n[[positions]]\nby = "b"\n'], [None])
        assert records.parse_text(text, "x").front["positions"] == [{"by": "b"}]


class TestCli:
    def lanes_toml(self, tmp_path: Path) -> Path:
        config = tmp_path / "lanes.toml"
        config.write_text(
            '[lane.a]\nkind = "cmd"\nvendor = "v"\nmodel = "m"\nroute = "local"\n'
            f'argv = ["{sys.executable}", "-c",'
            ' "import sys; sys.stdin.read(); print(\'STANCE: red\\\\nSUMMARY: s\\\\n'
            'ARGUMENTS: a\')"]\nstdin = true\n'
            '\n[lane.paid]\nkind = "openai-http"\nvendor = "v"\nmodel = "m"\n'
            'route = "metered-api"\nbase_url = "https://example.invalid/v1"\nmetered = true\n'
        )
        return config

    def test_dry_run_with_out_leaves_record_untouched(self, tmp_path, no_transport, capsys):
        path, config = make_record(tmp_path), self.lanes_toml(tmp_path)
        out = tmp_path / "assembled.md"
        code = main(["ask", str(path), "--config", str(config), "--dry-run", "--out", str(out)])
        assert code == 0
        assert path.read_text() == RECORD_TEXT
        assert [p["label"] for p in load(out).front["positions"]] == ["a", "paid"]
        assert "RECORD untouched" in capsys.readouterr().out

    def test_dry_run_without_out_writes_nothing(self, tmp_path, no_transport, capsys):
        path, config = make_record(tmp_path), self.lanes_toml(tmp_path)
        assert main(["ask", str(path), "--config", str(config), "--dry-run"]) == 0
        assert path.read_text() == RECORD_TEXT
        assert set(tmp_path.iterdir()) == {path, config}
        assert "use --out" in capsys.readouterr().out

    def test_real_run_updates_record_in_place_partial_exit_1(self, tmp_path, capsys):
        path, config = make_record(tmp_path), self.lanes_toml(tmp_path)
        code = main(["ask", str(path), "--config", str(config)])
        assert code == 1  # lane a filled; lane paid declined at the gate
        record = load(path)
        assert [p["label"] for p in record.front["positions"]] == ["a"]
        assert "declined:gate" in capsys.readouterr().out

    def test_lane_subset_selection(self, tmp_path, capsys):
        path, config = make_record(tmp_path), self.lanes_toml(tmp_path)
        assert main(["ask", str(path), "--config", str(config), "--lanes", "a"]) == 0
        assert [p["label"] for p in load(path).front["positions"]] == ["a"]

    def test_unknown_lane_name_exits_2(self, tmp_path, capsys):
        path, config = make_record(tmp_path), self.lanes_toml(tmp_path)
        assert main(["ask", str(path), "--config", str(config), "--lanes", "ghost"]) == 2
        assert "ghost" in capsys.readouterr().err

    def test_out_without_dry_run_exits_2(self, tmp_path, capsys):
        path, config = make_record(tmp_path), self.lanes_toml(tmp_path)
        code = main(["ask", str(path), "--config", str(config), "--out", str(tmp_path / "o")])
        assert code == 2

    def test_missing_record_exits_2(self, tmp_path):
        config = self.lanes_toml(tmp_path)
        assert main(["ask", str(tmp_path / "absent.md"), "--config", str(config)]) == 2

    def test_unparseable_record_exits_2(self, tmp_path, capsys):
        path = make_record(tmp_path, "no fences here\n")
        assert main(["ask", str(path), "--config", str(self.lanes_toml(tmp_path))]) == 2

    def test_bad_config_exits_2(self, tmp_path):
        config = tmp_path / "lanes.toml"
        config.write_text('[lane.x]\nkind = "smoke-signal"\n')
        assert main(["ask", str(make_record(tmp_path)), "--config", str(config)]) == 2

    def test_terminal_record_exits_2(self, tmp_path, capsys):
        text = RECORD_TEXT.replace('status = "open"', 'status = "decided"')
        path = make_record(tmp_path, text)
        assert main(["ask", str(path), "--config", str(self.lanes_toml(tmp_path))]) == 2
        assert path.read_text() == text

    def test_outbound_block_exits_1_codes_only(self, tmp_path, no_transport, capsys):
        path, config = make_record(tmp_path), self.lanes_toml(tmp_path)
        denylist = tmp_path / "deny.txt"
        denylist.write_text("shed\n")
        code = main([
            "ask", str(path), "--config", str(config), "--denylist", str(denylist),
        ])
        assert code == 1
        err = capsys.readouterr().err
        assert "denylist" in err and "nothing was dispatched" in err
        assert "shed" not in err
        assert path.read_text() == RECORD_TEXT
