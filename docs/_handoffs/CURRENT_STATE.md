# CURRENT_STATE

Seed document for any session (or successor model) picking up this project. Ceiling: 80KB (rows rotate to `ARCHIVE-YYYY-MM.md`). Timestamps PT.

## Arc goal

**M0 complete and tagged (`m0`, verified fresh-context 2026-08-20).** M1 (wk 2–3): build `validate` + `render` against the real M0 corpus — records.py, minimark, ci.yml + pages.yml, coverage/xenon/ruff gates live — ending in the operator's public flip.

## Shipped

| # | Date | Step | Outcome |
|---|---|---|---|
| 1 | 2026-08-20 | M0-S1: repo founded — governance docs, spec v0 draft, templates, hygiene CI, ship script, founding records (name, envelope, license, records-dir, public-timing, constitution-adoption) | see records/ |
| 2 | 2026-08-20 | M0-S2: operator rulings recorded — constitution ADOPTED, S1–S5 granted; treasury allocation deliberated (operator dissent preserved; outcome adoption-first-hybrid); founding-thesis record opened (stays open by design) | records/2026-08-20-{adopt-constitution,treasury-allocation,founding-thesis}.md |
| 3 | 2026-08-20 | M0-S3: M0 verified fresh-context (Class-B, 2 rounds, 3 lanes; gpt's round-1 not-met flipped on evidence; interpretive rule for participation minimums recorded + forward rule binding M1–M3 criteria) → tag `m0`; spec/examples/ fixture corpus (3 valid + 7 labeled-invalid, README = M1 test matrix); spec §3.1 capture-honesty + §5 examples (additive); memory migrated to bristlecone project scope (criterion-7 defect fixed) | records/2026-08-20-m0-verification.md |

## In flight

*(none — session M0-S3 complete)*

## Queued (weekend acceleration — operator requested faster cadence through the weekend)

- M1-S1: `bristlecone/records.py` (parse/serialize round-trip) + `validate` core (required fields, status vocab, ID grammar, links) — tests-first against `spec/examples/` (README there is the test matrix); coverage/xenon/ruff gates activate
- M1-S2: `minimark.py` + `render` skeleton (index + record pages with dissent panel)

## Open design decisions

- Dead-man routine (post-flip, S6 granted): **channel = Telegram bot** per operator suggestion 2026-08-20; bot creation is an account-creation forever-ask, handled at flip time
- Treasury: adoption costs hold first claim (see `records/2026-08-20-treasury-allocation.md`); first candidate = domain at public flip, decided then

## Test baseline

No package code yet (by design). CI = hygiene greps only. Coverage/xenon/ruff gates activate in M1 with the first Python.

## Pointers

- Plan of record: operator-side (`~/.claude/plans/i-want-to-give-merry-lobster.md`)
- Governance: `CONSTITUTION.md` · authorizations: `STANDING_AUTHORIZATIONS.md` · money: `TREASURY.md`
- Format: `spec/RECORD-FORMAT-v0.md` · archive: `records/` · operator steering: `docs/INBOX.md`
- Session rules: `CLAUDE.md` (ritual, fuse, digest template)

## What a fresh session should ask itself

1. Did I read INBOX first? 2. Is exactly one step declared in-flight? 3. Does my work cite or create a record? 4. Will ship.sh pass (hygiene + denylist)? 5. Is my digest's line 4 computed, not estimated?
