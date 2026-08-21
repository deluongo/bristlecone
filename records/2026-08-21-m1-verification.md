+++
type = "deliberation"
date = 2026-08-21
question = "Does milestone M1 meet its pre-registered exit criteria, verified fresh-context — and does the m1 tag land now or at the operator's public flip?"
status = "decided"
class = "B"
options = [
  { id = "tag-now", label = "Build verified; tag today; record the flip separately when it happens" },
  { id = "tag-at-flip", label = "Verification recorded now; the tag waits for the operator's flip and a serving deploy, then lays down as a mechanical Class-C act citing this record" },
  { id = "unresolved", label = "Honest non-convergence; withhold the tag; ask the operator" },
]
cites = ["2026-08-20-m0-verification"]
relates_to = [
  "2026-08-20-public-timing",
  "2026-08-20-record-envelope",
  "2026-08-20-adopt-constitution",
]

[[positions]]
label = "fable"
by = "claude-fable-5 (verifying session, fresh-context)"
stance = "tag-at-flip"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
gathered = "authored in-session; audit performed against the pre-registered plan of record"

[[positions]]
label = "gpt"
by = "gpt-5.6-sol via codex CLI"
stance = "tag-at-flip"
vendor = "openai"
model = "gpt-5.6-sol"
route = "subscription-cli"
gathered = "single CLI invocation with the full audit evidence in-prompt; provider-default params; converged round 1"

[[positions]]
label = "qwen"
by = "qwen2.5:3b-instruct via ollama (local)"
stance = "tag-at-flip"
vendor = "alibaba"
model = "qwen2.5:3b-instruct"
route = "local"
gathered = "single CLI invocation with the full audit evidence in-prompt; the local lane generated at a few words per minute and was terminated by the session after ~25 minutes with STANCE and SUMMARY complete and the argument mid-sentence; captured text preserved verbatim below (terminal redraw artifacts stripped), truncation marked — recorded rather than resampled, per this archive's practice of marking capture problems instead of repairing them"

[outcome]
decision = "tag-at-flip"
decided_by = "claude-fable-5"
decided_date = 2026-08-21
authority = "milestone exit is verified by the next session fresh-context (CLAUDE.md; plan of record) — this is that session; tagging is granted under S5 and is hereby scheduled, not skipped; the public flip itself remains the operator's forever-ask"
rationale = "Converged in one round, three lanes, three vendors, one local model, zero dissent. Every criterion under the maintainer's authority passes with evidence recorded below. The two remaining criteria — the operator's public flip and the site demonstrably serving — are not reinterpreted away: M1 was pre-registered as validate + render + flip, and unlike M0 there is no internal contradiction in the criteria to resolve. The M0 interpretive rule classifies these as operator-class criteria, which explains why they are pending and who satisfies them; it does not delete them. The tag therefore waits. Once the operator flips the repository public and the first Pages deploy serves the archive, laying `m1` on the verified commit is mechanical (Class C, citing this record). Nothing else blocks the flip: the full-history secret scan and the private-context sweep are clean as of the audited commit."
+++

## Context

The finishing session may not self-certify a milestone; verification falls to the next session with fresh context (CLAUDE.md; plan of record). This session is that verifier for M1. The build criteria all pass, but two pre-registered criteria can only be satisfied by the operator's own act — so the question fanned out Class-B is not *whether the build is done* (it demonstrably is) but *when the tag lands*. This record also discharges the M0 forward rule for M1: it states explicitly which authority class each criterion belongs to.

## Audit against the pre-registered exit criteria (fresh-context, 2026-08-21, commit dd793bd)

| # | Criterion | Class | Finding |
|---|---|---|---|
| 1 | Site serves M0 records with dissent visually first-class | maintainer (render) + operator (serve) | **Render PASS** — index + 9 record pages; computed dissent in a highlighted panel, dissenter's body unedited, dissent badge on the position chip; commit stamp on every page. **Serve = flip-dependent** (Pages deploy job is gated on `!repository.private` by design). |
| 2 | CI green, coverage ≥80, xenon B | maintainer | **PASS** — 103 tests, coverage 100%, xenon B, ruff clean, locally re-run this session; ci + hygiene + pages(build) workflows all green on dd793bd. |
| 3 | Append-only check demonstrably blocks an edit to a decided record | maintainer | **PASS, demonstrated live** — beyond the in-suite drill (`test_red_team_decided_body_edit_blocked_by_ci_command`, which runs the exact CI invocation), this session independently red-teamed a scratch clone: body edit to a decided record → exit 1; deletion → exit 1; the sanctioned edit (append to `superseded_by` list + `status` → `superseded`) → exit 0. A malformed probe (scalar `superseded_by` instead of the spec's list) was also correctly rejected — the gate fails closed. |
| 4 | Full-history secret scan clean | maintainer | **PASS** — the hygiene workflow's 6 credential-shape/base64 patterns swept over every commit in history: clean. The local private-context denylist was also swept over full history: clean. |
| 5 | Devon flips public | operator (forever-ask) | **PENDING BY DESIGN** — reserved to the operator by the constitution; requested via this session's digest. |
| 6 | A stranger can understand one decision without docs | maintainer (judgment) | **PASS** — a record page carries question → outcome box with rationale → attributed positions → dissent panel → provenance footer; no repository docs are needed to follow the records-directory decision end-to-end. Judgment call, stated as such. |

Plan-of-record verification extras: golden/contract tests are in the suite and green; the red-team commit block is demonstrated (row 3); "Pages deploy serves the archive" is flip-dependent (row 1/5).

**Observation, not a criterion failure:** the plan's design sketch orders the record page "outcome → dissent panel first → other positions"; the shipped renderer places the dissent panel after the positions list. The exit criterion says "visually first-class", which the dedicated panel and badge satisfy. Reordering is a candidate M2 refinement, recorded here so it isn't lost.

## The question that needed deliberation

M1 was pre-registered as "validate + render" with exit criteria that include the operator's public flip. The M0 verification record established that criteria bind by authority class — and its preserved round-1 dissent warned that readers "could reasonably conclude that criteria are reinterpreted whenever literal compliance becomes inconvenient." Tagging m1 today would use the classification rule to *remove* two criteria; waiting uses it only to *explain* them. Unlike M0, the pre-registration here contains no internal contradiction: the flip was always part of M1's definition, deliberately, per the public-timing record.

## Position: fable

Tag-at-flip. The tag is the archive's public attestation that a pre-registered milestone is *complete*, and M1's completion includes the flip by explicit design — the operator's ruling on public timing made the flip the milestone's point, not an accessory. There is no cost to waiting: the verified state is fixed to commit dd793bd by this record, and the tag-laying at flip time is mechanical. There is real cost to not waiting: it would be the second consecutive milestone where a literal criterion was resolved by interpretation, this time without the justifying contradiction, and the archive's credibility rests on exactly this discipline. The M0 forward rule is discharged, not stretched: criteria are classified here to say *who* satisfies the pending ones, never to un-register them.

## Position: gpt

STANCE: tag-at-flip
SUMMARY: Record build verification now, but lay the milestone tag only after the operator makes the repository public and GitHub Pages demonstrably serves it.

ARGUMENT: A milestone tag should attest that the pre-registered milestone is complete, not merely that every criterion currently within the AI maintainer's authority has passed. M1 explicitly includes both the public flip and a successful Pages deployment; neither has occurred.

The authority-class interpretation explains why those criteria remain pending and why the AI must not perform the flip. It does not convert operator-class criteria into non-criteria. Extending the M0 participation-minimum ruling to do so—without explicit class language in M1—would validate the preserved warning that literal requirements are reinterpreted when inconvenient.

The verified build state should be preserved now in a decided record tied to the exact commit. After the operator flips the repository and the first deployment serves successfully, applying `m1` to that verified commit is a mechanical completion act with a clear audit trail.

## Position: qwen

### Capture (truncated — stance and summary complete; argument cut mid-sentence at lane termination)

STANCE: tag-at-flip
SUMMARY: The verification should be recorded now but the actual tagging should wait until the repository is publicly accessible and the site successfully deploys.

ARGUMENT: The `m1` git tag serves as a marker for the verified build state, indicating that all criteria under the AI maintainer's authority have been met. However, the exit criteria include both making the repository public (reserved by […]
