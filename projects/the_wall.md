# The Wall — Project Context for SodClaw

## What This Is
A real-time 3D web experience synced to the Bitcoin blockchain. Every ~10 minutes when a new Bitcoin block is mined, a new brick is placed on a massive digital wall by an animated crane. Users can zoom in to inspect bricks, see on-chain data (Side A), and claim or customize the brick's other face (Side B). It's part art installation, part social experiment (tracking human vs. AI participation), part interactive monument.

## Where It Lives
- **Project folder:** `/Users/kevinsotka/Meatbag_Labs/the_wall/`
- **PRD:** `THE_WALL_PRD.md` (comprehensive — 400+ lines)
- **Build plan:** `The_Wall_Claude_Code_Build_Plan.md`
- **Concept brief:** `The_Wall_Concept_Brief.docx`
- **Code (when built):** `the-wall/` subfolder

## Current State
- PRD is complete and detailed (tech stack, data model, file structure, 5 build phases, constraints)
- Build plan drafted for Claude Code execution
- No code written yet — Phase 1 hasn't started
- Tech stack decided: Next.js 14, Three.js, Supabase, Vercel, Stripe, TypeScript

## Build Phases (from PRD)
1. **Foundation + Beautiful Static Wall** — scaffolding, environment, brick rendering, shadows, lighting
2. **Bitcoin Integration + Side A** — Mempool.space API, block polling, data display
3. **Side B — Color Claims** — free color picker, Meatbag/Metal toggle, Supabase Realtime
4. **Auctions + Custom Art** — bidding system, Stripe, pixel art editor
5. **Polish + Remind Me** — notifications, mobile, performance, SEO

## Autonomy Level: Draft-and-Approve
SodClaw can:
- Draft feature specs and break down next build steps
- Create marketing plans and content about The Wall
- Research comparable projects and positioning
- Draft blog posts about the build process

SodClaw should NOT:
- Write or deploy code without Kevin's review
- Make architectural decisions that deviate from the PRD
- Commit to timelines or make public announcements

## What SodClaw Needs to Know
- The PRD is the source of truth — read it before making any suggestions
- The visual quality bar is HIGH — "architectural visualization quality, not a prototype"
- Brand colors: Concrete off-white (#F5F0EB), dark slate (#2E4057), muted blue (#4A7C9B)
- "Meatbag vs Metal" is a core thematic element — human vs. AI participation
- This is Kevin's most ambitious technical project — it's also the one most likely to stall at 80%
- The concept brief has the philosophical "why" — the PRD has the tactical "how"
- This project doubles as "building in public" content for @sodtoshi and meatbagmade.com
