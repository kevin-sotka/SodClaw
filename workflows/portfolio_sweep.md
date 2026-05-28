# Workflow: Weekly Portfolio Sweep

> The heartbeat that keeps the command center honest. Crawls every project folder, detects what moved, refreshes activity data, records each project's git state (so the dashboard's "Git readiness" section stays current), applies the 60-day stale rule (proposing shelves, never auto-shelving), spots untracked folders, re-syncs the tracker + dashboard, and reports "what moved this week."

Packaged as an installable skill: `SodClaw/skills/portfolio-sweep/` (and `portfolio-sweep.skill`). Once installed it runs as the `/portfolio-sweep` slash command.

## How it runs
- **On demand:** Kevin says "run the sweep" / "what moved this week" / invokes `/portfolio-sweep`.
- **Scheduled:** auto-runs **Fridays at 6pm Pacific** (scheduled task `weekly-portfolio-sweep`, cron `0 18 * * 5`) — Kevin opens the weekend already knowing what to work on. Fires while the Claude app is open; if closed, runs at next launch. Once the Anthropic Routine equivalent is live, that becomes the always-on path and this Cowork task can be retired.

## Design principle: draft-and-approve
The sweep writes only *factual* updates automatically — `last_touched` dates, `_meta.last_swept`, file existence. It never auto-changes scores, progress, or a project's life status. Stale projects, suggested progress bumps, and new untracked folders are surfaced as **proposals** in the summary for Kevin to ratify. SodClaw proposes; Kevin decides.

## The two-tier model in action
The folder crawl is delegated to a **Haiku** read-only subagent (cheap, mechanical). The reconciliation, safe writes, mirror-sync, and the human-facing summary are the **Opus** orchestrator's job. This is the template for future SodClaw subagent skills.

Full instructions: `SodClaw/skills/portfolio-sweep/SKILL.md`.
