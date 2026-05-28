# Workflow: Asset Audit

> Capability for finding **referenced-but-missing assets** in any project (images, audio, fonts, etc. that the code calls for but that don't exist on disk).

This is packaged as an installable skill: `SodClaw/skills/asset-audit/` (and `asset-audit.skill`). Once installed it runs as the `/asset-audit` slash command.

## When SodClaw should reach for it
- Kevin mentions a playthrough/build where art, sprites, music, or sounds were missing or didn't load.
- Any "what's missing before this can ship?" question about a game or app.
- As part of evaluating a near-done project's real remaining scope (it often reveals more than memory suggests — Riventide looked like "~5 files," was actually 28).

## How it works (summary)
1. Delegates the scan to a **Haiku read-only subagent** to keep it cheap — it greps source/config for asset references and cross-references against files on disk.
2. SodClaw writes a `MISSING_ASSETS.md` punch list into the project.
3. If the project is in `portfolio.json`, SodClaw updates its `next_action` / `decision` / `notes`, syncs `dashboard.html` + `registry.md`, and re-publishes the dashboard artifact.

Full instructions live in `SodClaw/skills/asset-audit/SKILL.md`. First proven on Riventide (2026-05-23) and validated on the swatch web project.
