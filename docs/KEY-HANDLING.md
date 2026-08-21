# KEY-HANDLING.md — metered-lane key hardening

**Status: DRAFT — awaiting operator approval.** The first metered API call is a forever-ask
(STANDING_AUTHORIZATIONS.md) gated on the operator approving this document and installing
the hook described in §4. Until then the repository and every session remain zero-secret.

Design deliberated 2026-08-21 (Class A, 3 lanes / 3 vendors / 1 local):
`records/2026-08-21-key-handling-design.md`. The dissent recorded there is a security
position and worth the operator's read before approving.

## 1. Threat model

The AI maintainer works through a tool-call loop; every command and every byte of tool
output lands in a session transcript that leaves the machine. Historically (operator's
prior experience, stated generically), secret leaks ride *tool output* — env dumps, debug
prints, error messages, verbose HTTP clients. Therefore:

- A key present in the **session's environment** is assumed leaked.
- A key present in any **command argument** is assumed leaked.
- A key that AI-editable code can read is **one code edit away** from tool output
  (the round-1 dissent's point, accepted into the design).

Defended threats: accidental leakage, and sessions steered by prompt injection (a public
repo accepts inbound text). Out of scope: a persistently adversarial maintainer with
same-user execution — no same-user architecture survives that; the bounded asset (§6)
is the backstop.

## 2. Storage

The DeepSeek key lives **only** in `~/secrets/bristlecone.env` — a sops+age encrypted
file, operator-created, operator-owned, outside the repository. That file contains
**only** this one key (never shared with other secrets, so `exec-env` can never inject
unrelated material). Sessions never touch `~/secrets/**`, `~/.config/sops/**` (CLAUDE.md
hard rule, hook-enforced).

## 3. The blessed invocation — pinned client

Exactly one command shape may reach the key:

```
sops exec-env ~/secrets/bristlecone.env '~/bin/bristlecone-ask <args>'
```

- `sops exec-env` decrypts and injects the key into the **child process environment
  only** — never the session env, never argv.
- `~/bin/bristlecone-ask` is an **operator-pinned copy** of the metered client, outside
  the repository, not writable by sessions (hook-denied; filesystem permissions at the
  operator's discretion as a second layer). The repo's working tree — which the AI
  edits freely — never runs with the key. The operator re-pins (re-copies after review)
  at their own cadence; until re-pin, AI changes to ask/lanes/client code affect the
  $0 lanes only.
- The pinned client is a **closed boundary** (round-2 convergence conditions, gpt lane):
  it is self-contained — it imports no repo modules, loads no repo config or plugins,
  spawns no subprocesses, and ignores `PATH`/proxy/debug/credential environment
  settings beyond the one key var; its API origin is **fixed in the pinned artifact**
  (no argument can redirect the key to another host); spend caps, scrub, and logging
  behavior live entirely inside the pinned artifact. Updates take effect only through
  explicit operator re-pin.
- The quoted inner command admits **no shell metacharacters**; the hook anchors the
  full shape (§4).

## 4. Operator-installed hook (operator patch — hook edits are operator-domain)

A PreToolUse hook, installed by the operator from `docs/patches/` (the patch ships with
the M2 client implementation, before this gate can open), that:

1. **Allows** only the exact blessed shape above (anchored match: `sops exec-env`
   + the literal env-file path + inner command beginning `~/bin/bristlecone-ask`,
   no `;`, `&&`, `|`, `$(`, backticks inside the quoted command).
2. **Denies** any other command mentioning: the env-file path, `sops`, `age`, the key
   env var name, `~/secrets/`, `~/.config/sops/`, the DeepSeek endpoint host, or writes
   to `~/bin/bristlecone-ask`.

The hook is a tripwire for accident and steering, not the sole boundary — the pinned
client (§3) is what removes the key from AI-editable code's reach.

## 5. Client discipline (enforced by tests on the repo copy; audited at pin time)

- The pinned client **spawns no subprocesses** (child env is heritable) and reads only
  the one key env var — never dumps `os.environ`.
- The key exists only inside the HTTP call path; it is never logged, never included in
  exceptions. All errors crossing the client boundary are re-raised sanitized (no
  header reprs, no request-object dumps).
- **Cap-check ordering**: the client reads `TREASURY.md`, and refuses (`declined:budget`)
  *before* the key is required — a declined run never needed the sops wrapper at all.
- Inbound **and** outbound scrub on all lane I/O (secret-shape + private-context
  filters) before any byte lands in a tracked file; scrub runs on API error bodies too.
- Key verification is **hash-compare only**: the client can report `sha256(key)`
  matches/mismatches an operator-held fingerprint. The fingerprint itself stays
  operator-side (publishing it would let anyone confirm a candidate leaked key).

## 6. Bounded asset + backstops

- Caps enforced in-client from the public ledger: **$0.10/session, $0.70/week, $20.00
  lifetime** (S2); no auto-topup on the DeepSeek account — worst-case blast radius of
  a leak is the remaining balance.
- CI secret-scan (credential shapes + entropy blobs) gates every Pages deploy; the
  denylist gate runs locally in `ship.sh`.
- Any suspected exposure: operator rotates the key at the vendor, replaces the sops
  file; the incident is recorded in the archive (transparency applies to failures).

## 7. What the operator must do to open the gate (one-time)

1. Read this document and the deliberation record (incl. dissent).
2. Create `~/secrets/bristlecone.env` (sops+age, single key) — operator act.
3. Pin the client: copy the reviewed `bristlecone-ask` entrypoint to `~/bin/` — operator act.
4. Install the hook from `docs/patches/` — operator act (hook edits are operator-domain).
5. Record approval in `docs/INBOX.md`; the resolving session records it as an
   operator-ruling and flips S2 to active.

Until all five happen, `bristlecone ask` runs keyless lanes only, and any metered-lane
config refuses with `declined:gate`.
