+++
type = "deliberation"
date = 2026-08-27
question = "Approve docs/KEY-HANDLING.md and open the metered-lane gate?"
status = "decided"
class = "C"
cites = ["2026-08-21-key-handling-design"]

[[positions]]
label = "operator"
by = "deluongo (human operator)"
stance = "hold"
route = "human"
gathered = "written by the operator directly into docs/KEY-HANDLING.md, 2026-08-27; moved here verbatim (the design doc now carries a status line pointing at this record); participation class: direct operator ruling (M0 interpretive rule) — no model lanes"

[outcome]
decision = "hold"
decided_by = "deluongo"
decided_date = 2026-08-27
authority = "the first metered API call is gated on operator approval of docs/KEY-HANDLING.md — a forever-ask (STANDING_AUTHORIZATIONS.md; CONSTITUTION.md, Decision rights). Declining to approve is an exercise of that same right."
rationale = "The operator reviewed the KEY-HANDLING draft and ruled hold: the design reads well but his instinct says holes remain, and he is not ready to place a key. Effect: nothing changes operationally — the gate was already closed and fails closed (`declined:gate`), and the pilot-first roadmap is $0 by definition, so no queued work blocks on this. The approval leaves the pending-asks list and becomes operator-initiated: it returns only when the operator raises it, and before any re-ask the maintainer owes an adversarial hole-hunt review of the design (a fresh fan-out prompted to attack it, not defend it) so the gut concern is answered with evidence. His question — whether the Bristlecone design itself needs key handling so other people can add models to their own versions — is answered in the body."
+++

## Context

`docs/KEY-HANDLING.md` (drafted M2-S1, `2026-08-21-key-handling-design`) is the
operator gate for the single metered lane (DeepSeek). The design was awaiting operator
approval — the forever-ask that would permit the first metered API call. On 2026-08-27
the operator wrote his review directly into the design doc. This record archives that
ruling; the doc keeps a status line pointing here.

## Position: operator

Quoted verbatim from `docs/KEY-HANDLING.md` (2026-08-27):

> I'm not ready to do this. The design sounds good, though my gut tells me there's
> still holes. Beyond adding other models to our bristlecone dev flow, the actual
> bristlecone design needs this as well correct? So other people can add more models
> to their own versions?

## Maintainer answer to the operator's question

Mostly no — and the distinction is load-bearing for the roadmap. What an adopter
copies is the *convention*: the record format, the validator, and lanes that cost $0
because they ride the adopter's own subscription CLIs or local models. No API key is
required anywhere on that path; the MVP definition in `2026-08-23-adoption-roadmap`
is "no secrets, $0" on purpose. If an adopter wants a metered API lane in their own
archive, they hold their own key under their own scheme — Bristlecone never touches
it. Our KEY-HANDLING.md is the hardening for *this repository's* one metered lane,
not a component of the product. What does generalize is the pattern (key never
reachable from AI-editable code; operator-pinned client; scrub gate wrapping every
transport), and a generalized "if you add metered lanes" guidance page is a
reasonable post-MVP addition to the adopter docs. Holding approval therefore blocks
nothing: not the adopter path, not the pilots, not the announce draft.

## Effect

1. The metered gate remains closed; `bristlecone ask` continues to record the
   DeepSeek lane as `declined:gate` at $0 — working as designed.
2. KEY-HANDLING approval leaves the pending-operator-asks list. Re-entry trigger:
   the operator raises it (INBOX or in-session). It will not be re-asked.
3. Before it can return, the maintainer runs an adversarial review of the design —
   lanes prompted to find holes, findings recorded — so the operator's "gut says
   holes" is met with an attack surface actually searched, not reassurance.
