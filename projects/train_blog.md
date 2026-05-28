# Train Blog — Project Context for SodClaw

## What This Is
A PNW railroad history blog on meatbagmade.com (WordPress). Kevin writes engaging, deeply researched posts about Pacific Northwest railroad history — dramatic human stories, engineering marvels, labor history, and preservation.

## Where It Lives
- **Content folder:** `/Users/kevinsotka/Meatbag_Labs/train_lore/`
- **Topic list:** `pacific-northwest-railroad-topics.md` (32 topics, 5 completed)
- **Published posts:** HTML files in the train_lore folder
- **Skill file:** `wordpress-blog-writer` skill (installed in Claude.ai project)
- **Website:** meatbagmade.com (WordPress, self-hosted)

## Current State
- 5 of 32 topics published (Wellington Avalanche, Deschutes Canyon Railroad War, Stampede Pass, John Stevens/Marias Pass, Great Big Baked Potato)
- 27 topics remaining with full outlines, source links, and angle descriptions
- Each post is ~800-1000 words, HTML formatted, exported for WordPress upload

## Autonomous Workflow (Phase 2 Target)
1. Pick the next unpublished topic from the topic list
2. Research using web search (sources are pre-identified in the topic list)
3. Write the post following the established style (see below)
4. Export as HTML
5. Publish to WordPress via API or manual upload
6. Mark topic as `[x]` in the topic list
7. Log the publish in SodClaw workflow logs

## Content Style
- **Tone:** Engaging narrative history — not academic, not listicle. Like a great bar conversation about trains.
- **Structure:** Hook with a dramatic moment → context → story → legacy/modern connection
- **Length:** 800-1000 words
- **Sources:** Each topic has pre-identified sources in the topic list. Always verify facts.
- **Kevin's voice:** Accessible, enthusiastic, occasionally irreverent. He genuinely loves this stuff.
- **Audience:** History buffs, railroad enthusiasts, Pacific Northwest locals, casual readers who like a good story

## What SodClaw Needs to Know
- The wordpress-blog-writer skill in Claude.ai has the detailed writing instructions
- Posts should feel like they belong together as a series but each stands alone
- Kevin has a WordPress export file from April 2025 in the meatbag_made folder
- The blog is part of meatbagmade.com's content strategy — it builds Kevin's voice and SEO
- This is the easiest project to fully automate because the topic list is pre-built
