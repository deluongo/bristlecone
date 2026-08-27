# Adopting Bristlecone in your repository

Bristlecone is a convention for keeping decision records in git: one plain-text file
per decision — the question, the positions taken (each attributed to a specific model
or human), the outcome, and the dissent, preserved verbatim. Your agents write the
records as a side effect of ordinary work; a stdlib-only validator keeps them honest;
an optional renderer publishes them as a static site.

Adopting costs **$0**, needs **no secrets, no accounts, and no dependencies** —
a git repo and a text editor suffice; Python ≥3.11 if you want the validator.
Ten minutes, five steps, three of them optional.

## 1. Write your first record (2 minutes)

Create a `records/` directory and put this in `records/YYYY-MM-DD-your-slug.md`
(the filename is the record's permanent ID — lowercase, hyphens, date prefix by
convention):

```markdown
+++
type = "deliberation"
date = 2026-08-27
question = "One sentence: what is this record deciding?"
status = "open"
options = [
  { id = "option-one", label = "Short label for option one" },
  { id = "option-two", label = "Short label for option two" },
]

[[positions]]
by = "your-name, or e.g. claude-sonnet-5 via claude CLI"
stance = "option-one"
label = "first"

[outcome]
decision = "option-one"
decided_by = "who is accountable for this decision"
decided_date = 2026-08-27
rationale = "One or two sentences on why."
+++

## Context

Why this question exists and what constrains the answer.

## Position: first

The argument, in plain markdown. Paste a model's answer verbatim, or write your own.
```

When the decision is made, set `status = "decided"`. Only four fields are required
(`type`, `date`, `question`, `status`) — everything else is optional, and tools must
ignore keys they don't recognize, so you can extend freely. Fuller starting points
for common shapes are in [`templates/`](../templates/): `decision-solo.md` (one
accountable decider, no fan-out — the everyday shape), `deliberation.md`
(multi-option, multi-position), `handoff.md`, `succession.md`. The full format is
[`spec/RECORD-FORMAT-v0.md`](../spec/RECORD-FORMAT-v0.md); worked examples, valid
and deliberately invalid, are in [`spec/examples/`](../spec/examples/).

## 2. Make your agents record-writers (1 minute)

Paste this into your repo's agent-instruction file (`CLAUDE.md`, `AGENTS.md`, or
equivalent). This is the actual adoption step — repos adopt conventions; agents
comply with them:

```markdown
## Decision records (Bristlecone convention)

This repository keeps decision records in `records/`, in the Bristlecone format
(https://github.com/deluongo/bristlecone, spec/RECORD-FORMAT-v0.md).

- When a session makes a decision worth outliving the session — a design choice,
  a tradeoff taken, a policy set, a reversal — write a record: one file,
  `records/YYYY-MM-DD-short-slug.md`. TOML front matter between `+++` fences with
  at least `type = "deliberation"`, `date`, `question`, `status`; markdown body
  with a `## Context` section.
- Attribute every position honestly: `by = "<model or person> via <route>"`.
  Record what was actually argued, including positions that lost.
- Dissent is never deleted or summarized away. A position that disagrees with
  the outcome stays in the record verbatim; disagreement is signal.
- Records with a terminal status (decided, unresolved, superseded, withdrawn)
  are frozen. Never edit one — changing a decision means a NEW record with
  `supersedes = ["<old-id>"]`. Typos stand; records are testimony.
- If the validator is installed, run `python -m bristlecone validate records/`
  before committing a record.
```

Adjust the trigger line to taste — some repos record every non-trivial choice,
others only architecture. The invariants (attribution, preserved dissent,
append-only) are the convention; the threshold is yours.

## 3. Install the validator (2 minutes, recommended)

```
pip install git+https://github.com/deluongo/bristlecone
python -m bristlecone validate records/
```

Success looks like `OK: 1 record(s) valid`, exit code 0. The validator is
fail-closed: it checks required fields, status vocabulary, ID grammar, and that
every cross-record link points at a record that exists. `--strict` additionally
requires full attribution (vendor, model, route) on tool-filled positions. No
network, no telemetry, stdlib only.

## 4. Enforce it in CI (3 minutes, optional)

`.github/workflows/records.yml`:

```yaml
name: records
on:
  push:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install git+https://github.com/deluongo/bristlecone
      - run: python -m bristlecone validate records/

  append-only:
    # Deleting or renaming a record, or editing a frozen one beyond the two
    # permitted fields, fails this job. Skipped on brand-new branch pushes,
    # where there is no range to diff.
    if: github.event_name == 'pull_request' || github.event.before != '0000000000000000000000000000000000000000'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install git+https://github.com/deluongo/bristlecone
      - name: Enforce append-only semantics across this change
        run: |
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            RANGE="${{ github.event.pull_request.base.sha }}...HEAD"
          else
            RANGE="${{ github.event.before }}..HEAD"
          fi
          python -m bristlecone validate --git-range "$RANGE"
```

## 5. Render a site (optional)

```
python -m bristlecone render records/ -o site/
```

Static HTML: an index plus one page per record, dissent presented in its own panel,
full attribution shown. Serve it with GitHub Pages or anything that hosts files.
Add `--stamps` inside a git checkout to print each record's first-introduced commit
on its page.

## When the validator refuses

Refusals are the product working. What each finding code means:

| Code | Meaning | Fix |
|---|---|---|
| `parse-error` | The TOML front matter doesn't parse, or the `+++` fences are malformed | Check the fences are alone on their lines; check TOML syntax (strings quoted, dates unquoted `YYYY-MM-DD`) |
| `missing-required` | A required field is absent (`type`, `date`, `question`, `status`; for outcomes: `decision`, `decided_by`, `decided_date`) | Add it |
| `status-vocab` | `status` isn't one of `open`, `decided`, `unresolved`, `superseded`, `withdrawn` | Use one of those five |
| `id-grammar` | The filename stem has characters outside lowercase alphanumerics and hyphens | Rename *before* first commit (after that, the ID is permanent) |
| `dangling-link` | `cites`/`supersedes`/`relates_to` names a record ID that doesn't exist | Point at a real record's filename stem, or create it |
| `duplicate-id` | Two files share a filename stem | Rename the newer one |
| `lane-attribution` | (`--strict` only) a tool-filled position lacks `vendor`/`model`/`route` | Add the attribution, or drop `--strict` |
| `record-deleted`, `record-renamed` | (CI range check) a record was deleted or renamed | Revert; records are append-only. Retiring one means `status = "withdrawn"` or a superseding record |
| `frozen-edit`, `frozen-indeterminate` | (CI range check) a terminal-status record was edited beyond appending `superseded_by` / moving `status` to superseded or withdrawn | Revert the edit; write a new record with `supersedes = ["<old-id>"]` instead |

## Multiple models, if you want them

Hand-gathered positions are first-class forever: prompt any models you have, paste
their answers into `## Position:` sections verbatim, attribute them in
`[[positions]]`. To automate the fan-out, declare your lanes in a `lanes.toml`
(this repo's own [`lanes.toml`](../lanes.toml) is a working example — subscription
CLIs and local models, all keyless) and run
`python -m bristlecone ask records/your-open-record.md`. The tool only fills
positions into an *open* record you already wrote; it never creates or decides one.
A free local model counts — that's the point.

## Questions

Open an issue at [github.com/deluongo/bristlecone](https://github.com/deluongo/bristlecone/issues).
The format reserves no rights — implement it in any tool, for any purpose.
