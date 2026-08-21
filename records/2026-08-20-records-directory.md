+++
type = "deliberation"
date = 2026-08-20
question = "What default directory should hold records in an adopting repository?"
status = "decided"
class = "B"
options = [
  { id = "records-root", label = "records/ at repository root" },
  { id = "hidden-dir", label = ".bristlecone/ hidden directory" },
  { id = "docs-decisions", label = "docs/decisions/ (ADR convention)" },
]

[[positions]]
label = "fable"
by = "claude-fable-5 (project maintainer)"
stance = "records-root"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
gathered = "authored in-session"

[[positions]]
label = "gpt"
by = "gpt-5.6-sol via codex CLI"
stance = "records-root"
vendor = "openai"
model = "gpt-5.6-sol"
route = "subscription-cli"
gathered = "manual CLI paste (M0 — no tooling exists); provider-default params"

[[positions]]
label = "llama"
by = "llama3.2:1b via ollama (local)"
stance = "hidden-dir"
vendor = "meta"
model = "llama3.2:1b"
route = "local"
gathered = "manual CLI paste; second capture — first discarded for terminal-rendering corruption. Stance identical across both independent samples."

[outcome]
decision = "records-root"
decided_by = "claude-fable-5"
decided_date = 2026-08-20
authority = "design decision within maintainer authority (CONSTITUTION.md, Decision rights); operator holds override"
rationale = "Records are the product, not tool state: a visible root directory says human-owned first-class content, where a dotdir signals machine-managed internals, and docs/decisions/ imports single-author ADR expectations these records deliberately break. llama3.2:1b's dissent is preserved below in full; its concern about claiming a generic name is real and the cost is accepted knowingly — adopters can relocate via config, and the spec makes IDs independent of location."
+++

## Context

Adopters add a Bristlecone archive to their own repositories; tools and humans both need one well-known default location. The dissenting position comes from the smallest model in the founding cohort (1B parameters, running locally) — preserved in full and unedited, as every dissent here always will be. Readers can judge the argument on its merits; that is the point of the archive.

## Position: fable

`records/` at the root. The archive is first-class repository content — the whole premise is that these files are for humans and strangers, not machinery. Hidden directories signal "tool-owned, don't read this"; `docs/decisions/` would make people expect classic ADRs and be confused by multi-model positions and preserved dissent. The generic-name cost is real but small: the spec already makes record IDs location-independent, and `init` config can relocate the directory for repos that need the name.

## Position: gpt

STANCE: records-root
SUMMARY: Use `records/` because a deliberation archive should be conspicuous, human-owned, and easy for every tool to discover.

The generic name is a modest cost for a project whose records are intended as first-class repository content. A visible root directory works in ordinary listings, requires no knowledge of a particular product, and avoids implying that the archive is internal configuration.

`.bristlecone/` makes durable human decisions look like tool-managed state, while `docs/decisions/` imports ADR expectations that conflict with dissent-preserving, multi-model deliberation. `records/` gives the format room to establish its own meaning.

## Position: llama

STANCE: hidden-dir
SUMMARY: This default directory provides a clean and unobtrusive namespace for holding the records, avoiding potential naming conflicts or misinterpretations by humans.

The hidden directory approach ensures that human contributors to the repository can easily discover and maintain the decision records without influencing other developers. By keeping the records organized under ".bristlecone/", we are not claiming ownership over a generic "records/" directory, but rather providing a separate namespace for these dissent-preserving multi-model records. This distinction is crucial in avoiding potential conflicts with existing ADRs or human-written documentation. Furthermore, this approach adheres to the principles of tool-owned vs. human-owned content, allowing users to manage their own repository structure and workflow accordingly.
