---
name: sweep-gate
description: The in-app approval gate for the portfolio-sweep loop. After the verifier passes a sweep, this surfaces the HELD proposals (shelve, re-score, progress bump, onboard) as a numbered list in the Claude sweep thread and persists them to a pending ledger so nothing is lost between runs. Kevin ratifies by replying in plain language ("yes 1 and 3, no 2"); the gate applies ONLY explicitly-approved proposals to portfolio.json, drops the rejected, and carries the unanswered forward. Use right after sweep-verifier returns PASS, or when Kevin replies to a pending-proposals list. Reply-in-thread for ergonomics, ledger for durability. No Slack.
---

# Sweep Gate (in-app approval)

## Why this exists

The verifier guarantees the report is *true*. The gate guarantees that nothing **ratifiable** — a shelve, a re-score, a progress change, onboarding a new folder — gets written to the tracker without Kevin's explicit yes. The sweep can *propose* anything; only Kevin's reply turns a proposal into a write.

The approval surface is the **Claude sweep thread**, not Slack — Kevin lives in the Claude apps and avoids Slack on his phone. He ratifies by replying in plain language. That's *pull*, not push: the proposals wait for him. For the sweep that's fine (a shelve can sit unratified for days at zero cost); the content loops that template off this may later need a real push, but the sweep does not.

## The two halves: reply for ergonomics, ledger for durability

A chat reply is ephemeral — if proposals lived only in the thread, an unanswered one would vanish next run. So the gate keeps a durable **pending ledger**, `projects/portfolio_proposals.json`, and posts the same proposals as a numbered list in the thread. The reply is the interface; the ledger is the state that makes the reply applicable and keeps unanswered proposals alive.

Mechanics live in `gate.py` (this folder). The sweep calls into it; this skill describes when.

## The flow across two runs

**Run N — surface (after verifier PASS):**

1. Take the held proposals the verifier let through (the things Step 4 of the sweep deliberately did NOT auto-write).
2. `add_proposals(...)` them to the ledger with fresh ids, `status: "pending"`, and today as `raised`.
3. Post `render_for_thread(...)` — a numbered list — into the sweep thread, with the reply hint: *"reply e.g. 'yes 1 and 3, no 2'."*
4. Post the factual report freely (Doc → Slack and the thread). **The report never waits on the gate** — only the held changes do.

**Between runs — Kevin replies** in the thread: "yes 1, skip 2, yes 3" / "approve all" / "no to everything."

**Run N+1 (or whenever Kevin's reply is seen) — ratify:**

5. `parse_reply(reply, pending_ids)` → per-proposal approved/rejected. **Anything not mentioned stays pending and carries forward** — silence is never a yes.
6. `record_decisions(...)` writes those decisions into the ledger.
7. `apply_approved(ledger, portfolio, today)` applies **only** `approved` proposals to `portfolio.json`, returns the list of what it wrote.
8. Confirm in the thread exactly what was applied ("Shelved Oregon Fail; bumped train_lore to 45%. #2 left pending.").
9. `prune_resolved(...)` clears applied + rejected; pending entries remain for next time.
10. Re-sync mirrors (dashboard, registry) as the sweep's Step 5 already does.

## What posts freely vs. what's held

| Sweep output | Treatment |
|---|---|
| "What moved this week" factual summary | **Free** — Slack + thread. Reversible, no ratification. |
| `last_touched`, `_meta.last_swept`, `git_state` | **Auto** — factual safe writes (sweep Step 4). |
| Shelve a project (60-day rule) | **Held** — ledger + thread; needs a yes. |
| Re-score value/complexity | **Held** — needs a yes. |
| Progress bump | **Held** — needs a yes. |
| Onboard an untracked folder | **Held** — needs a yes (added as a stub on approval). |

## The constitutional boundary (enforced in code)

- A proposal applies **iff** explicitly approved. Silence ≠ yes; ambiguous ≠ yes.
- `apply_approved` only touches the fields its `kind` allows (`ALLOWED_CHANGE`) and **refuses** any proposal naming a forbidden field (`autonomy`, `gate`, `approval_rule`). The gate can change *what the tracker says*; it can never change *how approval works*. A refusal stops the run and flags Kevin — same severity as the verifier's gate-safety fail.
- The gate never invents a proposal. It only ever acts on what the verifier handed it and what Kevin's reply decided.

## Tier

The parse/apply is mechanical — **Haiku**. The only judgment is Kevin's reply. Cheap checker, cheap clerk; the Opus layer only drafts and phrases.

## Carry-forward & nudging

Proposals that go unanswered stay `pending` and reappear in the next run's list, tagged with their age ("raised 2026-06-12, 17d ago"). That aging tag is the gentle nudge — a 30-day-old shelve proposal Kevin keeps skipping is itself a signal worth a one-line "want me to just leave this one alone?" But the gate never auto-resolves it. Pending means pending until Kevin says otherwise.
