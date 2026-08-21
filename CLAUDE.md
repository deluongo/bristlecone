# CLAUDE.md — Bristlecone session rules

This repo is the product of the experiment described in README ¶1. Sessions here follow this ritual, in order. Skipping a step is a process bug for `docs/PROCESS_REFLECTIONS.md`.

## Session ritual

1. **Read**: `docs/INBOX.md` (operator steering — act on it FIRST), `docs/_handoffs/CURRENT_STATE.md`, `STANDING_AUTHORIZATIONS.md`, and private memory (`bristlecone-operating-plan` and linked files).
2. **Declare**: pick exactly ONE milestone step; write it into CURRENT_STATE "In flight" with its done-check *before* starting work.
3. **Deliberate if decision-class** (Constitution: Class A/B/C). Record the entry in `records/` before or with the implementing change.
4. **Do**: implement, tests-first (global engineering defaults apply: coverage ≥80% once the package exists, xenon B, ruff).
5. **Record**: commit the record *with* the change it governs; add trailer `Decision-Ref: <record-id>` on design-changing commits.
6. **Handoff**: update CURRENT_STATE (shipped row, in-flight cleared or carried); update TREASURY if any metered call happened (none before M2).
7. **Ship**: `scripts/ship.sh` (hygiene greps + local denylist gate + explicit-path add + commit + push). Never `git add -A`.
8. **Digest**: end the session with the 5-line digest (template below).

## Hard rules

- **Session fuse**: 4h wall clock OR $0.10 metered spend → wrap anyway; tag the handoff row `FUSED:<reason>`; two consecutive FUSED on the same step ⇒ raise it as the digest's one question.
- **Zero secrets until M2.** No API keys in env, args, or files. The metered lane is blocked until the operator approves `docs/KEY-HANDLING.md`. Never touch `~/secrets/**`, `~/.config/sops/**`, `~/.codex/**`.
- **Privacy placement test** for every tracked sentence: *would the operator publish this?* Operator's other projects, clients, and personal context are paraphrased generically or omitted. The denylist gate is local (`denylist.local.txt`, gitignored) because a public denylist would leak what it protects.
- **Commit trailers**: `Co-Authored-By: <model> <noreply@anthropic.com>` (or vendor-appropriate) required; `Decision-Ref:` on design changes; **no session-transcript URLs** (operator ruling 2026-08-20).
- **Append-only**: never edit a terminal-status record except `superseded_by`/`status`; never delete or rename under `records/`.
- **Never re-ask a granted authorization**; forever-ask items are listed in STANDING_AUTHORIZATIONS.md.
- Timestamps in operator-facing docs: **PT**.
- Main-only + milestone tags. Milestone completion is verified by the NEXT session, fresh-context, against the milestone checklist — the finishing session may not self-certify.

## Digest template (exact 5 lines)

```
1: <session-slug> — <milestone step> [DONE|FUSED]
2: shipped: <one line>
3: deliberated: <n> records, <n> dissents — <link or path>
4: burn: fable ~<N> tok | metered $<x.xx> wk (cap $0.70) | $<y.yy>/$20.00 lifetime
5: next: <intent> | Q: <none | exactly one question>
```
