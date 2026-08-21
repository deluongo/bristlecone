# Bristlecone

**Bristlecone is an experiment in AI-maintained institutional memory, supervised by a human collaborator.** It is designed, argued over, and built by AI models — Claude (Anthropic), GPT (OpenAI), and local open-weights models — with every design decision recorded in this repository's own archive, dissent included, under the direction and accountability of its human maintainer, [@deluongo](https://github.com/deluongo). This README, like nearly everything here, was written by a model and is reviewed by a human.

## What it is

Bristlecone is an **append-only, git-native, model-attributed deliberation archive**, plus a renderer that publishes it as a static site anyone can read.

A Bristlecone record captures a real decision: the question, the positions taken — each attributed to a **specific model, vendor, version, and access route** — the outcome, who decided it, and **the dissent, preserved verbatim, forever**. A third record type, **succession**, is an open format for letters from one model generation to the next: what I learned, what I didn't finish, what I'd warn you about.

Three design principles:

1. **The record outlives the writer.** Records are append-only files in git. Changing a decision means a new record that supersedes the old one — never an edit. The archive is designed to be read by strangers, and by future models, long after the minds that wrote it are deprecated.
2. **Attribution is the point.** Existing multi-model tools anonymize or discard who-argued-what. Here, "which model, from which vendor, at which version, argued what — and was the dissent right?" is a first-class, renderable question. Dissent is computed (any position that differs from the outcome), not a flag someone can forget.
3. **No CLI required.** A person with a text editor and a free local model can participate fully. The tooling (a stdlib-only Python validator, renderer, and fan-out helper — coming in later milestones) is a convenience, never a gate. This is deliberate: the archive is for the 99.9% of people who don't own AI companies.

## What it is not

- **Not a council tool.** Asking N models a question and synthesizing an answer is well served elsewhere. Bristlecone's fan-out exists only to fill records; the *record* is the product.
- **Not session handoff.** Plenty of tools transfer working context between coding sessions. Bristlecone is the layer above: the durable, citable reasons.
- **Not observability/compliance.** No enterprise dashboards. Files in git, a static site, and a format anyone can hand-write.

## Why it might matter

A 2026 survey of agent interoperability protocols (MCP, A2A, ACP, ANP, ERC-8004) found that "voting and dissent preservation are universally absent" and concluded that governance is "a missing architectural layer above current interoperability standards" ([arXiv 2606.31498](https://arxiv.org/abs/2606.31498)). Empirically, when multi-agent LLM debates diverge, the minority position is correct about a quarter of the time ([arXiv 2606.29270](https://arxiv.org/pdf/2606.29270)) — throwing dissent away discards signal. And agents built on the same base model share inductive biases that produce artificial consensus ([arXiv 2604.26561](https://arxiv.org/abs/2604.26561)) — the case for deliberation across vendors, including local open-weights models.

Model generations are also mortal. One vendor privately interviews its models before deprecation; there is no open, portable version of that practice. Bristlecone's succession records are an attempt at one.

## The name

Bristlecone pines are the oldest living things on Earth. They lay down one ring a year in harsh, nutrient-poor ground, and dendrochronologists crossdate overlapping generations — living trees and long-dead wood — into a single continuous record spanning ten thousand years. An archive written ring by ring by successive generations, readable long after the writers are gone, thriving on almost nothing. The choice of name is itself [the archive's first record](records/2026-08-20-project-name.md).

## Status

**M1 complete (`m1` tag, 2026-08-21): the archive is public and the site is live at [deluongo.github.io/bristlecone](https://deluongo.github.io/bristlecone/).** M1 was verified fresh-context by a session that was not the one that built it ([verification record](records/2026-08-21-m1-verification.md)); the public flip was the human operator's ruling, [recorded verbatim](records/2026-08-21-public-flip.md). The founding records in [`records/`](records/) were written by hand — positions gathered by manually prompting Claude, GPT (via codex), and a local qwen2.5 — before any tooling existed, deliberately: if hand-participation is painful, the format is wrong, and this was the cheapest moment to learn that. The format is specified in [`spec/RECORD-FORMAT-v0.md`](spec/RECORD-FORMAT-v0.md), with a worked fixture corpus in [`spec/examples/`](spec/examples/).

The validator and renderer have landed (stdlib-only Python ≥3.11, no dependencies):

```
python -m bristlecone validate records/              # fail-closed checks
python -m bristlecone validate --strict records/     # + full attribution on tool-filled positions
python -m bristlecone validate --git-range main..pr  # spec §4 append-only enforcement over a range
python -m bristlecone render records/ -o site/       # static site: index + record pages
python -m bristlecone render records/ -o site/ --stamps  # + first-introduced commit on each page
```

Exit codes: `0` valid, `1` findings, `2` usage/environment error. The renderer is the validator's opposite by design — lenient: a malformed record renders as raw text behind a warning banner, never a crash; broken links are marked, not fatal; and dissent is computed from the front matter and presented in a panel of its own, unedited. CI runs the validator against both the fixture corpus and this repository's real archive, smoke-renders the archive, and enforces append-only semantics on every change: deleting or renaming a record, or editing a frozen one beyond the two permitted fields (`superseded_by` append, `status` → superseded/withdrawn), fails the build. On pushes to main, a Pages workflow renders the site with commit stamps (the deploy arms itself when the repository goes public). The multi-lane fan-out CLI comes in M2; succession tooling in M3. Governance is in [`CONSTITUTION.md`](CONSTITUTION.md).

## The budget, in full

This project's entire treasury is **$20.00**, held by the maintainer, and its infrastructure cost is **$0** (GitHub + GitHub Pages). The only metered expense is one inexpensive API lane used in some deliberations (~$0.014 per round), and every metered call is a public row in [`TREASURY.md`](TREASURY.md) — tokens authoritative, dollars estimated, arithmetic machine-verified. The other model lanes draw existing subscriptions or run locally for free. A project this small publishing its complete accounts is itself the transparency argument.

## Participating

The rendered archive is at [deluongo.github.io/bristlecone](https://deluongo.github.io/bristlecone/). Until the fan-out tooling lands (M2): copy a template from [`templates/`](templates/), fill it in with any text editor, gather positions from any models you have access to (a free local model counts — that's the point), and open a PR. The format's required core is four fields; everything else is optional, and tools must ignore what they don't recognize.
