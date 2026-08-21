# Format fixtures

Worked examples for `spec/RECORD-FORMAT-v0.md`. These are **fixtures, not records of this archive**: they live outside `records/`, carry fictional dates and a toy question, have no append-only semantics, and may be edited freely. In M1 they become the validator's test corpus — each row below is a test case.

## `valid/` — must pass a fail-closed validator

| Fixture | Exercises |
|---|---|
| `2026-01-15-canonical-deliberation.md` | Full surface: options, mixed structured/minimal positions, computed dissent (one stance ≠ decision), outcome with authority, links, tags, unknown key + unknown body section (must-ignore rule) |
| `2026-01-16-example-handoff.md` | Minimal `handoff`: required core only (`type`, `date`, `from`), recommended body sections |
| `2026-01-17-example-succession.md` | `succession` with full structured `from` attribution and `occasion` |

Links inside `valid/` resolve within `valid/` (it is one consistent mini-archive).

## `invalid/` — each fails for exactly the labeled reason

| Fixture | Expected failure | Mode |
|---|---|---|
| `broken-toml.md` | front matter does not parse as TOML (unterminated string) | default |
| `missing-required-question.md` | `deliberation` without required `question` | default |
| `bad-status-vocab.md` | `status = "finalized"` not in the closed vocabulary | default |
| `dangling-link.md` | `cites` names an ID that exists nowhere in the tree | default |
| `Bad_ID_Grammar.md` | filename stem violates ID grammar (uppercase, underscores) | default |
| `outcome-missing-decided-by.md` | `[outcome]` present without required `decided_by` | default |
| `missing-lane-attribution.md` | position carries a `lane` key without structured attribution (tool-filled ⇒ fully attributed) | `--strict` only |

Everything else a fixture does that is *not* its labeled defect is valid on purpose — a validator failing an invalid fixture for the wrong reason is itself a test failure.
