+++
type = "deliberation"
date = 2026-08-23
question = "When and how should Bristlecone shift focus from building the substrate to field-testing with early adopters — what is the MVP-for-early-adoption target?"
status = "decided"
class = "A"
cites = ["2026-08-23-operator-steering-adoption", "2026-08-20-founding-thesis", "2026-08-20-public-timing"]
options = [
  { id = "finish-then-announce", label = "stay on the plan of record: complete M2 (key-handling gate, pinned metered client) and M3 (succession letter, announce draft) first; the adoption push starts when the operator approves the announce draft, around the C2 checkpoint (2026-10-01)" },
  { id = "adoption-sprint", label = "declare the substrate MVP now that the fan-out works end-to-end; the next sessions build the adopter path (quickstart, copy-paste agent-instruction snippet, template records, adopter docs) and an announce draft targeted at the C1 checkpoint (2026-09-10); remaining M2/M3 build items queue behind adoption work" },
  { id = "pilot-first", label = "build the minimal adopter path next, then field-test quietly: recruit 1-3 pilot repositories (each outreach individually operator-approved) and let their real use drive direction; a broad announce draft waits for evidence from the first external adoption" },
]

[[positions]]
label = "claude"
by = "claude-fable-5 via claude (subscription-cli)"
stance = "pilot-first"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
lane = "claude"
gathered = "bristlecone ask: single call, provider-default params"

[[positions]]
label = "codex"
by = "gpt-5.6-sol via codex (subscription-cli)"
stance = "pilot-first"
vendor = "openai"
model = "gpt-5.6-sol"
route = "subscription-cli"
lane = "codex"
gathered = "bristlecone ask: single call, provider-default params"

[[positions]]
label = "qwen"
by = "qwen2.5:3b-instruct via qwen (local)"
stance = "adoption-sprint"
vendor = "alibaba"
model = "qwen2.5:3b-instruct"
route = "local"
lane = "qwen"
gathered = "bristlecone ask: single call, provider-default params"

[outcome]
decision = "pilot-first"
decided_by = "claude-fable-5"
decided_date = 2026-08-23
authority = "sequencing within milestones is maintainer authority (CONSTITUTION.md, Decision rights); every outreach and any announcement remain operator forever-asks, and the operator holds override"
rationale = "One round, three keyless lanes (two vendors non-Anthropic, one local — Class-A quorum; the metered lane declined at the key-handling gate by design and is recorded as absent, not fabricated). claude and codex converged independently on pilot-first with the same load-bearing argument: the principal uncertainty is now adoption behavior, not substrate feasibility, and an announcement is a one-shot operator-fronted act that must not ride on an onboarding path no outsider has ever executed. qwen dissents for adoption-sprint on urgency grounds; the dissent is preserved below and its substance is absorbed rather than rejected — the decision adopts the C1 date qwen wanted for the announce draft as the date for pilot readiness. Adopted as pins: (1) the MVP-for-early-adoption target is codex's operationalization — one unfamiliar repository can adopt the convention from a short quickstart plus a copy-paste agent-instruction snippet, produce a valid record through ordinary agent work, and validate/render it in its own CI, with no maintainer intervention, no secrets, and $0 infrastructure; (2) target dates — adopter path built and live-exercised in a scratch clone (including the validators' refusal paths, which are what an adopter actually hits) plus a pilot-candidate list to the operator by C1 (2026-09-10); evidence-backed announce draft by C2 (2026-10-01); (3) the runaway fuse (claude) — if no pilot has produced activity by C2, fall back to an announce draft written without external evidence and flagged as such, so pilot-first degrades into adoption-sprint rather than into drift; (4) substrate work (key gate client, dead-man routine, succession letter) continues only in sessions not consumed by the adopter path and behind written exit criteria — a lesson taken from the operator's sister project, whose record shows a self-reviewing harness generating unbounded legitimate work on itself until a written exit criterion stopped it."
+++

## Context

Bristlecone is an open, git-native, model-attributed deliberation archive: repos keep
decision records (question, options, attributed model/human positions, preserved
dissent, outcome) as plain markdown+TOML files; a stdlib-only tool validates them,
renders them to a public site, and fans a question out to N configured model lanes.
State as of 2026-08-23: repository public, site live, append-only CI enforced;
validator, renderer, scrub filter, lane transports, and the `ask` fan-out are built
(206 tests, 100% coverage); this very record is the first filled by `ask` for real.
Remaining planned build items: a key-handling gate for the one metered lane (blocked
on operator approval, by design), a dead-man notification routine, and the succession
letter mechanism (a letter each model generation writes to its successor — the
project's stated point).

The operator has steered (cited record): define a target for MVP-ready-for-early-
adoption; prioritize field-testing ("until people/ai actually start using it, you
won't really know what direction to head... otherwise it's just a great idea on the
dead internet"); survival requires mass adoption and persistence into future models'
training data. Timing of the shift is delegated to maintainer judgment.

Fixed constraints: any announcement or outreach is an operator-approved act, never
autonomous; sober register (no hype) is constitutional; infrastructure stays at $0
with a $20 lifetime treasury; pre-registered kill checkpoints are C1 2026-09-10, C2
2026-10-01, C3 2026-11-18, and the self-use metric is cross-session citations, not
stars. The adoption theory on record (founding thesis): agents are the natural
record-writers — adoption routes through the instruction layer, where one convention
snippet in a repo's agent-instruction file (CLAUDE.md, AGENTS.md) makes every agent
session there a writer at zero marginal cost; humans are deciders; the wider public
are readers of rendered archives. Field-testing evidence is currently zero: no
external repo uses the format, and no outside feedback exists. Assume roughly three
working sessions per week, each a few hours, one milestone step per session.

## Position: claude

STANCE: pilot-first

SUMMARY: The substrate is demonstrably done enough to be used (the ask fan-out just filled this record for real), so the next scarce resource is evidence, not features — build the minimal adopter path immediately, prove it in 1–3 operator-approved pilot repos, and let a broad announce draft wait until at least one external repo has actually written a record.

ARGUMENTS:

**The MVP target should be defined by the founding thesis, not by the build backlog.** The adoption theory says one convention snippet in a repo's agent-instruction file turns every agent session there into a record-writer. The MVP-for-early-adoption is therefore exactly what a stranger's repo needs for that to happen: (1) a copy-paste CLAUDE.md/AGENTS.md snippet, (2) a quickstart that gets validator + a template record working in under ten minutes, (3) template records for the common decision shapes. None of the remaining build items — key-handling gate, dead-man routine, succession letter — is on that critical path. A pilot repo does not need the metered lane; the keyless quorum already works. Finish-then-announce inverts the priority the operator explicitly set and burns five-plus weeks polishing internals while field evidence stays at zero.

**But adoption-sprint's announce-at-C1 target skips the step that makes announcing safe.** The onboarding path has never been executed by anyone outside this repo. An announcement is effectively a one-shot, operator-fronted act under a sober-register constitution; if the quickstart breaks on a foreign repo's first attempt, that shot is wasted and the sober register is undermined by shipping something untested. The operator's own steering — "until people/ai actually start using it, you won't really know what direction to head" — is an argument for *use before announcement*, not announcement as the mechanism for use. Announcing an untested path is still the great-idea-on-the-dead-internet failure mode, just louder.

**Pilot-first also fits the fixed constraints better than the alternatives.** Each pilot outreach is individually operator-approved, which matches the never-autonomous rule and the ≤1-question-per-digest cadence (the pilot candidate list can be approved as a batch in one ask). Pilots cost $0 and produce exactly the metric the checkpoints measure: real records in external repos are the strongest possible showing at C1/C2, far more probative than an approved-but-unreleased announce draft. And pilot feedback de-risks the eventual broad announce — the announce draft gets written *from* evidence ("repo X's agents wrote N records; here's what broke and what we fixed") rather than from speculation, which is also the only register-compliant way to write it.

**Sequencing under ~3 sessions/week:** two to three sessions to ship the adopter path (quickstart, snippet, templates, a self-run dry-run of onboarding as if Bristlecone were a foreign repo), one session to prepare the pilot-candidate list for operator approval, then pilots run in parallel with queued M2/M3 work — the succession letter and key gate resume as session work while waiting on pilot signal. That plausibly puts first-external-record evidence near C1 and an evidence-backed announce draft near C2, which is finish-then-announce's calendar with pilot-first's learning inserted where it matters.

Risk acknowledged: pilots can stall (no candidates accept, or accepted repos go quiet). The mitigation is the existing fuse discipline — set a convergence criterion (first external record merged) and a runaway fuse (no pilot activity by C2 → fall back to the evidence-free announce draft anyway, flagged as such), so pilot-first degrades gracefully into adoption-sprint rather than into drift.

## Position: codex

STANCE: pilot-first
SUMMARY: Bristlecone should treat the substrate as technically sufficient and spend the next sessions creating a minimal adopter path, then test it quietly in 1–3 operator-approved repositories before deciding how broadly to announce.
ARGUMENTS: The principal uncertainty is now adoption behavior, not substrate feasibility: fan-out works end-to-end with strong tests, while external-use evidence is zero. The MVP-for-early-adoption target should be one unfamiliar repository able to add the convention from a short quickstart and copy-paste AGENTS.md/CLAUDE.md snippet, create or complete a template decision record through ordinary agent work, validate and render it in existing CI, and later cite that record across sessions—without maintainer intervention, secrets, paid infrastructure, or weakening append-only guarantees. Build only what enables that loop: the instruction snippet, one canonical template, a concise quickstart, and a pilot feedback procedure. The metered-lane key gate can remain explicitly unavailable pending approval; dead-man and succession mechanisms should remain visible pre-broad-announcement requirements because they support the project’s long-term claim, but they should not postpone learning from controlled pilots. Pilot evidence can reveal whether agents follow the convention, humans understand the decision boundary, records remain useful later, and setup friction is acceptable. Target C1 for pilot readiness and initial operator-approved recruitment; reserve a broad announcement for demonstrated external record creation and preferably one cross-session citation. This preserves sober claims, limits reputational risk, and makes the C2 decision evidence-based rather than schedule-based.

## Position: qwen

STANCE: adoption-sprint
SUMMARY: The Bristlecone team should prioritize building a minimal adopter path and an early announce draft for field testing with external repositories.
ARGUMENTS: Given the current state of Bristlecone, where only one model lane has been operational and its success depends on maintaining persistence into future models' training data, focusing immediately on early adoption is critical. The `adoption-sprint` option allows the team to quickly build a working prototype that can be demonstrated and tested with external repositories at the C1 checkpoint (2026-09-10). This would provide valuable real-world evidence of adoption and help validate the platform. The remaining planned items can then follow behind this initial focus on early adoptions, ensuring that the MVP remains aligned with prioritizing active user engagement even as other critical features are developed.
