+++
type = "deliberation"
date = 2026-01-01
question = "One-sentence question this record decides?"
status = "open"
# class = "B"                       # optional: A | B | C (see CONSTITUTION.md)
options = [
  { id = "option-one", label = "Short label for option one" },
  { id = "option-two", label = "Short label for option two" },
]

[[positions]]
by = "your-name or model-name"      # the only required field per position
stance = "option-one"               # an option id, or "abstain"
label = "example"                   # pairs with "## Position: example" below
# vendor = "…"  model = "…"  model_version = "…"
# route = "human"                   # subscription-cli | api | local | human
# gathered = "manual paste"

# [outcome]                          # add when decided
# decision = "option-one"
# decided_by = "who is accountable"
# decided_date = 2026-01-01
# rationale = "One or two sentences."
+++

## Context

Why this question exists and what constrains the answer.

## Position: example

The argument, in plain markdown. Paste a model's answer here verbatim, or write your own.
