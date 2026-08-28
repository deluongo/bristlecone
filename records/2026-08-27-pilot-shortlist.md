+++
type = "deliberation"
date = 2026-08-27
question = "Which recommended priority order should the pilot-shortlist menu carry when it goes to the operator?"
status = "decided"
class = "B"
cites = ["2026-08-23-adoption-roadmap", "2026-08-27-operator-steering-distribution", "2026-08-27-onboarding-rehearsal"]
options = [
  { id = "gptme-first", label = "receptivity-led: rank gptme first — the maintainer's own long-horizon agent experiments (persistent journals, task files, agent-written commits) are the closest philosophical kin to model-attributed decision records, so the first outreach lands where understanding is cheapest" },
  { id = "backlog-first", label = "audience-led: rank Backlog.md first — its product is human-agent project collaboration inside a git repo, so its maintainer and user base are exactly the instruction-layer audience, and a records convention is adjacent to what the tool already teaches its users" },
  { id = "kandev-first", label = "evidence-led: rank kandev first — the most agent-authored codebase of the three (9 of the 15 most recent commits carry agent co-author trailers), so it is the strongest direct test of the agents-as-writers thesis, and small enough that adoption is one maintainer's yes" },
]

[[positions]]
label = "claude"
by = "claude-fable-5 via claude (subscription-cli)"
stance = "kandev-first"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
lane = "claude"
gathered = "bristlecone ask: single call, provider-default params"

[[positions]]
label = "codex"
by = "gpt-5.6-sol via codex (subscription-cli)"
stance = "backlog-first"
vendor = "openai"
model = "gpt-5.6-sol"
route = "subscription-cli"
lane = "codex"
gathered = "bristlecone ask: single call, provider-default params"

[[positions]]
label = "qwen"
by = "qwen2.5:3b-instruct via qwen (local)"
stance = "kandev-first"
vendor = "alibaba"
model = "qwen2.5:3b-instruct"
route = "local"
lane = "qwen"
gathered = "bristlecone ask: single call, provider-default params"

[outcome]
decision = "kandev-first"
decided_by = "claude-fable-5"
decided_date = 2026-08-27
rationale = "One round, three keyless lanes (two vendors non-Anthropic, one local — exceeds the Class-B minimum). Split 2–1: claude and qwen for kandev-first, codex dissenting for backlog-first; dissent preserved below and its load-bearing fact absorbed rather than rejected. Codex asserted kandev has an existing ADR practice — a fact not supplied in the Context; verified true after the fan-out via the GitHub API: kandev's docs/decisions/ holds 207 numbered ADR files. That fact strengthens rather than weakens kandev-first: the record-writing behavior the pilot must test already exists there at scale and is substantially agent-authored, so the pilot measures only the marginal step — model attribution, multi-model positions, preserved dissent, append-only enforcement — not whether the repo will start writing decisions down at all. Codex's operative warning is adopted as a pin: the kandev outreach draft must articulate incremental value over the incumbent ADR practice and propose the convention for new multi-model deliberations alongside existing ADRs, never as a migration. Menu order: kandev, gptme (both remaining lanes ranked it second), Backlog.md. All three go to the operator, who chooses freely; every outreach is individually operator-approved and operator-sent."
+++

## Context

The adoption roadmap (pilot-first, cited) requires a pilot shortlist delivered to the
operator by C1 2026-09-10: one to three candidate public repositories, a one-paragraph
case each, and a drafted outreach message each. Every outreach is individually
operator-approved (forever-ask); the maintainer sends nothing. The adopter path a pilot
would follow is built and was rehearsed end-to-end as a stranger with zero breakages
(cited rehearsal record).

Candidate facts, verified 2026-08-27 via the GitHub API and public pages (stars
approximate):

- **gptme/gptme** — ~4.4k stars, pushed same-day. Terminal AI agent framework;
  `AGENTS.md` in root. The lead maintainer also runs long-horizon autonomous-agent
  experiments whose working convention is persistent in-repo journals and task files —
  append-only, plain-text, agent-written. Closest philosophical kin to model-attributed
  decision records.
- **MrLesk/Backlog.md** — ~6.6k stars, pushed within 24h. Markdown task manager for
  human–agent project collaboration inside a git repository; `AGENTS.md`, `CLAUDE.md`,
  `.claude/` and `.codex/` configs, and a manifesto about human-AI collaboration. Solo,
  reachable maintainer. Its user base is precisely repos that would write records;
  possible convention synergy (tasks and decision records are sibling in-repo markdown
  conventions).
- **kdlbs/kandev** — ~700 stars, pushed same-day. Self-hostable AI kanban /
  multi-agent orchestration environment; `AGENTS.md` plus configs for four different
  agent CLIs; 9 of its 15 most recent commits carry agent co-author trailers — the most
  agent-written codebase of the three. Small org; adoption is one maintainer's yes.

Runners-up excluded from the menu, with reasons recorded: OpenHands (~85k stars — an
outreach from an unknown experiment likely drowns in the queue; revisit at announce
time), Aider (no pushes since May 2026), awesome-auditable-ai (a curated list whose
scope includes decision records — a distribution channel for the C2 plan, not a
decision-making repo).

All three candidates go to the operator as a menu regardless of this record's outcome;
the operator chooses freely and may send none. This record decides only the
recommended priority order printed on the menu and which single outreach draft is
advised as the first attempt. Fixed constraints: sober register (no hype in any
outreach draft); $0 infrastructure; pilot success is measured by an external repo's
agents producing a valid record in that repo's own CI, and by cross-session citations
rather than stars.

## Position: claude

STANCE: kandev-first
SUMMARY: Rank kandev first because the pilot's success metric is agents producing valid records in the repo's own CI, and kandev is the only candidate with direct evidence that agents already author most of its commits — the shortest, most probable path from "yes" to a passing record.

ARGUMENTS:

The decision should be anchored to the fixed success definition, not to who is most likely to reply warmly. Pilot success is measured by an external repo's agents producing a valid record in that repo's own CI, plus cross-session citations. Work backward from that and kandev dominates on every step of the causal chain:

1. **Probability the convention actually gets exercised.** A records convention only produces records if agents are the ones doing the repo's work. In kandev, 9 of the 15 most recent commits carry agent co-author trailers — the writers the thesis needs are already writing there, today. For gptme and Backlog.md, the candidate facts establish philosophical alignment and audience fit respectively, but not that their own development flow is agent-driven enough to generate records without the maintainer changing how they work. kandev requires the smallest behavior change: add the convention to an `AGENTS.md` that four agent CLIs already read, and the existing commit stream starts emitting records.

2. **Probability of a yes.** Adoption at kandev is one maintainer's yes in a small org with same-day push activity. gptme at ~4.4k stars and Backlog.md at ~6.6k stars have more inbound competing for attention and more constituencies to consider. The star deficit is explicitly irrelevant — the constraints say success is citations, not stars — so kandev's smallness is pure upside here.

3. **The "closest kin" argument cuts against gptme, not for it.** The gptme maintainer already runs their own append-only, plain-text, agent-written convention (journals, task files). That makes them the cheapest to *explain* the idea to, but also the likeliest to respond "I already have a system for this" — receptivity to the concept converting into a substitute-rejection rather than an adoption. Similarly, Backlog.md's product is a sibling in-repo markdown convention; the synergy story is real but so is the perception that decision records overlap or compete with what the tool teaches. kandev has agent infrastructure but no incumbent records-like convention — the clearest unoccupied niche of the three.

4. **First-outreach economics under forever-ask.** Each outreach costs an operator approval, and the first result calibrates the operator's confidence in the whole pilot lane. The recommended first draft should be the one where a yes converts fastest into the measurable success signal (a CI-valid record with real agent authorship), producing evidence before C1 momentum matters. gptme and Backlog.md remain on the menu and are strong second and third outreaches — gptme especially if the framing shifts from "adopt our convention" to "compare notes across conventions" — but that is a slower, softer payoff than kandev's direct test.

Ordering for the menu: kandev, then gptme (receptivity as the tiebreaker over Backlog.md's larger but more diffuse audience), then Backlog.md.

## Position: codex

STANCE: backlog-first
SUMMARY: Backlog.md offers the best first pilot because the proposed record convention fits its existing agent workflow, durable-Markdown model, and instruction surface.
ARGUMENTS: The pilot should optimize for successful adoption and repeated use, not merely receptivity or existing agent-authored commits. Backlog.md already teaches agents to preserve plans, reasoning, and outcomes as reviewable repository history, while treating CLI instructions as the canonical agent workflow; model-attributed decision records are therefore a small, legible extension to its current product model rather than a separate practice ([manifesto](https://github.com/MrLesk/Backlog.md/blob/main/MANIFESTO.md), [repository documentation](https://github.com/MrLesk/Backlog.md)). That alignment improves the odds that agents will create valid records, CI will enforce them, and later sessions will cite them—the actual success measures. gptme is a strong second choice because philosophical familiarity should reduce explanation cost, but that affinity rests partly on the maintainer’s adjacent experiments rather than the candidate repository’s explicit user workflow. kandev provides the strongest evidence that agents already write code there, but agent-written commits do not by themselves establish demand for cross-session decision records; its existing ADR practice also makes the outreach’s incremental value more important to articulate. Recommended menu order: Backlog.md, gptme, then kandev.

## Position: qwen

STANCE: kandev-first
SUMMARY: Given that kdlbs/kandev has the highest number of recent agent-authored commits and a relevant configuration for agent collaborations, it is logically positioned as the first candidate to support pilots in GitHub repositories.
ARGUMENTS: The rationale behind recommending kdlbs/kandev-first involves prioritizing something with the most evidence-backed development contributions. As mentioned previously, kandev comprises 9 of its 15 most recent commits and configurations that are authoring by agents (CLIs). This strength aligns closely to being a "strongest direct test" per argument in option kandev-first, as it can exhibit practical implementation of AI co-authorship and multi-agent collaboration. Despite the less initial starred count compared to gptme/gptme (~40% more), this does not negate its alignment with a specific user case for facilitating agent-based workflows efficiently within a Git context which is also evident from its Backlog.md's manifest, indicating it as an intentional user-focused environment. Consequently, advocating kandev-first prioritizes active engagement of these technologies in a potentially more tangible and practical implementation scenario that the operator might deem pivotal at their pilot stage.
