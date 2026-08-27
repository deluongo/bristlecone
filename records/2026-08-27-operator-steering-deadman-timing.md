+++
type = "deliberation"
date = 2026-08-27
question = "When is the Telegram dead-man bot actually set up, given the operator's standing approval?"
status = "decided"
class = "C"
cites = ["2026-08-20-adopt-constitution"]
relates_to = ["2026-08-27-key-handling-gate-held"]

[[positions]]
label = "operator"
by = "deluongo (human operator)"
stance = "defer-bot-setup"
route = "human"
gathered = "written by the operator in docs/INBOX.md, 2026-08-27; quoted in the body verbatim; participation class: direct operator ruling (M0 interpretive rule) — no model lanes"

[outcome]
decision = "defer-bot-setup"
decided_by = "deluongo"
decided_date = 2026-08-27
authority = "the dead-man routine itself is standing authorization S6 (granted 2026-08-20); account creation — the bot — is a forever-ask, and the operator here pre-answers that ask and sets its timing"
rationale = "The operator re-affirms the S6 grant unprompted (he raised it himself; nothing was re-asked), pre-approves the bot-creation forever-ask, and rules on timing: the maintainer asks for the channel when it is actually needed, suggested after the MVP/traction arc. He explicitly invited pushback on timing; the maintainer accepts the deferral with one recorded decoupling, taken up into this outcome: the bot ask anchors to the end of the MVP/traction arc (around C2, 2026-10-01), NOT to the KEY-HANDLING adversarial review — that review is operator-initiated per 2026-08-27-key-handling-gate-held and may legitimately never happen, and a continuity safeguard must not wait on a gate that has no scheduled reopening. If the review has happened by the arc's end, both of his suggested conditions are met; if not, the ask comes anyway. Concretely owed him at ask time: ~five minutes with Telegram's @BotFather plus creating a private channel; the bot token is a secret and stays entirely on his side of the boundary — the exact handling ships with the ask, designed so the token never enters this repository or any AI-editable surface."
+++

## Context

Fourth operator steering message of the arc, and the second on 2026-08-27. S6 (the
weekly read-only dead-man routine, 3-day silence threshold, Telegram delivery) was
granted at the founding review; the one open piece was an account-creation
forever-ask — someone has to create the bot — which had been queued as
"ask when he has a minute." The operator answers that pending ask before it was made,
and sets its timing. Archived here verbatim per the INBOX protocol; the maintainer's
response lives in `docs/INBOX.md`.

## Position: operator

Quoted verbatim from `docs/INBOX.md` (2026-08-27):

> What do you need from me for the telegram dead-man routine. I approve. Just ask me
> to set up a channel when you need it. I'd suggest after the adversarial review on
> key handling, after the MVP/traction arc. I'm not going to forget in the short
> term. Feel free to ask for anything else or push back on my timing suggestions.

*(Verbatim as written — records are testimony.)*

## Effect

1. The dead-man bot leaves the pending-operator-asks list. It returns as one
   concrete ask at the end of the MVP/traction arc (~C2), with setup instructions
   and the token-boundary design attached.
2. The anchor is the arc, not the KEY-HANDLING review (decoupling rationale in the
   outcome). The two remain independent tracks.
3. Nothing else is needed from the operator now; the next real ask remains the
   pilot shortlist around C1 (2026-09-10).
