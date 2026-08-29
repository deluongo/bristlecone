# Treasury

Opening balance: **$20.00** (notional — the operator holds the cash; metered API spend draws against it). Infrastructure cost: $0 (GitHub, GitHub Pages). Subscription lanes (Claude, codex) draw existing subscription quota — no cash. Local lanes (ollama) are free.

## Rate table

No metered calls are permitted before the M2 key-hardening review. The rate table below will be pinned from the provider's published prices, with a recorded date, before the first metered call. Tokens are authoritative; dollars are estimates derived from this table.

| Lane | Model | $/Mtok in | $/Mtok out | Recorded |
|---|---|---|---|---|
| deepseek | deepseek-chat | — | — | (pinned at M2) |

## Ledger

Append-only. One row per metered call, written from the provider's `usage` field at call time. Zero-cost lanes appear when used in a deliberation so the cost story is complete. Arithmetic (per-row cost and running balance) is machine-recomputed by the validator from M1.

| Date (PT) | Session | Record | Lane | tok_in | tok_out | Est. cost | Balance |
|---|---|---|---|---|---|---|---|
| 2026-08-20 | m0-s1 | 2026-08-20-record-envelope | claude-opus-5 (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-20 | m0-s1 | 2026-08-20-record-envelope | gpt-5.6-sol via codex (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-20 | m0-s1 | 2026-08-20-record-envelope | qwen2.5:3b via ollama (local, ×2 samples) | — | — | $0.00 | $20.00 |
| 2026-08-20 | m0-s1 | 2026-08-20-license | claude-opus-5 (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-20 | m0-s1 | 2026-08-20-license | gpt-5.6-sol via codex (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-20 | m0-s1 | 2026-08-20-license | qwen2.5:3b via ollama (local, ×2 samples) | — | — | $0.00 | $20.00 |
| 2026-08-20 | m0-s1 | 2026-08-20-records-directory | gpt-5.6-sol via codex (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-20 | m0-s1 | 2026-08-20-records-directory | llama3.2:1b via ollama (local, ×2 samples) | — | — | $0.00 | $20.00 |
| 2026-08-20 | m0-s3 | 2026-08-20-m0-verification | claude-fable-5 (subscription) † | — | — | $0.00 | $20.00 |
| 2026-08-20 | m0-s3 | 2026-08-20-m0-verification | gpt-5.6-sol via codex (subscription, ×2 rounds) † | — | — | $0.00 | $20.00 |
| 2026-08-20 | m0-s3 | 2026-08-20-m0-verification | qwen2.5:3b via ollama (local, ×2 rounds, round 2 discarded) † | — | — | $0.00 | $20.00 |
| 2026-08-21 | m1-verify | 2026-08-21-m1-verification | claude-fable-5 (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-21 | m1-verify | 2026-08-21-m1-verification | gpt-5.6-sol via codex (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-21 | m1-verify | 2026-08-21-m1-verification | qwen2.5:3b via ollama (local) | — | — | $0.00 | $20.00 |
| 2026-08-21 | m2-s1 | 2026-08-21-key-handling-design | claude-fable-5 (subscription, ×2 rounds) | — | — | $0.00 | $20.00 |
| 2026-08-21 | m2-s1 | 2026-08-21-key-handling-design | gpt-5.6-sol via codex (subscription, ×2 rounds) | — | — | $0.00 | $20.00 |
| 2026-08-21 | m2-s1 | 2026-08-21-key-handling-design | qwen2.5:3b via ollama (local, ×2 rounds) | — | — | $0.00 | $20.00 |
| 2026-08-21 | m2-s1 | 2026-08-21-ask-lane-architecture | claude-fable-5 (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-21 | m2-s1 | 2026-08-21-ask-lane-architecture | gpt-5.6-sol via codex (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-21 | m2-s1 | 2026-08-21-ask-lane-architecture | qwen2.5:3b via ollama (local) | — | — | $0.00 | $20.00 |
| 2026-08-23 | m2-s4 | 2026-08-23-adoption-roadmap | claude-fable-5 via `bristlecone ask` (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-23 | m2-s4 | 2026-08-23-adoption-roadmap | gpt-5.6-sol via `bristlecone ask` (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-23 | m2-s4 | 2026-08-23-adoption-roadmap | qwen2.5:3b via `bristlecone ask` (local) | — | — | $0.00 | $20.00 |
| 2026-08-23 | m2-s4 | 2026-08-23-adoption-roadmap | deepseek — `declined:gate`, no call dispatched (KEY-HANDLING unapproved) | 0 | 0 | $0.00 | $20.00 |
| 2026-08-27† | m2-s7 | 2026-08-27-onboarding-rehearsal | qwen2.5:3b via `bristlecone ask` (local; rehearsal record in scratch repo) | — | — | $0.00 | $20.00 |
| 2026-08-27 | m2-s8 | 2026-08-27-pilot-shortlist | claude-fable-5 via `bristlecone ask` (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-27 | m2-s8 | 2026-08-27-pilot-shortlist | gpt-5.6-sol via `bristlecone ask` (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-27 | m2-s8 | 2026-08-27-pilot-shortlist | qwen2.5:3b via `bristlecone ask` (local) | — | — | $0.00 | $20.00 |
| 2026-08-27 | m2-s9 | 2026-08-27-operator-steering-outreach-pitch | claude-fable-5 (subscription, outreach-draft critique ×2 rounds) | — | — | $0.00 | $20.00 |
| 2026-08-27 | m2-s9 | 2026-08-27-operator-steering-outreach-pitch | gpt-5.6-sol via codex (subscription, outreach-draft critique ×2 rounds) | — | — | $0.00 | $20.00 |
| 2026-08-27 | m2-s9 | 2026-08-27-operator-steering-outreach-pitch | qwen2.5:3b-instruct via ollama (local, outreach-draft critique) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-outreach-cadence | claude-fable-5 via `bristlecone ask` (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-outreach-cadence | gpt-5.6-sol via `bristlecone ask` (subscription) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-outreach-cadence | qwen2.5:3b-instruct via `bristlecone ask` (local) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-gptme-invite-review | claude-fable-5 via `bristlecone ask` (subscription, round 1 critique) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-gptme-invite-review | gpt-5.6-sol via `bristlecone ask` (subscription, round 1 critique) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-gptme-invite-review | qwen2.5:3b-instruct via `bristlecone ask` (local, round 1 critique) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-backlog-invite-review | claude-fable-5 via `bristlecone ask` (subscription, round 1 critique) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-backlog-invite-review | gpt-5.6-sol via `bristlecone ask` (subscription, round 1 critique) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-backlog-invite-review | qwen2.5:3b-instruct via `bristlecone ask` (local, round 1 critique — `failed:format` after one repair, capture preserved, no resample) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-gptme-invite-review | claude-fable-5 via `bristlecone ask` (subscription, round 2 re-vote) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-gptme-invite-review | gpt-5.6-sol via `bristlecone ask` (subscription, round 2 re-vote) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-gptme-invite-review | qwen2.5:3b-instruct via `bristlecone ask` (local, round 2 re-vote — `failed:format`, capture preserved, no resample) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-backlog-invite-review | claude-fable-5 via `bristlecone ask` (subscription, round 2 re-vote) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-backlog-invite-review | gpt-5.6-sol via `bristlecone ask` (subscription, round 2 re-vote) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-backlog-invite-review | qwen2.5:3b-instruct via `bristlecone ask` (local, round 2 re-vote, one repair reprompt) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-backlog-invite-review | claude-fable-5 via `bristlecone ask` (subscription, round 3 re-vote) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-backlog-invite-review | gpt-5.6-sol via `bristlecone ask` (subscription, round 3 re-vote — `failed:timeout` at 600s, no stance) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-backlog-invite-review | qwen2.5:3b-instruct via `bristlecone ask` (local, round 3 re-vote, one repair reprompt) | — | — | $0.00 | $20.00 |
| 2026-08-29 | m2-s11 | 2026-08-29-backlog-invite-review | gpt-5.6-sol via `bristlecone ask` (subscription, round 3 transport retry as codex-r3b — `failed:timeout` again at 600s, no stance) | — | — | $0.00 | $20.00 |

*(All founding-deliberation lanes were subscription or local: $0.00 cash. Token counts are unavailable from subscription/local CLIs in M0 — captured from M2 wherever providers report usage (DEFERRED DEF-005). "×2 samples" marks lanes whose first capture was discarded for terminal-rendering corruption; stances were identical across samples, and the second capture is the position of record.)*

*(† Late-recorded 2026-08-21: the M0-S3 session used these lanes for the m0-verification deliberation but did not add their $0.00 rows — an omission against this ledger's "zero-cost lanes appear when used" contract, logged in `docs/PROCESS_REFLECTIONS.md`. Rows are appended here with their true dates; the running balance is unaffected.)*
