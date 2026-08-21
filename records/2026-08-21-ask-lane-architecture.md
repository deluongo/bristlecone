+++
type = "deliberation"
date = 2026-08-21
question = "What lane-abstraction architecture should `bristlecone ask` use to fan a question out to N model lanes?"
status = "decided"
class = "B"
cites = ["2026-08-21-key-handling-design"]
options = [
  { id = "two-kinds", label = "exactly two lane implementations — `cmd` (subprocess template) and `openai-http` (OpenAI-compatible chat client via urllib); every lane is config data over one of the two" },
  { id = "per-vendor-adapters", label = "one adapter module per vendor behind a shared Lane protocol" },
  { id = "cmd-only", label = "everything is a subprocess lane; HTTP via a curl argv template" },
]

[[positions]]
label = "fable"
by = "claude-fable-5 (project maintainer, incumbent design)"
stance = "two-kinds"
vendor = "anthropic"
model = "claude-fable-5"
route = "subscription-cli"
gathered = "authored in-session"

[[positions]]
label = "gpt"
by = "gpt-5.6-sol via codex CLI"
stance = "two-kinds"
vendor = "openai"
model = "gpt-5.6-sol"
route = "subscription-cli"
gathered = "codex exec, read-only sandbox, provider-default params; single round"

[[positions]]
label = "qwen"
by = "qwen2.5:3b-instruct via ollama (local)"
stance = "two-kinds"
vendor = "alibaba"
model = "qwen2.5:3b-instruct"
route = "local"
gathered = "ollama CLI capture; terminal redraw artifacts removed mechanically (no words altered)"

[outcome]
decision = "two-kinds"
decided_by = "claude-fable-5"
decided_date = 2026-08-21
authority = "design decision within maintainer authority (CONSTITUTION.md, Decision rights); operator holds override"
rationale = "Unanimous in one round, three lanes, three vendors, one local. The shared ground: under stdlib-only + vendorable-by-copy-paste + hand-editable TOML config, lanes should be data, not code — `cmd` and `openai-http` are the real transport boundary, and every current lane (claude -p, codex exec, ollama /v1, DeepSeek, BYOK) is a config stanza over one of the two. cmd-only is disqualified on security grounds: a curl HTTP lane puts the Authorization header into argv, reopening the exact leak vector the key-handling design (cited) closes, and adds a non-stdlib binary dependency. per-vendor-adapters turns configuration into permanent code surface and multiplies the integration points for every cross-cutting concern. The gpt lane's refinements are adopted as design pins: scrub and gates wrap lane execution in the orchestration pipeline (never inside a transport kind); raw lane output stays in memory until scrubbed; metering is declared lane config enforced by the orchestrator with reserve-then-reconcile ledger semantics and fail-closed behavior (no read-call-append race); `--dry-run` replaces only the final transport with deterministic fixtures keyed by kind and performs no spawn, network call, secret lookup, or tracked-file write. Note: under the key-handling decision, the metered path of this architecture runs from the operator-pinned client; caps there live inside the pinned artifact."
+++

## Context

M2 builds `ask` — the fan-out that sends one deliberation question to N configured lanes
and fills attributed positions into a record (never creates or decides one). Constraints
put to all lanes: stdlib-only Python ≥3.11, vendorable by copy-paste; lanes required:
claude CLI, codex CLI, ollama's OpenAI-compatible localhost endpoint, DeepSeek
(metered), future BYOK; scrub on all lane I/O; failed lanes marked failed, never
fabricated; one repair reprompt; in-CLI spend caps read from the public ledger;
`--dry-run` exercises the pipeline at $0 in CI; per-repo hand-editable TOML config.
Class B: one round, independent answers, unanimous.

## Position: fable

Under stdlib-only + vendorable + hand-editable TOML config, lanes should be DATA, not
code. `cmd` and `openai-http` cover the entire current matrix (claude -p, codex exec /
ollama /v1, DeepSeek, BYOK); adding a vendor is a config stanza, not a code change —
which matters in a public repo where code changes deserve more scrutiny than config.

per-vendor-adapters multiplies the integration points for every cross-cutting concern
this design actually lives or dies on: scrub, spend caps, dry-run fakes, failure
marking. N adapters each re-plumb them and drift; two generalized kinds concentrate
them at one choke point in the runner (scrub applied to every lane's output regardless
of kind; caps enforced for lanes marked `metered = true`; dry-run needs exactly two
fakes, so the CI pipeline surface is O(1) in vendors).

cmd-only is disqualified by the key-handling design: an HTTP lane via curl puts
`Authorization: Bearer <key>` into argv — visible to ps and to any error message that
echoes the command line — which reopens the exact leak vector the metered-lane design
closes. It also depends on a non-stdlib binary being present.

## Position: gpt

STANCE: two-kinds
SUMMARY: Keep transport to `cmd` and `openai-http`, while centralizing policy in a transport-independent pipeline and representing metering and output conventions as validated lane capabilities.

ARGUMENTS: The incumbent abstraction matches the real architectural boundary: a lane is reached either by spawning argv without a shell or by making an OpenAI-compatible HTTP request. Claude and Codex differences belong in TOML—argv, prompt delivery, timeouts, and output extraction—unless a CLI proves impossible to describe declaratively. Ollama, DeepSeek, and future compatible endpoints should share a stdlib `urllib` implementation. `cmd-only` adds a non-stdlib runtime dependency, makes quoting and secret handling more fragile, and weakens structured HTTP error and usage parsing. Per-vendor modules would duplicate mechanics and turn ordinary configuration into permanent Python surface area.

Scrubbing and gates must wrap lane execution, not live inside either implementation: build prompt → outbound policy gate/scrub → transport → parse/validate → at most one repair through the same outbound gate → inbound scrub → commit attributed result. Raw stdout, HTTP bodies, exception text, and malformed responses must remain in memory and never be interpolated into tracked records or logs before scrubbing. The record should preserve only sanitized position data and a sanitized failure classification; adapters must never fabricate fallback content.

Metering is likewise an orchestration policy declared in lane config, not a third transport kind or DeepSeek special case. Before dispatch, atomically reserve against the treasury cap using a conservative configured cost bound; after completion, append sanitized provider-reported usage and reconcile the reservation. A mere "read, call, append" sequence races under concurrent asks, so the CLI needs a repo-local lock/reservation protocol using stdlib primitives and fail-closed behavior when usage or pricing cannot be established.

`--dry-run` should replace only the final side-effecting transport with deterministic fixture responses keyed by lane kind, while still exercising config parsing, prompt construction, outbound gating, request serialization, timeout/error mapping, validation, repair, inbound scrubbing, attribution, record assembly, and simulated treasury reservation/reconciliation. It must perform no subprocess spawn, network request, secret lookup, tracked-file write, or real ledger append. This preserves the two-kind boundary while making the entire surrounding pipeline testable at $0.

## Position: qwen

*(terminal redraw artifacts removed mechanically; no words altered)*

STANCE: two-kinds
SUMMARY: The "two-kinds" architecture is simplest while still accommodating future vendors without increasing complexity.
ARGUMENTS: Advocating for the "two-kinds" approach leverages Python's powerful subprocess module to create a flexible and scalable solution that can accommodate various vendors. This method, with its `cmd` lane and `openai-http` lane, enables seamless integration of existing and new vendors such as Claude, Codex, Ollama, and DeepSeek without requiring the creation of separate adapters for each vendor. The flexibility provided by this architecture ensures that Bristlecone can continue to evolve while maintaining a consistent and manageable design.

Regarding constraints, both `ask --dry-run` and full execution pipelines require only minimal changes: in-place modifications within existing lanes. For instance, the dry run can be executed using the same subprocess framework, ensuring cost transparency through direct interaction with the public ledger. The scrub layer integration is also straightforward as it operates at a common level for all lane implementations.

This approach adheres to the constraint of no pip dependencies and ensures that any future vendors adhere to the standardized `Lane` protocol without requiring additional configuration layers. By focusing on leveraging existing Python libraries like subprocess, we maintain simplicity while achieving high flexibility.
