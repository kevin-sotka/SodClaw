---
name: sweep-budget
description: The budget guard for the portfolio-sweep loop. Single source of truth for which model tier runs each stage (Haiku for mechanical crawl/verify/gate work, Opus only for judgment) and the per-run token cap. Before each stage the loop checks the projected total against the cap and STOPS with a partial result rather than silently overspending. Use as the loop's accounting layer; read budget.json for the config and call budget.py to gate stages. The cap barely bites on a weekly sweep — this exists to build the tiering muscle for higher-cadence loops.
---

# Sweep Budget Guard

## Why this exists

Every loop iteration is a full prompt execution, so cost compounds — a loop firing often, or many in parallel, can run up a bill fast. The guard does two things: **tiers** the work (cheap models for triage and checking, the expensive model only where a second opinion is worth paying for) and **caps** the run (a ceiling that stops a runaway before it spends, not after).

On the weekly sweep the absolute cost is trivial — the cap almost never bites. That's the point of building it *here*: prove the tiering and the stop-decision on the safe, cheap loop, then template the same config onto the content loops (a blog pipeline firing more often, sessions running in parallel) where the cap matters for real.

## Single source of truth

`budget.json` (this folder) holds the config: each stage's tier and token estimate, and the per-run cap. The loop reads it; `budget.py` enforces it. Don't scatter tier choices back into prose across the skills — when a tier changes, change `budget.json`.

| Stage | Tier | Why |
|---|---|---|
| crawl | Haiku | read-only folder + git crawl, mechanical |
| reconcile | **Opus** | judgment: what moved, what to propose, how to phrase |
| verify | Haiku | re-derive truth, grade the draft against it |
| gate | Haiku | parse Kevin's reply, apply approved proposals |
| escalated_call | **Opus** | *only* when the verifier flags a real judgment call |

The shape to remember: **Opus drafts and phrases; Haiku checks and clerks.** A healthy run is mostly Haiku tokens with Opus the minority.

## The cap and the stop-decision

`per_run_tokens` is the ceiling. Before each stage the loop calls `BudgetRun.check(stage)`:

- **Projected total ≤ cap** → proceed; after the stage, `charge(stage, actual_tokens)` records what it really cost.
- **Projected total > cap** → **stop before that stage runs.** Return the partial result with the budget decision, rather than spending into the overage. The check happens *before* the expensive stage, so a runaway crawl can't drag Opus down with it.

Tripping the cap on a sweep means something is wrong — a crawl that escaped its exclusions and ate `node_modules`, say — not a bigger-than-usual week. Treat a cap-stop as a signal to investigate, the same way a double verifier-fail is.

## How it sits in the loop

The guard wraps the whole sweep as its accounting layer:

```
run = BudgetRun()
for stage in [crawl, reconcile, verify, gate]:
    ok, decision = run.check(stage)        # gate BEFORE spending
    if not ok: return partial(decision)    # stop, report what we have
    result = run_stage(stage)              # at model_for(stage)
    run.charge(stage, result.tokens)       # record actual
report(run.summary())                      # total, opus share, under_cap
```

`model_for(stage)` / `tier_for(stage)` give the loop the right model to spawn each stage on, straight from the config — so the tiering isn't a guideline the orchestrator might forget, it's a lookup.

## Tier

The guard itself is pure accounting — no model, no API calls. It just decides and records. Effectively free.
