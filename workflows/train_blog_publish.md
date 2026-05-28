# Workflow: Train Blog Auto-Publish

> Fully autonomous workflow for publishing PNW railroad history posts to meatbagmade.com.

## Trigger
- Scheduled: 1x per week (target: Tuesday publish)
- Manual: Kevin says "write a train post" or "next train blog"

## Steps

### 1. Pick Topic
- Read `/Users/kevinsotka/Meatbag_Labs/train_lore/pacific-northwest-railroad-topics.md`
- Find the next unchecked `[ ]` topic
- Prefer topics that connect to recently published ones (series momentum)
- If Kevin specifies a topic, use that instead

### 2. Research
- Use web search to gather source material from the URLs listed in the topic entry
- Cross-reference at least 2 sources for key facts
- Look for the most dramatic/human angle — lead with that
- Gather any relevant dates, names, numbers for accuracy

### 3. Write
- Follow the voice and style in `sod_profile/voice_and_taste.md`
- Follow the wordpress-blog-writer skill conventions (if accessible)
- Structure: dramatic hook → context → narrative → legacy/modern connection
- Length: 800-1000 words
- Include a compelling title and meta description

### 4. Format
- Export as HTML (matching existing post format in train_lore folder)
- Save to `/Users/kevinsotka/Meatbag_Labs/train_lore/[slug]-blog-post.html`
- Use consistent formatting with previous posts

### 5. Publish
- **Phase 2a (manual):** Save HTML file, notify Kevin to upload to WordPress
- **Phase 2b (automated):** Use WordPress REST API to publish directly
  - Will need: WordPress API credentials, category/tag conventions
  - TBD: API key storage, featured image handling

### 6. Update Registry
- Mark topic as `[x]` in `pacific-northwest-railroad-topics.md`
- Log publish in `workflows/logs/YYYY-MM-DD.md`

## Quality Checks
- [ ] Title is compelling (would you click it?)
- [ ] Opening line hooks — dramatic moment, surprising fact, or vivid scene
- [ ] Facts are sourced and cross-referenced
- [ ] Voice matches Kevin's style (not academic, not listicle)
- [ ] Length is 800-1000 words
- [ ] HTML is clean and matches existing post format
- [ ] No banned words from voice_and_taste.md

## Dependencies
- Access to web search for research
- Write access to train_lore folder
- Eventually: WordPress API credentials for auto-publish

## Status: Ready for Phase 2a (manual publish handoff)
