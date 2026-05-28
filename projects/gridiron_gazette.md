# Gridiron Gazette — Project Context for SodClaw

## What This Is
A fantasy football newsletter/website. Kevin's take on NFL and fantasy football content — opinionated, data-informed, fun. Connected to his broader sports content interests (he also runs HR Derby for fantasy baseball).

## Where It Lives
- **Website folder:** `/Users/kevinsotka/Desktop/meatbag_made/thegridirongazette/`
- **Website:** thegridirongazette.com
- **Current state:** Basic website with logo, index page, mock draft page, waitlist signup (PHP)

## Current State
- Website exists with branding (logo, 50s diner aesthetic)
- Has a waitlist signup form (PHP)
- Has a news fetching script (fetch_news.php)
- No regular content cadence established yet
- Dormant — needs a content strategy and automation plan

## What Exists in the Folder
- `index.html` — landing page
- `mock.html` — mock draft content
- `TGGlogo.png` — brand logo
- `50s diner copy.png` — design reference
- `fetch_news.php` — news aggregation script
- `signup_waitlist.php` — email capture
- `mockdraft.png` — visual asset

## Autonomous Workflow (Phase 2 Target)
### During NFL Season (Sept-Feb)
1. Pull weekly NFL stats, injuries, matchups from public APIs or web search
2. Generate weekly newsletter content: start/sit advice, waiver wire picks, matchup analysis
3. Write in Kevin's voice (see Ghostwriter CLAUDE.md for voice DNA)
4. Publish to thegridirongazette.com
5. Cadence: Weekly (Wednesdays or Thursdays, before Sunday games)

### Offseason (Feb-Aug)
1. Monthly content: draft analysis, dynasty rankings, keeper strategy
2. Mock draft content
3. Cadence: Monthly

## Content Style
- **Tone:** Fun, opinionated, slightly contrarian. Not ESPN corporate, not Reddit degenerate. Somewhere in between.
- **Kevin's angle:** "What do you do when your entire league is going zero RB?" — he thinks about strategy, not just rankings
- **Format:** Newsletter-style with sections (hot takes, waiver wire, matchup spotlight)
- **Data:** Use real stats but don't drown in them. Stats support stories, not the other way around.

## What SodClaw Needs to Know
- This is a greenfield content operation — the content format, cadence, and distribution need to be defined
- Kevin ran fantasy football content as conversation-based work last year, never formalized it
- thegridirongazette.com is a separate domain from meatbagmade.com
- The PHP scripts suggest it was built for a basic web host (not WordPress)
- This project needs a content strategy before automation can kick in
- NFL season starts September — there's time to build the system
- Kevin also has a Fantasy Football Agent concept (podcast-capable) in his ideas backlog
