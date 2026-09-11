# Public Portfolio Page — meatbagmade.com/projects

`projects.html` is the WordPress-ready fragment. `projects-preview.html` is the same thing wrapped in a full document — double-click it to preview in a browser.

## Publish (first time, ~5 min)

1. WP Admin → **Pages → Add New**. Title: "Projects" (slug `projects`).
2. Add a **Custom HTML** block. Paste the entire contents of `projects.html`.
3. Preview → Publish. Your theme's header/footer wrap it automatically; all styles are scoped (`mbm-` prefix) so nothing should clash.

## Update cycle

1. Edit blurbs/links/labels in `projects/portfolio.json` (each public project's `public` field; Doc's intro is in `_meta.public_page.doc_intro`). Voice rules: `prompts/doc_voice.md`.
2. Run `python3 SodClaw/build_public_page.py`
3. Re-paste `projects.html` into the WP page.

Later, step 3 can be automated via the WordPress REST API (app password + `POST /wp-json/wp/v2/pages/<id>`) — same hook the train-blog auto-publish would use.

## Card titles

By default a card is titled with the project name up to the em dash. Set `public.name` in
`portfolio.json` when the internal project name isn't the public one (e.g. `kevinsotka_com`
shows as "Business & AI Consulting").

## Open items

- **hitfactory.games**: the card links there, but the domain timed out on 2026-09-04 and its
  DNS still points at a Namecheap parking IP. Confirm `site/dist/` is actually being served
  before this page goes live, or the studio card sends folks to a parked page.
- Individual game cards are folded into the Hit Factory Games tile (2026-09-04). Riventide is
  the one exception and still has its own card. If a game deserves a spotlight, give it back a
  `public` block — otherwise the studio site is the game browser.
- Within a label, cards run linked-first then portfolio order. The meatbagmade.com front-door
  card lands 4th among the Live ones; add an explicit sort key if you want it leading.
