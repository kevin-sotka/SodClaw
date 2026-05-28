# Project Registry — Meatbag Labs

> Master index of all projects. SodClaw reads this to know what exists, where it lives, what state it's in, and what needs attention.
>
> **Source of truth for scores/progress/status is now `projects/portfolio.json`.** This file is the human-readable narrative; `portfolio.json` is the machine-readable data that powers the dashboard (`dashboard.html` / the "Portfolio Command Center" Cowork artifact). When a project changes, update `portfolio.json` first, then regenerate the dashboard, then reconcile this narrative. Scoring is defined in `projects/scoring_rubric.md`.

Last updated: 2026-05-24 (weekly sweep)

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
- **Status:** Dormant — website exists, no recent content
- **Location:** `/Users/kevinsotka/Meatbag_Labs/thegridirongazette/`  *(corrected — was wrongly listed under /Desktop)*
- **Context:** `projects/gridiron_gazette.md`
- **Website:** thegridirongazette.com (renewed 2026-05-24, $18/yr) → redirects to meatbagmade.com/thegridirongazette/ (vanity domain over main site, like HR Derby)
- **Autonomy level:** Full-auto (research → write → publish)
- **Next action:** Define content format, build first automated issue
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
- **Status:** Shelved (2026-05-24, moved to Exploratory tier) — game-001 pipeline complete (gdd/scripts/vibe/QA)
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
- **Status:** Early stage — competitive briefs drafted
- **Location:** `/Users/kevinsotka/Meatbag_Labs/consulting-quickening/`
- **Context:** Contains competitive briefs for applied AI consulting + SMB rapid deploy
- **Autonomy level:** Kevin-only
- **Next action:** Define MVP offering and first target client

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

---

## Summary Dashboard

Live, interactive version: open `dashboard.html` or the **Portfolio Command Center** artifact in Cowork. The table below is the at-a-glance fallback.

| Group | Projects |
|------|----------|
| **Autonomous** | Train Lore, Gridiron Gazette, The Wall |
| **Active** | HR Derby, Novel, Riventide (shipped), Block Train (parked) |
| **Exploratory** | Consulting, AI Company Trail, Roblox Railways (shelved), Gerlok (shelved), Motif (shelved) |
| **Launched · shelved** | Ghostwriter, Swatch, Milk And Butt, Oregon Fail |

### Decisions waiting on Kevin (from the dashboard)
- **AI Enablement / Consulting** — top of the value board, Kevin's clearest revenue path. Kevin defining next steps (MVP offering + first client). Staying flagged.
- **Gridiron Gazette** — picking up in earnest ~2026-06-07 (reminder set). Needs attention soon.

_Resolved 2026-05-24: Riventide is shipped — the "28 missing assets" were a false alarm (dead references to cut content), so it's off the attention list._
_Reclassified 2026-05-24: Block Train → Active (parked); Roblox Railways → Exploratory (shelved); Ghostwriter, Swatch, Milk And Butt + newly-found Oregon Fail → new "Launched · shelved" category._
_Shelved earlier: Gerlok, Motif of the Cadence Collective._

---

## Registry Rules

- Update this file whenever a project's status changes
- New projects go in Exploratory by default — they must earn their way up
- If a project hasn't been touched in 60 days, it's a candidate for shelving
- Shelved ≠ dead. It means "not now, and that's okay."
