+++
type = "deliberation"
date = 2026-01-15
question = "Who decided this?"
status = "decided"
options = [
  { id = "yes", label = "Yes" },
  { id = "no", label = "No" },
]

[outcome]
decision = "yes"
decided_date = 2026-01-15
+++

## Context

When `[outcome]` is present, `decided_by` is required — the accountable party is the point of the field. It is absent here.
