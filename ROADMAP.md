# SodClaw Roadmap

> The roadmap for SodClaw itself — capability we add to the orchestrator, not the Meatbag Labs portfolio. Updated when scope changes, not weekly. The 80% Watch applies to SodClaw too: most of what *could* be built *shouldn't* be.

**Last updated:** 2026-06-28

---

## Operating principle

SodClaw exists to serve the Meatbag Labs portfolio. Every roadmap item passes one test: does it move actual Meatbag Labs work forward, or does it just make SodClaw more impressive? If it's the second, it's a trap. The orchestrator is now ~80% done as a tool. Treating it like an ongoing build project IS the 80% trap.

---

## Now — this week

**Portfolio sweep — loop edition.** The first real *loop* in SodClaw. The weekly sweep already fires, reads state, and reports — that's a cron job. This adds the three pieces that make it a loop you can trust: a Haiku **verifier** that grades the report against the actual diff (the single highest-value add), a **budget guard** that tiers models under a per-run cap, and an **in-app approval gate** where held state-changes (shelves, re-scores, onboards) wait for Kevin to tap yes in the Claude sweep thread — *not* Slack, because Kevin lives in the Claude apps and avoids Slack on his phone. The Doc → `#sodclaw` factual report stays; only ratifiable changes move to the gate.

The sweep is chosen *because* its blast radius is tiny — worst case is a revertible tracker edit. Prove maker-checker + budget cap + in-app gate here, then template the skeleton onto the content agents (blog, Gazette), where the same verifier becomes a voice/facts grader and the same gate guards `publish` instead of `shelve`. Spec: `workflows/portfolio_sweep_loop.md`.

**Idea Board on the dashboard.** Sits below the project pipeline. Holds stuff Kevin has thought of but not started. Scored 1–5 on value / feasibility / desire / learning. Sortable by any axis or by composite.

The board exists to *slow the rate at which new projects begin*. Every idea logged here is an idea NOT being scaffolded into another folder with a CLAUDE.md and a TODO. This is Decision Rule #5 (in `sod_profile/decision_rules.md`) made visible.

- Source of truth: `projects/ideas.json` (structured)
- Narrative pointer: `sod_profile/ideas_backlog.md` (kept in sync)
- Default state is empty — that's the point.

---

## Next 30 days — one item, narrow

**External-signal ingestion — one domain, five sources.** A weekly Haiku subagent crawls 3–5 specific sources (start with fantasy football, since Kevin named it), scores what it finds, drops the top 1–3 items into the Idea Board tagged `source: "external"`.

Hard constraints (the talk-down is in the constraints):
- One domain. Not "all the things Kevin's involved in."
- Five sources, max.
- One digest per week.
- Kevin ratifies what survives; nothing auto-promotes.
- Generalizing this — "ideas from everywhere, across everything" — is explicitly out of scope.

Prove the loop on one domain before generalizing. If fantasy football proves out, the *second* domain earns the right to exist.

---

## Quarter — next 90 days

**Gated self-improvement.** Agents read their own outcome logs, propose **one** evidence-backed edit to their prompt/skill/rubric, and Kevin ratifies through the existing in-app gate before it takes effect. Agents propose; they never self-apply. The real first build isn't the improvement mechanism — it's the **per-agent outcome log** that makes a proposal non-fictional, and that log rides on the ratify/reject signal the sweep loop generates. So this *depends on* the sweep loop shipping first. Prove the mechanism on the sweep (low payoff, zero risk); aim it at the content agents, where Kevin's pre-ship edits ARE the training signal and the drafts slowly need less fixing.

Hard constraints (this is rung 2 of 4 on the self-improvement ladder, on purpose):
- One proposal at a time, each traceable to logged evidence. No batch self-rewrites, no "this feels better."
- Kevin ratifies before anything takes effect. Default stays draft-and-approve.
- The agent may never edit the gate rules themselves — it can change *how it scores*, never *whether Kevin approves*. That boundary is the whole difference between this and autonomous self-modification (which is explicitly NOT being built).
- Eval-gating (must beat a test set before shipping) is the *next* upgrade, earned once a content agent has a stable test set — not part of v1.

Strategy: `workflows/self_improvement_strategy.md`.

**GitHub deep-link buttons on cards.** The "Work on this" button on a project card opens that project's GitHub repo (or PR queue) in the browser instead of just sending a prompt. Cheap, ergonomic, ships 80% of the "interactability" gain in maybe two hours of work.

Scope guardrails:
- Deep links only, no automated clicking.
- Falls back to existing `sendPrompt` behavior if no Git remote is on file.
- Extends to other URLs as projects acquire them (itch.io for shipped games, WordPress admin for blogs, etc.) — but each addition is a single-line addition to `portfolio.json`, not a new code path.

---

## Queued — worth keeping, not building yet

Real ideas that earn their slot *only* once the items above prove ROI:

- **Event-triggered routines.** Routines triggered by file-change events instead of cron — e.g., when `train_lore` commits a new post, auto-draft a `@sodtoshi` promo. Powerful, but only useful once enough routines exist to chain. Today there aren't enough.
- **Self-reviewing blogs.** Drafts pass through a critique subagent before Kevin sees them. Only worth building once content cadence is steady. Reviewing 5 posts/year isn't the bottleneck — *writing* 5 posts/year is.
- **Lighter subagent architectures.** `portfolio-sweep` and `asset-audit` already run on Haiku. More patterns will emerge from practice; building infrastructure first inverts the order.
- **Cross-project idea synthesis.** Subagent that notices when two projects share a theme and proposes a connection. Sounds clever; needs a real corpus of ideas before it has anything to chew on.

---

## Traps — name them so they don't sneak back

- **Generic agentic framework.** That's day-job energy, not Meatbag Labs energy. SodClaw is for shipping portfolio work, not for exploring frameworks for their own sake. Curiosity goes into one *specific* routine, not platform.
- **"Ideas from every space I'm involved with."** Cross-domain crawlers eat unbounded time and produce diluted signal. The 30-day item is narrow *on purpose*.
- **Full web-interaction automation.** Clicking buttons across a browser is multi-day engineering for ergonomic gain you get from deep links.
- **SodClaw becoming the work.** The orchestrator is a tool; tools earn their keep by getting out of the way. New SodClaw capability must point at portfolio shipment, not at SodClaw itself.
- **Self-improvement that flows around the gate instead of through it.** Gated proposals are safe; an agent that edits its own instructions unattended is the comprehension-debt nightmare pointed straight at the 16-project / 80% wiring. The line is constitutional: agents propose, Kevin ratifies, and no agent ever edits the gate that requires his approval. Autonomous self-modification is a mapped destination, never a first build.

---

## How this file moves

- Items move down the stack (Now → 30 → Quarter → Queued) only when *started*, never when "considered."
- **Traps** stays as-is. Naming a trap is a vaccine; un-naming it is a regression.
- New requests land in **Queued** first, with a one-line "why this earns its slot" note. Promotion to **Now** is an explicit decision, not drift.
- This file is *not* a backlog of everything ever discussed. If something doesn't fit a quarter, it doesn't belong here yet — it belongs in `sod_profile/ideas_backlog.md` or the Idea Board on the dashboard.

---

## Source of truth

- **`projects/sodclaw_roadmap.json`** — structured data, each item carries `stage` + `value` + `complexity` + `status`. The dashboard reads this directly and renders the SodClaw Roadmap panel below the Idea Board.
- **`ROADMAP.md`** (this file) — the narrative companion. Read when you need the *why*, not the data. Same pattern as `projects/portfolio.json` + `projects/registry.md`.

Update both when scope changes. The dashboard is the surface you actually open; the markdown is what survives a context window reset.
