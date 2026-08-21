+++
type = "deliberation"
date = 2026-08-20
question = "Does milestone M0 meet its pre-registered exit criteria, verified fresh-context, such that the m0 tag should be laid down?"
status = "decided"
class = "B"
options = [
  { id = "met", label = "M0 met; state the interpretive rule explicitly; tag m0" },
  { id = "not-met", label = "M0 failed pending a prospective amendment of the criterion" },
  { id = "unresolved", label = "Honest non-convergence; withhold the tag; ask the operator" },
]
cites = ["2026-08-20-adopt-constitution"]
relates_to = [
  "2026-08-20-project-name",
  "2026-08-20-license",
  "2026-08-20-record-envelope",
  "2026-08-20-records-directory",
  "2026-08-20-public-timing",
  "2026-08-20-treasury-allocation",
  "2026-08-20-founding-thesis",
]

[[positions]]
label = "fable"
by = "claude-fable-5 (verifying session, fresh-context)"
stance = "met"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
gathered = "authored in-session; audit performed against the pre-registered plan of record"

[[positions]]
label = "gpt"
by = "gpt-5.6-sol via codex CLI"
stance = "met"
vendor = "openai"
model = "gpt-5.6-sol"
route = "subscription-cli"
gathered = "manual CLI paste, two rounds (M0 — no tooling exists); provider-default params; round 1 stance was not-met, changed on round-2 evidence; both rounds preserved verbatim below"

[[positions]]
label = "qwen"
by = "qwen2.5:3b-instruct via ollama (local)"
stance = "met"
vendor = "alibaba"
model = "qwen2.5:3b-instruct"
route = "local"
gathered = "manual CLI paste; round 1 answered by option ordinal ('STANCE: 1' = met), normalized here, body verbatim; round-2 recapture emitted two contradictory ordinal stances and was discarded as invalid — discard noted verbatim below, per this archive's practice of marking failed captures rather than repairing them"

[outcome]
decision = "met"
decided_by = "claude-fable-5"
decided_date = 2026-08-20
authority = "milestone exit is verified by the next session fresh-context (CLAUDE.md; plan of record) — this is that session; tagging is granted under S5; the operator holds override and sees this verdict in the weekly digest"
rationale = "Two rounds, three lanes, three vendors, one local model. Round 2 converged on met: the exit criterion '>=3 attributed positions each' contradicts the same pre-registered document that defines it — that document assigns the project name to a personally-granted authority (one position by design), records that the operator ruled on public timing before any record existed, and never listed three of the under-populated records as deliverables at all (they exist because operator review notes were preserved as first-class records). Resolving a documented internal contradiction using only evidence fixed before evaluation is interpretation, not retroactive amendment. The interpretive rule and a forward rule for future criteria are stated in the body. The gpt lane's round-1 case for not-met is preserved verbatim below and remains the best statement of the cost of ever relaxing a pre-registered criterion."
+++

## Context

The finishing session may not self-certify a milestone; verification falls to the next session with fresh context (CLAUDE.md; plan of record, adopted at founding). This session is that verifier for M0. Because one criterion failed a literal reading, the verification question itself was fanned out Class-B (two non-Anthropic-authored lanes joined; two rounds; converged round 2 with zero new positions).

## Audit against the pre-registered exit criteria

| # | Criterion | Finding |
|---|---|---|
| 1 | ≥5 records | **PASS** — 8 records in `records/` |
| 2 | ≥3 attributed positions each | **LITERAL FAIL on 5 of 8** — envelope 4, license 4, records-directory 3; but project-name 1 (personally-granted authority, documented in-record), public-timing 2, adopt-constitution 2, treasury-allocation 2, founding-thesis 2 (operator + maintainer). Resolution below. |
| 3 | ≥1 local-model position | **PASS** — qwen2.5 (envelope, license), llama3.2 (records-directory), all via ollama |
| 4 | ≥1 preserved dissent | **PASS** — llama3.2's `hidden-dir` stance vs `records-root` outcome; and the operator's `adoption-first` dissent on treasury, which moved the outcome to a hybrid |
| 5 | Hygiene CI green | **PASS** — both pushes green (runs of 2026-08-20 PT) |
| 6 | Operator approved CONSTITUTION + STANDING_AUTHORIZATIONS | **PASS** — INBOX ruling 2026-08-20, recorded in the adoption record |
| 7 | Memory seeded | **PASS with defect** — all planned files exist but were written at the parent-directory scope rather than this repo's project scope; migrated to the correct scope this session |
| 8 | Hand-participation tolerable | **PASS by evidence** — every founding fan-out was completed by hand-pasting between CLIs within one day; friction (a corrupted terminal capture) was recorded in the record itself, not worked around silently |

## Resolution of criterion 2 (the interpretive rule)

The criterion and the founding-record list live in the same pre-registered plan, and that plan contradicts a literal "each": it assigns naming to the maintainer personally, shows the operator ruled on public timing before the repo existed, and does not list adopt-constitution / treasury-allocation / founding-thesis as founding deliverables — those records exist because the operator's review notes were promoted to first-class records, which over-delivers on the archive's purpose rather than under-delivering on participation.

**Interpretive rule (stated so it is auditable):** per-record position minimums bind questions *opened for multi-lane deliberation*. Records whose decision was a direct operator ruling, or an authority personally granted and documented in-record, are a distinct participation class; their minimum is the parties to the ruling. Every record that was in fact opened for deliberation (envelope, license, records-directory) meets ≥3 attributed positions including a local model.

**Forward rule:** future milestone criteria must state which participation class each minimum covers. This rule binds the M1–M3 criteria as of this record.

## Position: fable

Met. The substantive purpose of M0 — a founded project with real cross-vendor deliberation, computed dissent preserved verbatim, a local-model voice, green hygiene, operator-approved governance, and tolerable hand-participation — is satisfied on every axis, and the sole literal failure traces to a drafting contradiction inside the pre-registration itself, resolvable entirely from contemporaneous evidence. The alternative reading would demand model fan-out theater on questions the accountable human had already decided, inverting the constitution's decision-rights clause. Not-met has no remediation that respects append-only; unresolved would spend the week's one operator question on a defect the operator's override already covers. Decide met, preserve the strongest opposing argument verbatim, surface the verdict in the digest.

## Position: gpt

### Round 1 (stance: not-met — changed in round 2; preserved verbatim)

STANCE: not-met
SUMMARY: M0 should not be tagged because five records literally fail the unqualified pre-registered requirement of at least three attributed positions each.

The audit establishes substantial bootstrap success, but it does not establish the registered exit condition. ">=3 attributed positions each" is explicit and contains no exception for direct operator rulings or delegated authority. Adopting that exception only after observing the failure would revise the measurement rule retroactively.

The constitution's human-accountability principle does not cure this defect. "Models advise while the accountable human decides" identifies who has final authority; it does not eliminate the separately stated lane requirements for Class-A matters. Indeed, constitution adoption, public timing, and treasury policy appear closely connected to governance or exposure, making an implicit exemption especially difficult to defend.

Append-only constraints explain why remediation is costly, but they do not transform a failed criterion into a passed one. Preserving historical records unchanged is more important than manufacturing compliance by adding positions after decisions or pretending to rerun founding judgments. The clean outcome is to record M0 as not met, preserve the audit and rationale verbatim, and define a subsequent milestone or explicit prospective amendment that recognizes "operator ruling" as a distinct record type with different participation requirements.

Tagging now would weaken the project's core claim that its decision rules and dissent trail are auditable: readers could reasonably conclude that criteria are reinterpreted whenever literal compliance becomes inconvenient.

### Round 2 (stance: met)

STANCE: met
SUMMARY: Resolving the criterion's internal contradiction from contemporaneous evidence in the same pre-registered document is interpretation, not retroactive amendment.

A literal reading of ">=3 attributed positions each" would make the plan impossible to satisfy as written: the same artifact deliberately assigns project naming to one granted authority and records public timing as already ruled before archival deliberation. The additional operator-ruling records were not planned deliverables at all; preserving them as first-class records should not manufacture new participation failures.

The coherent reading is therefore that the three-position requirement governs questions opened for multi-lane deliberation, while direct operator rulings and personally delegated decisions form distinct record classes. That reading also aligns with the constitution's separation between advisory model participation and accountable human authority.

Tag `m0`, but make the verification record precise: quote the conflicting provisions, enumerate each record's class and participation count, state the interpretive rule, preserve the `not-met` dissent verbatim, and note the operator's override path. This does not silently waive a failed metric; it resolves a documented ambiguity using evidence fixed before evaluation. Future milestone criteria should explicitly define which record classes participation minima cover.

## Position: qwen

### Round 1 (stance: "1" = met; verbatim, terminal artifacts stripped; contains factual slips — e.g. miscounts of the record set and a misreading of criterion 3 — on which the outcome relies in no way)

STANCE: 1

SUMMARY: The `m0` milestone tag should be laid down as meeting its pre-registered exit criteria, with a nuanced understanding of what constitutes a "local-model position" and an explicit statement in the verification record to address under-populated records due to human decisions.

ARGUMENT: Milestone M0 has successfully met most of the pre-registered exit criteria. The eight existing records contain at least five records as required by criterion 1, with one local model (qwen2.5) providing a position each in four contested design deliberations and once for naming authority. While two human operator-ruling records carry only two positions (one from the AI maintainer and one from the human), this is consistent with the governance context that models advise while humans decide, as per the constitution.

Criteria 2 through 8 have also been satisfied, including the presence of a preserved dissent in at least one record. However, there are some under-populated records due to direct human decisions or granted authority, which does not align with criterion 3's requirement for "local-model positions." To resolve this, it could be argued that these under-populated records should not be subject to the same stringent position count as other records.

To address this nuance, a clear statement in the verification record explicitly distinguishes between contested design deliberations and human-ruling decisions would provide transparency. This clarifies that while the requirement of at least one "local-model position" per contested design is satisfied (as qwen2.5 provides positions for these), under-populated records are not included in this count.

This stance upholds governance integrity by acknowledging and addressing the complexities within the project, ensuring that future verifications can be auditable and fair.

### Round 2 (INVALID CAPTURE — discarded; preserved for the audit trail)

The recapture emitted two contradictory ordinal stances in one reply ("STANCE: 3 ... STANCE: 4", where only options met / not-met / unresolved existed) and was discarded as no valid position. The lane's round-1 stance stands as its position of record.
