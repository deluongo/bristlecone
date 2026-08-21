+++
type = "deliberation"
date = 2026-01-15
question = "Should the example project indent with tabs or spaces?"
status = "decided"
options = [
  { id = "tabs", label = "Tab characters" },
  { id = "spaces", label = "Space characters" },
]
relates_to = ["2026-01-16-example-handoff"]
tags = ["style", "example"]
# Unknown keys exercise the must-ignore rule: tools must not break on the next line.
review_priority = "low"

[[positions]]
label = "model-a"
by = "example-model-9b via localrunner (local)"
stance = "spaces"
vendor = "exampleco"
model = "example-model-9b"
model_version = "9b-2026-01"
route = "local"
params = { temperature = 0.2 }
gathered = "manual paste"

[[positions]]
label = "model-b"
by = "other-model-large via vendor CLI"
stance = "tabs"
vendor = "othervendor"
model = "other-model-large"
route = "subscription-cli"
gathered = "manual paste"

[[positions]]
by = "a. human, by hand"
stance = "spaces"

[outcome]
decision = "spaces"
decided_by = "a. human"
decided_date = 2026-01-15
authority = "style decisions delegated to the maintainer in the example project's founding notes"
rationale = "Two of three positions; renderers display uniformly."
+++

## Context

A deliberately trivial question so the fixture's structure, not its content, is the point. Note the third position: `by` alone is the only per-position requirement, so a hand-writer participates with one line.

## Position: model-a

Spaces render identically in every viewer; the archive's readers outnumber its writers.

## Position: model-b

Tabs encode intent, not appearance; readers choose their own width. This position's stance differs from the outcome, so tools must compute it as dissent and renderers must present it first-class and unedited.

## Position: a. human, by hand

Spaces. Written in a text editor with no tooling, as the format promises.

## Afterword

An unknown body section, present to exercise the must-ignore rule.
