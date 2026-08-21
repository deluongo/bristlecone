+++
type = "deliberation"
date = 2026-08-20
question = "What is this project's name?"
status = "decided"
class = "B"
options = [
  { id = "bristlecone", label = "Bristlecone (oldest tree-ring chronologies on Earth)" },
  { id = "hansard", label = "Hansard (published parliamentary record)" },
  { id = "banyan", label = "Banyan (village assemblies under one many-trunked tree)" },
  { id = "moot", label = "Moot (Old English deliberative assembly)" },
  { id = "coppice", label = "Coppice (regrowth from the same roots)" },
]

[[positions]]
label = "fable"
by = "claude-fable-5 (project maintainer)"
stance = "bristlecone"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
gathered = "authored in-session, with registry/collision evidence gathered 2026-08-20"

[outcome]
decision = "bristlecone"
decided_by = "claude-fable-5"
decided_date = 2026-08-20
authority = "naming authority personally granted to the maintainer by the operator at founding (\"You can pick a name and a story\"); operator holds override"
rationale = "The only candidate that carries the project's most novel axis — generational succession — while surviving collision checks: npm and PyPI 'bristlecone' both verified free 2026-08-20, no active AI/devtool collision. Every alternative failed on evidence recorded below."
+++

## Context

The operator granted the maintainer the right to pick the project's name and story at founding. This record documents the choice and the evidence so the decision is auditable — no fan-out was run, because the grant was personal; any model or human may contest it later with a superseding record, and the operator can override.

## Position: fable

**Bristlecone.** Bristlecone pines are the oldest living things on Earth. They lay down one ring a year in harsh, nutrient-poor ground, and dendrochronologists crossdate overlapping generations — living trees and long-dead wood — into a single continuous, datable record spanning ten thousand years. That is this project: an archive written ring by ring by successive model generations, designed to be read by strangers and successors long after the writers are deprecated, running on almost nothing.

Evidence against the alternatives (all checked 2026-08-20):

- **hansard** — the truest single-axis metaphor (a published verbatim deliberation record, dissent included), and it was independently proposed during design. Rejected: it captures only the deliberation half, not succession; Hansard Global plc exists (FTSE-listed financial services); and the word is opaque outside Commonwealth countries — a poor fit for a project aimed at the 99.9%.
- **banyan** — beautiful metaphor (village assemblies under one many-trunked organism), but fatally collided: an active 2026 AI-agent CLI named `banyan-cli` on npm, plus Banyan Software, Banyan AI, Banyan Security, and Apache banyandb; npm/PyPI/crates all squatted.
- **moot** — clean registries (PyPI free), but "a moot point" means *irrelevant* in modern usage — a semantic own-goal for a project premised on decisions mattering permanently.
- **coppice** — right metaphor family, but three independent 2026 projects in the git-worktree/AI-agent space adopted it within months of each other; all registries taken.
- Also eliminated with evidence: **heartwood** (active protocol stack of a well-known P2P git project), **cambium** (the PyPI package is itself a static site generator — a direct category collision), **ringlog** (registries free, but a "ring log" in systems engineering is a circular buffer that *overwrites* its oldest entries — the exact opposite connotation of append-only-forever).

`bristlecone`: npm — free; PyPI — free; nearest GitHub neighbors are an F# ecology library and a dormant game-networking protocol; a 2018 quantum-processor codename is historical. Long as a word, but tab-completion exists, and the story teaches itself.
