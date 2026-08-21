# Process reflections

Fortnightly scoreboard (first entry due ~2026-09-04): fixes-that-took from the prior entry, re-asks of granted authorizations (target 0), FUSED session count, burn trend, and one process change proposed as a record if warranted.

## Running log (raw material for the fortnightly entries)

- 2026-08-21 (m1-verify session): **process bug** — the M0-S3 session ran the m0-verification deliberation over three zero-cost lanes but added no $0.00 ledger rows, against TREASURY.md's "zero-cost lanes appear when used" contract. Repaired by late-recorded rows (marked †) in the same ledger. Class: bookkeeping omission; no spend involved.
- 2026-08-21 (M2-S2 session): **process bug — local gate weaker than CI gate.** The session ran xenon locally with `--max-modules B` while ci.yml enforces `--max-modules A`, so main went red for one commit (`laneconfig.py` module-ranked B on average complexity; hygiene and pages stayed green). Fixed within the session by decomposing the parser into smaller helpers (avg 5.29 → 3.73) — no gate was weakened. Rule going forward: pre-ship gate runs must copy the exact commands out of ci.yml, not reconstruct them from memory.
- 2026-08-21 (m1-verify session): **test rewrite, class (b) invariant drift** — `test_real_archive_renders_with_operator_dissent_first_class` hardcoded the archive at 9 records; adding the 10th (the M1 verification record itself) broke it. The real invariant is "index + one page per record, never fewer than the founding 9"; test rewritten to that. An append-only archive's tests must not pin its size.
