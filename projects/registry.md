# Project Registry — Meatbag Labs

> Master index of all projects. SodClaw reads this to know what exists, where it lives, what state it's in, and what needs attention.
>
> **Source of truth for scores/progress/status is now `projects/portfolio.json`.** This file is the human-readable narrative; `portfolio.json` is the machine-readable data that powers the dashboard (`dashboard.html` / the "Portfolio Command Center" Cowork artifact). When a project changes, update `portfolio.json` first, then regenerate the dashboard, then reconcile this narrative. Scoring is defined in `projects/scoring_rubric.md`.

Last updated: 2026-09-04 (weekly sweep, unattended): **the headline is the map, not a project.** Eleven tracked projects were physically relocated into `hitfactory.games/` since the last sweep — RT1/Riventide, Oregon_Fail, Foundry, Gerlok, motif-of-the-cadence-collective, swatch, factory-cats, kalevala-runo, splice-lab, snow-day-tycoon — and `consulting-quickening` was renamed to `consulting/`. Every one of those `location` paths in `portfolio.json` was pointing at an empty lot; all twelve corrected as factual writes. **Two git corrections, both good news:** The Wall has a clean synced repo at `the_wall/the-wall` (remote `kevin-sotka/the-wall`, last commit 4/20) and HR Derby has one at `hr-derby/github` (remote `kevin-sotka/hr-derby`, last commit 4/05) — both were carried as `not_a_repo`, both now off the not-portable list. Sixteen projects moved: **Riventide** is the big one — a vanilla-JS browser build published 9/02 replacing pygbag, loading-hang and silent-music fixes, `docs/` repointed, five commits and the first since February. **Foundry** now holds 27 game packages under `games/` (lower-falls, jimothy-prince-of-ballard, murmuration, the-aviary, +23), 219 files. **jobclaw** at 161 files (was 87). **kevinsotka.com** and **Gridiron Gazette** both touched today. Also moved: mbmnovel (8/31), Know Kevin (8/31), meatbag_method (8/19), meatbag_made_brand + kalevala-stories + Sotka family history (8/17), train_lore (8/30), aphelion (9/02), hitfactory.games (9/03), SodClaw (today). One shelve candidate: **Claim Wrangler at 72 days** — raised as a question with the HR Derby precedent attached. NEW UNTRACKED: **hit-factory** (23 files, synced repo `kevin-sotka/hit-factory`, 8/25 — distinct from hitfactory.games) and **kevin-sotka.github.io** (2 files, Pages root, likely infrastructure). Git readiness worsening at the center: **SodClaw 29 uncommitted, still no commit since 2026-05-28**; Riventide 173 uncommitted (but committing again); Train Lore 12 uncommitted + 2 unpushed. Held proposals now **13** — five of the old eight look already answered by reality (#1 aphelion, #2 jobclaw, #6 Sotka family history all landed in the tracker on 9/04; #4 superseded by the new Foundry number). No scores/progress/status auto-changed. Sweep verified PASS on all 5 checks before writes; the Haiku crawl reported 11 folders "missing" and every repo as `not_a_repo` — both wrong, corrected by a direct re-derivation of every mtime and git state.

Prior (2026-09-04, public page refresh, Kevin-directed): four folders promoted out of the untracked/unknown pile and into `portfolio.json` as real rows — **Hit Factory Games** (the studio umbrella over `hitfactory.games/`; `games.json` is its source of truth, 34 games, 13 shipped), **Sotkajärvi — Kalevala Stories** (7 tales live under `meatbagmade.com/the-land/sotkajarvi/`), **Sotka Family History** (answers the 8/14 proposal #6 track-or-ignore: TRACK), and **SodClaw** itself, which had no row in its own ledger. `jobclaw` promoted unknown → active (answers proposal #2). `meatbag_made_brand` renamed **Meatbag Made — The Land** and marked active — the Aug 2026 homepage rebuild. Public `/projects` page rebuilt: new links for the Gazette (thegridirongazette.com), Riventide (GitHub Pages, itch.io dropped), the novel (meatbagmade.com/cyberpunk-noir-novel/) and Train Lore (now the /category/trains/ archive rather than the site root); individual game cards folded into the studio tile; The Wall and AI Company Trail pulled from the public page (still shelved, unchanged in the tracker). Scores and progress untouched. **This narrative file is still stale below this line** — Train Lore's "5 of 32" and the Gazette's "no real issue shipped yet" predate reality by months; `portfolio.json` wins.

Prior (2026-08-14): (weekly sweep, unattended: two weeks' worth of dust, nine projects moved, no sweep ran on 8/07. **jobclaw** was the busiest claim: a full rack of resume variants cut 8/13 (87 files now, was 49), still an untracked `unknown` stub, the oldest open question on the books. **Gridiron Gazette** auto-pushed news daily through today (last commit 8/13), hands-off as designed. **Train Lore** front page + stories.json refreshed 8/09, now **13 published dispatches**, so the '5 of ~32' note in this file is still stale. **Meatbag Made novel** drafted chapter_13_marcus.md (8/01) and added the master arc + personhood taxonomy bible docs (8/09). **Aphelion** near doubled to **62 source files** under src/ (was 34), built 8/03, still carried at 5%. **Oregon Fail**, marked shipped/100%, picked up `snack-dash-v1.js/.css` on 8/12: an unexplained new game in an old camp. **business_strategist** got an Idea_Aggregator.docx (8/11), **meatbag_made_brand** a meatbag_tag.png (8/03), **Meatbag Method** its site-page PUBLISH-STEPS (8/04). NOTHING crossed the 60-day line, zero shelve candidates; nearest is Claim Wrangler at 51d, then Know Kevin at 27d. NEW UNTRACKED FOLDER: **Sotka family history** (10 files, 8/10: CLAUDE.md, sotka-research-log.html, a scanned 1995 reunion article, 7 photos), raised as a proposal rather than auto-stubbed. Git readiness unchanged and drifting: SodClaw **27 uncommitted, no commit since 2026-05-28**, Train Lore 10 uncommitted + **2 unpushed**, Gazette 3 uncommitted, Riventide still 171 since Feb, AI-company-trail 6; The Wall and Aphelion still **not_a_repo**. factory-cats and splice-lab are the only clean repos. Held proposals pending Kevin (in-app), 8 total: #1 aphelion 5% to 15% (evidence refreshed), #2 jobclaw unknown to active, #3 Train Lore 45% to 55% + notes fix, #4 Foundry progress 50%, #5 giga-foundry track-or-fold, all five now **14 days old**, plus new #6 Sotka family history track-or-ignore, #7 mbmnovel 36% to 40%, #8 Snack Dash own-project-or-add-on. No scores/progress/status auto-changed. Sweep verified PASS on all 5 checks before writes; the Haiku crawl mis-dated Aphelion (claimed 5/24) and was corrected against a direct re-derivation of every mtime and git state.)

Prior (2026-07-31 (weekly sweep, unattended: a genuinely busy week — six projects moved. **Aphelion** (giga-foundry) went from a stub to 34 source files across core/planet/render/ship/sim + ARCHITECTURE.md, still carried at 5% progress — the single biggest gap between tracker and reality. **jobclaw** kept building (5 applications, 5 company dossiers, screener prep, pipeline.json touched 7/31) — the "track or ignore" stub question is answered by the work; proposed for promotion to Active. **Foundry** rolled a second line-off game package, *Jimothy, Prince of Ballard* (full publishable bundle: gdd, index.html, atlas, audio, icons, harness, 7/28). **Meatbag Method** got a site-page (index.html, publish.sh, assets, logo/title art, wordpress-embed, 7/29). **Train Lore** picked up hero art for two-trains-one-track + the-switchback-era and a push-lore.sh update (7/27), and Kevin committed — uncommitted dropped 18 → 2 — but 2 commits sit unpushed; stories.json now shows **11 published**, so the "5 of ~32" note is stale. **Gridiron Gazette** auto-pushed news daily through 7/31 (commit 435484c), hands-off as designed. NOTHING crossed the 60-day line — zero shelve candidates this run; nearest are business_strategist (52d) and meatbag_made_brand (54d), both status `unknown`. No untracked top-level folders; giga-foundry/ is a container (aphelion tracked, runs/ is run output) — flagged as a question whether the harness itself should be tracked. Git readiness: SodClaw 26 uncommitted (was 23), Train Lore 2 uncommitted + **2 unpushed**, Gazette 2 uncommitted, Riventide still 171 since Feb, Aphelion **not a repo at all**, The Wall still not_a_repo. Held proposals pending Kevin (in-app): #1 aphelion 5%→15%, #2 jobclaw unknown→active, #3 Train Lore 45%→55% + notes fix, #4 Foundry progress/notes for the second shipped package, #5 giga-foundry track-or-fold. No scores/progress/status auto-changed. Sweep verified PASS on all 5 checks — plus an independent Haiku re-derivation of every mtime and git state — before writes.)

Prior (2026-07-24): weekly sweep, unattended: a working week with two fresh tracks. Moved: **Train Lore** — front page refreshed 7/21 (index.html), on top of the still-pending post-#6 bump; **Gridiron Gazette** — news pipeline auto-committed fresh copy today (commit 7/24, 1 wagon still unpushed); **jobclaw** — not idle, built another application inside it (Panasonic resume, 7/24), still an unknown stub pending track-or-ignore. **HR Derby crossed the 60-day line** — 62 days idle, status active → the first honest shelve-candidate of the run (push or park, Kevin's call; never auto-shelved). NEW UNTRACKED FOLDER: **kevinsotka.com** (13 files, 7/23) — a consulting/enablement web presence (bio, methodology, evidence, ecosystem-strategy + 3 HTML mockups), reads like kin to Meatbag Method; auto-added as an unknown stub, pending track/fold/ignore. Git readiness: SodClaw repo 23 uncommitted, Train Lore drifted to 18, Gazette 2 uncommitted + 1 unpushed, Riventide still 171 since Feb; The Wall still not_a_repo. Held proposals pending Kevin (in-app): #1 Train Lore 40%→45% (post #6, carried from 7/03, now 21d), #2 mbmnovel 33%→36% (ch.12, carried from 7/18). Carried-forward stubs still pending track-or-ignore: jobclaw, Know Kevin, business_strategist, meatbag_made_brand. No scores/progress/status auto-changed. Sweep verified PASS on all 5 checks before writes.)

Ratified (2026-07-24, in-app): Kevin approved proposals **#1 Train Lore 40%→45%** and **#2 mbmnovel 33%→36%** (both applied). **HR Derby NOT shelved** — it's in daily use by the league and Kevin monitors it; reclassified active→**shipped** (live/monitored) so the 60-day file-mtime stale rule stops flagging a live-but-hands-off product. **kevinsotka.com promoted** from unknown stub to a tracked **Active** project and designated the **consulting hub**; Kevin chose **hub-designation only** (no folders moved on disk) and rolled up **consulting-quickening** alone under it (its competitive briefs feed the hub; stays shelved, stays in place). business_strategist, meatbag_made_brand, Know Kevin, and meatbag_method stay independent for now.

Prior (2026-07-18): weekly sweep, unattended: a good working week. Moved: **Meatbag Made novel** — Chapter 12 (Marcus) drafted (prewriting + continuity tracker + master arc, 7/14), which was literally the pending next_action; **Train Lore** — another dispatch down the line (two-trains-one-track story + a new post in the chute, 7/15) on top of the still-pending post-#6 bump; **jobclaw** — not idle, a full HP job application built inside it (resume, cover letter, dossier, outreach, proof page, 7/15), still an unknown stub pending track-or-ignore; **Gridiron Gazette** — news pipeline auto-committed fresh copy today (commit 7/17). Nothing newly stale enough to shelve (hr-derby closest at 56 days, approaching the 60-day line). No new untracked folders. Git readiness: SodClaw repo 23 uncommitted, Train Lore drifted to 17, Gazette 3 uncommitted + 1 unpushed, Riventide still 171 since Feb; The Wall still not_a_repo. Held proposals pending Kevin (in-app): #1 Train Lore 40%→45% (post #6, carried from 7/03, 15d), #2 mbmnovel 33%→36% (ch.12). Carried-forward stubs still pending track-or-ignore: jobclaw, Know Kevin, business_strategist, meatbag_made_brand. No scores/progress/status auto-changed. Sweep verified PASS on all 5 checks before writes.)

Prior (2026-07-13): weekly sweep: a moving week, Kevin present and directing. NEW CLAIM STAKED: **Meatbag Method** — Kevin's first consulting foray, an AI-education YouTube brand (teach-to-fish, not sell-the-fish); Episode 0 "AI Basics" + Episode 1 "Build Your Own Newsletter (fantasy football)" decks built; existing projects become live demos. Added as Active/active per Kevin. SHELVED by Kevin's direct call: **AI Company Trail** (active → shelved; consulting energy redirects to the Method) and **The Wall** reconfirmed shelved. Moved: novel Chapter 12 (Marcus) drafting underway, Gridiron Gazette fresh news commit 7/13, Train Lore new dispatch 7/12, Foundry game-album slate 7/08. New untracked folder **jobclaw** (job-search agent, 30 files, 7/07) auto-added as unknown stub, pending track-or-ignore. Nothing newly stale enough to shelve (hr-derby at 51 days). Git readiness: SodClaw repo 22 uncommitted, Train Lore drifted to 15, Riventide still 171 since Feb, Gazette 2. No scores/progress auto-changed; the two status changes were Kevin-ratified live.

Prior (2026-07-03): weekly sweep: steady week. Moved: Train Lore (new story drafted, John Stevens / Marias Pass, 6/29, uncommitted), Gridiron Gazette (news pipeline fresh, auto-commit 7/02), Foundry (new game "halcyon" worked on 7/03), Know Kevin (grew to 6 files incl. a corporate POC deck, 7/01; still pending track-or-ignore). Nothing stale enough to shelve; no untracked folders. Git readiness: Train Lore drifted to 14 uncommitted (was clean), SodClaw repo now 21 uncommitted (was 15), Riventide still 171 uncommitted since Feb, Gazette 3 uncommitted. Held proposal: Train Lore progress 40% to 45% (post #6 drafted), pending Kevin. No scores/progress/status changed. Sweep verified PASS on all 5 checks before writes.

Prior (2026-06-26): weekly sweep: quiet week. Moved — Train Lore (poster image), Gridiron Gazette (news feed refreshed), Meatbag Made novel (ch.11 review gdoc back from Kevin), Claim Wrangler (skill + dashboard + claims ledger scaffolded). Nothing stale enough to shelve; every active/exploratory project touched within ~2 weeks. No untracked folders. Git readiness flags carried forward: SodClaw repo 15 uncommitted; Riventide repo 171 uncommitted since Feb. No scores/progress/status changed.

Prior (2026-06-23): weekly sweep + Kevin corrections — Gridiron Gazette LAUNCHED 100% as a western-themed fantasy newsletter (old briefs are now separate future products); novel reset to ~33% at ch.11; Snow Day Tycoon, Oregon Fail, and Splice Lab all marked shipped/100%; Claim Wrangler now TRACKED (exploratory/active) — family tool for prepping + tracking out-of-network Aetna claims.

---

## Priority Tier: Autonomous (hand these off)

### 1. PNW Railroad History Blog ("Train Lore")
- **Status:** Active — 5 of 32 topics published
- **Location:** `/Users/kevinsotka/Meatbag_Labs/train_lore/`
- **Also lives in:** Claude.ai Project (has a wordpress-blog-writer skill)
- **Context:** `projects/train_blog.md`
- **Website:** meatbagmade.com (WordPress)
- **Autonomy level:** Full-auto (research → write → publish, no approval needed)
- **Next action:** Pick next topic from `pacific-northwest-railroad-topics.md`, draft and publish
- **Cadence goal:** 1 post/week

### 2. Gridiron Gazette (Fantasy Football Newsletter)
- **Status:** Active — format defined, demos built, no real issue shipped yet (2026-06-07 pickup)
- **Location:** `/Users/kevinsotka/Meatbag_Labs/thegridirongazette/`  *(corrected — was wrongly listed under /Desktop)*
- **Context:** `projects/gridiron_gazette.md`
- **Website:** thegridirongazette.com (renewed 2026-05-24, $18/yr) → redirects to meatbagmade.com/thegridirongazette/ (vanity domain over main site, like HR Derby)
- **Autonomy level:** Full-auto (research → write → publish)
- **What's built (as of 2026-05-29):** `product-briefs.md` — 3 researched concepts (Brief 1 "The 9AM Brief"/Concierge, Brief 2 "Coach in Your Pocket", Brief 3 "League Drama Engine"/Diner). Plus a **live demo reel** deployed to Pages (PHP dropped, clean static): working mockups for the 9AM Brief and "The Tuesday Dispatch," plus a polished geo-game "Where in the World is Chargers, San Diego?" (mobile pinch-zoom fixed).
- **Open decision:** which concept becomes issue #1. SodClaw rec → hand-built v1 of **Brief 3 (League Drama Engine)**: matches the Gazette name, plays to Kevin's voice, shippable in one session with no league-sync pipeline. Brief 1 is the better long-term product but needs the data plumbing, so it's the "build the machine" follow-up.
- **Next action:** Pick issue-#1 format, then hand-write + publish one real issue for one league this season.
- **Cadence goal:** Weekly during NFL season, monthly offseason

### 3. The Wall (Bitcoin + 3D Art)
- **Status:** Active — PRD complete, build plan drafted, no code yet
- **Location:** `/Users/kevinsotka/Meatbag_Labs/the_wall/`
- **Context:** `projects/the_wall.md`
- **Website:** TBD (will be on meatbagmade.com or standalone)
- **Autonomy level:** Draft-and-approve (features + marketing plans, Kevin approves before ship)
- **Next action:** Begin Phase 1 build (foundation + beautiful static wall)
- **Tech stack:** Next.js, Three.js, Supabase, Vercel

---

## Active Tier: Kevin-Driven

### 4. Roblox Railways
- **Status:** Shelved (2026-05-24, moved to Exploratory tier) — game-001 pipeline complete (gdd/scripts/vibe/QA). **Stirred 2026-06-10:** game-002 scripts appeared (MainUI.lua etc.) — sweep proposes un-shelving; Kevin to confirm.
- **Location:** `/Users/kevinsotka/Meatbag_Labs/robloxrailways/`
- **Context:** Has its own `CLAUDE.md` with full orchestration guide + 4 skill files
- **Autonomy level:** Kevin-only (co-builds with his son)
- **Next action:** Parked. game-001 pipeline complete. Resume to import into Roblox Studio + publish (highest personal-satisfaction project — good kid-time revival).

### 5. HR Derby (Fantasy Baseball)
- **Status:** Active — 2026 season running
- **Location:** `/Users/kevinsotka/Meatbag_Labs/hr-derby/`  *(corrected — was wrongly listed under /Desktop)*
- **Context:** Has its own `claude.md`
- **Website:** meatbagmade.com/hr-derby/
- **Autonomy level:** Kevin-only (commissioner duties)
- **Next action:** Season in progress, maintain standings

### 6. Meatbag Made Novel
- **Status:** Active — 3 chapters drafted, series bible complete
- **Location:** `/Users/kevinsotka/Meatbag_Labs/mbmnovel/`
- **Context:** Has its own `CLAUDE.md` + novel-writer skill
- **Autonomy level:** Kevin-only (creative writing)
- **Next action:** Continue chapter drafting

### 7. Ghostwriter (@sodtoshi)
- **Status:** Launched · shelved (2026-05-24, new category) — system built, skills iterate over time
- **Location:** `/Users/kevinsotka/Meatbag_Labs/ghostwriter-sodtoshi/`
- **Context:** Has its own `CLAUDE.md` with full voice DNA + workflow commands
- **Autonomy level:** Draft-and-approve (drafts tweets, Kevin approves before posting)
- **Next action:** Parked. Launch post for the dashboard tool drafted (`outputs/2026-05-24-portfolio-command-center.md`). Resume when Kevin wants a posting cadence.

---

## Exploratory Tier: Early Stage / Paused

### 8. AI Enablement Startup (Consulting)
- **Status:** Shelved (2026-06-07, 89 days idle) — competitive briefs drafted. Richest value vein on the map; shelved ≠ dead, just not now.
- **Location:** `/Users/kevinsotka/Meatbag_Labs/consulting-quickening/`
- **Context:** Contains competitive briefs for applied AI consulting + SMB rapid deploy
- **Autonomy level:** Kevin-only
- **Next action:** Revive when ready to drive the stake — define MVP offering and first target client

### 9. Riventide (Indie RPG)
- **Status:** Shipped (Active tier) — on itch.io (macOS). The 2026-05-23 "missing assets" audit was a **false alarm** (dead references to cut content, not real gaps).
- **Location:** `/Users/kevinsotka/Meatbag_Labs/RT1/`
- **Context:** Has README + publishing guide; `RT1/MISSING_ASSETS.md` marked resolved
- **Autonomy level:** Paused
- **Next action:** Optional only — prune dead scene/music references from the convoluted code, or call it fully done.

### 10. Gerlok
- **Status:** Shelved (2026-05-23) — old code scaffold, untouched ~14 months
- **Location:** `/Users/kevinsotka/Meatbag_Labs/Gerlok/`
- **Context:** Has README + setup scripts
- **Autonomy level:** Shelved
- **Next action:** None unless Kevin revives it

### 11. AI Company Trail
- **Status:** Active — confirmed very much alive by Kevin (2026-05-23). Next.js app with Supabase
- **Location:** `/Users/kevinsotka/Meatbag_Labs/AI-company-trail/`
- **Context:** Has its own `CLAUDE.md` + build spec
- **Autonomy level:** Kevin-only
- **Next action:** Define the next build milestone (candidate for promotion to Active tier)

### 12. The Block Train
- **Status:** Paused (moved to Active tier + parked 2026-05-24) — one rhyming story draft
- **Location:** `/Users/kevinsotka/Meatbag_Labs/the_block_train/`
- **Autonomy level:** Shelved
- **Next action:** None unless Kevin revives it

### 13. Motif of the Cadence Collective
- **Status:** Shelved (2026-05-23) — Godot game, untouched ~13 months
- **Location:** `/Users/kevinsotka/Meatbag_Labs/motif-of-the-cadence-collective/`
- **Autonomy level:** Shelved
- **Next action:** None unless Kevin revives it

### 14. Milk And Butt
- **Status:** Launched · shelved (2026-05-24) — early multi-page web app/game (~1 year old)
- **Location:** `/Users/kevinsotka/Meatbag_Labs/Milk And Butt/`
- **Autonomy level:** Shelved
- **Next action:** None unless Kevin revives it

### 15. Swatch
- **Status:** Launched · shelved (2026-05-24) — early color-swatch web tool (~1 year old)
- **Location:** `/Users/kevinsotka/Meatbag_Labs/swatch/`
- **Autonomy level:** Shelved
- **Next action:** None unless Kevin revives it

### 16. Oregon Fail (Indie Game)  *(NEW — found 2026-05-24)*
- **Status:** Launched · shelved — "reverse Oregon Trail" web game, played online (kevin-sotka.github.io/oregon-fail), playthrough video on disk
- **Location:** `/Users/kevinsotka/Meatbag_Labs/Oregon_Fail/`
- **Autonomy level:** Paused
- **Next action:** None unless revived; strong content-mining candidate (the build/playthrough)

### 17a–d. Untracked stubs *(auto-added by sweep 2026-06-12 — pending Kevin: track or ignore)*
- **Foundry** (`/Foundry/`, 10 files, touched 2026-06-12) — likely Game Foundry pipeline working folder; confirm track vs fold into SodClaw
- **Know Kevin** (`/Know Kevin/`, 1 file, touched 2026-06-09)
- **business_strategist** (`/business_strategist/`, 2 files, touched 2026-06-09)
- **meatbag_made_brand** (`/meatbag_made_brand/`, 19 files, touched 2026-06-07)

### 17. Runo — Songs of the Kalevala  *(NEW — built 2026-06-11 by the Game Foundry, shipped 2026-06-12)*
- **Status:** Shipped — live at https://kevin-sotka.github.io/kalevala-runo/ (Ep I: Birth of Väinämöinen, Ep II: The Sampo); first game off the Foundry line
- **Location:** `/Users/kevinsotka/Meatbag_Labs/kalevala-runo/` → github.com/kevin-sotka/kalevala-runo (synced)
- **Stack:** Phaser 3 via CDN, 100% procedural art, WebAudio synth placeholder (Kevin's music pass pending), static on GitHub Pages
- **Autonomy level:** Draft-and-approve
- **Next action:** Kevin playtests the live site, sets scores; music pass later
- **Open decision:** third runo before promoting out of Exploratory, or let v1 ride?

---

## Summary Dashboard

Live, interactive version: open `dashboard.html` or the **Portfolio Command Center** artifact in Cowork. The table below is the at-a-glance fallback.

| Group | Projects |
|------|----------|
| **Autonomous** | Train Lore, Gridiron Gazette, The Wall |
| **Active** | HR Derby, Novel, Riventide (shipped), Block Train (parked) |
| **Exploratory** | Consulting, AI Company Trail, Runo (shipped — live on Pages), Splice Lab (Foundry build — awaiting playtest), Snow Day Tycoon (Foundry build — v1 verified, awaiting playtest), Roblox Railways (shelved), Gerlok (shelved), Motif (shelved) |
| **Launched · shelved** | Ghostwriter, Swatch, Milk And Butt, Oregon Fail |

### Decisions waiting on Kevin (from the dashboard)
- **AI Enablement / Consulting** — top of the value board, Kevin's clearest revenue path. Kevin defining next steps (MVP offering + first client). Staying flagged.
- **Gridiron Gazette** — picked up 2026-06-07. Format work already done (3 briefs + live demo reel); open decision is which concept ships as issue #1. SodClaw rec: hand-built Brief 3 this session.

_Resolved 2026-05-24: Riventide is shipped — the "28 missing assets" were a false alarm (dead references to cut content), so it's off the attention list._
_Reclassified 2026-05-24: Block Train → Active (parked); Roblox Railways → Exploratory (shelved); Ghostwriter, Swatch, Milk And Butt + newly-found Oregon Fail → new "Launched · shelved" category._
_Shelved earlier: Gerlok, Motif of the Cadence Collective._

---

## Registry Rules

- Update this file whenever a project's status changes
- New projects go in Exploratory by default — they must earn their way up
- If a project hasn't been touched in 60 days, it's a candidate for shelving
- Shelved ≠ dead. It means "not now, and that's okay."
