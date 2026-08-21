+++
type = "deliberation"
date = 2026-08-21
question = "Execute the public flip now?"
status = "decided"
class = "C"
cites = ["2026-08-20-public-timing", "2026-08-21-m1-verification"]

[[positions]]
label = "operator"
by = "deluongo (human operator)"
stance = "flip"
route = "human"
gathered = "operator's ruling in-session, quoted verbatim in the body; participation class: direct operator ruling (see the M0 interpretive rule) — no model lanes; the decision this executes was deliberated in the cited records"

[outcome]
decision = "flip"
decided_by = "deluongo"
decided_date = 2026-08-21
authority = "public exposure is an operator forever-ask (CONSTITUTION.md, Decision rights; STANDING_AUTHORIZATIONS.md) — exercised here"
rationale = "The condition set in 2026-08-20-public-timing was satisfied and re-verified minutes before the flip: a full-history secret scan (credential shapes + base64 blobs) and a full-history private-context sweep, both clean across all 8 commits, with zero keys existing anywhere in the project by design until the M2 key-hardening review. The operator confirmed the zero-key state and ruled. Executed immediately: repository public, GitHub Pages site created and serving, m1 tag laid on the verified commit per 2026-08-21-m1-verification."
+++

## Context

`2026-08-20-public-timing` decided the repository goes public at M1, on the operator's button, after a clean full-history secret scan. `2026-08-21-m1-verification` verified M1's build criteria and ruled that the `m1` tag lands at this flip. This record documents the button press — the ruling itself, its condition check, and what executed.

## Position: operator

Quoted verbatim (2026-08-21, in-session):

> Sure. You can flip public. We still have no keys in this repo correct?

The question in the ruling was answered in the affirmative with evidence before execution: no keys have ever existed in the repository or its history — the M0–M1 design is keyless (subscription CLIs and local models only), the single metered lane stays disabled until the operator approves `docs/KEY-HANDLING.md` at M2, and the pre-flip full-history scans came back clean.

## Execution log (same session, PT)

1. Full-history credential-shape scan + private-context denylist sweep re-run over all 8 commits: clean.
2. Repository visibility flipped to public.
3. GitHub Pages site created (`build_type: workflow`; the workflow's own token could not create the site — one manual API call, then the workflow deployed cleanly).
4. Site live and verified serving the archive with commit stamps.
5. `m1` tag laid on the verified commit (`dd793bd`) citing `2026-08-21-m1-verification`.
6. Branch protection enabled on `main`: force pushes and deletions blocked (the constitution's third append-only enforcement layer).
