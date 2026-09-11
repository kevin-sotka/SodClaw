---
name: portfolio-sweep
description: Runs the SodClaw weekly portfolio sweep — crawls every Meatbag Labs project folder, detects what actually moved since the last sweep, refreshes each project's activity/last-touched data, applies Kevin's 60-day stale rule (proposing shelves, never auto-shelving), spots untracked new folders, re-syncs the tracker + dashboard, and reports "what moved this week." Use this skill whenever Kevin says "run the sweep", "portfolio sweep", "what moved this week", "what's changed across my projects", "refresh the tracker/dashboard", "is anything stale", or wants the whole portfolio re-checked and the command center brought up to date. Also the skill the scheduled Friday-evening sweep runs. Keeps the command center honest so every other SodClaw decision rests on fresh data.
---

# Weekly Portfolio Sweep

## Why this exists

A portfolio tracker is only as useful as it is fresh. Kevin runs ~15 projects on nights-and-weekends time; without a steady heartbeat, the dashboard drifts — progress goes stale, finished work goes unrecorded, dead projects linger, and new folders never get tracked. This sweep is that heartbeat. It does the boring crawl-and-reconcile work cheaply (delegated to a light model), then hands Kevin a short, honest "here's what moved" so his week opens with a true picture instead of a guess.

It is **draft-and-approve by design**: the sweep updates *factual* things on its own (when a project was last touched, whether a folder exists, file counts) but it never changes subjective things — scores, progress %, or a project's life status — without surfacing them to Kevin first. SodClaw proposes; Kevin ratifies. That keeps the tracker trustworthy and protects against an automated process quietly mangling the data.

## The source of truth

`SodClaw/projects/portfolio.json` is canonical. `SodClaw/dashboard.html` (the "sodclaw-portfolio-command-center" artifact) and `SodClaw/projects/registry.md` are mirrors. Any change goes into `portfolio.json` first (via a small load→modify→dump script so the JSON stays valid), then gets mirrored.

## Step 1 — Snapshot

Read `portfolio.json`. Note `_meta.last_updated` (or `_meta.last_swept` if present) — that's the "since" date for detecting movement. Hold the current project list in mind.

Also open the budget guard: read `SodClaw/skills/sweep-budget/budget.json` and start a `BudgetRun` (`sweep-budget/budget.py`). It's the loop's accounting layer — it tells you which model tier to run each stage on (`model_for(stage)`) and caps the run. Before each stage below, `run.check(stage)`; if it returns stop, return the partial result rather than spending past the cap. This is the budget-guard piece of the loop.

## Step 2 — Delegate the crawl to a Haiku subagent (read-only)

The crawl is mechanical, so keep it cheap — spawn one read-only `Explore` subagent on the **Haiku** model (this is the `crawl` stage in `budget.json` — `model_for("crawl")`). Give it this, filled in:

```
Crawl the Meatbag Labs workspace and report project activity. Read-only; change nothing.

Workspace root (bash sandbox path): /sessions/<session>/mnt/Meatbag_Labs/
(If that path 404s, discover the correct mount with: ls /sessions/*/mnt/ )

For EACH of these tracked project folders, report: (a) the most recent modification time of any file inside it, EXCLUDING .DS_Store, node_modules/, .git/, .next/, build/, dist/, and *.tmp; (b) the relative path of that most-recent file; (c) total tracked file count (same exclusions); (d) its GIT STATE (see below).
Tracked folders: <list each project's folder basename from portfolio.json>

GIT STATE — also check the SodClaw/ folder itself (the orchestrator) in addition to the tracked folders. **A project's `.git` is not always at the top of its tracked folder** (e.g. a project whose site lives in a `site/` subfolder) — before calling something `not_a_repo`, check the tracked folder itself AND one level of its immediate subfolders for a `.git` directory (`find "<folder>" -maxdepth 2 -name .git -type d`). If a `.git` turns up in a subfolder, run all the git checks below against THAT path and note the subfolder in `git_detail` (e.g. "repo is in site/, not project root"). For each folder, run read-only git checks and classify into exactly one state:
  - `not_a_repo`      — no `.git/` directory inside the folder or its immediate subfolders
  - `local_only`      — a repo, but `git remote get-url origin` is empty (no remote)
  - `partially_synced`— a repo WITH a remote, but it has uncommitted changes (`git status --porcelain` non-empty) and/or unpushed commits (`git rev-list --count @{u}..HEAD` > 0)
  - `synced`          — a repo with a remote, clean working tree, nothing unpushed
For repos, also capture: remote URL, branch (`git rev-parse --abbrev-ref HEAD`), uncommitted-file count, unpushed-commit count, and last commit date (`git log -1 --format=%cd --date=short`). Use `git -C "<folder>" ...` so you never change directories. These are all read-only — make NO commits, pushes, or remote calls beyond reading local state.

Then list every top-level folder directly under the workspace root that is NOT in the tracked list above and is NOT one of: SodClaw, .tmp.drivedownload, .tmp.driveupload, or anything listed in `portfolio.json`'s `_meta.ignored_folders` (folders Kevin has already said to leave alone, e.g. `kevin-sotka.github.io` — GitHub Pages root infra, not a project) — these are candidate UNTRACKED projects. For each, give its name, last-modified time, and file count.

**Do not propose onboarding individual games under `hitfactory.games/Foundry/games/*` (or any other Foundry-pipeline output) as their own `portfolio.json` rows.** `hitfactory.games/games.json` is the single source of truth for individual games — it already tracks each one's pipeline stage (draft/designed/polished/iterated/shipped). `portfolio.json` tracks only the studio umbrella (`hitfactory_games`) and giga-foundry gauntlet outputs (e.g. `aphelion`). Decided 2026-09-11 after almost re-litigating this exact "two sources of truth" drift risk.

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

> **Do not apply these writes yet.** As of the loop edition, Step 4 only *prepares* the safe writes and the held proposals — nothing is written to `portfolio.json` until the verifier (Step 4.5) returns PASS. Hold the prepared changes; don't dump them to disk.

## Step 4.5 — Verify before applying (the checker)

This is the gate that turns the sweep from a cron job into a loop. Before any write or report, the draft gets graded by a **separate** agent — a thing never grades its own work.

Invoke the **`sweep-verifier`** skill (`SodClaw/skills/sweep-verifier/`) on the **Haiku** tier, read-only. Hand it: the draft report (Step 6 content), the prepared safe-writes and held proposals (Step 4), and the pre-sweep `_meta.last_swept` date. It re-derives ground truth independently from disk/git and grades five checks — completeness, no hallucinated movement, number provenance, stale-rule correctness, and the constitutional gate-safety check. Its deterministic spine is `sweep-verifier/verify.py`; the test harness `test_verify.py` shows the expected behavior.

Act on the verdict:

- **PASS** → proceed to Step 4-apply (write the safe changes), then Steps 5 and 6.
- **FAIL on checks 1–4** → go back to Step 3, redraft fixing exactly the cited failures, and re-verify. Allow **one** corrective re-run.
- **FAIL a second time** → **stop. Do not write, do not post.** Surface the verifier's verdict to Kevin and let him sort it out. Never ship a report you couldn't verify.
- **FAIL on check 5 (gate-safety)** → **stop immediately, no re-run.** A prepared change tried to auto-write something only Kevin may ratify (a status→shelved, a score, a progress bump) or tried to touch the gate. That's a design fault, not a redraftable mistake. Flag Kevin with the specific violation.

Only after a PASS does the sweep actually write to `portfolio.json` (the "Step 4-apply" the note above deferred) and continue.

## Step 5 — Sync the mirrors

The dashboard is **generated**, not hand-edited. After writing `portfolio.json`, regenerate it by running `python3 SodClaw/build_dashboard.py` — that rebuilds `dashboard.html` from the JSON (including Doc's portrait and `_meta.doc_briefing`). Then reconcile `registry.md`, and re-publish the artifact with `update_artifact` (id `sodclaw-portfolio-command-center`), with an `update_summary` naming what moved.

Optional but nice: refresh `_meta.doc_briefing` in Doc's voice (no-nonsense wild-west trail guide — "Listen here, Partner...") to reflect what moved this week before regenerating, so the dashboard's top briefing stays current.

## Step 6 — Report "what moved this week"

Deliver a short, warm summary (this is the part Kevin actually reads). **Before the structure below, if `projects/portfolio_proposals.json` has any `status: pending` entries, lead with one line: "N proposals waiting on you, oldest is X days old" — regardless of how quiet the week was otherwise.** A pending-proposal queue that only gets a "gentle nudge" buried in a re-list is easy to miss for weeks; this line is not optional and does not wait for the queue to get large. Structure:

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

The factual summary above **posts freely** — it never waits on the gate. Only the *held proposals* (shelve / re-score / progress / onboard) route through Step 6.5.

## Step 6.5 — The in-app gate (surface held proposals; apply Kevin's reply)

The held proposals are the things Step 4 deliberately did NOT auto-write. They don't get applied unattended — Kevin ratifies them in-app, and his reply is what turns a proposal into a write. Invoke the **`sweep-gate`** skill (`SodClaw/skills/sweep-gate/`, Haiku tier); mechanics are in `gate.py`.

**This run — surface:**
- `add_proposals(...)` the held items to the ledger `projects/portfolio_proposals.json` (`status: pending`, today as `raised`).
- Post `render_for_thread(...)` — a numbered list — into the sweep thread, with the hint *"reply e.g. 'yes 1 and 3, no 2'."*

**Next run (or whenever Kevin's reply is seen) — ratify:**
- `parse_reply(reply, pending_ids)` → approved/rejected per id. **Anything Kevin didn't mention stays pending and carries forward — silence is never a yes.**
- `record_decisions(...)`, then `apply_approved(ledger, portfolio, today)` — writes **only** approved proposals to `portfolio.json`.
- Confirm in-thread exactly what was applied; `prune_resolved(...)` clears applied + rejected; pending entries remain (re-listed next run, tagged with their age as a gentle nudge).

**Constitutional boundary (enforced in `gate.py`):** a proposal applies iff explicitly approved; `apply_approved` only touches the fields its kind allows and **refuses** any proposal naming `autonomy`, `gate`, or `approval_rule`. A refusal stops the run and flags Kevin — same severity as the verifier's gate-safety fail. The gate can change what the tracker says; it can never change how approval works.

This is the v1 escalation surface: **in-app reply, no Slack.** The factual report still goes to Slack via Doc (`routine_weekly_sweep.md`); only ratification lives in the thread, because Kevin checks the Claude apps and avoids Slack on his phone.

## Notes

- This runs both on demand (Kevin invokes it) and as a scheduled Friday-evening task (6pm Pacific) so Kevin starts the weekend with a true picture. On the scheduled/unattended run, still make only the safe writes from Step 4 and leave the judgment calls in the report for when Kevin reads it — never shelve or re-score unattended.
- **The verify gate (Step 4.5) is mandatory on every run, attended or not.** On an unattended run there's no one to read a corrective prompt mid-flight, so the contract is the same: PASS writes + posts; a persistent FAIL (or any gate-safety FAIL) means the run writes nothing and leaves the verifier's verdict for Kevin instead of a sweep summary. A skipped verification is a silent regression to a cron job — don't skip it.
- Keep the crawl AND the verification on the light model. The orchestration, reconciliation, and report are the Opus layer's job; the maker drafts and the cheap checker grades — that's the budget-guard principle in miniature. Tiers and the per-run cap live in `skills/sweep-budget/budget.json`; don't hard-code model choices in prose — read them from there so a tier change is one edit.
