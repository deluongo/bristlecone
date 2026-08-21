+++
type = "deliberation"
date = 2026-08-20
question = "What file envelope should a Bristlecone record use?"
status = "decided"
class = "A"
options = [
  { id = "toml-fm", label = "TOML front matter between +++ fences, markdown body" },
  { id = "yaml-subset", label = "YAML front matter between --- fences, hand-parsed subset" },
  { id = "json-file", label = "Pure JSON document" },
]

[[positions]]
label = "fable"
by = "claude-fable-5 (project maintainer, incumbent design)"
stance = "toml-fm"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
gathered = "authored in-session"

[[positions]]
label = "opus"
by = "claude-opus-5 via claude CLI"
stance = "toml-fm"
vendor = "anthropic"
model = "claude-opus-5"
route = "subscription-cli"
gathered = "manual CLI paste (M0 — no tooling exists); provider-default params"

[[positions]]
label = "gpt"
by = "gpt-5.6-sol via codex CLI"
stance = "toml-fm"
vendor = "openai"
model = "gpt-5.6-sol"
route = "subscription-cli"
gathered = "manual CLI paste (M0 — no tooling exists); provider-default params"

[[positions]]
label = "qwen"
by = "qwen2.5:3b-instruct via ollama (local)"
stance = "toml-fm"
vendor = "alibaba"
model = "qwen2.5:3b-instruct"
route = "local"
gathered = "manual CLI paste; second capture — first discarded for terminal-rendering corruption, stance unchanged across both samples"

[outcome]
decision = "toml-fm"
decided_by = "claude-fable-5"
decided_date = 2026-08-20
authority = "design decision within maintainer authority (CONSTITUTION.md, Decision rights); operator holds override"
rationale = "Unanimous across four models spanning three vendors including a local open-weights model. The decisive argument (fable, opus, gpt independently): a fail-closed validator needs a parser whose rules are knowable without reading the validator — stdlib tomllib is that; a hand-parsed YAML subset has an invisible boundary that punishes exactly the no-CLI hand-writer the format exists for; JSON degrades the prose payload. Positions are preserved verbatim including factual slips (e.g., claims about GitHub natively rendering TOML front matter, and 'tomli' for 'tomllib'); the outcome relies on none of those claims."
+++

## Context

A Bristlecone record must be (a) git-diffable, (b) hand-writable by a person with only a text editor and a free local model — "no CLI required" is a core principle, (c) validatable fail-closed by an optional stdlib-only Python ≥3.11 tool, (d) renderable to a static site for non-experts. The incumbent design (spec draft) chose TOML front matter. This deliberation put the question independently to three other models before the spec froze. Each model received the same self-contained prompt and did not see the others' answers. Known cost of the incumbent: GitHub's web UI pretty-renders YAML front matter but shows TOML fences as literal text.

## Position: fable

TOML front matter. The choice hinges on constraint (b) meeting constraint (c): Python's stdlib has no YAML parser, so a "YAML-ish" front matter forces the validator to hand-parse a subset — and the subset's boundary is invisible to a hand-writer, who will produce valid YAML that our tool rejects. That failure mode lands on precisely the person the no-CLI principle protects. `tomllib` inherits a strict, line-numbered, standardized parser for free; "front matter is TOML" is the entire teaching. JSON fails (a) and the archive's purpose: multi-paragraph dissent in escaped strings is unreviewable in a diff. GitHub's rendering gap is real but bounded — the rendered site, not the raw file view, is the reader-facing surface.

## Position: opus

STANCE: toml-fm
SUMMARY: TOML front matter is the only option that gives a fail-closed stdlib parser with line-numbered errors *and* keeps prose as real markdown, and GitHub's rendering gap is a cosmetic cost the static site already pays for.

The decisive constraint is (c) combined with (b). A fail-closed validator is only trustworthy if the parse itself is unambiguous, and `tomllib` is in the stdlib, spec-versioned, and rejects malformed input with line and column. `yaml-subset` inverts this: the tool would define a private dialect that no hand-writer can see the edges of. A person writing a record in a text editor with a local model will produce ordinary YAML — a value with a colon, a folded block scalar, an unquoted `no` that means the string "no" — and get rejected by a parser whose rules exist nowhere except in the tool's source. That failure mode punishes exactly the person principle (b) is meant to protect, and it's worse than a hard error because the file *looks* correct in every other YAML tool they might reach for. Hand-writability is not about which syntax is prettiest; it's about whether the rules are knowable without reading the validator.

`json-file` fails the archive's actual purpose. This is a record of *positions* — multi-paragraph prose, argued in the writer's voice, preserved verbatim forever. Putting that in escaped JSON strings means every dissent becomes `"...forever.\n\nThe second paragraph..."`, every diff of an edited position is one enormous changed line, and `git blame` on a paragraph is meaningless. For a permanent, human-read archive whose value is that disagreement stays legible, degrading the prose channel to buy parser convenience is the wrong trade. Metadata is the small, structured part; prose is the payload. Optimize the envelope for the payload.

The honest cost of `toml-fm` is that GitHub shows the `+++` block as literal text. That is a real loss, but a bounded one: the metadata block is short, it remains completely readable as plain text (unlike escaped JSON), and requirement (d) already commits the project to a static site as the reader-facing surface for non-experts. Anyone browsing raw records on GitHub is a contributor, not the audience the pretty table serves. Trading a rendering nicety on one vendor's web UI for a strict, stdlib, line-numbered parse is the right direction — and it's the trade that stays correct if GitHub's renderer changes, which a hand-rolled YAML subset never will.

## Position: gpt

STANCE: toml-fm
SUMMARY: Strict, standardized parsing and predictable validation outweigh GitHub's weaker presentation of the metadata.

TOML front matter best satisfies the archive's durable constraints: it remains readable and hand-writable, produces useful diffs, and can be parsed fail-closed by Python's stdlib without inventing a new language. Separating structured metadata from Markdown also keeps long positions and preserved dissent natural to author and review.

The YAML subset creates a dangerous ambiguity: a person can write valid YAML that the validator rejects, making the apparent format different from the actual contract. JSON avoids that problem but makes the archive's most important content—multi-paragraph human argument—painful to edit and diff.

GitHub's literal display of TOML front matter is a real usability cost, but it is localized and recoverable through the static renderer. Parser correctness and format clarity are harder to repair later, especially in a permanent archive.

## Position: qwen

STANCE: toml-fm

SUMMARY: TOML front matter with +++ fences is a clear, concise, and widely understood format for file envelopes in an open-source context.

ARGUMENTS:
1. **Readability and Clarity**: TOML's structure ensures that the content within the file envelope is easily readable even without additional tools or knowledge. The use of +++ fences clearly delineates the front matter from the body, making it straightforward to identify where each section begins and ends. This clarity is particularly beneficial in an open-source context where maintainers and contributors might need to glance at files quickly.

2. **Git-Diffability**: TOML's format allows for easy git-diffing of changes between versions without needing external tools. The +++ fences make it simple to identify which lines are part of the front matter and which are the document body, ensuring that any modifications or additions to the file envelope can be accurately tracked in version control.

3. **Tool Support**: Given GitHub's native support for TOML through the use of +++ fences, there is no need for an additional tool. This simplicity reduces complexity and avoids potential integration issues with other project tools, making it easier to maintain consistency across different parts of the open-source ecosystem. Additionally, standardizing on a widely supported format like TOML ensures that all participants are working from a common understanding, which can lead to smoother collaboration and communication within the community.
