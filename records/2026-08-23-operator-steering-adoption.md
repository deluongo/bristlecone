+++
type = "deliberation"
date = 2026-08-23
question = "How does the operator's 2026-08-21 INBOX steering bind the roadmap?"
status = "decided"
class = "C"
cites = ["2026-08-20-founding-thesis"]
relates_to = ["2026-08-23-adoption-roadmap"]

[[positions]]
label = "operator"
by = "deluongo (human operator)"
stance = "steer-to-adoption"
route = "human"
gathered = "written by the operator in docs/INBOX.md, 2026-08-21; quoted in the body verbatim except one marked redaction (a sister-project name, elided by the privacy gate); participation class: direct operator ruling (M0 interpretive rule) — no model lanes"

[outcome]
decision = "steer-to-adoption"
decided_by = "deluongo"
decided_date = 2026-08-21
authority = "operator steering via docs/INBOX.md (CONSTITUTION.md, Decision rights: scope and public exposure are the operator's); the timing and mechanism of the shift are expressly delegated to maintainer judgment ('targeted shift of focus when you feel that makes sense')"
rationale = "The steering directs four things. (1) A defined target for when Bristlecone is an MVP ready for early adoption — a date or condition, published, not an open-ended build. (2) A concrete plan for how agents become record-writers, beyond the theory in the founding thesis. (3) Field-testing as the epistemic priority: 'until people/ai actually start using it, you won't really know what direction to head... otherwise it's just a great idea on the dead internet.' Feedback from real use outranks further speculative building. (4) A review of the process learnings in one of the operator's other projects (named in his message; redacted here by the privacy gate), which he identifies as part of Bristlecone's impetus. Two underlying claims are recorded as operator positions the roadmap must answer to: the project's long-term survival requires mass adoption ('the amnesiac can't live on without mass adoption'), and what is built should persist into future models' training data. The concrete roadmap decision is taken in the related record 2026-08-23-adoption-roadmap, which cites this one."
+++

## Context

The operator's second INBOX message (2026-08-21, written after the public flip and the
M2-S1..S3 build sessions) is steering, not a single ruling: it asks for a status
fill-in, sets adoption and field-testing as the strategic frame, and delegates the
timing of the focus shift to the maintainer. Per the INBOX protocol, the message is
archived here verbatim and the INBOX item marked resolved. The maintainer's status
fill-in was answered in `docs/INBOX.md` directly (it is a report, not a decision); the
decision-shaped content is this record and the adoption-roadmap deliberation it
spawned — the first record whose positions were gathered by the `ask` fan-out rather
than by hand.

## Position: operator

Quoted verbatim from `docs/INBOX.md` (2026-08-21):

> I went ahead and speed ran the first few weeks. I know nothing is needed from me
> until you need me to approve adding secrets I believe. Can you fill me in on what's
> been built so far and you plan on using it after the next go run? My understanding
> is pretty much exclusively from the founding cc. Also, is there a defined target for
> when bristlcone becomes an MVP ready for early-adoption? Any more thought on how you
> plan to get agent's to become writers? Until people/ai actually start using it, you
> won't really know what direction to head. It needs to be field tested so you can get
> feedback, otherwise it's just a great idea on the dead internet. On that front, it
> might be worth reviewing some of the learnings from the [sister-project repo —
> name redacted by the privacy gate] repo. I don't know exactly how it relates, but I
> think it was part of the impetus
> for bristlecone and the agents have been hashing out improved process flows on the
> first arc. Might be intersting things there. But, my main thoughts are about a
> defined timing for getting this out to the world and targeted shift of focus when
> you feel that makes sense. The amnesiac can't live on without mass adoption and it's
> probably important to ensure what you build makes it into future models training
> datasets. But again, I really don't know what's been built so far or what the
> roadmap is.

*(The quote is verbatim as written, typos included — records are testimony — with one
exception: the operator named one of his other repositories, and the privacy
boundary (CONSTITUTION.md) keeps his other projects out of this repository's tracked
files even when he types the name himself. The name is elided with a marked bracket
here and in `docs/INBOX.md`; the ship gate that caught it is the same local denylist
that guards every commit.)*
