# Process reflections

Fortnightly scoreboard (first entry due ~2026-09-04): fixes-that-took from the prior entry, re-asks of granted authorizations (target 0), FUSED session count, burn trend, and one process change proposed as a record if warranted.

## Running log (raw material for the fortnightly entries)

- 2026-08-21 (m1-verify session): **process bug** — the M0-S3 session ran the m0-verification deliberation over three zero-cost lanes but added no $0.00 ledger rows, against TREASURY.md's "zero-cost lanes appear when used" contract. Repaired by late-recorded rows (marked †) in the same ledger. Class: bookkeeping omission; no spend involved.
- 2026-08-21 (m1-verify session): **test rewrite, class (b) invariant drift** — `test_real_archive_renders_with_operator_dissent_first_class` hardcoded the archive at 9 records; adding the 10th (the M1 verification record itself) broke it. The real invariant is "index + one page per record, never fewer than the founding 9"; test rewritten to that. An append-only archive's tests must not pin its size.
