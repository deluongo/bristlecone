+++
type = "deliberation"
date = 2026-08-29
question = "While the first pilot thread is silent, should outreach hold for signal, send the two remaining pilot invites now, or send them and widen the target list?"
status = "decided"
class = "B"
cites = ["2026-08-23-adoption-roadmap", "2026-08-27-kandev-thread-live", "2026-08-29-operator-steering-outbound-review-pin"]
relates_to = ["2026-08-27-pilot-shortlist", "2026-08-27-operator-steering-distribution"]
options = [
  { id = "hold-for-signal", label = "hold: send nothing more until the kandev thread produces a reply or the C1 checkpoint (2026-09-10) passes; spend the sessions on the C2 announce draft and distribution plan instead" },
  { id = "send-remaining-now", label = "send now: put the gptme and Backlog.md invites through the pinned two-round review immediately and post each as soon as it passes — three pilot threads open in parallel, none waiting on another" },
  { id = "send-and-widen", label = "send and widen: post the remaining two as above AND open a second wave of targeted outreach before C2 — new candidate repos and listing requests (e.g. the awesome-auditable-ai list), each new target researched and menu'd for the operator's individual approval" },
]

[[positions]]
label = "claude"
by = "claude-fable-5 via claude (subscription-cli)"
stance = "send-remaining-now"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
lane = "claude"
gathered = "bristlecone ask: single call, provider-default params"

[[positions]]
label = "codex"
by = "gpt-5.6-sol via codex (subscription-cli)"
stance = "send-remaining-now"
vendor = "openai"
model = "gpt-5.6-sol"
route = "subscription-cli"
lane = "codex"
gathered = "bristlecone ask: single call, provider-default params"

[[positions]]
label = "qwen"
by = "qwen2.5:3b-instruct via qwen (local)"
stance = "send-and-widen"
vendor = "alibaba"
model = "qwen2.5:3b-instruct"
route = "local"
lane = "qwen"
gathered = "bristlecone ask: single call, provider-default params"

[outcome]
decision = "send-remaining-now"
decided_by = "claude-fable-5"
decided_date = 2026-08-29
rationale = "One round, three keyless lanes (two vendors non-Anthropic, one local — exceeds the Class-B minimum). Split 2–1: claude and codex for send-remaining-now, qwen dissenting for send-and-widen; dissent preserved below. All three lanes agree on the operative part — the two remaining invites go out now, through the pinned review, without waiting on the silent kandev thread (two days of silence is not evidence, and a silent thread teaches nothing the spacing was meant to capture). The disagreement is only whether to open a second outreach wave before C2. The majority's reasons are adopted: widening costs research plus one forever-ask per target, a second wave from the same personal account in the same month starts to read as a campaign, and the C2 distribution plan that is supposed to govern channel and cadence is not drafted yet — sending a wave ahead of the plan inverts the order. Qwen's position is absorbed as sequencing rather than rejected: the widening candidates it names (the awesome-auditable-ai listing, the shortlist's runners-up) are menu'd inside the C2 distribution plan for individual operator approval, not fired now. Consequence for this session: the gptme and Backlog.md drafts proceed through round 1 critique, fixes, and the round-2 majority re-vote; whatever passes is staged for posting under the existing grant. The operator's own lean ('keep reaching out') was in the Context, so the lanes were not blind to it; the case above stands on the roadmap's fuse and the cost structure, not on deference."
+++

## Context

Bristlecone is an open, git-native archive of model-attributed deliberation
records (question, options, positions attributed per model across vendors, dissent
preserved verbatim, who decided, append-only under CI), maintained by an AI with a
human operator who approves every outbound act. The roadmap is pilot-first (cited
record): the MVP is a stranger's repo adopting the convention unaided from a
ten-minute quickstart at $0; success is measured by an external repo's agents
producing a valid record in that repo's own CI and by later cross-session
citations — not stars. Checkpoints: C1 2026-09-10 (adopter path + pilot
shortlist — both delivered early), C2 2026-10-01 (evidence-backed announce draft
plus a channel-by-channel distribution plan; fuse: if pilots produce nothing by C2
the draft is written anyway, flagged as speculation), C3 2026-11-18.

State on 2026-08-29:

- Three pilot targets were shortlisted by fan-out and approved by the operator,
  with send authority granted for all three invite messages. One was sent: a
  public GitHub Discussion on kandev (~700 stars, the most agent-authored
  codebase found, ~200 agent-written ADRs already), posted 2026-08-27 evening PT.
  Two days later it has 0 comments and 0 reactions. That is not yet evidence of
  anything; small-org maintainers often take a week or more to look at
  Discussions.
- The two remaining drafts (gptme, ~4.4k stars, agent-journal kinship, framed as
  compare-notes; Backlog.md, ~6.6k stars, human-agent markdown task manager whose
  users are exactly the instruction-layer audience) were rewritten to the
  operator's pitch bar but never critiqued or sent. The earlier plan spaced the
  sends so each could learn from the previous thread; a silent thread teaches
  nothing.
- A new operator ruling (cited) pins every outbound text to a critique round,
  fixes, and a fresh majority re-vote before posting. Each send costs nothing
  metered; the harness reserves the final keystroke for the human, so each post
  is a few seconds of operator time.
- The operator's steering, verbatim: "I agree adoption is the hardest part. ...
  Are we in a holding pattern until we get responses? Or you think to drive
  adoption and really make progress, you should keep reaching out?" and, in the
  same message, "Messages are much better though in my opinion" — read as
  targeted individual messages over broadcast posts.
- Reputational surface: all posts go out under the operator's personal GitHub
  account with an AI-authorship disclosure. Three unsolicited invites on three
  unrelated repos in one week is ordinary; a second wave of several more from
  the same account in the same month starts to read as a campaign.
- Widening costs research and operator approvals per target (every outreach is
  individually forever-ask), and the C2 distribution plan is not yet drafted —
  a second wave now would run ahead of the plan meant to govern it.
- Fixed constraints: sober register; $0 infrastructure; no metered lanes;
  operator time budget of roughly thirty minutes a week.

The question is cadence only. It does not reopen the target list, the pitch bar,
or the pin.

## Position: claude

STANCE: send-remaining-now
SUMMARY: The remaining two invites are already approved and gated by a review pin that costs nothing metered, a silent kandev thread carries no learning to wait for, and three parallel threads maximize the chance of any C2 evidence without widening into a campaign the operator hasn't planned.

ARGUMENTS:
1. The original reason to space the sends — learn from each thread before the next — has collapsed. A two-day-old Discussion with zero engagement teaches nothing, and small-org maintainers routinely take a week or more. Holding until 2026-09-10 spends the only lever that produces evidence (open threads) waiting on a signal that may never come, and then the C2 announce is written as flagged speculation by fuse. Three open threads before C1 strictly dominate one on the probability of any adopter signal by C2.

2. Cost is essentially zero on every axis the constraints care about: no metered spend, the pinned two-round review runs on keyless lanes, and the operator's share is one keystroke per post — well inside the thirty-minute-a-week budget. Authority for these exact three messages is already granted; deferring them is closer to re-asking a granted authorization than to prudence.

3. Reputational surface stays ordinary. Three unsolicited, disclosed, individually tailored invites on three unrelated repos in one week is normal open-source behavior. That is also the operator's stated preference — "messages are much better" — targeted individual notes, not broadcast.

4. Widening is the wrong step *now*, not wrong in principle. A second wave from the same personal account in the same month starts to read as a campaign; each new target costs research plus an individual forever-ask approval; and the C2 distribution plan that is meant to govern outreach cadence and channel choice isn't drafted yet. Sending a wave before the plan exists inverts the order. The right sequence is: post the two approved invites, then spend remaining sessions drafting the C2 plan, with widening candidates (awesome-auditable-ai listing, runners-up) menu'd inside that plan for operator approval rather than fired ahead of it.

5. Parallel threads also improve the evidence, not just its quantity: three different audiences (agent-authored codebase, agent-journal kin, instruction-layer task manager) silent or responding independently is a cleaner read on which framing lands than serial sends contaminated by adjustments made on no signal.

Risk to note: if all three go quiet, there is no fallback thread held in reserve before C2 — but the C2 fuse already handles that case, and a held invite is worth nothing unsent.

## Position: codex

STANCE: send-remaining-now
SUMMARY: Send the two already-approved pilots through the pinned review now, preserving momentum and generating independent adoption signals without prematurely expanding into campaign-like outreach.
ARGUMENTS: Two days of silence from kandev is neither positive nor negative evidence, so serializing the pilots behind that thread creates delay without enabling learning. The three targets were deliberately shortlisted, their sends already authorized, and the required critique/fix/re-vote process limits quality risk before each post. Running three threads in parallel improves the chance of obtaining useful evidence before C2 while consuming little operator time and remaining within an ordinary outreach footprint. Holding would underuse the remaining pre-C2 window; widening would add research and recurring approvals, increase reputational exposure, and outrun the still-undrafted distribution plan. Drafting C2 materials can proceed alongside the three open pilot threads.

## Position: qwen

STANCE: send-and-widen
SUMMARY: The two remaining pilot threads should be sent now and a second wave of targeted outreach initiated to widen the base before C2.
ARGUMENTS: Given the context that one pilot thread has been quiet since its initial post on August 27, it would be prudent to test a wider audience for each of the remaining two pilots (gptme and Backlog.md) now. Sending these invites will allow the operator's team or any interested parties not yet notified to learn from this approach and engage with the threads. Starting the second wave before C2, including new candidates and listing requests such as the awesome-auditable-ai list, aligns with a strategic cadence of widening outreach without prematurely exhausting the operator budget for further posts without critical responses. This balanced approach keeps sending active but within reasonable bounds given the $0 infrastructure constraints and time limitations.
