# Routine: Weekly SodClaw Sweep (cloud, always-on)

> The cloud-resident twin of the local `portfolio-sweep` skill. Runs on Anthropic-managed infrastructure as a Claude Code Routine, fires on a schedule whether Kevin's Mac is open or shut, posts a Doc-voiced summary to `#sodclaw` in Slack, and proposes any tracker updates as a `claude/sweep-...` branch for Kevin to review on his phone.

This is the piece that makes the "agents kept working while my laptop was closed" claim honest.

## What's different from the local sweep

The local `portfolio-sweep` skill (still useful, still runnable on demand) crawls Kevin's whole `Meatbag_Labs/` folder on his Mac. It sees all 16 projects, including the 11 that aren't in Git.

The cloud Routine can only see what's in Git — currently five `kevin-sotka` repos: SodClaw, train_lore, thegridirongazette, Riventide, AI-company-trail. So its sweep is structurally narrower. It tells the truth about what it can see and is explicit about what it can't. The implicit nudge: the more projects in Git, the fuller the Friday report.

Division of labor:
- **Cloud Routine (this file):** Friday 6pm Pacific, always-on, git-and-portfolio-truth report.
- **Local sweep (`workflows/portfolio_sweep.md`):** on-demand from Kevin's Mac, fills in filesystem activity for the non-git projects, deeper crawl when Kevin wants it.

When the Routine has run cleanly for a couple of weeks, the local Cowork `weekly-portfolio-sweep` scheduled task can be disabled — the Routine replaces it for the recurring case. The local sweep skill stays available for on-demand runs.

## Configuration

| Field | Value |
|---|---|
| Name | `sodclaw-friday-sweep` |
| Description | Weekly portfolio sweep — Friday 6pm Pacific, posts as Doc to #sodclaw |
| Schedule | Weekly, **Friday 18:00 America/Los_Angeles** |
| Repositories | `kevin-sotka/SodClaw` (primary), plus `kevin-sotka/train_lore`, `kevin-sotka/thegridirongazette`, `kevin-sotka/Riventide`, `kevin-sotka/AI-company-trail` for git-state checks |
| Branch policy | Default — push only to `claude/sweep-YYYY-MM-DD` branches (Routines enforces this) |
| Secrets | `SODCLAW_DOC_WEBHOOK_URL` — the Doc incoming-webhook URL for `#sodclaw` |
| Connectors | None required for the post (we post via webhook + curl, not the Slack connector, so Doc's identity stays intact) |
| Run cap impact | 1 run / week against Kevin's Pro budget of 5 runs / day. Negligible. |

## The prompt

Paste the contents of [`prompts/routine_weekly_sweep_prompt.md`](../prompts/routine_weekly_sweep_prompt.md) as the Routine's prompt verbatim. It's maintained as a separate file so it can be edited in Git without re-saving the Routine config every time.

## Setup steps (one-time, in the Routines UI / CLI)

1. Open Claude Code Routines and create a new routine named `sodclaw-friday-sweep`.
2. Add the five repositories above. `kevin-sotka/SodClaw` is the primary; the others are read-only context.
3. Schedule: **Weekly, Friday 18:00, America/Los_Angeles**.
4. Add a secret named `SODCLAW_DOC_WEBHOOK_URL` and paste the webhook URL from the Slack app's Incoming Webhooks page (the one starting `https://hooks.slack.com/services/T...`). Don't put this URL anywhere in the repo.
5. Paste the prompt from `prompts/routine_weekly_sweep_prompt.md`.
6. Save and enable. The first run will fire next Friday at 6pm Pacific — or trigger one manually now to confirm Doc speaks correctly end-to-end before Friday.

## What to watch for

- **First-run sanity:** The first Friday post should look like a normal sweep summary in Doc's voice. If it looks off, check the branch the Routine pushed — that's the receipt for what it actually wrote.
- **Double sweeps:** Once the Routine has run cleanly twice, disable the local Cowork `weekly-portfolio-sweep` task so Kevin doesn't get two pings.
- **Webhook leak:** If the webhook URL is ever pasted into a commit, into the Routine prompt body, or anywhere else that lands in the repo, rotate it from the Slack app's Incoming Webhooks page immediately and update the Routine secret.
- **Cap math:** Pro tier is 5 runs/day. Friday weekly = 1. Even with occasional manual API triggers, well under cap.
