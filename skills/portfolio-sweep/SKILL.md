---
name: portfolio-sweep
description: Runs the SodClaw weekly portfolio sweep — crawls every Meatbag Labs project folder, detects what actually moved since the last sweep, refreshes each project's activity/last-touched data, applies Kevin's 60-day stale rule (proposing shelves, never auto-shelving), spots untracked new folders, re-syncs the tracker + dashboard, and reports "what moved this week." Use this skill whenever Kevin says "run the sweep", "portfolio sweep", "what moved this week", "what's changed across my projects", "refresh the tracker/dashboard", "is anything stale", or wants the whole portfolio re-checked and the command center brought up to date. Also the skill the scheduled Sunday-evening sweep runs. Keeps the command center honest so every other SodClaw decision rests on fresh data.
---

# Weekly Portfolio Sweep

## Why this exists

A portfolio tracker is only as useful as it is fresh. Kevin runs ~15 projects on nights-and-weekends time; without a steady heartbeat, the dashboard drifts — progress goes stale, finished work goes unrecorded, dead projects linger, and new folders never get tracked. This sweep is that heartbeat. It does the boring crawl-and-reconcile work cheaply (delegated to a light model), then hands Kevin a short, honest "here's what moved" so his week opens with a true picture instead of a guess.

It is **draft-and-approve by design**: the sweep updates *factual* things on its own (when a project was last touched, whether a folder exists, file counts) but it never changes subjective things — scores, progress %, or a project's life status — without surfacing them to Kevin first. SodClaw proposes; Kevin ratifies. That keeps the tracker trustworthy and protects against an automated process quietly mangling the data.

## The source of truth

`SodClaw/projects/portfolio.json` is canonical. `SodClaw/dashboard.html` (the "sodclaw-portfolio-command-center" artifact) and `SodClaw/projects/registry.md` are mirrors. Any change goes into `portfolio.json` first (via a small load→modify→dump script so the JSON stays valid), then gets mirrored.

## Step 1 — Snapshot

Read `portfolio.json`. Note `_meta.last_updated` (or `_meta.last_swept` if present) — that's the "since" date for detecting movement. Hold the current project list in mind.

## Step 2 — Delegate the crawl to a Haiku subagent (read-only)

The crawl is mechanical, so keep it cheap — spawn one read-only `Explore` subagent on the **Haiku** model. Give it this, filled in:

```
Crawl the Meatbag Labs workspace and report project activity. Read-only; change nothing.

Workspace root (bash sandbox path): /sessions/<session>/mnt/Meatbag_Labs/
(If that path 404s, discover the correct mount with: ls /sessions/*/mnt/ )

For EACH of these tracked project folders, report: (a) the most recent modification time of any file inside it, EXCLUDING .DS_Store, node_modules/, .git/, .next/, build/, dist/, and *.tmp; (b) the relative path of that most-recent file; (c) total tracked file count (same exclusions); (d) its GIT STATE (see below).
Tracked folders: <list each project's folder basename from portfolio.json>

GIT STATE — also check the SodClaw/ folder itself (the orchestrator) in addition to the tracked folders. For each folder, run read-only git checks and classify into exactly one state:
  - `not_a_repo`      — no `.git/` directory inside the folder
  - `local_only`      — a repo, but `git remote get-url origin` is empty (no remote)
  - `partially_synced`— a repo WITH a remote, but it has uncommitted changes (`git status --porcelain` non-empty) and/or unpushed commits (`git rev-list --count @{u}..HEAD` > 0)
  - `synced`          — a repo with a remote, clean working tree, nothing unpushed
For repos, also capture: remote URL, branch (`git rev-parse --abbrev-ref HEAD`), uncommitted-file count, unpushed-commit count, and last commit date (`git log -1 --format=%cd --date=short`). Use `git -C "<folder>" ...` so you never change directories. These are all read-only — make NO commits, pushes, or remote calls beyond reading local state.

Then list every top-level folder directly under the workspace root that is NOT in the tracked list above and is NOT one of: SodClaw, .tmp.drivedownload, .tmp.driveupload — these are candidate UNTRACKED projects. For each, give its name, last-modified time, and file count.

Report as a compact table: folder | last_modified (YYYY-MM-DD) | most_recent_file | file_count | git_state | git_detail (remote / branch / uncommitted / unpushed / last_commit), followed by an "UNTRACKED FOLDERS" section and a one-line SodClaw git_state. Under 400 words. Use one efficient `find ... -printf` per folder for the timestamp, and one `git -C ...` block per folder for the git state.
```

If the project is huge (e.g. the_wall, AI-company-trail with node_modules), the exclusions keep it fast. Trust the subagent's timestamps but sanity-check anything surprising (e.g. a project that "moved" but whose only changed file is a lockfile).

## Step 3 — Reconcile (this is the judgment layer)

Today's date comes from the environment. For each tracked project compute **days-since-touch** from the crawl's last_modified.

Apply these rules:

- **Moved since last sweep** (last_modified newer than `_meta.last_swept`): mark it as moved this week. Record the new `last_touched` date. Do NOT auto-change `progress` — instead, if it clearly advanced (e.g. Riventide assets appeared, a new chapter file exists), note it as a *suggested* progress update for Kevin to confirm.
- **Stale ≥ 60 days** AND status is `active` or `exploratory` (skip anything already `shelved`/`shipped`/`paused`): add it to a **shelve-candidates** list to propose. Never flip status to shelved automatically — that's Kevin's call (his rule: "shelved ≠ dead, it means not now").
- **Untracked folder found**: propose adding it to the Exploratory tier as a stub (status `unknown`, scores blank pending Kevin). Don't fabricate scores.
- **Reminder/decision came due**: if a project's `decision` references a date that has passed, flag it as due.
- **Git readiness** (mobile reach): the priority projects that need to be reachable from mobile are **`train_lore`, `the_wall`, `gridiron_gazette`**, plus **SodClaw itself** (the orchestrator entry point — without it in Git, nothing is reachable). Flag for the report: any priority project (or SodClaw) whose `git_state` is `not_a_repo` or `local_only` → "not yet portable"; any repo whose `git_state` is `partially_synced` → "in Git but drifted (N uncommitted / M unpushed)". This is a surfaced proposal, not an action — the sweep never creates repos, adds remotes, commits, or pushes on its own.

## Step 4 — Apply the safe updates

Edit `portfolio.json` with a script. Safe to write automatically:

- Set/refresh each project's `last_touched` (add the field if missing).
- Set `_meta.last_swept` to today and bump `_meta.last_updated`.
- Write each project's `git_state` object from the crawl (keys: `repo`, `state`, `remote`, `uncommitted`, `unpushed`, `branch`, `last_commit`, `checked`=today), and write `_meta.sodclaw_git_state` for the orchestrator + `_meta.git_inventory_run`=today. This is purely factual observation, so it's a safe auto-write — the dashboard's "Git readiness" section reads these fields directly.
- For untracked folders Kevin approves (or, on an unattended run, add them as `status: "unknown"` stubs so nothing is lost — flagged in the report for review).

Do NOT auto-write: score changes, progress changes, or status→shelved. And never *change* git itself (no init/remote/commit/push) — the sweep only records git state, it doesn't migrate anything. Those go in the report as proposals.

## Step 5 — Sync the mirrors

The dashboard is **generated**, not hand-edited. After writing `portfolio.json`, regenerate it by running `python3 SodClaw/build_dashboard.py` — that rebuilds `dashboard.html` from the JSON (including Doc's portrait and `_meta.doc_briefing`). Then reconcile `registry.md`, and re-publish the artifact with `update_artifact` (id `sodclaw-portfolio-command-center`), with an `update_summary` naming what moved.

Optional but nice: refresh `_meta.doc_briefing` in Doc's voice (no-nonsense wild-west trail guide — "Listen here, Partner...") to reflect what moved this week before regenerating, so the dashboard's top briefing stays current.

## Step 6 — Report "what moved this week"

Deliver a short, warm summary (this is the part Kevin actually reads). Structure:

```
## Portfolio sweep — <date>

Moved this week: <project — what changed>, ...   (or "quiet week")
Needs your attention: <current flagged decisions + anything ≥80%>
Git readiness: <priority projects / SodClaw not yet portable; repos that have drifted>   (only if any; ask whether to set up Git)
Stale (60+ days) — shelve candidates: <project — days idle>   (only if any; ask push/shelve)
New untracked folders: <name>   (only if any; ask add/ignore)
Suggested progress updates: <project: X% → Y%?>   (only if any; ask to confirm)
```

Lead with movement and attention items. Keep proposals as questions — Kevin decides. If it was a quiet week with nothing flagged, say so in a sentence and stop; don't manufacture work.

## Notes

- This runs both on demand (Kevin invokes it) and as a scheduled Sunday-evening task. On the scheduled/unattended run, still make only the safe writes from Step 4 and leave the judgment calls in the report for when Kevin reads it — never shelve or re-score unattended.
- Keep the crawl on the light model. The orchestration, reconciliation, and report are the Opus layer's job.
