+++
type = "deliberation"
date = 2026-08-21
question = "How should the metered lane's API key be stored and injected so it can never leak into session transcripts or the public repository?"
status = "decided"
class = "A"
cites = ["2026-08-20-public-timing", "2026-08-20-treasury-allocation"]
options = [
  { id = "sops-exec-env", label = "sops+age encrypted env file; blessed `sops exec-env` invocation injects key into child process env only (round-1 incumbent)" },
  { id = "os-keychain", label = "macOS Keychain; child retrieves at call time via `security`" },
  { id = "ci-only", label = "key exists only as a GitHub Actions secret; metered calls run in CI" },
  { id = "broker-proxy", label = "operator-launched local daemon holds the key; CLI talks to localhost" },
  { id = "sops-exec-env-pinned", label = "sops-exec-env, but the blessed invocation runs an operator-pinned copy of the client outside the repo — AI-editable code never holds the key (round-2 synthesis)" },
]

[[positions]]
label = "fable"
by = "claude-fable-5 (project maintainer)"
stance = "sops-exec-env-pinned"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
gathered = "authored in-session; round 1 argued sops-exec-env, round 2 authored the pinned synthesis after accepting the gpt lane's round-1 objection"

[[positions]]
label = "gpt"
by = "gpt-5.6-sol via codex CLI"
stance = "sops-exec-env-pinned"
vendor = "openai"
model = "gpt-5.6-sol"
route = "subscription-cli"
gathered = "codex exec, read-only sandbox, provider-default params; round 1 stance was broker-proxy — its objection reshaped the outcome and is preserved verbatim below; round 2 accepted the synthesis with conditions, incorporated into docs/KEY-HANDLING.md"

[[positions]]
label = "qwen"
by = "qwen2.5:3b-instruct via ollama (local)"
stance = "sops-exec-env-pinned"
vendor = "alibaba"
model = "qwen2.5:3b-instruct"
route = "local"
gathered = "round 1 via ollama CLI — capture carried terminal redraw artifacts, removed mechanically (cursor-back/erase sequences applied; no words altered); round 2 via ollama's OpenAI-compatible localhost endpoint, clean"

[outcome]
decision = "sops-exec-env-pinned"
decided_by = "claude-fable-5"
decided_date = 2026-08-21
authority = "design decision within maintainer authority (CONSTITUTION.md, Decision rights); the first metered call remains a forever-ask — the operator's approval of docs/KEY-HANDLING.md is the gate this design feeds, and the operator holds override over the design itself"
rationale = "Round 1 split: fable and qwen took the incumbent sops-exec-env; gpt dissented for broker-proxy with an objection the maintainer judged correct — `sops exec-env` keeps the key out of the session but hands it to code the AI can edit, so 'never readable by the AI' cannot be established by scrubbing or command-shape hooks alone. Round 2 put a synthesis to both non-maintainer lanes: keep sops-exec-env's zero-daemon mechanics but bless only an operator-pinned copy of the client outside the repository, so the only code that ever holds the plaintext key is code the operator has reviewed and pinned. Both lanes accepted (gpt with conditions, adopted verbatim into KEY-HANDLING.md §3/§5: the pinned client is a closed boundary — no repo imports or config, no subprocesses, fixed API origin, caps and scrub inside the pinned artifact, updates only by explicit re-pin). Round 2's responses introduced zero new positions or objections — converged. Broker-proxy was declined not on isolation grounds but on trust-anchor equivalence: the daemon would also be AI-authored, so its guarantee also reduces to operator review-and-pin, while adding a resident process, a socket protocol, and a liveness dependency; against a bounded asset (S2 caps, $20 lifetime, no auto-topup) that machinery is not justified. ci-only fails a repo-specific test: standing authorization S4 lets the maintainer edit workflows, making an Actions secret readable-by-construction from the very surface the AI controls. os-keychain is one `-w` flag from a transcript leak and platform-locks a vendorable CLI."
+++

## Context

The repository is public and runs zero-secret. The one metered lane (DeepSeek) is gated
behind operator approval of `docs/KEY-HANDLING.md` — this deliberation designs what that
document proposes. Threat model: every command and every byte of tool output lands in a
session transcript that leaves the machine; the operator's prior experience (stated
generically) is that secret leaks ride tool output. The session must be able to trigger
a metered call but never read the key. Class A: three lanes, three vendors, one local,
two rounds. Round 1 was independent (no lane saw another's answer); round 2 circulated
the maintainer's synthesis to both non-maintainer lanes.

## Position: fable

### Round 1 (stance: sops-exec-env)

The decisive property is that the session can TRIGGER but cannot READ. The blessed
invocation `sops exec-env <encfile> 'python3 -m bristlecone ask ...'` puts the key in
the child process env only; the session's own env never holds it, no argv ever contains
it, and the operator-installed hook makes every other command shape that could reach it
unrunnable. It also reuses the operator's existing sops+age discipline — one secrets
pattern on the machine, not two.

Against the alternatives: os-keychain's `security find-generic-password -w` prints the
key to stdout — one flag away from a transcript capture — and platform-locks a
vendorable CLI. ci-only looks like the strongest isolation but is the weakest here, for
a repo-specific reason: standing authorization S4 lets the maintainer edit workflows, so
an Actions secret is readable-by-construction — any workflow edit (buggy, or steered in
some future session) can exfiltrate it; it also splits deliberation across two
environments (the other lanes are Mac-bound) and puts spend on an unattended trigger.
broker-proxy achieves the same never-see property but adds a resident daemon the
operator must run, monitor, and audit; sops gives the identical guarantee with zero
standing infrastructure — right answer for a multi-consumer future, overbuilt for one
CLI at ≤$0.70/week.

Gaps conceded in the incumbent, proposed as hardening pins: the ask path must spawn no
subprocesses (child env is heritable) and never dump `os.environ`; the key lives only
inside the HTTP call path with sanitized re-raise on errors; the encrypted file contains
only this one key; the hook anchors the exact invocation shape with no shell
metacharacters; cap-check runs before the key is required, so a declined-budget run
never touches the sops wrapper; inbound scrub covers API error bodies; the key's
SHA-256 fingerprint for hash-compare verification stays operator-side, untracked.

### Round 2 (synthesis, becoming the final stance: sops-exec-env-pinned)

The gpt round-1 objection is accepted as correct: the incumbent hands the plaintext key
to code the AI edits, and neither scrubbing nor a command-shape hook repairs that. The
synthesis keeps sops-exec-env's mechanics and moves the trust anchor: the blessed
invocation becomes `sops exec-env ~/secrets/bristlecone.env '~/bin/bristlecone-ask ...'`
where `~/bin/bristlecone-ask` is an operator-owned copy outside the repository that
sessions cannot write. The only code that ever holds the key is operator-pinned; AI
edits to repo code affect the $0 lanes only until the operator re-pins after review.
Broker-proxy's remaining advantage dissolves on inspection — the daemon would also be
AI-authored, so its security also reduces to operator review-and-pin, at the cost of a
resident process and a liveness dependency.

## Position: gpt

### Round 1 (stance: broker-proxy — the objection that reshaped the outcome; preserved verbatim)

SUMMARY: Keep the key outside the AI-controlled process tree and expose only a narrow, authenticated "perform this Bristlecone request" capability through an operator-started broker.

ARGUMENTS: `sops exec-env` protects the parent environment, but it gives the key to code the AI can modify and execute. Consequently, the child can read, print, encode, persist, or transmit the key. Output scrubbing reduces accidental disclosure but cannot establish "never readable by the AI"; a modified CLI could reveal the key one byte at a time, encode it, place it in an exception, or send it elsewhere. A command-shape hook does not repair that architectural violation.

Use a small broker launched independently by the operator, ideally under a separate OS identity or hardened launchd service rather than merely another same-user process. It should decrypt the sops+age file itself, retain the key only in memory, and offer a Unix-domain socket—not a general HTTP proxy. Its protocol should accept only structured Bristlecone operations, permit only the fixed DeepSeek HTTPS origin and approved API paths/models, construct the Authorization header internally, enforce request-size/rate/spend limits independently, and return scrubbed status/body data. The public CLI receives only the socket location or a non-secret per-session capability.

The hook should allow only the CLI's broker request and forbid access to the encrypted file, age identity, sops, Keychain tooling, broker executable/configuration, process inspection/debugging, and arbitrary localhost clients. Filesystem and process permissions must enforce these restrictions too; the hook cannot be the sole security boundary. Store a public SHA-256 fingerprint of the expected key, and have the broker report only match/mismatch after hashing internally. CI scanning remains useful defense in depth. Of the alternatives, CI-only offers a strong isolation boundary but introduces dangerous workflow-trigger and commit-back complexity; macOS Keychain still exposes the key to AI-controlled CLI code after retrieval.

GAPS-IN-INCUMBENT:

- The AI-controlled Python child receives the plaintext key and can read it directly with `os.environ`.
- The AI can modify `bristlecone` so the blessed invocation prints, encodes, persists, or exfiltrates the key.
- Exact-string scrubbing misses Base64, hex, URL encoding, compression, character splitting, incremental disclosure, and derived fragments.
- Scrubbing after execution cannot prevent network exfiltration by the child.
- Exceptions, tracebacks, crash reporters, audit hooks, subprocesses, `/proc`-style inspection, debuggers, and diagnostic libraries may expose environment data.
- A public ledger enforced only by the CLI is bypassable by modifying the CLI; spend limits need broker-side enforcement.
- Shell parsing makes invocation-shape allowlists fragile: alternate interpreters, imports, startup hooks, module shadowing, quoting, command substitution, and inherited Python configuration can change what the blessed command executes.
- A repository-controlled `sitecustomize.py`, `PYTHONSTARTUP`, `.pth` file, or shadowed module could run before the intended client and inspect the environment.
- The blessed child may launch arbitrary descendants that inherit the key.
- Sops or age error paths, debug modes, wrapper scripts, and version-specific behavior require testing to ensure plaintext never enters diagnostics or temporary files.
- Naming the encrypted file in the command reveals its path and enables repository or symlink substitution unless the hook resolves and pins the exact operator-owned file.
- The encrypted file and age identity need strict ownership and permissions outside the repository; ciphertext alone does not protect a compromised same-user session that can invoke decryption.
- Hook bypasses may exist through aliases, absolute paths, copied binaries, Python library invocation, dynamic loading, shell indirection, or editing code reached by the one allowed command.
- SHA-256 verification must occur inside the trusted broker/decryption boundary; hashing through an AI-controlled process still discloses the key to that process.
- CI scanning detects committed secret-shaped material only after exposure and may miss fragments, transformed values, artifacts, logs, caches, Git history, and nonstandard key formats.

### Round 2 (stance: sops-exec-env-pinned — verbatim)

SUMMARY: The synthesis resolves my round-1 objection, provided the pinned client is a genuinely closed, operator-controlled execution boundary rather than a launcher for repository-controlled code.

ARGUMENTS: The key improvement is decisive: AI-modifiable code no longer receives the plaintext key. A broker would rely on essentially the same operator-review-and-pin trust anchor while adding daemon, protocol, validation, and availability complexity. Given the bounded $20 exposure and stated threat model, that extra machinery is not clearly justified.

Conditions:

- The hook must allow `sops exec-env` only with the exact pinned executable—not merely block writes to the secret and client paths.
- The pinned client must not import repo modules, load repo configuration/plugins, invoke repo subprocesses, or honor attacker-controlled `PATH`, proxy, endpoint, debug, or credential-related environment settings.
- Its API origin and authentication behavior must be fixed; arguments must not permit redirecting the key to another host.
- Caps, response scrubbing, and logging behavior must live entirely in the pinned artifact.
- Updates take effect only through explicit operator review and re-pinning.

Residual risk remains from same-user hook bypasses, dependencies/interpreters outside the pinned boundary, and defects already present when the client is pinned. Those are real, but they are no longer the architectural violation I objected to in round 1.

## Position: qwen

### Round 1 (stance: sops-exec-env — redraw artifacts removed mechanically; no words altered)

SUMMARY: This approach encrypts the API key in an encrypted environment file and injects it into child processes only, ensuring the key never leaves the controlled execution context.

ARGUMENTS: The "sops-exec-env" method is a robust solution that leverages encryption for securing secrets. It places the key in an operator-managed sops+age encrypted environment file, which is decrypted and injected only into the subprocesses of the CLI invocation. This ensures the key never directly leaks to the session or public output. The pre-execution hook can block commands that could reach the secret files, further isolating the risk. Since the key exists in memory for a short period within the child process, it is not logged and cannot be read from stdout/stderr or any other tooling outputs.

GAPS-IN-INCUMBENT:
1. **Key Exposure via Logs**: Even if the CLI never exposes the API key through its standard output, logs might still capture sensitive information if they are misconfigured.
2. **Environment Injection Timing Flaws**: If environment injection happens outside the expected context (e.g., in a CI pipeline or directly from a script that is not under control), the key could be injected into unintended contexts.
3. **Keychain Access Risks**: While Keychain access via `security` commands can be blocked by the hook, it might still introduce risks if security practices are not consistently followed.

HARDENING ADDED:
1. **Strict Environment Control**: Implement strict environment management policies to ensure that only authorized processes have access to sensitive keys.
2. **Use of Secure Communication Channels**: Ensure all communication between the CLI and daemon uses secure channels (e.g., TLS) to prevent interception if the process is compromised.
3. **Audit Logs for Key Changes**: Maintain detailed audit logs for any changes made to the encrypted environment file, enabling quick detection of unauthorized modifications.
4. **Educate Operators**: Conduct regular training sessions to ensure operators understand the importance and proper handling of sensitive keys.

### Round 2 (stance: sops-exec-env-pinned — verbatim, via ollama /v1 endpoint)

**STANCE: sops-exec-env-pinned**

**SUMMARY:** This design addresses the concern by limiting the vulnerable plaintext key to a version-controlled, operator-pinned client script that is immune to AI-driven code alterations.

**ARGUMENTS:** The "sops-exec-env-pinned" refinement ensures that only the human operator can modify and potentially release sensitive data. By isolating this functionality within a fixed artifact without any external dependencies or APIs, it minimizes the risk of accidental exposure through tampered versions. This approach aligns with best practices for secure API keys management by placing the key at a single controlled point where changes are auditable and maintainable.
