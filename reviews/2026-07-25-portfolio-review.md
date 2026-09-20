# Meatbag Labs — Full Portfolio Review

> Date: 2026-07-25. Requested by Kevin: review strategy + user-facing content for every project, run a code review on each, rate on **value / complexity / originality / code quality** (1–5), and propose **5 improvements per project** — at least one per rating category, two of them code. Kevin picks what to act on; nothing here is executed.
>
> **What I could actually see:** the SodClaw repo in full (orchestrator code got a real line-by-line review). The other project repos (train_lore, thegridirongazette, Riventide, AI-company-trail) and the 11 non-git folders live outside this session, so their code-quality ratings come from portfolio evidence, project docs, and known facts — marked *(provisional)*. Attach those repos to a future session for a true code pass.

---

## Portfolio-level findings (read this first)

1. **The heartbeat is down.** `_meta.last_swept` is 2026-05-30 — the Friday sweep hasn't landed in **8 weeks**. The Gridiron Gazette decision ("pick up ~2026-06-07") came due and nothing fired. Until the Routine actually runs weekly, the command center is a photograph, not a dashboard. Fixing this is worth more than any single project improvement below.
2. **Gridiron has a hard external deadline and jumped the queue.** NFL season starts in ~6 weeks. Kevin's own kill-date rule says: real issue ships this season or the domain dies. It's late July — this is now the #1 decision.
3. **The tracker has drifted from its own docs.** `registry.md` (last updated 05-24) disagrees with `portfolio.json` (novel: "3 chapters" vs "~6"; Riventide filed under Exploratory heading but tiered `active`). `CLAUDE.md`'s status list is missing `launched-shelved`. The dashboard footer says "scores **ratified** by Kevin" while `portfolio.json` says scores are "**pending** Kevin's ratification" — one of those is lying to you.
4. **The portfolio is missing projects.** This environment carries skills for **Claim Wrangler** (superbill-prep), **game-foundry**, and the **sweep-verifier/sweep-budget** loop — none of which exist in `portfolio.json`. New things are being built off-book, which is exactly what the sweep exists to catch.
5. **Data-integrity smells in portfolio.json:** `autonomy` holds status words (`"paused"`, `"shelved"`) alongside real autonomy levels (`full-auto`, `kevin-only`) — two enums leaked into one field. And Oregon Fail is marked `not_a_repo` while the registry says it's served at `kevin-sotka.github.io/oregon-fail` — Pages hosting requires a repo, so one of those is wrong.

**Ratings summary** (my proposals — Kevin ratifies; complexity = cost to run, higher is worse):

| # | Project | Value | Complexity | Originality | Code quality |
|---|---------|-------|------------|-------------|--------------|
| 1 | SodClaw (orchestrator) | 4.0 | 2.5 | 4.5 | 3.5 |
| 2 | Train Lore | 3.0 | 1.5 | 3.5 | 3.0 *(prov.)* |
| 3 | Gridiron Gazette | 3.0 | 2.5 | 2.5 | 1.5 *(prov.)* |
| 4 | The Wall | 3.5 | 4.5 | 5.0 | — (scaffold) |
| 5 | HR Derby | 2.5 | 2.5 | 3.0 | — *(unseen)* |
| 6 | Meatbag Made Novel | 3.5 | 1.5 | 4.0 | n/a |
| 7 | Ghostwriter (@sodtoshi) | 3.5 | 2.5 | 3.0 | — *(unseen)* |
| 8 | AI Enablement Consulting | 4.5 | 3.0 | 2.5 | n/a |
| 9 | Riventide (RT1) | 2.5 | 2.5 | 3.5 | 2.0 *(prov.)* |
| 10 | AI Company Trail | 3.0 | 3.5 | 4.0 | — *(unseen)* |
| 11 | Roblox Railways | 3.0 | 3.0 | 3.5 | — *(unseen)* |
| 12 | Oregon Fail | 2.5 | 2.0 | 4.0 | — *(unseen)* |
| 13 | Gerlok | 1.5 | 2.5 | 1.5 | — *(unseen)* |
| 14 | The Block Train | 2.0 | 1.0 | 3.5 | n/a |
| 15 | Motif of the Cadence Collective | 2.0 | 3.0 | 2.5 | — *(unseen)* |
| 16 | Swatch | 2.0 | 1.0 | 2.0 | 3.0 *(prov.)* |
| 17 | Milk And Butt | 2.0 | 1.5 | 3.0 | — *(unseen)* |

---

## 1. SodClaw (the orchestrator) — the one I code-reviewed for real

**Ratings:** Value 4.0 · Complexity 2.5 · Originality 4.5 · Code quality 3.5

**Strategy & content.** The three-layer design (portfolio.json → two dashboards → registry) is sound and the Doc/wild-west framing is genuinely distinctive — nobody else's project tracker has a trail guide with opinions. The weak spot is operational, not architectural: the sweep that keeps it honest isn't firing, and the manual "keep two renderers in sync" rule is the kind of chore that always loses to entropy. User-facing content (Doc's briefing, card copy, empty-states like "Clean trail") is on-voice and good; the briefing itself is 2 months stale.

**Code review findings** (`index.html`, `build_dashboard.py`, `scripts/git_migrate_priority.sh`):

- **Latent crash — blank dashboard.** `index.html:343` and the template in `build_dashboard.py` compute `mean(p.value)` for every project unconditionally, and `cardHTML` dereferences `TIER[p.tier].c` (`index.html:284`). The portfolio-sweep skill explicitly adds untracked folders as `status:"unknown"` stubs with **blank scores** — the first time that happens, `Object.values(null)` throws and the whole page renders empty. Your own workflow is one quiet Friday away from killing your own dashboard.
- **Escaping is incomplete.** `esc()` (`index.html:236`) only escapes single quotes and newlines, but the onclick attributes are double-quoted — a `"` in a project name or decision text breaks the markup. `cardHTML`/`renderAttention` inject `name`, `next_action`, and `decision` into `innerHTML` raw, and `build_dashboard.py:367` splices Doc's briefing into HTML unescaped (one `<` in Doc's dialogue breaks the page). Self-authored data, so not a security hole — but it's fragile against your own prose.
- **~350 lines duplicated.** The CSS + render JS exists twice (index.html and the Python template string) with a comment-enforced sync rule. They've already micro-drifted (footer text, `git_priority` embedded in data vs hardcoded). Extract one `render.js` + one CSS block; have `build_dashboard.py` read them from disk and inline them.
- **The migrate script contradicts the dashboard.** `GIT_PRIORITY` names `the_wall` as a must-be-in-git project (`index.html:188`), but `git_migrate_priority.sh:28-32` only migrates train_lore, gridiron, and SodClaw — the tool that fixes the flag skips one of the flagged. Also its manual fallback points at `github.com/organizations/kevin-sotka/...`, which 404s for a personal account.
- **Mobile is the primary surface, but the scatter is hover-only.** Bubble tooltips (`<title>`) never appear on a phone, and the bottom-left cluster (Swatch/Milk And Butt/Block Train/Gerlok at near-identical coordinates) overlaps into an unreadable blob. `act()`'s fallback also alerts "Copied to clipboard" without awaiting the write — on failure it lies.
- **Orphan:** `wagon_trail_tracker.svg` (77KB) is referenced nowhere.

**Five improvements:**
1. **[Value]** Put a staleness banner on the dashboard: if `last_swept` > 10 days old, say so in red at the top. Right now stale data looks identical to fresh data, which quietly defeats the whole product.
2. **[Complexity]** De-duplicate the renderer into one shared `render.js`/CSS source that `build_dashboard.py` inlines at build time. Kills the "mirror every edit" rule forever.
3. **[Originality]** Use the orphaned wagon-trail art: render each project as a wagon positioned along a trail by progress %. It's the "AI Company Trail" theme actually doing work, it fixes the scatter's mobile problem, and the asset already exists.
4. **[Code]** Make the renderers defensive: null-safe `mean()`, fallback tier/status styling, and proper HTML/attribute escaping on all injected fields. This is the crash-on-stub fix.
5. **[Code]** Fix `git_migrate_priority.sh`: add `the_wall` (and `hr-derby`, which automation below needs), correct the personal-account URL, and extend the credential safety-net beyond the single hardcoded `signup_waitlist.php` filename.

---

## 2. Train Lore — PNW Railroad Blog

**Ratings:** Value 3.0 · Complexity 1.5 · Originality 3.5 · Code quality 3.0 *(provisional — repo not attached)*

**Strategy & content.** This is the best-designed content operation in the portfolio: pre-built 32-topic runway, established voice, proven format. And it's the clearest miss: labeled "full-auto," last touched **March 3**, 5 of 32 published. The reason is visible in `workflows/train_blog_publish.md` — the pipeline is "full-auto" until step 5, where it becomes "save HTML, notify Kevin to upload to WordPress." A human upload step in an automated pipeline means the pipeline runs at the speed of the human, i.e., not at all since March. The content style guide itself is excellent.

**Five improvements:**
1. **[Value]** Restart cadence with a batch: draft posts #6–9 in one session, schedule them 1/week inside WordPress. A month of runway from one sitting, and the blog looks alive again immediately.
2. **[Complexity]** Close the Phase 2b gap — WordPress REST API with an Application Password. This deletes the only manual step and makes "full-auto" true instead of aspirational.
3. **[Originality]** Add a signature closer to every post: "Ride it today" — 2–3 sentences on what a reader can still physically visit (trail, museum, surviving trestle) with a map link. Turns history posts into weekend-trip content, which is far more shareable and very PNW.
4. **[Code]** Write `publish.py`: parse the topic list for the next `[ ]`, post the HTML via WP REST, flip the checkbox, append to the SodClaw log. One script, the whole workflow.
5. **[Code]** Add front-matter (title/slug/date/tags/sources) to each post HTML so tooling — and the future Routine — can index the archive instead of guessing from filenames.

---

## 3. Gridiron Gazette — Fantasy Football

**Ratings:** Value 3.0 · Complexity 2.5 · Originality 2.5 · Code quality 1.5 *(provisional — but the credential problem is documented fact)*

**Strategy & content.** The June 7 pickup date passed unnoticed (see portfolio finding #1). The strategy doc is honest that this is a greenfield content op wearing a website costume; the drafted 5-section format in `workflows/gridiron_weekly.md` is good and just needs ratification. Fantasy content is a brutally crowded space — the 50s-diner brand is the only distinctive asset, and current content barely uses it. Kevin's own kill-rule applies: ship this season or release the domain.
**Code (known facts):** `signup_waitlist.php` contains a **live database password** in a file that's been sitting on disk for over a year — your own migrate script has a special abort just to avoid committing it. `fetch_news.php` is untested legacy.

**Five improvements:**
1. **[Value]** Decide this week: commit to the drafted format and ship **Issue #0 (preseason special)** to the waitlist by Labor Day, or consciously kill it now and save the attention. Recommendation: ship Issue #0 — it's one writing session and it tests whether anyone opens it before you build automation.
2. **[Complexity]** v1 distribution is "publish to the page + one tweet." No email platform, no Substack, no backend decisions until four consecutive weekly issues have shipped. Infrastructure debates are how this project died the first time.
3. **[Originality]** Go all-in on the diner: sections become "The Blue Plate Special" (start/sits), "Counter Talk" (hot take), "Leftovers" (waivers). Retro-diner fantasy football is ownable; generic newsletter sections are not.
4. **[Code]** Move the DB credentials out of `signup_waitlist.php` into an untracked config outside the webroot, and **rotate that password** — it predates all of this tooling.
5. **[Code]** Replace `fetch_news.php` with a scheduled pull from a free fantasy API (Sleeper's is keyless) that emits the weekly data block (injuries, waiver %, matchups) the newsletter template consumes. That's the entire automation backbone for the season.

---

## 4. The Wall — Bitcoin + 3D Art

**Ratings:** Value 3.5 · Complexity 4.5 · Originality 5.0 · Code quality — *(scaffold only; nothing meaningful to review yet)*

**Strategy & content.** The most original concept in the portfolio — a physical-feeling monument that accretes with the blockchain, plus the Meatbag-vs-Metal social experiment, is a genuinely new object. It's also the project most likely to die at 80%, and the PRD (5 phases including auctions, Stripe, pixel editors) is scoped like a funded startup, not a 1-hour-a-day builder. Docs already disagree: `the_wall.md` says "no code written yet" while portfolio notes say "Next.js app scaffolded" at 45% — reconcile before resuming or you'll re-plan work that's done.

**Five improvements:**
1. **[Value]** Treat Phase 1 as a shippable product, not a milestone: a beautiful static wall with live block count is already a URL worth tweeting. Shipping it early creates the public accountability this project needs to survive its own ambition.
2. **[Complexity]** Cut Phase 4 (auctions/Stripe/pixel art) from v1 entirely. Free color claims only. That removes payments, fraud, and moderation — roughly half the integration surface — and you can add money later if anyone shows up.
3. **[Originality]** The Meatbag-vs-Metal counter is the hook — put it on screen from Phase 1, even seeded with placeholder data. It's the thing people will screenshot; don't bury it in Phase 3.
4. **[Code]** Get `the_wall/` into a private repo **before** Phase 1 code grows (it's the only GIT_PRIORITY project with no repo, and the migrate script currently skips it — see SodClaw fix #5).
5. **[Code]** Lock the rendering approach in the PRD now: bricks as a Three.js `InstancedMesh` with LOD, not per-brick meshes. At one brick per ~10 minutes forever, naive meshes hit a wall (sorry) within months, and retrofitting instancing is the classic Three.js rewrite.

---

## 5. HR Derby — Fantasy Baseball

**Ratings:** Value 2.5 · Complexity 2.5 · Originality 3.0 · Code quality — *(not in git, unseen)*

**Strategy & content.** Small audience (~9 league members) but live, loved, and mid-season — this is a keep-running project, not a growth project. Manual burden 4 (daily HR updates by hand) is the whole cost, and it's the most automatable chore in the portfolio: MLB's StatsAPI is free and public.

**Five improvements:**
1. **[Value]** Auto-generate a short weekly recap in Kevin's voice ("pennant race" narrative, biggest mover, smack-talk fodder) and post it with the standings. For a 9-person league, the commissioner's color commentary *is* the product.
2. **[Complexity]** Automate the daily pull (below) and this project drops from manual-burden 4 to ~1 — it becomes a true set-and-forget through September.
3. **[Originality]** Add a season-arc race chart (cumulative HRs per player over time) instead of a table-only standings page. One chart makes the season legible and screenshot-able.
4. **[Code]** Write the daily job: fetch HR logs from MLB StatsAPI for the drafted players, recompute standings, regenerate the static HTML. Cron it (or a GitHub Action once it's in a repo).
5. **[Code]** Put `hr-derby/` in a private repo — automation that only lives on a laptop that sleeps is automation that misses days; a repo lets the daily job run in the cloud.

---

## 6. Meatbag Made — Novel

**Ratings:** Value 3.5 · Complexity 1.5 · Originality 4.0 · Code quality n/a *(prose project — "code" reads as tooling)*

**Strategy & content.** Correctly identified as the recharge project — its portfolio value is partly that it powers everything else. Series bible v5 + ~6 chapters is real momentum. The only strategic risk is treating it like the other projects: it should never get automated, scored against revenue, or guilt-tracked.

**Five improvements:**
1. **[Value]** Protect a fixed slot (one scene per week, whichever evening) rather than a progress %. Cadence is the only metric that matters for a novel; % complete is noise for a first draft.
2. **[Complexity]** Explicitly exempt it from the sweep's stale-flagging (a `no_stale_flag: true` field). A "STALE — shelve?" prompt on the recharge project is the system working against its owner.
3. **[Originality]** Serialize one polished excerpt per finished act on meatbagmade.com — "novel being written in public by the meatbag" is on-brand, feeds Content Is the Product, and creates gentle external momentum.
4. **[Code]** Put the manuscript + series bible in a private repo. It's the highest personal-value, least-recoverable asset in the portfolio and it currently has no version history or offsite copy.
5. **[Code]** Add a consistency-lint pass to the novel-writer skill: after each chapter, check names, dates, and established facts against the series bible and emit discrepancies. Cheap to run, and continuity bugs are the #1 revision tax at book length.

---

## 7. Ghostwriter — @sodtoshi

**Ratings:** Value 3.5 · Complexity 2.5 · Originality 3.0 · Code quality — *(unseen)*

**Strategy & content.** Strategically this is not a project, it's the **distribution layer for every other project** — shelving it means Train Lore posts, The Wall's build-in-public arc, and game launches all ship into silence. The voice system is reportedly intact, and a launch post for the Command Center has been sitting drafted since May 24. Reach 4 is the highest in the portfolio; it's shelved anyway. That's the mismatch to fix.

**Five improvements:**
1. **[Value]** Un-shelve at minimum viable cadence: 2 posts/week, drafts queued for approval. The trigger for each post is another project shipping — Ghostwriter should never need original ideas, only amplification.
2. **[Complexity]** Batch the approval: 10 drafts reviewed in one Sunday pass instead of per-tweet pings. Drops review-frequency from 4 to ~2 and makes draft-and-approve actually sustainable.
3. **[Originality]** Publish the rotting Command Center launch post — "I built a wild-west dashboard with an AI trail guide named Doc to manage my 16 side projects" is the exact high-concept-plus-absurdist content the voice doc calls for.
4. **[Code]** Add a `queue.json` (draft, status: pending/approved/posted, source-project) so the approval pipeline survives across sessions and nothing ships twice or vanishes.
5. **[Code]** Build the voice-lint: run every draft against the banned-word list and voice rules in `sod_profile/voice_and_taste.md` before it reaches Kevin. Rejecting "game-changer" automatically is cheaper than Kevin doing it manually forever.

---

## 8. AI Enablement Startup — Consulting

**Ratings:** Value 4.5 · Complexity 3.0 · Originality 2.5 · Code quality n/a *(no code — briefs only)*

**Strategy & content.** Top of the value board, only real revenue path, flagged since May, still at "competitive briefs." The blocker is a definition problem, not an effort problem — and "AI consulting" as a category is maximally crowded, so the generic version loses. Kevin's unfair advantage is specific: he *already does this at his day job* (training non-technical ops teams) and he has a public portfolio proving he ships. The strategy is to productize that exact thing, narrowly.

**Five improvements:**
1. **[Value]** Define the one offer and write it down this week: e.g. "AI Enablement Sprint — 2 weeks, fixed price, your ops team leaves running 3 real AI workflows." One page: who it's for, what they get, the number. This single artifact unblocks everything else.
2. **[Complexity]** Productize to cut the manual-burden-5: fixed intake questionnaire, canned diagnostic, templated deliverable. Every hour of packaging removes recurring hours from each engagement — the only way an all-Kevin business fits in Kevin's calendar.
3. **[Originality]** Position as "the trainer who actually ships": the differentiator isn't AI expertise, it's the 16-project portfolio and the Doc dashboard as living proof. Sell the demo you already built; competitors have slide decks.
4. **[Code]** Ship `meatbagmade.com/consulting` — one page, the offer, a plain intake form. Smallest useful action; makes the business referable.
5. **[Code]** Turn the day-job-style AI-readiness diagnostic into a small scored web questionnaire (static JS, no backend). It's the lead magnet, the sales call prep, and a Content-Is-the-Product artifact in one.

---

## 9. Riventide — Indie RPG (RT1)

**Ratings:** Value 2.5 · Complexity 2.5 · Originality 3.5 · Code quality 2.0 *(provisional — per your own audit: "convoluted," dead references to cut content)*

**Strategy & content.** Shipped — the portfolio's proof that Kevin finishes things. Two loose ends: **171 uncommitted files** against a last commit of Feb 19 (the shipped game's actual source isn't safely in git), and the dead-reference cleanup you already scoped. Strategically it should exit the attention economy: 95% progress keeps it hovering near the 80%-watch zone forever for a project that's done.

**Five improvements:**
1. **[Value]** Mine it for content: a shipping postmortem ("what shipping an indie RPG at 1hr/day actually took") + itch devlog. The story of finishing is worth more now than any patch.
2. **[Complexity]** Mark it terminal in the tracker: progress 100, a `done: true` flag, out of every future attention pass. Shipped projects shouldn't cost weekly attention cycles.
3. **[Originality]** Package the music Kevin wrote along the way as a name-your-price soundtrack on the itch page — near-zero effort, deepens the page, and it's a second thing to post about.
4. **[Code]** Commit and push the 171 drifted files **as shipped** (tag it `v1.0-shipped`) before anything else touches that folder. Right now the released game and the repo disagree, and only the laptop knows the truth.
5. **[Code]** Do the scoped dead-reference prune (scenes/music removed from the game that code still calls) as one small PR — it closes the "convoluted" note and makes any future revival cheap instead of archaeological.

---

## 10. AI Company Trail

**Ratings:** Value 3.0 · Complexity 3.5 · Originality 4.0 · Code quality — *(repo exists, 6 uncommitted files; unseen from here)*

**Strategy & content.** "Oregon Trail but you're running an AI company" is a genuinely funny, current conceit with real viral potential — and it's the theme the SodClaw dashboard already borrows, so there's brand synergy sitting unused. Confirmed alive in May, untouched since April, next action still "define the next build milestone" — i.e., it has energy but no finish line, which is the 80%-wall setup.

**Five improvements:**
1. **[Value]** Define the milestone as "one complete playable run" — start a company, survive N events, reach an ending, share a result card. A single closed loop is demoable, tweetable, and testable; feature lists are none of those.
2. **[Complexity]** Defer Supabase until a feature genuinely needs a server. A single-player run fits in localStorage; every table you don't create is maintenance you don't owe.
3. **[Originality]** The share card is the growth mechanic: "My AI startup died of GPU shortage at month 7" as an auto-generated image. Oregon Trail's death screens are the most-memed part of the original — that's the feature to steal.
4. **[Code]** Commit the 6 drifted files and get the repo clean — it's one of only two project repos with drift, and drift is how work gets lost.
5. **[Code]** Add one Playwright smoke test (boot → start run → first event renders). Nights-and-weekends gaps are exactly when a broken main goes unnoticed for a month.

---

## 11. Roblox Railways

**Ratings:** Value 3.0 · Complexity 3.0 · Originality 3.5 · Code quality — *(pipeline outputs unseen)*

**Strategy & content.** Highest personal-satisfaction score in the portfolio (5) and the full game-001 pipeline (GDD → Luau → vibe → QA) is complete — it's shelved *one session before the payoff*: importing into Studio and hitting publish with the kid. That's not a shelve, that's stopping at 95%.

**Five improvements:**
1. **[Value]** Schedule the single revival session: import game-001 into Roblox Studio with his son and publish it. The value of this project is that specific shared moment; everything else is machinery.
2. **[Complexity]** Pre-stage everything solo beforehand (files staged, checklist written, Studio updated) so the kid-session is 100% payoff and fits inside an hour. Kid attention spans don't survive debugging.
3. **[Originality]** Capture the moment — publish-button click and first playthrough reaction — as the content artifact. "My kid and I shipped a Roblox game with an AI pipeline" is a top-tier @sodtoshi post.
4. **[Code]** Before the session, re-QA the March-era Luau against current Roblox API deprecations (Roblox deprecates aggressively; four stale months is real risk). Fix ahead of time, not live in front of the kid.
5. **[Code]** Archive game-001's pipeline artifacts (gdd.md, scripts, vibe-notes, QA report) into git. It's also the template for game-002 — currently existing only on one machine.

---

## 12. Oregon Fail

**Ratings:** Value 2.5 · Complexity 2.0 · Originality 4.0 · Code quality — *(unseen)*

**Strategy & content.** Launched, playable, done — a "reverse Oregon Trail" with a name good enough to be the pitch. Registry says it's live at `kevin-sotka.github.io/oregon-fail` while portfolio says `not_a_repo` — those can't both be true (Pages requires a repo). Best use now: content mine and cross-promo for AI Company Trail.

**Five improvements:**
1. **[Value]** Cut the existing `playthrough.mp4` into 2–3 short clips + a "how I built a joke game" post. The asset already exists; the content is one editing session away.
2. **[Complexity]** Resolve the repo contradiction and then freeze it: correct `git_state` in portfolio.json, mark terminal, zero ongoing attention.
3. **[Originality]** When AI Company Trail ships, cross-link the two as the "Trail Cinematic Universe" — a running gag that makes both games more memorable and funnels players between them.
4. **[Code]** Find/verify the actual oregon-fail repo backing the Pages site, and record the true remote in portfolio.json — right now the tracker's git inventory has a known-false row.
5. **[Code]** Add a lightweight analytics beacon (GoatCounter or similar, free) to the live page — one script tag answers "does anyone still play this?", which is exactly the data a revive-or-ignore decision needs.

---

## 13. Gerlok

**Ratings:** Value 1.5 · Complexity 2.5 · Originality 1.5 · Code quality — *(unseen; "intent unknown")*

**Strategy & content.** A ~16-month-old Node scaffold whose own registry entry says "intent unknown." A project with no rememberable purpose isn't shelved, it's unburied. The kindest move is a 15-minute archaeology pass and then a decision.

**Five improvements:**
1. **[Value]** Spend 15 minutes recovering the intent from the README/launcher and write 3 sentences into the registry. If nothing comes back, that's the answer: mark it dead (Kevin's rules say shelved ≠ dead — this one might just be dead).
2. **[Complexity]** Move it (and other dead scaffolds) into a `graveyard/` folder that the sweep skips — shrinks every future crawl and the mental load of a 16-item tracker.
3. **[Originality]** If it ever revives, it needs a concept before code — a scaffold without a "why" scores 1.5 for a reason. No revival without one paragraph of intent.
4. **[Code]** The notes mention a launcher with "API-key setup" — scrub the folder for any committed keys or `.env` files **before** archiving, and revoke anything found (16-month-old keys are exactly what leaks).
5. **[Code]** Archive properly: delete `node_modules`, tar the source, keep the tarball. Frees disk, keeps the option.

---

## 14. The Block Train

**Ratings:** Value 2.0 · Complexity 1.0 · Originality 3.5 · Code quality n/a *(one story draft; no code exists)*

**Strategy & content.** One rhyming-story draft — this is a **children's book seed**, not software, and it's mis-filed in a software tracker. A trains-and-blocks kids' book from the PNW-railroad-blog guy with a kid co-builder is actually a coherent lane.

**Five improvements:**
1. **[Value]** Run the only test that matters: read the draft to his kid at bedtime. Reaction data decides finish-or-park in five minutes.
2. **[Complexity]** Keep it a document forever — no site, no app, no infra. Its complexity score of 1 is its best feature.
3. **[Originality]** If the bedtime test passes, connect it to the Train Lore audience — "the railroad-history blogger wrote a train book for kids" is a self-marketing combination none of the pieces have alone.
4. **[Code]** Put the draft in git (it's an unversioned single file from Jan 2025 — one disk failure from gone).
5. **[Code]** If illustration ever happens, build the one script this needs: a print-ready PDF pipeline (text + images → KDP-spec PDF). That's the entire technical scope of a picture book.

---

## 15. Motif of the Cadence Collective

**Ratings:** Value 2.0 · Complexity 3.0 · Originality 2.5 · Code quality — *(unseen Godot scaffold)*

**Strategy & content.** Godot scaffold, ~15 months idle, intent unknown. Same treatment as Gerlok: archaeology, then archive. The music angle (given Kevin actively makes music — see Riventide) is the only thread worth writing down before it's forgotten.

**Five improvements:**
1. **[Value]** Same 15-minute archaeology as Gerlok: recover the concept into 3 registry sentences, then decide dead vs. dormant.
2. **[Complexity]** Move to the `graveyard/` folder with Gerlok; out of the sweep, out of mind.
3. **[Originality]** If any part survives, it's the music-driven-game idea paired with Kevin's actual music — note that one sentence in the ideas backlog and let the scaffold go.
4. **[Code]** Record the Godot version in the archive note before shelving — Godot 3→4 broke project compatibility, and a revival that doesn't know its engine version starts with a migration surprise.
5. **[Code]** Strip the `.godot/` import cache and any exported binaries before archiving (routinely the bulk of a Godot folder's size).

---

## 16. Swatch

**Ratings:** Value 2.0 · Complexity 1.0 · Originality 2.0 · Code quality 3.0 *(provisional — "self-contained index.html, largely functional")*

**Strategy & content.** A finished-ish single-file color tool. Color pickers are a commodity, but a working free tool is worth more published than shelved — as a meatbagmade.com breadcrumb it costs nothing to host.

**Five improvements:**
1. **[Value]** Publish it as-is to GitHub Pages under meatbagmade branding with a one-line footer link back to the main site. Ten minutes, permanent small SEO/discovery asset.
2. **[Complexity]** Nothing to run, keep it that way — single file, no build, no deps.
3. **[Originality]** The one twist worth adding if ever touched again: a built-in WCAG contrast checker between any two swatches — turns a toy into a tool designers actually bookmark.
4. **[Code]** Add basic meta tags (title, description, og:image) so the published page is legible to search and link unfurls.
5. **[Code]** Quick pass for hardcoded local paths / console errors before publishing (typical 1-year-old single-file app issues), then it's genuinely done.

---

## 17. Milk And Butt

**Ratings:** Value 2.0 · Complexity 1.5 · Originality 3.0 · Code quality — *(unseen; "appears largely finished")*

**Strategy & content.** A complete multi-page site/game at 70%, name that makes people look twice, and a **QR code** — which strongly suggests it was built to be encountered in the physical world, and that intent is about to be lost to memory. Classic 80%-watch case: it's nearly done and nobody remembers what done was.

**Five improvements:**
1. **[Value]** Ship-or-shelve consciously: it "appears largely finished," so define the missing 30% concretely (one list), then either close it out in a session or write "shelved at 70% because X" in the registry. No more limbo.
2. **[Complexity]** Static multi-page site — host on Pages for free, no backend, done.
3. **[Originality]** Recover and write down the QR-code plan (stickers? a physical gag? a scavenger thing?) before it evaporates. The real-world component is the original part of this project.
4. **[Code]** Crawl the site for broken links/missing assets across its pages (asset-audit skill exists for exactly this) — "appears finished" and "is finished" differ by exactly that list.
5. **[Code]** Verify the QR code's target URL still resolves — a year-old QR pointing at a dead or moved URL makes every printed copy worthless.

---

## If Kevin only picks five things total

1. **Fix the Friday sweep** — the Routine hasn't fired in 8 weeks; everything else depends on the heartbeat (SodClaw).
2. **Gridiron Issue #0 by Labor Day, or kill it** — the only hard external deadline in the portfolio (Gridiron #1).
3. **Write the one-page consulting offer** — highest value score, blocked only on a definition (Consulting #1).
4. **Wire Train Lore's WordPress auto-publish** — makes the flagship "full-auto" claim true and restarts the content engine (Train Lore #2/#4).
5. **Commit Riventide's 171 drifted files** — the only shipped product whose source isn't safely versioned (Riventide #4).
