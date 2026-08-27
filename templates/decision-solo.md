+++
# The everyday shape: one accountable decider, no fan-out. Rename this file to
# records/YYYY-MM-DD-<slug>.md — the filename stem becomes the permanent ID.
type = "deliberation"
date = 2026-01-01
question = "One-sentence question this record decides?"
status = "decided"                  # write "open" first if the decision isn't made yet
options = [
  { id = "chosen-thing", label = "Short label for what was chosen" },
  { id = "rejected-thing", label = "Short label for the alternative considered" },
]

[[positions]]
by = "your-name, or model-name via route"   # the only required field per position
stance = "chosen-thing"             # an option id, or "abstain"
label = "decider"                   # pairs with "## Position: decider" below
# route = "human"                   # subscription-cli | api | local | human

[outcome]
decision = "chosen-thing"
decided_by = "who is accountable"
decided_date = 2026-01-01
rationale = "One or two sentences: why this option, and what was given up."
+++

## Context

Why this question came up and what constrained the answer. A stranger (or a future
model) reading only this file should understand the situation.

## Position: decider

The reasoning, in plain markdown. If an alternative was seriously considered and
rejected, say why here — a future reader's first question is "did they think of X?".
