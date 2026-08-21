+++
type = "deliberation"
date = 2026-01-15
question = "May a tool-filled position skip structured attribution?"
status = "open"

[[positions]]
by = "some model, filled in by a tool"
lane = "example-lane"
+++

## Context

This position carries a `lane` key, marking it tool-filled, but omits the structured attribution fields (`vendor`, `model`, `route`). Default validation accepts it (hand-writers may stay minimal); `--strict` fails it — tool-filled implies fully attributed.
