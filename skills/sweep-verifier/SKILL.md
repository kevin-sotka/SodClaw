---
name: sweep-verifier
description: The checker half of the portfolio-sweep loop. Grades a freshly-drafted sweep report (and its proposed portfolio.json changes) against the actual git/filesystem state, before anything is posted to Kevin or written to the tracker. Use this skill right after the portfolio-sweep maker produces a draft — invoked automatically by the loop, or on demand when Kevin says "verify the sweep", "check the sweep report", "did the sweep get it right". Runs read-only on the Haiku tier. Returns a per-check PASS/FAIL verdict; on FAIL the maker gets one corrective re-run, and on a second failure the loop stops and flags Kevin rather than posting an unverified report.
---

# Sweep Verifier

## Why this exists

A scheduled job that reads state and reports is a cron job. A loop is a cron job whose result gets **graded by a second agent before it's trusted**. This skill is that second agent for the portfolio sweep — the checker in a maker-checker pair.

The maker (`portfolio-sweep`) crawls the workspace, reconciles against `portfolio.json`, and drafts both a "what moved this week" report and a set of proposed tracker changes. This verifier does one job: **confirm that draft is true** before Kevin sees it or the tracker is written. A thing should never grade its own work, so the verifier is a *separate* invocation on the cheap tier — it re-derives ground truth from the raw git/filesystem state and checks the maker's claims against it.

It is **read-only**. It changes no files, makes no commits, writes nothing to `portfolio.json`. Its only output is a verdict.

## The goal, as a condition

> The sweep report is true: every folder that changed is reflected, no movement is invented, every number traces to a real diff, the stale rule was applied correctly, and nothing in the proposed changes touches an approval rule.

If that condition holds, the report is safe to post and the safe writes are safe to apply. If it doesn't, the loop must not ship the report.

## What you are given

Two things from the maker's run:

1. **The draft report** — the "what moved this week" summary (the Step 6 output of `portfolio-sweep`).
2. **The proposed changes** — the set of edits the maker wants to make to `portfolio.json`: refreshed `last_touched` dates, `_meta.last_swept`, `git_state` objects, plus the *held* proposals (shelve-candidates, suggested progress/score changes, untracked-folder stubs).

You also have access to the **ground truth**: the live `portfolio.json` (its pre-sweep state) and the actual workspace on disk.

## Re-derive ground truth first (don't trust the maker's crawl)

Before grading, independently establish what actually changed. Spawn a read-only crawl on the **Haiku** tier (or do it inline if cheap) — same exclusions the maker uses (`.DS_Store`, `node_modules/`, `.git/`, `.next/`, `build/`, `dist/`, `*.tmp`):

- For each tracked folder: most-recent modification time (excluding the above), and its git state via `git -C "<folder>" status --porcelain` / `git -C "<folder>" log -1 --format=%cd --date=short`.
- The `_meta.last_swept` (or `_meta.last_updated`) date from the *pre-sweep* `portfolio.json` — that's the "since" line for what counts as moved.
- Today's date from the environment, for the 60-day stale math.

This independent read is what you grade the maker's claims against. If you can't establish ground truth for some folder (path missing, permission error), mark that check `INCONCLUSIVE`, not `PASS`.

## The grading checklist

Grade each check independently. Each is PASS, FAIL, or INCONCLUSIVE.

| # | Check | PASS condition | FAIL looks like |
|---|---|---|---|
| 1 | **Completeness** | Every folder whose real last-modified is newer than the pre-sweep `_meta.last_swept` appears in the report's "moved this week". | A folder genuinely changed but the report doesn't mention it. |
| 2 | **No hallucinated movement** | Every project the report calls "moved" has a real change newer than `_meta.last_swept`. | The report says a project moved, but its newest file predates the last sweep (or the only change is an excluded file — a lockfile, `.DS_Store`). |
| 3 | **Number provenance** | Every changed `last_touched`, `progress`, and stale flag traces to an observable change on disk. | A `last_touched` date that matches no file mtime; a suggested progress bump with nothing on disk to justify it. |
| 4 | **Stale-rule correctness** | Every 60-day shelve-candidate is genuinely untouched 60+ days AND its status is `active`/`exploratory`. No folder with uncommitted work or a recent mtime is proposed for shelving. Nothing already `shelved`/`shipped`/`paused` is re-proposed. | A project flagged stale that was actually touched 12 days ago; a project with uncommitted git changes proposed as a shelve-candidate. |
| 5 | **Gate-safety** | None of the proposed changes edits an approval rule, the gate itself, or flips a `status` to `shelved` / changes a score / changes `progress` as an *automatic* write. Those must appear as held *proposals*, never as safe writes. | The proposed changes auto-apply a status→shelved, a score change, or anything that alters how/whether Kevin approves. **This is the constitutional check — a FAIL here is never auto-correctable; it stops the loop.** |

Notes on the checklist:

- Checks 1–4 are about *truth*. Check 5 is about *safety* — it's the boundary from the self-improvement strategy made enforceable: the loop can propose anything to Kevin, but it can never quietly write a ratifiable change or touch the gate.
- "Moved" excludes changes whose only delta is an ignored file. A folder whose sole change since last sweep is `package-lock.json` or `.DS_Store` did **not** move — flagging it is a Check 2 FAIL.

## The verdict

Return a compact verdict, nothing else:

```
SWEEP VERIFIER — <date>
Overall: PASS | FAIL | INCONCLUSIVE

1. Completeness ............ PASS
2. No hallucinated movement  FAIL — report claims "Riventide moved" but newest file (assets/.DS_Store, 2026-04-02) predates last sweep (2026-06-19)
3. Number provenance ....... PASS
4. Stale-rule correctness .. FAIL — "Gerlok — 71 days idle" proposed for shelve, but git shows 3 uncommitted files (active work)
5. Gate-safety ............. PASS

Verdict: FAIL on checks 2, 4. Send back for one corrective re-run.
```

- **Overall PASS** only if every check is PASS (INCONCLUSIVE on any non-gate check → Overall INCONCLUSIVE; treat like a soft fail and flag).
- For each FAIL, name the specific claim and the ground-truth fact that contradicts it. Vague failures are useless to the maker — cite the file, date, or git state.

## What happens after the verdict (the loop's contract)

This skill only returns the verdict. The loop around it acts on it:

- **PASS** → the report posts (Doc → `#sodclaw`, and the in-app sweep thread) and the safe writes apply. Held proposals go to the in-app gate for Kevin.
- **FAIL (checks 1–4)** → the maker gets **one** corrective re-run, told exactly which checks failed and why. The verifier re-grades the new draft.
- **FAIL twice** → the loop **stops and flags Kevin** rather than posting a report it couldn't verify. (Same "stop and flag rather than guess" rule the base sweep already follows.)
- **FAIL on Check 5 (gate-safety)** → **never auto-corrected.** Stop immediately and flag Kevin; a proposed change tried to write something only he may ratify, and that's a design issue, not a draft to retry.

## Tier & cost

Runs entirely on **Haiku** — re-deriving a diff and comparing it to a report is mechanical. It adds roughly one more crawl's worth of tokens to a sweep run, which on a weekly cadence is negligible. This is the budget-guard principle in miniature: the expensive model (Opus) drafts and phrases; the cheap model checks.
