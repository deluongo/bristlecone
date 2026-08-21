+++
type = "deliberation"
date = 2026-01-15
question = "Is 'finalized' a legal status?"
status = "finalized"
+++

## Context

`status` must be one of `open | decided | unresolved | superseded | withdrawn`. The must-ignore rule covers unknown keys and unknown values in *open* vocabularies; `status` is a closed vocabulary, so this fails.
