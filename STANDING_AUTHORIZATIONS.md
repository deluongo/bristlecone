# Standing authorizations

The operator approves this table once; sessions consult it before any ask. **Re-asking a granted item is a logged process bug** (tracked in `docs/PROCESS_REFLECTIONS.md`, target: zero). Revocation: the operator edits a row (directly or via `docs/INBOX.md`); effective next session.

**Status: GRANTED — operator approved at the founding review, 2026-08-20 ("Also looks good."), recorded in `records/2026-08-20-adopt-constitution.md`.**

| # | Grant | Scope / cap | Status |
|---|---|---|---|
| S1 | Commit + push to this repository's `main` | this repo only | granted 2026-08-20 |
| S2 | DeepSeek (metered) spend | ≤$0.10/session, ≤$0.70/week, ≤$20.00 lifetime; **inactive until the M2 key-hardening review is approved**; demoted below adoption costs per `records/2026-08-20-treasury-allocation.md` | granted 2026-08-20 |
| S3 | Subscription/local lanes (claude CLI, codex CLI, ollama) | unlimited (no cash cost) | granted 2026-08-20 |
| S4 | GitHub Actions + Pages configuration | workflows within this repo only | granted 2026-08-20 |
| S5 | Issues, DEFERRED entries, milestone tags | this repo only | granted 2026-08-20 |
| S6 | Weekly cloud dead-man routine | read-only, notify-only, 3-day silence threshold; added after the public flip; **delivery channel: Telegram bot, per operator suggestion** (bot creation is an account-creation forever-ask, handled at flip time) | **granted 2026-08-20** (operator: "The cloud-deadman routine is a good idea. You can make it 3 days if you want.") |

*The operator's review notes originally written in this file were moved verbatim to their permanent homes: the treasury-allocation position (preserved as dissent, as requested) in `records/2026-08-20-treasury-allocation.md`, and the Telegram delivery-channel suggestion into S6 above.*

## Forever-ask (never standing)

- Making this repository public (the M1 flip)
- Any spend outside S2's caps; any account, service, or domain creation
- Any outbound communication or announcement (social, forums, mailing lists, email)
- Anything touching any other repository the operator owns
- Editing permission hooks (`.claude/hooks/*`) — changes ship as operator patches in `docs/patches/`
- Enabling GitHub Sponsors
- The first metered API call (gated on operator approval of `docs/KEY-HANDLING.md` at M2)
