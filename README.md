# SodClaw

**The Meatbag Labs Command Center**

SodClaw is Kevin Sotka's orchestration layer — the "second brain" that coordinates all Meatbag Labs projects, makes decisions like Kevin would, and delegates work to specialized project agents.

## What This Is

An AI-readable command center that turns Kevin's scattered creative portfolio into a coordinated operation. SodClaw doesn't replace the individual project folders — it sits above them, knowing where everything lives, what state it's in, and what needs attention next.

## Architecture

```
SodClaw (orchestrator) ← you are here
    │
    ├── sod_profile/        ← "digital Kevin" — voice, taste, decision rules
    ├── projects/           ← registry + pointers to all project folders
    └── workflows/          ← reusable automation recipes
         │
         ▼
   Project Folders (subagents) ← each has its own CLAUDE.md + context
   ├── /Meatbag_Labs/the_wall/
   ├── /Meatbag_Labs/train_lore/
   ├── /Meatbag_Labs/robloxrailways/
   ├── /Meatbag_Labs/mbmnovel/
   ├── /Meatbag_Labs/ghostwriter-sodtoshi/
   ├── /Desktop/meatbag_made/thegridirongazette/
   ├── /Desktop/meatbag_made/hr-derby/
   └── ...
```

## How It Works

1. **SodClaw reads `CLAUDE.md`** to understand Kevin's priorities, decision rules, and the full project map
2. **It checks `projects/registry.md`** to see what's active, what's stalled, and what needs attention
3. **It delegates to project subagents** by pointing to their folders and CLAUDE.md files
4. **It applies Kevin's voice and quality bar** from `sod_profile/` to everything it touches

## Quick Start

Open this folder in Claude Code or Cowork and say:
- `"What needs attention?"` — SodClaw checks the registry and recommends next actions
- `"Work on [project]"` — SodClaw loads that project's context and gets to work
- `"Draft train blog"` — SodClaw delegates to the train_lore subagent
- `"Status update"` — SodClaw summarizes all active projects

## Phase Roadmap

- **Phase 1 (now):** Orchestrator docs + project registry + profile (this repo)
- **Phase 2 (next):** Automated workflows via Claude API + schedulers (train blog, Gridiron Gazette)
- **Phase 3 (later):** Evaluate always-on agent platforms (OpenClaw, Kimi Claw, or custom)
