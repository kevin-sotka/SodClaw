---
name: asset-audit
description: Scans a software/game project for "referenced-but-missing" assets — files (images, audio, fonts, video, models) that the code or config calls for but that don't actually exist on disk. Use this skill whenever the user asks to "audit assets", "find missing assets", "check for missing files", "what assets/images/sounds are missing", "scan for broken asset references", mentions a playthrough or build where art/audio/sprites/music were absent or failed to load, or wants to know what a game/app needs before it can ship. Trigger it even when the user names a specific project folder rather than saying "asset audit" verbatim. Delegates the scan to a lightweight (Haiku) read-only subagent to keep it cheap, then writes a MISSING_ASSETS.md punch list in the project and updates the SodClaw portfolio tracker.
---

# Asset Audit

## What this does and why

Games and apps reference asset files by path or name — `pygame.image.load("backgrounds/faerie.png")`, `<img src="logo.png">`, `preload("res://music/theme.ogg")`. Over a project's life, code starts referencing assets that were never created, got renamed, or were deleted. The result is a game that runs but has blank screens and silent scenes — exactly the kind of thing you only catch on a full playthrough.

This skill finds those gaps **statically**, without playing through anything, by cross-referencing every asset reference in the source against the files that actually exist on disk. The scan is mechanical and read-only, so it runs on a **lighter model (Haiku) via a subagent** — that keeps token cost low for what is essentially a grep-and-compare job. The orchestrator (you) then turns the findings into a punch list and updates the tracker.

Scope is deliberately **missing-only**: assets referenced but absent. It does not chase orphaned/unused files or oversized assets — that keeps the output short and actionable.

## Step 1 — Identify the target project

If the user named a project or folder, use it. If not, ask which project (or infer from the current SodClaw context / the project being discussed). You need an absolute path to the project root. Note its bash-sandbox path too if they differ.

## Step 2 — Delegate the scan to a Haiku subagent (read-only)

Spawn one subagent with the **Haiku model** and a read-only profile (the `Explore` agent type is ideal). The whole point is to keep this cheap, so do not run the scan in the main context. Hand it this prompt, filled in:

```
Investigate the project at <ABSOLUTE_PROJECT_PATH> (bash sandbox path: <SANDBOX_PATH>) to produce a concrete punch list of MISSING asset files — assets that the code or config references but that do NOT exist on disk. Read-only scoping; do not fix anything.

Do this:
1. Find asset references. Grep the source for asset-loading calls and for string literals ending in common asset extensions: .png .jpg .jpeg .gif .webp .svg .bmp .tga .ogg .mp3 .wav .flac .mp4 .webm .ttf .otf .glb .gltf .fbx .obj. Cover the patterns for whatever stack this is, e.g.:
   - pygame / Python: pygame.image.load, pygame.mixer.music.load, pygame.mixer.Sound, load_image, load_sound
   - Web: src=, href=, url(...) in HTML/CSS/JS, import statements for asset files
   - Godot: load("res://..."), preload("res://..."), .tscn / .tres scene references
   - Unity / Unreal / generic: any explicit relative or absolute asset path in code or config
   - Config/data: JSON/YAML/TOML/XML fields like "background", "image", "music", "sprite", "icon", "sound"
2. List the asset files that actually exist on disk (find the assets/, public/, resources/, content/ dirs and anything holding media).
3. Cross-reference, accounting for relative paths and subfolders. Report only the references with NO matching file on disk.
4. Resolve dynamic/constructed paths as far as you can; if a filename is built at runtime and you can't resolve it, note it as ambiguous rather than guessing.

Report concisely (under 300 words) as grouped lists by asset type (images / audio / fonts / other). For each missing item give: the expected file path, and the source file + line (or config field) that references it. If NOTHING is missing, say so explicitly and report how many references you checked. Note any ambiguous/unresolved references separately.
```

Wait for the subagent's report. Trust it but sanity-check: the counts and file/line citations should be specific. If the report is vague or the project stack wasn't handled, re-run with a tightened prompt rather than padding the output yourself.

## Step 3 — Write the punch list into the project

Write `MISSING_ASSETS.md` at the project root using this structure. Group by asset type, give exact paths and the referencing source location, and date the scan. If nothing is missing, still write the file with a clean bill of health so there's a record.

```markdown
# <Project> — Missing Assets Punch List

> Scan date: <YYYY-MM-DD> (by SodClaw asset-audit). These files are **referenced in code/config but absent on disk**. Verify each path before sourcing/creating — a few may be intentional or unused. Total: <N> files.

## Background / images (<n>)
- `relative/path/file.png` — referenced in `src/file.ext` line NN

## Audio (music + SFX) (<n>)
- `relative/path/track.ogg` — referenced in `src/file.ext` line NN

## Fonts / other (<n>)
- ...

## Ambiguous (couldn't fully resolve)
- <runtime-constructed reference> — `src/file.ext` line NN

## Notes
- <clustering observations, what's end-game vs early, any quick wins>
```

## Step 4 — Update the SodClaw tracker (if the project is in the portfolio)

Read `SodClaw/projects/portfolio.json`. If this project has a record there, update it so the dashboard reflects reality:

- `next_action`: point at the concrete work, e.g. `"Source/create N missing assets (X images + Y audio) — see <project>/MISSING_ASSETS.md"`.
- `decision`: if the gap is non-trivial, frame the real choice (finish vs shelve) with the true count, since the scan often reveals more than a playthrough memory suggested.
- `notes`: append the scan date and headline counts.

Then keep the three layers in sync exactly as SodClaw normally does: mirror the same change into `SodClaw/dashboard.html`'s embedded `DATA` array, reconcile `SodClaw/projects/registry.md`, and re-publish the dashboard artifact with `update_artifact`. Edit `portfolio.json` with a small script (load → modify → dump) so the JSON stays valid.

If the project is **not** in the portfolio, skip the tracker update — just leave the `MISSING_ASSETS.md` file and report the findings in chat.

## Step 5 — Report back

Give the user the headline counts, link the `MISSING_ASSETS.md` with a `computer://` link, and — if the scan revealed materially more (or less) than expected — say so plainly, since that changes the finish-or-shelve calculus. Offer the obvious next move (e.g. "want me to generate the missing images?") but let the user make the taste/energy call.

## Notes on judgment

- A reference with no file isn't always a bug — placeholder code, commented-out features, or optional assets exist. Flag, don't assume. That's why the punch list says "verify before sourcing."
- Keep the subagent on the light model. If a project is huge (tens of thousands of files), tell the subagent to scope the file-existence check to the asset directories rather than walking the whole tree.
