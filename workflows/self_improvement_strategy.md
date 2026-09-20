# SodClaw Self-Improvement Strategy — Gated Proposals

> How SodClaw's agents get better over time without Kevin losing the thread. The agents propose improvements to their own instructions; Kevin ratifies through the gate he already uses. The orchestrator improves; Kevin stays the editor of record. This is the safe rung on the self-improvement ladder — deliberately not the autonomous one.

**Last updated:** 2026-06-28
**Status:** strategy / not yet built. Substrate (outcome logging) is the first build.

---

## The goal, stated as a condition

> Each SodClaw agent gets measurably better at matching Kevin's judgment over time — because it learns from where it diverged from him — and Kevin trusts every change because he ratified it, traced to real evidence, before it took effect. No agent ever edits its own instructions unattended, and no agent can edit the gate that requires Kevin's approval.

Everything below is the machinery that has to hold for that sentence to be true and safe. The features are not the point; that sentence is.

---

## Why gated proposals, and not the other rungs

Self-improvement splits into four strategies by **what gets improved** and **who ratifies the change**. SodClaw is building rung 2 on purpose.

1. **Outcome logging** — the substrate. Not improvement itself; the record improvement runs on. Zero risk. Everything else needs it.
2. **Gated proposals** (← we are building this). The agent reads its own outcome log, proposes one specific edit to its prompt/skill/rubric, and Kevin ratifies through the existing in-app gate before it takes effect. Safe, compounds, fits draft-and-approve.
3. **Eval-driven** — same as 2, but a proposed change must beat a test set before it ships. Rigorous, more setup. The right *later* upgrade for the content agents. Uses `skill-creator`'s eval tooling.
4. **Autonomous self-modification** — the agent rewrites itself, changes take effect with no gate. The comprehension-debt nightmare pointed straight at Kevin's 16-project / 80% wiring. Mapped as a destination, **not** built.

The thread through all of them: *self-improvement is only as safe as the ability to measure whether a change was actually an improvement.* The measurement layer (rungs 1 and 3) is the real unlock. Rungs 2–4 are just increasingly autonomous ways of acting on a measurement. We build the measurement, then let agents propose against it through the gate that already exists.

---

## The substrate: outcome logs (build this first)

Gated proposals are the easy part — the agent suggests, Kevin taps yes. The hard, valuable part is underneath: a per-agent **outcome log** that makes "propose an improvement" non-fictional.

Every divergence between an agent's judgment and Kevin's becomes one logged data point:

- A **verifier** caught an error in the agent's output → log what it caught.
- Kevin **ratified or rejected** a held proposal → log which, and the context.
- A draft got **revised** before it shipped → log the delta (this is the richest signal for content agents).

Without this log, "propose an improvement" is the agent guessing. With it, the agent has evidence:

> *"In the last six sweeps, you rejected my stale-flag proposal four times when the folder had uncommitted work. I should stop flagging those."*

That is a real, defensible, ratifiable proposal. The log is the first build because it's what every other rung stands on.

**Format (per agent):** append-only JSONL, one record per divergence, lives beside the agent. Each record carries: `date`, `agent`, `type` (`verifier_catch` | `ratified` | `rejected` | `revised`), `context` (what the agent proposed/produced), `outcome` (what Kevin did), and `note` (the diff or reason, where available). Kept append-only so the improvement loop reads history, never rewrites it.

---

## The improvement loop: second-order maker-checker

The first-order loop checks **the work** — is the sweep report true. The self-improvement loop checks **the agent** — is the sweep skill itself getting better. It runs on a slower clock: not every run, but monthly, or triggered when an agent's outcome log accumulates *N* divergences.

One iteration:

1. The agent reads its own outcome log.
2. It identifies **one** pattern with enough evidence to act on.
3. It proposes **one specific edit** to its skill / rubric / prompt — written as a diff, with the log records that justify it cited inline.
4. The proposal goes through the **same in-app gate** Kevin uses for the sweep (the scheduled-task thread — no Slack). Kevin replies yes/no.
5. On yes, the edit takes effect and the proposal itself is logged (so the next loop knows what's already been tried).

Same escalation surface, same "tap yes," just guarding a skill-file edit instead of a shelf decision. **One gate, two kinds of thing flowing through it.**

---

## Per-project fit — where this earns its keep

| Agent | Prove the mechanism here? | Run it for value here? | Why |
|---|---|---|---|
| **Portfolio sweep** | ✅ safest place to prove it | ❌ low payoff | Its job barely changes run-to-run — little to improve. Perfect crash-test dummy, weak ongoing beneficiary. |
| **Railroad blog** | — | ✅ highest payoff | Voice + quality bar Kevin holds in his head. Every pre-ship revision is a divergence the agent can learn from. Drafts slowly need less fixing. |
| **Gridiron Gazette** | — | ✅ high payoff | Same as the blog — recurring content with a held standard. Strong second target. |
| **Novel / Ghostwriter** | — | ⏳ later | Voice-critical, but cadence is too irregular yet for a useful log. Revisit once output is steady. |

**Rollout:** prove the machinery on the **sweep** (cheap, safe, nothing irreversible), but *aim* it at the **content agents** — because there, Kevin's edits ARE the training signal, and the improvement compounds into drafts that need less of his hour.

---

## The guardrail that keeps this from becoming the thing Kevin fears

This is what keeps gated self-improvement from sliding into the autonomous version (rung 4) that was deferred:

1. **One proposal at a time.** No batch self-rewrites. One pattern, one edit, one decision.
2. **Every proposal traces to logged evidence.** No "this feels better." If the log doesn't justify it, it doesn't get proposed.
3. **Kevin ratifies before anything takes effect.** Same gate, every time. Default autonomy stays draft-and-approve.
4. **The agent may never edit the gate rules themselves.** It can propose changing *how it scores complexity*. It cannot propose *removing the requirement that Kevin approves*. The gate is constitutional; everything downstream of it is amendable. This single boundary is the difference between rung 2 and rung 4.

If a proposed change would alter the approval mechanism, the verifier rejects it before it ever reaches Kevin.

---

## What this is NOT

- **Not autonomous self-modification.** Agents propose; they do not self-apply. (That's rung 4 — deferred, not built.)
- **Not eval-gated yet.** v1 ratification is Kevin's judgment against logged evidence, not a test-set score. Evals (rung 3) are the *next* upgrade, earned once the content agents have a stable test set worth scoring against.
- **Not a framework.** This is portfolio-serving capability, not a generic self-improving-agent platform. (See ROADMAP Traps: "Generic agentic framework.") It exists to make Kevin's content agents need less of his hour — nothing more.
- **Not running everywhere at once.** Proven on the sweep, aimed at the blog. One agent earns the next agent's slot.

---

## Build order

1. **Outcome-log format + capture.** Wire the four divergence types into the sweep first (it already generates ratify/reject signal via its proposals). Start capturing immediately — the log is worthless without history, so the clock starts the day this lands.
2. **The improvement loop on the sweep.** Monthly read-log → propose-one-edit → in-app gate. Crash-test the mechanism where the worst case is a skill tweak Kevin can revert.
3. **Port to the railroad blog.** Same loop, richer signal (revisions, not just ratifications). This is where it starts paying for itself.
4. **Then earn rung 3.** Once the blog has a stable test set, upgrade its gate from "Kevin's judgment" to "must beat the test set, then Kevin's judgment."

---

## Source of truth & how this file moves

- This doc is the **narrative**. When the loop is built, structured config (log paths, trigger thresholds, per-agent enablement) lives alongside each agent's skill, mirrored into `portfolio.json` `_meta` where the dashboard needs to surface it.
- New rungs move down the build order only when *started*, never when "considered" — same rule as `ROADMAP.md`.
- The four guardrails are constitutional. Naming them is a vaccine; un-naming one is a regression. They do not get edited by the system they govern.
