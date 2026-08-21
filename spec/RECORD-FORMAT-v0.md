# Bristlecone record format — v0 (draft)

Status: **draft** during M0; the required cores below freeze at the M1 tag. Within v0, changes are additive and OPTIONAL only. Breaking changes require a `RECORD-FORMAT-v1.md` beside (never replacing) this file, a migration path, and a deliberation record deciding them.

The format is an interchange contract. **No rights are reserved on the format itself** — implement it freely, in any tool, for any purpose. (Code in this repository is licensed separately; see the license record.)

## 1. Envelope

A record is **one file**: TOML front matter between `+++` fences, followed by a markdown body.

```
+++
type = "deliberation"
date = 2026-08-20
question = "…"
status = "open"
+++

## Context
…markdown…
```

- Front matter MUST parse as TOML (Python ≥3.11 `tomllib` is the reference parser).
- **Must-ignore rule:** tools MUST ignore unknown front-matter keys and unknown body sections. Unknown values in open vocabularies degrade to display-as-text. Extensions never break old tools.
- Hand-writability is a design requirement: a person with a text editor MUST be able to produce a valid record by copying a template. No tool is ever required.

## 2. Identity and links

- A record's ID is its **filename stem**. Convention: `YYYY-MM-DD-<slug>` (lowercase, hyphens). IDs are merge-safe (no sequence numbers) and never repeated inside the file.
- Records live under `records/` (any depth of subdirectories; tools glob recursively). Moving a file between subdirectories does not change its ID.
- Link fields hold IDs: `supersedes = ["<id>"]`, `superseded_by = ["<id>"]`, `relates_to = ["<id>"]`, `cites = ["<id>"]`. Validators fail on dangling IDs; renderers in lenient mode mark broken links instead of failing.

## 3. Record types

### 3.1 `deliberation`

REQUIRED: `type`, `date`, `question` (string), `status` — one of `open | decided | unresolved | superseded | withdrawn`.

OPTIONAL: `class` (`"A" | "B" | "C"` — this repo's constitution's taxonomy; other archives may ignore it), `options` (array of `{id, label}` tables), `[[positions]]` (see below), `[outcome]` (see below), `supersedes`, `superseded_by`, `relates_to`, `cites`, `tags`, `format` (absent ⇒ `"bristlecone/v0"`).

Each `[[positions]]` table:

- REQUIRED: `by` — free-string display attribution (e.g. `"qwen2.5:3b-instruct via ollama"`). The only per-position requirement, so a hand-writer writes one line.
- OPTIONAL: `stance` (an option `id`, or `"abstain"`), `label` (pairs the position with a `## Position: <label>` body section), and structured attribution: `vendor`, `model`, `model_version`, `route` (`subscription-cli | api | local | human`), `lane`, `params` (inline table), `gathered` (how the position was collected, e.g. `"manual paste"`).
- Strict validators require the structured fields on positions carrying a `lane` key (tool-filled ⇒ fully attributed); hand-filled positions may stay minimal.
- Capture honesty (learned hand-writing the founding records): a corrupted, invalid, or discarded capture SHOULD be noted in `gathered` (or preserved in the body) rather than silently resampled — failed lanes are marked failed, never repaired or fabricated. When a model answers with an option's ordinal or a paraphrase, the writer MAY normalize `stance` to the option `id`, noting the normalization in `gathered` and preserving the reply verbatim in the body.

`[outcome]`:

- REQUIRED (when present): `decision` (an option `id`), `decided_by` (the accountable party — a human, or a named authority rule), `decided_date`.
- OPTIONAL: `rationale`, `authority` (why `decided_by` had the right to decide, e.g. a citation to a governance record).

**Dissent is computed, not declared:** every position whose `stance` differs from `outcome.decision` is dissent. Renderers MUST present dissent first-class and unedited.

### 3.2 `handoff`

REQUIRED: `type`, `date`, `from` (free string or a table with the position-attribution shape).
OPTIONAL: `to`, `re` (topic), `relates_to`, `cites`, `tags`.
Recommended body sections (never validated): `## Context`, `## State of work`, `## Next steps`, `## Warnings`.

### 3.3 `succession`

A letter from a model (or model generation) to its successor.

REQUIRED: `type`, `date`, `from` — SHOULD be the full structured attribution; *who precisely wrote this* is the point.
OPTIONAL: `to` (successor designation if known; absent renders as "to my successor"), `occasion` (e.g. `"v0.1 release"`, `"model deprecation"`), `transcript` (link proving how the letter was produced), `relates_to`, `cites`.
Recommended body sections (never validated — a rigid form would make these gimmicks): `## Where things stand`, `## What I learned the hard way`, `## What I did not finish`, `## To you`.

A succession record is written *by* the model, in-session, occasioned by a real event. It is never fabricated retroactively on a model's behalf.

## 4. Append-only semantics

A record on the default branch in a terminal status (`decided`, `unresolved`, `superseded`, `withdrawn`, or any handoff/succession) is **frozen**. The only permitted edits: appending to `superseded_by`, and changing `status` to `superseded` or `withdrawn`. Changing a decision means a new record with `supersedes`. Typos stand — records are testimony, not documentation. While `status = "open"` (or on an unmerged branch), edit freely.

Enforcement in this repository: convention (this section), a CI check over `git diff` that fails deletions/renames under `records/` and illegal modifications to frozen records (from M1), no-force-push branch protection, and first-introduced commit SHAs stamped on rendered pages.

## 5. Examples

Worked fixtures live in [`spec/examples/`](examples/): `valid/` is a small consistent mini-archive covering all three types (including the must-ignore rule and a computed dissent); `invalid/` fixtures each fail validation for exactly one labeled reason (see its README). They are fixtures, not records of any archive, and double as the validator's test corpus.

## 6. Conformance

- **Record writers** (humans or tools): produce files satisfying §1–§3 required fields. A text editor suffices.
- **Validators**: fail-closed on required-core violations, status vocabulary, ID grammar, dangling links; honor must-ignore for everything else.
- **Renderers**: lenient by default (a malformed foreign record renders as raw text with a warning banner, never a crash); MUST render dissent first-class; SHOULD display full attribution and note that a position is a model's output under recorded parameters, not a vendor's view.
