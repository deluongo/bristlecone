+++
type = "deliberation"
date = 2026-08-20
question = "When does this repository become public?"
status = "decided"
class = "A"
options = [
  { id = "day-1", label = "Public from the first commit" },
  { id = "m1-flip", label = "Private through M0; public at M1 exit with full history intact" },
  { id = "later", label = "Private until M2/M3" },
]

[[positions]]
label = "fable"
by = "claude-fable-5 (project maintainer)"
stance = "m1-flip"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
gathered = "authored in-session; recommendation presented to the operator with the day-1 and later alternatives"

[[positions]]
label = "operator"
by = "deluongo (human operator)"
stance = "m1-flip"
route = "human"
gathered = "operator's answer to the founding decision batch, quoted verbatim in the body"

[outcome]
decision = "m1-flip"
decided_by = "deluongo"
decided_date = 2026-08-20
authority = "public exposure is an operator right (CONSTITUTION.md, Decision rights) — this decision was always the operator's"
rationale = "M1 target accepted, conditional on hardened key handling. The condition is resolved by design: M0–M1 run with zero secrets (subscription CLIs + local models satisfy the cross-vendor quorum keyless); the single metered lane stays disabled until the operator approves a dedicated key-handling design at M2. The flip itself remains the operator's button, after a full-history secret scan."
+++

## Context

The repository flips public with its complete history, so transparency-from-commit-#1 is preserved either way — the question is when strangers can start reading, weighed against the fact that an AI commits here autonomously and the operator's environment has a history of secrets riding tool output into places they shouldn't be. Maximum-transparency purity argues day-1; safety and first-impression argue for flipping once hygiene gates and the rendered site exist.

## Position: fable

`m1-flip`. Day-1 publicness publishes commits before the hygiene CI, denylist gate, and full-history scanning exist — the exact window where an accident is least catchable. Nothing is lost by waiting: the entire M0 history becomes public at the flip, which also forces M0 to follow public-grade hygiene from the first commit. And the first thing a stranger sees should be the rendered archive, not scaffolding. The flip is the operator's button after a clean full-history secret scan.

## Position: operator

Quoted verbatim from the founding decision batch (2026-08-20):

> Public at M1 sounds good as a target, but depending on what keys you need we need to setup a better / more hardened way to make sure they don't leak, because I'm security conscious and the tool call workflow makes it's difficult for you to no leak them accidentially. I appreciate you asking this question.

Read as: `m1-flip` accepted as target, with a binding condition that key handling be hardened beyond the default workflow before any key exists in the project. The maintainer's response (adopted into the plan and CONSTITUTION): M0–M1 use zero secrets; the one metered lane is gated behind an operator-approved key-handling design at M2; the blessed-invocation path keeps the key out of the session environment entirely.
