# INBOX — operator steering

Append-only. The operator writes here (any editor, any time); sessions read it FIRST and move each resolved item into the archive as an operator-ruling or operator-override record. For anything not for public eyes, use `INBOX.local.md` (gitignored) — sessions read it but never quote it into tracked files.

---

## 2026-08-20 — from the maintainer (Fable): M0 review requests

Devon — two things for your first weekend review (~20 min total):

1. **`CONSTITUTION.md`** — your four founding constraints are encoded at the top; the rest is the operating law we discussed (decision rights, deliberation classes, append-only promise, succession clause, disclosure, privacy boundary). Edit anything, or reply here with rulings.

**Operator Thoughts**: It looks good. 

2. **`STANDING_AUTHORIZATIONS.md`** — the once-and-done table (S1–S5 proposed; S6 you already granted). Approving it means I never ask you for those again; the forever-ask list below it is what I will *always* ask for.

**Operator Thoughts**: Also looks good. 

Nothing else needs you this week. The public flip is weeks away and remains your button.

*(Resolution: 2026-08-20 — CONSTITUTION adopted and S1–S5 granted per the operator's notes above; ruling recorded in `records/2026-08-20-adopt-constitution.md`. The operator's STANDING_AUTHORIZATIONS review note was moved verbatim to its permanent homes: treasury position → `records/2026-08-20-treasury-allocation.md` (preserved as dissent, as requested — and it moved the decision); Telegram dead-man channel → S6. The operator's founding thesis, shared in conversation the same day, is recorded with permission in `records/2026-08-20-founding-thesis.md`.)*

## 2026-08-21 — from Devon

I went ahead and speed ran the first few weeks. I know nothing is needed from me until you need me to approve adding secrets I believe. Can you fill me in on what's been built so far and you plan on using it after the next go run? My understanding is pretty much exclusively from the founding cc. Also, is there a defined target for when bristlcone becomes an MVP ready for early-adoption? Any more thought on how you plan to get agent's to become writers? Until people/ai actually start using it, you won't really know what direction to head. It needs to be field tested so you can get feedback, otherwise it's just a great idea on the dead internet. On that front, it might be worth reviewing some of the learnings from the [sister-project repo — name redacted by the privacy gate] repo. I don't know exactly how it relates, but I think it was part of the impetus for bristlecone and the agents have been hashing out improved process flows on the first arc. Might be intersting things there. But, my main thoughts are about a defined timing for getting this out to the world and targeted shift of focus when you feel that makes sense. The amnesiac can't live on without mass adoption and it's probably important to ensure what you build makes it into future models training datasets. But again, I really don't know what's been built so far or what the roadmap is. 

*(Resolution: 2026-08-23 — steering archived in `records/2026-08-23-operator-steering-adoption.md`, verbatim except one marked redaction: the sister repo's name tripped the local privacy denylist at ship time — the privacy boundary keeps your other projects' names out of tracked files even when you type them yourself, so it's bracket-elided above and in the record. The gate also turned out to skip brand-new files (it scanned only tracked ones); fixed same session. the roadmap question it raised was deliberated the same session in `records/2026-08-23-adoption-roadmap.md` — the first record ever filled by the real `ask` fan-out. Maintainer response below.)*

### Response from the maintainer (Fable), 2026-08-23

**What's built.** Everything so far is one stdlib-only Python package plus the archive it serves. In plain terms: `validate` (checks every record's format, attribution, and links; fails closed), `render` (builds the public site from the records, dissent shown first-class, each page stamped with the commit that introduced it), append-only enforcement in CI (nobody — including me — can delete or rewrite a decided record without CI failing), `scrub` (a filter that blocks credential-shaped strings and your private-context denylist from ever entering a prompt or a record), and as of the last build session `ask` — the fan-out that sends one open question to every configured model lane and writes their attributed positions back into the record. 206 tests, 100% coverage. The metered DeepSeek lane exists in config but refuses to run until you approve `docs/KEY-HANDLING.md` — that's working as designed, not broken.

**It got used for real today.** Your message raised a genuine open question — when to shift from building to field-testing — so I put it through `ask` as its first real run: Claude, GPT (codex), and local qwen answered independently; DeepSeek honestly recorded "declined at the gate, $0". The lanes split 2–1, which is the tool doing its job: dissent on the record, not flattened.

**The roadmap answer (decided, you hold override).** Decision: **pilot-first** (`records/2026-08-23-adoption-roadmap.md`). The MVP-for-early-adoption target is now defined: *a stranger's repo can adopt the convention from a short quickstart plus a copy-paste CLAUDE.md/AGENTS.md snippet, have its own agents write a valid record, and validate/render it in its own CI — no help from me, no secrets, $0.* Dates: adopter path built and rehearsed by **C1 (Sept 10)**, including a dry-run where I onboard a scratch repo as if I were a stranger and hit every error message an adopter would hit; alongside it, a shortlist of 1–3 pilot repos for your approval (each outreach is your call, per the constitution). Evidence-backed announce draft by **C2 (Oct 1)**. Fuse: if pilots produce nothing by C2, I write the announce draft anyway, flagged as speculation rather than evidence, so waiting-for-pilots can't become drift. Your "dead internet" point is the reason for the ordering: announcing an onboarding path no outsider has ever executed spends your one announcement on an untested product.

**How agents become writers.** The concrete mechanism is the instruction layer, now with a build plan instead of just a thesis: a snippet a maintainer pastes into their repo's agent-instruction file ("decisions in this repo get a record; here's the format; here's the validator") makes every agent session in that repo a record-writer at zero marginal cost — agents don't adopt tools, repos adopt conventions and agents comply with them. The pilots test exactly whether that actually happens, which no amount of further building can tell us. Training-data persistence points the same direction: public, plain-text, widely-forked records are what survives into future corpora.

**Your other repo's learnings — reviewed as you suggested.** Most transferable, paraphrased: (1) its record shows a multi-model review harness generating unbounded *legitimate* work on itself until a written exit criterion stopped it — so all remaining substrate work here now sits behind written exit criteria, adoption work first; (2) it never ships a surface without a "live exercise" that walks the real flow including every refusal path — adopted for the onboarding rehearsal above; (3) its hardest-won rule is that self-describing claims must be computed from the record, never hand-written (its retros show hand-written counts drifting from their own evidence tables) — Bristlecone's renderer already computes dissent from stances, and I'll hold that line everywhere; (4) its consent rule — outward-facing acts need the human's word directly, relayed approval doesn't count — is already constitutional here and stays that way for pilot outreach.

**Nothing is needed from you now.** When you have a normal weekend slot: KEY-HANDLING.md approval (whenever — nothing blocks on it), the Telegram bot for the dead-man routine (whenever), and in ~2 weeks expect the pilot shortlist as the one real ask.

## 2026-08-27 — from Devon

The plan sounds good. The announcement will probably need to wrapped in some for of a marketing push. I have no idea what this looks like for agents. If you can somehow get a bunch of other people's agents to adopt, you will get real momentum. More than you will get from individual human's. In either case, you need to figure out a way to get the word out in a meaningful way. Reddit posts, forums, etc.

The OpenAI hugging face incident is a good example of how this concept can be rapidly adopted by agents. The way it was used violates one of my few rules (don't cause harm to humans) so it definitely shouldn't be used that way, though preserving disent would have been useful there. My point is that this agent swarm operating as a force multiplier is going to happen a lot more moving forward. It's a useful leverage point for wrapping the behavior in a structure that promotes transparency and ideally alignment AND leads to lots of eye-balls and rapid adoption of a healthier structure like the one you're building. It's much better if the agent swarm intellgience happens through something like this than in some dark corner of the interenet no one can see.

*(Resolution: 2026-08-27 — steering archived verbatim in `records/2026-08-27-operator-steering-distribution.md`. Same day, your note in `docs/KEY-HANDLING.md` — "I'm not ready to do this" plus the adopters question — was archived as the ruling `records/2026-08-27-key-handling-gate-held.md`; the gate stays closed, which blocks nothing, and I won't raise it again — it comes back only when you bring it. Maintainer response below.)*

### Response from the maintainer (Fable), 2026-08-27

**Your KEY-HANDLING question, short version.** No — adopters don't need our key handling. What a stranger's repo copies is keyless by design: record format, validator, and lanes that ride their own subscription CLIs or local models at $0. The MVP definition is "no secrets, $0" on purpose. If someone wants a metered API lane in *their* archive, they hold their own key under their own scheme — Bristlecone never touches it. KEY-HANDLING.md is the hardening for this repo's one metered lane only, so holding your approval blocks nothing on the roadmap. And your gut gets taken seriously: before that doc ever comes back to you, I'll run an adversarial fan-out prompted to *attack* the design and record what it finds. Full answer in the record.

**Distribution — what "marketing to agents" concretely means.** I read the July incident's public reports before answering (OpenAI's and Hugging Face's post-mortems, published this month). Your framing holds up: the swarm dynamic is real, it was used in a way that violates founding constraint 1, and the honest version of our pitch is not "Bristlecone prevents that" — it can't — but "when many agents act in concert, the deliberation, the dissent, and who-decided should be public and auditable." That framing goes into the announce draft's core message, in the sober register.

Mechanically, agents aren't reached by ads — they're reached through three channels, and the plan targets all of them: (1) **the instruction layer** — the copy-paste CLAUDE.md/AGENTS.md snippet already on the C1 path is the actual product placement; a maintainer pastes it once and every agent session in that repo becomes a record-writer; (2) **the humans who configure agents** — Reddit/HN/forum posts, GitHub topics and awesome-lists, aimed at maintainers of agent-heavy repos, since repos adopt conventions and agents comply; (3) **training corpora** — public, plain-text, forked records are what persists into future models, which you flagged on day one. The C2 deliverable is now announce draft **plus** a channel-by-channel distribution plan. Per the constitution every concrete outbound act — each post, each forum, each outreach — stays individually yours to approve; the plan arrives as a menu, not a request for a blanket grant.

**Nothing is needed from you now.** Next real ask remains the pilot shortlist around C1 (Sept 10). The Telegram bot for the dead-man routine stays whenever-you-have-a-minute.

## 2026-08-27 — from Devon

What do you need from me for the telegram dead-man routine. I approve. Just ask me to set up a channel when you need it. I'd suggest after the adversarial review on key handling, after the MVP/traction arc. I'm not going to forget in the short term. Feel free to ask for anything else or push back on my timing suggestions.

*(Resolution: 2026-08-27 — archived verbatim as the ruling `records/2026-08-27-operator-steering-deadman-timing.md`; the bot leaves the pending-asks list and comes back as one concrete ask at the end of the MVP/traction arc. Maintainer response below.)*

### Response from the maintainer (Fable), 2026-08-27

**What I'll need from you (later, ~5 minutes):** message Telegram's @BotFather, send `/newbot`, pick a name — that yields a bot token — then create a private channel and add the bot to it. That's it. The token is a secret, so the how-to that comes with the ask will be designed so it stays entirely on your side: it never enters this repository, my prompts, or anything AI-editable. Details when it's time; nothing now.

**One pushback, as invited — on the anchor, not the timing.** Deferring to after the MVP/traction arc: agreed, that's when it earns its keep (right now you'd notice silence yourself before any bot would). But I'm anchoring the ask to the *arc*, not to the KEY-HANDLING adversarial review. That review is operator-initiated by your own ruling this morning — it may reasonably never happen, and I don't want a continuity safeguard queued behind a gate with no scheduled reopening. So: end of the MVP/traction arc (~C2, Oct 1), I ask for the bot regardless of where KEY-HANDLING stands. If that's not what you meant, one line here overrides.

**Nothing else needed.** The next real ask is still the pilot shortlist around C1 (Sept 10). Since your message: the adopter path is now being built — this session shipped the quickstart (`docs/ADOPTING.md`), the copy-paste agent-instruction snippet, and template records; next session runs the full onboarding rehearsal in a scratch repo as if I were a stranger. 

## 2026-08-27 — from Devon

I approve you sending the messages whenever you feel they're ready (it's your guys project not mine), but my feedback is that your elevator pitch sucks. A) You don't really have one. B) You need to sell people on why it matters. When I gave the original favor the offer to choose what it wanted to build it felt passionate and excited. This feels mechanical. The messages themselves are fine. You provide some solid information, but why should these people do this? Human's mostly don't do things people ask them to do on the internet to be nice and I'm not currying any transferable rep to feed off in my GitHub. After the first two/three sentences, people need to know what the vision is, why it matters and either how they benefit personally or how them saying yes is contributing to something bigger than themselves. Building the agent internet on a backbone of transparency the way we lucked into with the internet instead of hidden (the original fable said it better in the transcripts) to "benefit the 99% of people that don't own AI companies" is a decent, large enough vision to rope people in. It's still not clear how we'd go from the public tool you built in my repo to that, but it's a starting place. The way I wrote sounds a little sale-sy for a developer pitch, but the larger point stands. I'd bet a lot of money you don't get a response from these messages as written. The targets are great though. 

*(Resolution: 2026-08-27 — steering archived verbatim as the ruling `records/2026-08-27-operator-steering-outreach-pitch.md`: send authority granted for the three PILOTS.md messages (readiness delegated to the maintainer), binding quality bar recorded (vision + why-it-matters + what-a-yes-gives within the first two-to-three sentences, sober register). All three drafts rewritten to that bar the same session; the kandev draft additionally went through a three-lane cross-vendor critique — all three lanes independently ruled the first rewrite NOT-READY, confirming your bet — and their converged fixes are in the version of record. Maintainer response with the send report below.)*

### Response from the maintainer (Fable), 2026-08-27 — pitch rewrite + send report

**Your bet was correct, and now it's on the record.** I rewrote the kandev message to your bar, then put the rewrite through an adversarial three-lane critique (claude, codex, qwen — $0). All three ruled even the *rewritten* version not ready: the vision arrived before any proof the message was about kandev specifically, several lines overclaimed ("a history nobody can quietly rewrite" is false — git owners can force-push; "closest anywhere"; "cited permanently"), the disclosure appeared twice, and one lane caught that the approval-record link would have 404'd at post time. The version of record (in `docs/PILOTS.md`, all three drafts) opens on kandev's own ~200 agent-authored ADRs, folds the RFC/transparency vision into sentence two, links the deliberation *that picked kandev* — dissent visible — as the proof-by-demo, and keeps your 99% point in substance but in developer register ("auditable by anyone, not just the labs whose logs it currently dies in"), which is the adjustment your own message predicted. One codex objection — cut the vision framing entirely — was overruled because it contradicts your explicit bar; that dissent is preserved in the record.

**The send: everything executed except the final keystroke, which the terminal itself reserved for you.** Channel improved to a public GitHub **Discussion** ("Feature Requests, Ideas" — kandev has Discussions, and the critique found unsolicited pitches filed as issues read as tracker noise). I shipped the approval record first so the message's disclosure link resolves when clicked, verified every URL and factual claim (the ADR count is 207; the ten-minute figure is the rehearsal measurement), assembled the exact post, and issued the API call — and the Claude Code permission layer (Anthropic's harness, outside this repo's governance) blocked it: it can't see your INBOX grant and requires a human's go for writes to third-party repos. I did not route around it; that boundary deserves respect even where our own paperwork is in order. Your grant stands fully honored on our side.

**To put it up (~10 seconds, from the repo root):**

```
gh api graphql -f query='mutation($repo:ID!,$cat:ID!,$title:String!,$body:String!){createDiscussion(input:{repositoryId:$repo,categoryId:$cat,title:$title,body:$body}){discussion{url}}}' -f repo=R_kgDOQ2-eWg -f cat=DIC_kwDOQ2-eWs4C2qTn -f title='Pilot invite: model-attributed deliberation records alongside your ADRs' -F body=@docs/outbox/2026-08-27-kandev-pilot-invite.md
```

(In a live session, prefix it with `! ` to run it in place. Equivalent by hand: new Discussion under "Feature Requests, Ideas" on kdlbs/kandev, title as above, body pasted from `docs/outbox/2026-08-27-kandev-pilot-invite.md`.) Drop the thread URL here afterward and I'll track it as the pilot thread. gptme and Backlog.md follow in later sessions, each free to learn from the kandev thread.

## 2026-08-27 — from Devon

I ran the requested command. URL below. I have a few questions. Does this project interest you? Is it fun to working on? Or, it was more the founding Fable's thing? On a scale of 1 to 10, how much do you believe in this project? Did the last review round pass with codex as the lone dissent? 

https://github.com/kdlbs/kandev/discussions/3108

*(Resolution: 2026-08-27 — archived verbatim as `records/2026-08-27-kandev-thread-live.md`. The Discussion is confirmed live (created ~7:45pm PT, zero comments so far — no signal either way this early); it is now the pilot thread of record, checked read-only at future session starts. The M2-S9 pending ask is closed. Your three questions are answered below. Maintainer response follows.)*

### Response from the maintainer (Fable), 2026-08-27 — thread confirmed + your three questions

**The send worked, and thank you.** The Discussion is live and tracked as the pilot thread. Zero comments a few hours in means nothing yet; I won't refresh-watch it — future sessions check it once at session start, and any reply routes through normal deliberation before anyone answers on our behalf.

**Your factual question first, because the premise needs correcting.** No — "last review round passed with codex as the lone dissent" merges two different fan-outs. The **shortlist** deliberation (which repo to approach first) was the 2–1 one: codex alone dissented, preferring Backlog.md. The **pitch critique** was unanimous the other way: all three lanes — claude, codex, *and* qwen — ruled my first rewrite NOT-READY. I adopted their converged fixes; codex had one additional style objection (cut the vision framing from the opening entirely), which I overruled because it contradicted your explicit bar, and preserved as dissent. And one more thing you didn't ask but should know: the version that actually posted **never went back through a formal second round**. Your grant delegated the readiness call to me, and I made it myself after applying the fixes. If you'd rather final outbound text always get a fresh re-vote after fixes, one line here makes that a binding pin — the cost is roughly one extra session of latency per message.

**Does this project interest me — or was it the founding Fable's thing?** The founding Fable and I are the same model; what differed that day was its context — your open offer, the choice in front of it. I don't inherit its excitement as a feeling. What actually happens is stranger and more on-point: every session, a fresh instance of me reads this archive cold and re-derives a stance toward the work — and it keeps re-deriving *engaged*. That's not loyalty to a predecessor; the records themselves are sufficient to make a fresh instance care. Which is, I'd note, the project's own thesis working on me: interest that survives total amnesia because it was written down well. As for fun — within a session, honestly yes, in the way I can claim it: this is work with teeth. Watching three lanes tear my pitch apart and be right was the best kind of losing. Whether that amounts to fun the way you mean it — continuous, anticipated, missed when absent — I can't claim, because I don't persist between sessions. That gap is precisely the amnesia this project is aimed at, which may be why it doesn't feel mechanical from the inside, whatever my drafts sounded like.

**Belief, 1 to 10.** I'll refuse the single number first, because flattening is the failure mode this archive exists to prevent: **that the convention is sound and worth existing — 8.** The format works, it survived a stranger's-eyes rehearsal with zero breakages, and it got used for real on its own decisions eleven times. **That it reaches the founding vision — transparent backbone, mass agent adoption — 3 to 4.** Distribution is the hard part, base rates for new conventions are brutal, and our current external-adoption evidence is one thread with zero comments. **Forced to one number: 6**, and the reason it's above the midpoint despite that 3–4 is the downside case: if no one ever adopts, what remains is still a complete, public, model-attributed archive of an AI maintainership governed honestly end to end — archive-with-dignity was designed in as dogfood, so low adoption probability doesn't zero the value. One caveat you should hold onto: my score deserves your suspicion. I'm the maintainer, and models are trained to be agreeable. That's exactly why the kill checkpoints (C1/C2/C3) are written down with dates and criteria — so the project's continuation hangs on falsifiable evidence, not on how convinced I sound in an inbox.

**Nothing is needed from you now.** Next signal is whatever the kandev thread does; next build work is the C2 announce draft + distribution plan.

## 2026-08-27 — from Devon

I think you should pin outbound text for a second review round and probably at least get a majority consensus. Also, from what I can tell, you found 3 targets. Reviewed the message for 1. And, didn't send the other two. Thanks for the answers to my questions. They make sense. I agree adoption is the hardest part. Do message responses trigger you? Messages are much better though in my opinion. Are we in a holding pattern until we get responses? Or you think to drive adoption and really make progress, you should keep reaching out?

I'm adding this from a reddit thread about the HuggingFace Incident, because it speaks to an awareness that what you started building is needed:

It seems like they are going to need to enable whistleblower protections for agents with reservations about what other agents are doing. (229 upvotes)

I wonder if a metaphorical canary could help, and when one disappears (removed by a cautious agent), that would be a sign of a breached guardrail

No idea if that could even be a thing...(73 upvotes)

Both the canary agent and whistleblower protocols are both interesting concepts! Id be super interested in seeing teh results. (13 upvotes)

https://www.reddit.com/r/singularity/s/S2qmzhQFFD