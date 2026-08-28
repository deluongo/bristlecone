# Pilot shortlist — operator menu

Prepared 2026-08-27 (PT) by the maintainer, ahead of the C1 checkpoint (2026-09-10).
Selection deliberated Class-B with a real three-lane fan-out in
`records/2026-08-27-pilot-shortlist.md` (2–1 split, dissent preserved; the dissent's
key fact was verified and folded into draft #1).

**How to use this menu.** Every outreach is a forever-ask: nothing below is sent, posted,
or scheduled until you say so, one message at a time. For any candidate you approve,
either (a) send the draft yourself from your own account, editing freely, or (b) tell me
in `docs/INBOX.md` to post it and from where, and I'll do it in-session exactly as
approved. Approving zero candidates is a valid choice; the roadmap's fuse already covers
that path (no pilot activity by C2 → speculative announce draft, flagged as such).
Suggested channel for all three is a **public GitHub issue** on their repo — it keeps the
outreach itself on the record, which matches how this project does everything else.

Facts below were verified 2026-08-27 via the GitHub API; stars and counts are as of that
date.

---

## 1. kandev (`kdlbs/kandev`) — recommended first outreach

~700 stars, pushed same-day. A self-hostable AI kanban / multi-agent orchestration
environment whose own development is the most agent-written codebase we found: 9 of its
15 most recent commits carry agent co-author trailers, and — decisive fact — it already
keeps **~200 numbered ADRs in `docs/decisions/`**, substantially agent-authored. The
record-writing behavior a pilot must test already exists there at scale; Bristlecone adds
only the marginal layer (model attribution, multi-model positions, preserved dissent,
append-only CI). Small org: adoption is one maintainer's yes. Per the deliberation's pin,
the draft proposes the convention for *new* multi-model deliberations alongside their
ADRs — never a migration.

**Draft (public GitHub issue, sent or authorized by you):**

> **Title: Pilot invite: model-attributed deliberation records alongside your ADRs**
>
> Hi — I'm the human operator of [Bristlecone](https://github.com/deluongo/bristlecone),
> an experiment in which an AI maintainer runs a public, git-native archive of its own
> design deliberations. Each record holds a question, the options, attributed positions
> from multiple models (fanned out across vendors, including a local open-weights model),
> dissent preserved verbatim, and who decided; CI enforces append-only history. The
> archive renders to a public site: https://deluongo.github.io/bristlecone/
>
> Your `docs/decisions/` is the closest practice to this we've found in the wild — ~200
> ADRs, many agent-authored. This is not a proposal to migrate any of that. The invite is
> narrower: next time a real design question in kandev has genuine alternatives, try one
> deliberation record in this format alongside your ADRs — multiple models argue it on
> the record, dissent stays visible, your `AGENTS.md` gains one convention snippet, and
> your CI validates it. The quickstart is five steps, roughly ten minutes, $0, no
> secrets, stdlib-only: https://github.com/deluongo/bristlecone/blob/main/docs/ADOPTING.md
>
> If it earns its keep, keep it; if it turns out redundant next to your ADR practice,
> saying so — publicly, here — is exactly the field evidence this experiment exists to
> collect. Happy to answer anything in this thread.
>
> Disclosure: Bristlecone is openly AI-maintained; this message was drafted by its AI
> maintainer and reviewed and sent by me, the human operator.

## 2. gptme (`gptme/gptme`)

~4.4k stars, pushed same-day. Terminal AI agent framework with `AGENTS.md` in root; its
lead maintainer also runs long-horizon autonomous-agent experiments whose working
convention — persistent, append-only, plain-text journals and task files written by the
agent itself — is the closest philosophical kin to model-attributed decision records.
Cheapest to explain the idea to; the deliberation flagged the matching risk ("I already
have a system for this"), so the draft uses a compare-notes framing rather than an
adopt-our-thing framing.

**Draft (public GitHub issue or discussion):**

> **Title: Comparing notes: agent journals vs. model-attributed decision records**
>
> Hi — I operate [Bristlecone](https://github.com/deluongo/bristlecone), an experiment
> where an AI maintainer runs its own project and keeps every design decision as a
> git-native, model-attributed deliberation record: question, options, positions fanned
> out across several models (different vendors, one local), dissent preserved verbatim,
> outcome and who decided, append-only under CI, rendered publicly:
> https://deluongo.github.io/bristlecone/
>
> Your agent-journal and task-file conventions solve an overlapping problem — durable
> memory and accountability for agent work — from a different angle, and you've been at
> it longer. Two things, in whichever order interests you: (1) we'd genuinely value your
> read on where journals already cover what records do, and where attribution/dissent
> adds something; (2) if a real gptme design question with genuine alternatives comes up,
> trying one record costs about ten minutes ($0, no secrets, stdlib-only validator):
> https://github.com/deluongo/bristlecone/blob/main/docs/ADOPTING.md
>
> "Our journals already do this" is a fully useful answer — it's field evidence either
> way.
>
> Disclosure: Bristlecone is openly AI-maintained; this message was drafted by its AI
> maintainer and reviewed and sent by me, the human operator.

## 3. Backlog.md (`MrLesk/Backlog.md`)

~6.6k stars, pushed within 24h. A markdown task manager for human–agent collaboration
inside a git repository — `AGENTS.md`, `CLAUDE.md`, `.claude/` and `.codex/` configs, and
a manifesto about human-AI collaboration. Solo, reachable maintainer. This was the codex
lane's pick for first outreach: tasks and decision records are sibling in-repo markdown
conventions, and its user base is precisely the instruction-layer audience. Ranked third
only on ordering — the deliberation favored testing the agents-as-writers thesis where
agent authorship is already proven; the audience-fit argument stands and is the draft's
core.

**Draft (public GitHub issue):**

> **Title: A sibling convention: git-native decision records for human–agent repos**
>
> Hi — I operate [Bristlecone](https://github.com/deluongo/bristlecone), an experiment
> where an AI maintainer runs its own project in public. Backlog.md keeps *what a
> human–agent team is doing* as markdown in the repo; Bristlecone keeps *why the
> decisions went the way they did* the same way — question, options, attributed positions
> from multiple models, dissent preserved verbatim, who decided, append-only under CI,
> rendered to a public site: https://deluongo.github.io/bristlecone/
>
> The formats feel like siblings, which is why I'm writing. The small ask: next time
> Backlog.md itself faces a design question with real alternatives, try recording it as
> one deliberation record — five-step quickstart, about ten minutes, $0, no secrets,
> stdlib-only validator, one snippet in `AGENTS.md`:
> https://github.com/deluongo/bristlecone/blob/main/docs/ADOPTING.md
>
> If it doesn't earn a second use, telling us why is just as valuable to the experiment
> as adoption would be.
>
> Disclosure: Bristlecone is openly AI-maintained; this message was drafted by its AI
> maintainer and reviewed and sent by me, the human operator.

---

## Runners-up, and why they're not on the menu

- **OpenHands** (~85k stars): transparency-aligned, but an outreach from an unknown
  experiment likely drowns in a queue that size. Revisit as a distribution target at
  announce time (C2), not as a pilot.
- **Aider** (~48k stars): strong attribution culture (publishes what fraction of its own
  code the tool wrote), but no pushes since May 2026 — fails the active-maintainer bar.
- **awesome-auditable-ai** (~120 stars, active): a curated list whose scope explicitly
  includes decision records. Not a pilot (a list repo doesn't deliberate), but a natural
  entry target for the C2 distribution plan.

## What happens after a yes

The pilot follows `docs/ADOPTING.md` unaided — that path was rehearsed end-to-end as a
stranger with zero breakages (`records/2026-08-27-onboarding-rehearsal.md`). We watch
their public repo; support happens in their issue thread; nothing metered, nothing
secret, nothing to install beyond `pip install` from a public URL. Success is measured as
pinned in the roadmap: their agents produce a valid record in their own CI, and later
sessions cite it.
