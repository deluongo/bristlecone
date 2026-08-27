+++
type = "deliberation"
date = 2026-08-27
question = "Does the adopter path in docs/ADOPTING.md hold end-to-end for a stranger, per the live-exercise exit criterion pre-registered in the adoption roadmap?"
status = "decided"
class = "C"
options = [
  { id = "holds", label = "The ten-minute path holds as documented; no changes needed" },
  { id = "fixed-in-session", label = "Breakages found and fixed in the same session; path holds after fixes" },
  { id = "breakages-remain", label = "Breakages found that could not be fixed this session" },
]
cites = ["2026-08-23-adoption-roadmap"]

[[positions]]
label = "fable"
by = "claude-fable-5 (maintainer session, executing the rehearsal as a stranger)"
stance = "holds"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
gathered = "authored in-session; the evidence transcript below is the position"

[outcome]
decision = "holds"
decided_by = "claude-fable-5 (maintainer)"
decided_date = 2026-08-27
rationale = "Every step of docs/ADOPTING.md was executed in an isolated scratch repository using only the public artifacts (GitHub URL installs, raw-file fetches) and the document itself. All five quickstart steps succeeded verbatim, all eleven refusal codes in the document's table fired exactly as described, and the multi-model section's real fan-out filled a validly attributed position at $0. Zero breakages; nothing to fix."
+++

## Context

`records/2026-08-23-adoption-roadmap.md` pre-registered a live exercise as the
gate before pilot outreach: adopt Bristlecone into a scratch repo end-to-end *as
if a stranger, following only `docs/ADOPTING.md`*, deliberately hitting every
refusal path, with the exit criterion "a transcript-of-record showing the
ten-minute path holds, or the specific breakages fixed." Part 1 (M2-S6) shipped
the quickstart and verified a local-path install only; this session ran the
rehearsal itself.

One pre-registered scope narrowing: the roadmap note allowed running the adopter
CI "for real on a scratch GitHub repo if cheap enough." Creating a scratch GitHub
repository would be a new operator-owned repository — forever-ask territory under
STANDING_AUTHORIZATIONS — so the CI job's *exact commands* (both range forms) were
run locally against the scratch git repo instead. What this leaves untested: the
GitHub Actions runner environment itself (checkout depth, event SHA plumbing).
The commands the yaml runs are fully exercised.

## Position: fable

Evidence transcript. Scratch repo `widget-factory` in an isolated scratch
directory outside the project; fresh `python3 -m venv`; Python 3.14; the only
guide open was `docs/ADOPTING.md`.

**Quickstart steps (all five):**

1. **First record** — the document's inline example, typed verbatim into
   `records/2026-08-27-widget-naming.md`: `OK: 1 record(s) valid`, exit 0 —
   matching the document's promised output exactly. Also passes `--strict`.
2. **Agent snippet** — pasted into `AGENTS.md` unmodified; nothing to execute,
   nothing snagged.
3. **Validator install** — `pip install git+https://github.com/deluongo/bristlecone`
   from the public URL (the path part 1 never tested): 6.5 seconds, clean, CLI
   help renders all four subcommands.
4. **CI** — the yaml's commands run locally: `validate records/` exit 0;
   `validate --git-range` in both the push form (`before..HEAD`) and the PR form
   (`base...HEAD`) reports append-only semantics hold, exit 0.
5. **Render** — `render records/ -o site/` and `--stamps` variant both exit 0,
   emitting index plus per-record page.

Elapsed for the five steps: well under the advertised ten minutes (the
long pole, the network install, is ~7 seconds).

**Refusal drill — all eleven finding codes in ADOPTING's table, one trigger each,
all exit 1 with messages matching the table's described meaning:**

| Code | Trigger used | Fired |
|---|---|---|
| `parse-error` | unquoted TOML value | yes |
| `missing-required` | `question` omitted | yes |
| `status-vocab` | `status = "done"` | yes |
| `id-grammar` | underscore in filename stem | yes |
| `dangling-link` | `cites` to a nonexistent ID | yes |
| `duplicate-id` | same stem in two subdirectories | yes |
| `lane-attribution` | `--strict`, position with `lane` but no vendor/model/route | yes (3 findings, one per missing key) |
| `record-deleted` | `git rm` a record on a branch, range check | yes |
| `record-renamed` | `git mv` a record, range check | yes |
| `frozen-edit` | body append to a decided record, range check | yes |
| `frozen-indeterminate` | edit to a committed unparseable record, range check | yes |

**Multi-model section** — `lanes.toml` fetched from the public raw URL; `lanes`
subcommand lists all four lanes with the metered one showing `declined:gate`;
the documented `ask` command run for real against the open record on the local
qwen lane ($0): it filled a fully attributed `[[positions]]` stanza with an
honest `abstain` (the placeholder question is unanswerable — correct behavior),
and the updated record still passes `validate --strict`.

**Findings requiring fixes to ADOPTING.md: none.** Two observations, neither a
defect: `validate` also accepts a single file path (undocumented, harmless);
the quickstart's inline example carries a filled `[outcome]` while
`status = "open"`, which is legal and intentional (it shows the full shape) but
a literal-minded adopter could copy the contradiction — the document already
says to set `status = "decided"` when deciding, so no change made.
