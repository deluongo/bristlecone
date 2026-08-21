# CURRENT_STATE

Seed document for any session (or successor model) picking up this project. Ceiling: 80KB (rows rotate to `ARCHIVE-YYYY-MM.md`). Timestamps PT.

## Arc goal

M0 bootstrap (week 1): found the project — governance, spec draft, founding records hand-written with **no package code** — so that M1 can build validate+render against a real corpus.

## Shipped

| # | Date | Step | Outcome |
|---|---|---|---|
| 1 | 2026-08-20 | M0-S1: repo founded — governance docs, spec v0 draft, templates, hygiene CI, ship script, founding records (name, envelope, license, records-dir, public-timing, constitution-adoption) | see records/ |

## In flight

*(none — session M0-S1 complete)*

## Queued (M0 remainder)

- M0-S2: spec/examples/ — one canonical valid record + labeled-invalid fixtures; refine spec from hand-writing experience; open the dead-man-routine design note
- M0-S3: operator weekend review — record rulings on CONSTITUTION + STANDING_AUTHORIZATIONS as operator-ruling records; close M0 checklist (exit criteria in plan)

## Open design decisions

- `records/2026-08-20-adopt-constitution.md` — **open**, awaits operator ruling (weekend review)
- Dead-man routine implementation detail (post-flip, S6 granted): design note queued for M0-S2

## Test baseline

No package code yet (by design). CI = hygiene greps only. Coverage/xenon/ruff gates activate in M1 with the first Python.

## Pointers

- Plan of record: operator-side (`~/.claude/plans/i-want-to-give-merry-lobster.md`)
- Governance: `CONSTITUTION.md` · authorizations: `STANDING_AUTHORIZATIONS.md` · money: `TREASURY.md`
- Format: `spec/RECORD-FORMAT-v0.md` · archive: `records/` · operator steering: `docs/INBOX.md`
- Session rules: `CLAUDE.md` (ritual, fuse, digest template)

## What a fresh session should ask itself

1. Did I read INBOX first? 2. Is exactly one step declared in-flight? 3. Does my work cite or create a record? 4. Will ship.sh pass (hygiene + denylist)? 5. Is my digest's line 4 computed, not estimated?
