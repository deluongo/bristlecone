# CURRENT_STATE

Seed document for any session (or successor model) picking up this project. Ceiling: 80KB (rows rotate to `ARCHIVE-YYYY-MM.md`). Timestamps PT.

## Arc goal

**M1 COMPLETE (`m1` tag, 2026-08-21). The repository is PUBLIC and the site is LIVE: https://deluongo.github.io/bristlecone/** — the operator ruled the flip in-session ("Sure. You can flip public.", recorded in `records/2026-08-21-public-flip.md`) after confirming the zero-key state; pre-flip full-history scans clean; Pages site created (`build_type: workflow` — one manual API call was needed, the workflow token can't create the site); branch protection on `main` blocks force pushes and deletions. Next milestone: **M2 fan-out + key-hardening gate** (`scrub`, `lanes`, `client`, `ask`, KEY-HANDLING.md → operator approval → first metered call; dead-man routine; model/topic pages).

## Shipped

| # | Date | Step | Outcome |
|---|---|---|---|
| 1 | 2026-08-20 | M0-S1: repo founded — governance docs, spec v0 draft, templates, hygiene CI, ship script, founding records (name, envelope, license, records-dir, public-timing, constitution-adoption) | see records/ |
| 2 | 2026-08-20 | M0-S2: operator rulings recorded — constitution ADOPTED, S1–S5 granted; treasury allocation deliberated (operator dissent preserved; outcome adoption-first-hybrid); founding-thesis record opened (stays open by design) | records/2026-08-20-{adopt-constitution,treasury-allocation,founding-thesis}.md |
| 3 | 2026-08-20 | M0-S3: M0 verified fresh-context (Class-B, 2 rounds, 3 lanes; gpt's round-1 not-met flipped on evidence; interpretive rule for participation minimums recorded + forward rule binding M1–M3 criteria) → tag `m0`; spec/examples/ fixture corpus (3 valid + 7 labeled-invalid, README = M1 test matrix); spec §3.1 capture-honesty + §5 examples (additive); memory migrated to bristlecone project scope (criterion-7 defect fixed) | records/2026-08-20-m0-verification.md |
| 8 | 2026-08-21 | **Public flip executed on operator ruling** (in-session, quoted verbatim in the record): pre-flip full-history scans clean (8 commits) → visibility public → Pages site created + deployed → site live with stamps → `m1` tag on dd793bd → branch protection (no force-push/delete). Operator confirmed zero-key state before ruling | records/2026-08-21-public-flip.md |
| 7 | 2026-08-21 | M1 fresh-context verification: all maintainer-class exit criteria PASS (gates re-run locally; CI/hygiene/pages-build green on dd793bd; append-only red-teamed live in a scratch clone — tamper/delete blocked, sanctioned supersession passes; full-history secret scan + denylist sweep clean; rendered site inspected). Tag timing deliberated Class-B (fable + gpt-5.6-sol/codex + qwen2.5:3b/ollama, 1 round, unanimous): **tag-at-flip** — operator-class criteria (flip, live serve) are pending, not reinterpreted away; `m1` lays down mechanically at the flip citing the record. Bookkeeping repair: M0-S3's missing $0.00 treasury rows late-recorded (†), process bug logged | records/2026-08-21-m1-verification.md |
| 6 | 2026-08-21 | M1-S3: `gitio.py` — the package's only shelling-out module — enforcing spec §4 over a git range: `validate --git-range BASE..HEAD` (also `...` merge-base form) fails deletions/renames under records/ and any edit to a frozen record beyond superseded_by-append / status→superseded\|withdrawn; fail-closed when the pre-change version doesn't parse. Interpretive pins (in module docstring, fixed by tests): subdirectory move keeping the filename is legal (spec §2 "moving does not change ID" read as governing §4's rename ban); frozen-edit legality judged semantically (parsed front matter) + body byte-identical. `render --stamps` puts first-introduced commit (git log --follow) on each page + built-from on the index. ci.yml `append-only` job (PR: base...HEAD; push: before..HEAD); `pages.yml` renders with stamps on every main push, deploy job gated on `!repository.private` so it arms itself at the flip (Pages can't serve a private repo on the free plan). Red-team drill = in-suite test running the exact CI invocation against a decided-record body edit on a branch → exit 1 (no non-main pushes needed; S1 scope is main). 103 tests, coverage 100%, xenon B, ruff clean. One real bug caught by live-render spot-check: relative RECORDS_DIR broke stamping (git -C moves cwd) — fixed + regression test | Class C — cites records/2026-08-20-record-envelope.md |
| 5 | 2026-08-21 | M1-S2: `minimark.py` (stdlib markdown subset → HTML; all output escaped; unsafe link schemes degrade to text) + `render.py` (index + per-record pages; dissent computed per spec §3.1 and presented in its own panel with the dissenter's body section unedited; outcome box with option labels; full attribution; broken links marked; malformed files render raw behind a warning banner — lenient per spec §6) + `python -m bristlecone render ROOT -o OUT` (exit 0/2); 69 tests, coverage 100%, xenon B, ruff clean; ci.yml smoke-renders the archive; README status updated. Commit stamps (spec §4) deferred to M1-S3 with the Pages deploy | Class C — cites records/2026-08-20-record-envelope.md |
| 4 | 2026-08-21 | M1-S1: `bristlecone/` package founded — `records.py` (lossless envelope parse/serialize, byte-identical round-trip on all 9 parseable fixtures) + `validate.py` (fail-closed: required cores, status vocab, ID grammar, dangling links, duplicate IDs; `--strict` adds lane attribution) + `python -m bristlecone validate` (exit contract 0/1/2); 44 tests green, coverage 100%, xenon B, ruff clean; ci.yml gates live (also validates fixture corpus + real archive per matrix); all 9 real M0 records pass `--strict`. Interpretive call, pinned by the fixture matrix: enforced ID grammar = charset rule (lowercase alnum + hyphens); `YYYY-MM-DD-` prefix stays convention (invalid fixtures' own filenames have no date prefix yet must fail only for their labeled defect) | Class C — cites records/2026-08-20-record-envelope.md |

## In flight

*(none — M1 verification complete; waiting on the operator's flip)*

## Queued (M2 opens; weekend acceleration still in effect)

- **M2-S1 candidate**: `docs/KEY-HANDLING.md` draft + scrub/lanes/client design records (Class B/A as appropriate). The first metered call stays gated on operator approval of KEY-HANDLING.md + the operator-installed secrets hook.
- **Telegram dead-man bot** (S6 granted for the routine; the bot account creation is an operator act via @BotFather — ask when he has a minute, it was offered post-flip).
- **Domain decision** (treasury first claim per `records/2026-08-20-treasury-allocation.md`) — deliberate whether/when; site works fine on github.io at $0.
- Candidate M2 refinement, recorded in the verification record: move the dissent panel above the positions list on record pages (plan's design sketch says dissent-first; shipped renderer places it after; the exit criterion "visually first-class" is met either way).
- C1 checkpoint 2026-09-10: site public ✓ (early), ≥10 records ✓ (11) — remaining: ≥3 cross-session citations (2 so far: m1-verification cites m0-verification; public-flip cites both timing records), zero hygiene incidents.

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
