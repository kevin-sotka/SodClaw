# Workflow: Portfolio Sweep — Loop Edition

> The first real *loop* in SodClaw. Takes the existing weekly sweep (a scheduled job that reads state and reports) and adds the three pieces that turn a scheduled job into a loop you can trust: a verifier subagent, a budget guard, and an in-app approval gate. The lowest-blast-radius place to prove the maker-checker pattern before templating it onto the content agents. Substrate for [`self_improvement_strategy.md`](self_improvement_strategy.md).

**Last updated:** 2026-06-28
**Status:** spec / not yet built.
**Builds on:** [`portfolio_sweep.md`](portfolio_sweep.md) (the existing sweep) and [`routine_weekly_sweep.md`](routine_weekly_sweep.md) (the cloud Routine that posts to Slack).

---

## What "loop" adds over the sweep that already exists

The sweep already fires on a schedule, reads `portfolio.json`, detects what moved, and reports. That's the *maker* half — and it already runs.

What separates a loop from the cron job it is today is the **decision logic in the middle, checked by a second agent.** A cron job runs a fixed script; a loop runs a model that reads state, chooses an action, and has its result graded before anything is trusted. This spec adds the three missing pieces:

1. A **verifier** subagent — the checker half of maker-checker.
2. A **budget guard** — tiered models, a token ceiling per run.
3. An **in-app approval gate** — held state-changes wait for Kevin to tap yes, in the Claude app, not Slack.

The Slack report (`routine_weekly_sweep.md`, Doc → `#sodclaw`) **stays as-is.** This spec changes the *approval* surface, not the *reporting* surface. The factual "what moved" summary still posts to Slack; only the things that need Kevin's ratification move to the in-app gate.

---

## The goal, stated as a condition

> Kevin opens the weekend already knowing what moved and what needs a decision, without having prompted anything — and he trusts it because a second agent checked the report was true, the run stayed in budget, and nothing irreversible happened unattended.

The three features below are exactly the three sub-conditions that have to hold for that sentence to be safe.

---

## Feature 1 — The verifier subagent (the checker)

**Its goal, as a condition:** *the sweep report is true.* Met when every folder that changed is reflected, no movement is invented, and every progress/stale number traces to a real diff.

**How it runs:** after the maker (the existing Haiku crawl + Opus reconciliation) produces the draft report and its proposed `portfolio.json` changes, a **separate** Haiku subagent reads the draft *against the actual git/filesystem diff* and grades it. The maker and checker are different agent invocations on purpose — a thing should not grade its own work.

**Grading criteria (the checker's pass/fail checklist):**

| Check | Pass condition |
|---|---|
| Completeness | Every folder with a real change since `_meta.last_swept` appears in the report. |
| No hallucinated movement | Nothing is reported as moved that has no corresponding diff. |
| Number provenance | Every changed progress %, `last_touched`, and stale flag traces to an observable change. |
| Stale-rule correctness | 60-day proposals fire only on folders genuinely untouched 60+ days (not folders with uncommitted work). |
| Gate-safety | No proposed change edits an approval rule or the gate itself (see Feature 3). |

**On fail:** the verifier returns the specific failed check(s). The maker gets one corrective re-run. If it fails twice, the loop **stops and flags Kevin** rather than posting a report it couldn't verify — same "stop and flag rather than guess" principle as the base sweep.

---

## Feature 2 — The budget guard

**Its goal, as a condition:** *the loop never costs more than the work is worth.* Met when the run stays under its token ceiling and Opus was spent only on flagged judgment calls, not routine crawling.

**Tiering (cheap for triage, expensive for second opinions):**

| Stage | Model | Why |
|---|---|---|
| Folder crawl | Haiku | Mechanical, read-only. Already Haiku in the base sweep. |
| Verification | Haiku | Checking a diff against a report is mechanical. |
| Reconciliation + summary | Opus | Judgment: what to propose, how to phrase it for Kevin. |
| Escalated judgment calls | Opus | Only when the verifier flags something real (a proposed shelf, a new untracked project, a re-score). |

**The ceiling:** a per-run token cap. Weekly cadence makes the absolute cost trivial — the point of the cap on *this* loop isn't to save money, it's to **build the tiering muscle** for the loops where it matters (a content loop firing more often, or sessions running in parallel). If a run would blow the cap, it stops and reports the partial result rather than silently spending. The cap and tier assignments are the reusable artifact this loop produces.

---

## Feature 3 — The in-app approval gate

**Its goal, as a condition:** *nothing that changes ratifiable state ships without Kevin.* Met when the report posts freely but every proposed shelf, re-score, or new-project onboard is held until Kevin replies yes.

**Where the gate lives:** the **Weekly portfolio sweep scheduled-task thread in the Claude app** — not Slack. Kevin checks the Claude apps frequently and avoids Slack on his phone, so the approval surface follows where he already is. The verifier-checked report *and* its held state-changes both land in that thread; Kevin ratifies by replying in-app.

**What posts freely vs. what's held:**

| Sweep output | Treatment |
|---|---|
| "What moved this week" factual summary | Posts freely — Slack (Doc) **and** the in-app thread. Read-only, reversible, no ratification needed. |
| `last_touched`, `_meta.last_swept`, file-existence updates | Written automatically. Factual. |
| Proposed shelf (60-day rule) | **Held.** Tap yes in-app. |
| Proposed re-score (value/complexity) | **Held.** Tap yes in-app. |
| New untracked project onboard | **Held.** Tap yes in-app. |

**The honest tradeoff, named for later:** Slack is *push*; the in-app thread is *pull* (it waits for Kevin to check). For this sweep that's fine — nothing it holds is time-sensitive; a proposed shelf can sit three days at zero cost. **Flag for the content loops:** a "publish?" approval that sits unseen for a week means a post doesn't ship. Those may eventually want a real push notification — but that's a future-loop problem, not a reason to wire Slack approval into the sweep today.

**Constitutional boundary:** the gate rules themselves are not editable by the loop. The loop can propose changing *what* it flags; it can never propose removing the requirement that Kevin approves. The verifier's gate-safety check (Feature 1) enforces this before anything reaches Kevin.

---

## One loop iteration, end to end

1. **Scheduler fires** (Friday 6pm Pacific, existing schedule).
2. **Maker reads state** — Haiku crawls folders, Opus reconciles against `portfolio.json`, drafts the report + proposed changes.
3. **Checker grades** — separate Haiku verifies the draft against the real diff. On double-fail → stop + flag Kevin.
4. **Budget guard** — run stays under the token cap; Opus touched only judgment calls. Over cap → stop + report partial.
5. **Report posts freely** — Doc → Slack, and into the in-app sweep thread.
6. **Held changes wait** — shelves / re-scores / onboards posted as in-app proposals; Kevin taps yes to apply.
7. **State updates** — ratified changes written to `portfolio.json`; `_meta.last_swept` advanced so the next run resumes cleanly.

Step 3 is the difference between a loop and the cron job this is today.

---

## How this templates onto the content agents

Get steps 2–6 working here and the skeleton ports directly:

- The **verifier** becomes a voice-and-facts grader instead of a diff-checker.
- The **gate** guards `publish` instead of `shelve`.
- The **budget guard** matters more (higher cadence) — the tier assignments carry over.
- The **outcome log** from [`self_improvement_strategy.md`](self_improvement_strategy.md) rides on the ratify/reject signal this gate generates.

Prove it on the sweep (worst case: a revertible tracker edit). Aim it at the blog (where the stakes — and the payoff — are real).

---

## Build order

1. **Verifier subagent** — the single highest-value add. A Haiku checker with the Feature-1 checklist, run after the existing maker.
2. **In-app gate** — route held changes into the scheduled-task thread; define the post-freely vs. held split.
3. **Budget guard** — assign tiers, set the per-run cap, wire the stop-on-over-cap behavior.
4. **Then** the outcome log rides on top (start of the self-improvement strategy).
