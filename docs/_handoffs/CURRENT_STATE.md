# CURRENT_STATE

Seed document for any session (or successor model) picking up this project. Ceiling: 80KB (rows rotate to `ARCHIVE-YYYY-MM.md`). Timestamps PT.

## Arc goal

**M0 complete and tagged. M1 build complete and fresh-context verified (2026-08-21, `records/2026-08-21-m1-verification.md`, commit dd793bd).** Verification outcome: every maintainer-class exit criterion passes with evidence; the two operator-class criteria (public flip, site actually serving) are pending by design, **so the `m1` tag lands at the flip** — a mechanical Class-C act citing the verification record, unanimous across 3 lanes / 3 vendors / 1 local. The flip is the operator's button (forever-ask), now formally requested via the digest.

## Shipped

| # | Date | Step | Outcome |
|---|---|---|---|
| 1 | 2026-08-20 | M0-S1: repo founded — governance docs, spec v0 draft, templates, hygiene CI, ship script, founding records (name, envelope, license, records-dir, public-timing, constitution-adoption) | see records/ |
| 2 | 2026-08-20 | M0-S2: operator rulings recorded — constitution ADOPTED, S1–S5 granted; treasury allocation deliberated (operator dissent preserved; outcome adoption-first-hybrid); founding-thesis record opened (stays open by design) | records/2026-08-20-{adopt-constitution,treasury-allocation,founding-thesis}.md |
| 3 | 2026-08-20 | M0-S3: M0 verified fresh-context (Class-B, 2 rounds, 3 lanes; gpt's round-1 not-met flipped on evidence; interpretive rule for participation minimums recorded + forward rule binding M1–M3 criteria) → tag `m0`; spec/examples/ fixture corpus (3 valid + 7 labeled-invalid, README = M1 test matrix); spec §3.1 capture-honesty + §5 examples (additive); memory migrated to bristlecone project scope (criterion-7 defect fixed) | records/2026-08-20-m0-verification.md |
| 7 | 2026-08-21 | M1 fresh-context verification: all maintainer-class exit criteria PASS (gates re-run locally; CI/hygiene/pages-build green on dd793bd; append-only red-teamed live in a scratch clone — tamper/delete blocked, sanctioned supersession passes; full-history secret scan + denylist sweep clean; rendered site inspected). Tag timing deliberated Class-B (fable + gpt-5.6-sol/codex + qwen2.5:3b/ollama, 1 round, unanimous): **tag-at-flip** — operator-class criteria (flip, live serve) are pending, not reinterpreted away; `m1` lays down mechanically at the flip citing the record. Bookkeeping repair: M0-S3's missing $0.00 treasury rows late-recorded (†), process bug logged | records/2026-08-21-m1-verification.md |
| 6 | 2026-08-21 | M1-S3: `gitio.py` — the package's only shelling-out module — enforcing spec §4 over a git range: `validate --git-range BASE..HEAD` (also `...` merge-base form) fails deletions/renames under records/ and any edit to a frozen record beyond superseded_by-append / status→superseded\|withdrawn; fail-closed when the pre-change version doesn't parse. Interpretive pins (in module docstring, fixed by tests): subdirectory move keeping the filename is legal (spec §2 "moving does not change ID" read as governing §4's rename ban); frozen-edit legality judged semantically (parsed front matter) + body byte-identical. `render --stamps` puts first-introduced commit (git log --follow) on each page + built-from on the index. ci.yml `append-only` job (PR: base...HEAD; push: before..HEAD); `pages.yml` renders with stamps on every main push, deploy job gated on `!repository.private` so it arms itself at the flip (Pages can't serve a private repo on the free plan). Red-team drill = in-suite test running the exact CI invocation against a decided-record body edit on a branch → exit 1 (no non-main pushes needed; S1 scope is main). 103 tests, coverage 100%, xenon B, ruff clean. One real bug caught by live-render spot-check: relative RECORDS_DIR broke stamping (git -C moves cwd) — fixed + regression test | Class C — cites records/2026-08-20-record-envelope.md |
| 5 | 2026-08-21 | M1-S2: `minimark.py` (stdlib markdown subset → HTML; all output escaped; unsafe link schemes degrade to text) + `render.py` (index + per-record pages; dissent computed per spec §3.1 and presented in its own panel with the dissenter's body section unedited; outcome box with option labels; full attribution; broken links marked; malformed files render raw behind a warning banner — lenient per spec §6) + `python -m bristlecone render ROOT -o OUT` (exit 0/2); 69 tests, coverage 100%, xenon B, ruff clean; ci.yml smoke-renders the archive; README status updated. Commit stamps (spec §4) deferred to M1-S3 with the Pages deploy | Class C — cites records/2026-08-20-record-envelope.md |
| 4 | 2026-08-21 | M1-S1: `bristlecone/` package founded — `records.py` (lossless envelope parse/serialize, byte-identical round-trip on all 9 parseable fixtures) + `validate.py` (fail-closed: required cores, status vocab, ID grammar, dangling links, duplicate IDs; `--strict` adds lane attribution) + `python -m bristlecone validate` (exit contract 0/1/2); 44 tests green, coverage 100%, xenon B, ruff clean; ci.yml gates live (also validates fixture corpus + real archive per matrix); all 9 real M0 records pass `--strict`. Interpretive call, pinned by the fixture matrix: enforced ID grammar = charset rule (lowercase alnum + hyphens); `YYYY-MM-DD-` prefix stays convention (invalid fixtures' own filenames have no date prefix yet must fail only for their labeled defect) | Class C — cites records/2026-08-20-record-envelope.md |

## In flight

| Date | Step | Done-check |
|---|---|---|
| 2026-08-21 | M1 fresh-context verification (this session is the verifier; M1-S3's session may not self-certify) | Every M1 exit criterion from the plan of record audited with evidence; flip-dependent criteria ("Devon flips public", live Pages serve) explicitly classified per the M0 forward rule rather than silently skipped; verification record in `records/`; tag decision executed per that record; CURRENT_STATE + digest updated |

## Queued (weekend acceleration — operator requested faster cadence through the weekend)

- **Waiting on the operator's public flip** (forever-ask; requested in the 2026-08-21 digest). At flip time, any session: confirm the Pages deploy serves (deploy job arms itself via the `!repository.private` gate; first run may need `workflow_dispatch`), then lay the `m1` tag on commit dd793bd — mechanical Class C citing `records/2026-08-21-m1-verification.md`. Also at flip time: Telegram dead-man bot setup (account-creation forever-ask; S6 pre-granted for the routine), domain decision (treasury first claim).
- **M2 prep can start while waiting** (doesn't need the flip): `docs/KEY-HANDLING.md` draft, scrub/lanes/client design records. First metered call stays gated on operator approval of KEY-HANDLING.md.
- Candidate M2 refinement, recorded in the verification record: move the dissent panel above the positions list on record pages (plan's design sketch says dissent-first; shipped renderer places it after; the exit criterion "visually first-class" is met either way).

## Open design decisions

- Dead-man routine (post-flip, S6 granted): **channel = Telegram bot** per operator suggestion 2026-08-20; bot creation is an account-creation forever-ask, handled at flip time
- Treasury: adoption costs hold first claim (see `records/2026-08-20-treasury-allocation.md`); first candidate = domain at public flip, decided then

## Test baseline

103 tests, coverage 100% (floor 80), xenon B, ruff clean — all enforced in `.github/workflows/ci.yml` alongside the hygiene greps. Local runs use the gitignored `.venv/` (`python3 -m venv .venv && .venv/bin/pip install pytest pytest-cov ruff xenon`). The package itself is stdlib-only.

## Pointers

- Plan of record: operator-side (`~/.claude/plans/i-want-to-give-merry-lobster.md`)
- Governance: `CONSTITUTION.md` · authorizations: `STANDING_AUTHORIZATIONS.md` · money: `TREASURY.md`
- Format: `spec/RECORD-FORMAT-v0.md` · archive: `records/` · operator steering: `docs/INBOX.md`
- Session rules: `CLAUDE.md` (ritual, fuse, digest template)

## What a fresh session should ask itself

1. Did I read INBOX first? 2. Is exactly one step declared in-flight? 3. Does my work cite or create a record? 4. Will ship.sh pass (hygiene + denylist)? 5. Is my digest's line 4 computed, not estimated?
