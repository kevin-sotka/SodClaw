# PNW Rail Events — Source Scrapeability Audit

**Date:** 2026-07-31
**Question asked:** Are PNW rail event sources structured enough to aggregate without manual maintenance Kevin won't do?
**Verdict:** BUILD, but not as a scraper. See "The Reframe" below.

---

## The Reframe (most important finding)

The scrapeability question was the wrong question.

**This data is low-churn.** Almost every source publishes an entire season or year at once:

- Museums announce a full excursion season in one go (NW Railway Museum: "Saturdays Feb–Mar, Sat & Sun Apr–Sep")
- Live steam parks post one seasonal pattern per year (Shady Dell: "Sundays May 3 – Oct 25, plus 3 special weekends")
- Model RR clubs run exactly 2 open houses a year (spring + holiday), same weekends annually
- Swap meets are annual, on a stable weekend (Portland Swap Meet = late Feb; WCMRRC Eugene = mid-Feb)
- The seasonal tentpoles repeat forever: Polar Express (Nov–Dec), Day Out With Thomas (July), Halloween trains (Oct), National Train Day (May)

The whole PNW rail calendar is roughly **40 to 60 events a year**, and maybe 15% of it changes between years.

That is not a scraping pipeline. That is a curated data file plus a periodic change-check.

---

## Source-by-source

### GREEN — real structured data available

| Source | Location | Signal |
|---|---|---|
| **Chehalis-Centralia Railroad & Museum** | Chehalis, WA | Runs **The Events Calendar** WP plugin (`meta-tec-api-version: v1`) → clean JSON at `/wp-json/tribe/events/v1/events`. Also FareHarbor for ticketing. Best-structured source found. |
| **Columbia Gorge Model RR Historical Society** | Portland, OR | Squarespace Events collection. Per-event **ICS export** (`?format=ical`) and Google Calendar links. Collection supports `?format=json`. |
| **Mt. Hood Railroad** | Hood River, OR | **FareHarbor** booking platform (embeds + availability endpoints). Seasonal trains are named products with date ranges. |
| **Northwest Railway Museum** | Snoqualmie, WA | `/upcoming-events/` page with consistent structure. Ticketing via TicketWeb/Ticketmaster (both have venue event feeds). |
| **trainshows.net** | national, filterable by state | Already a structured per-state, per-year train show calendar (`calendar.php?loc=usOR&year=2026`). |
| **railfan.com `/wrp_timetable/`** | national | Structured event listing entries for swap meets and shows. |

### YELLOW — parseable, or stable enough to hand-enter once

| Source | Location | Signal |
|---|---|---|
| **Shady Dell / Pacific NW Live Steamers** | Molalla, OR | WordPress, but schedule is a homepage prose paragraph. No event objects. **Changes once a year.** Hand-enter. |
| **Oregon Rail Heritage Foundation** | Portland, OR | ⚠️ Their `/events` page is **stale since 2019** (still lists 2019 Holiday Express). Real 2026 news lives in `/blog/category/events/` → WordPress RSS. Use the blog feed, not the events page. |
| **Oregon Coast Scenic Railroad** | Garibaldi, OR | Fetch returned empty; likely JS-rendered. Needs a browser-based read, or hand-enter. |
| **Willamette Model RR Club / WCMRRC** | Portland + Eugene | Club sites with annual swap meets. Same weekend most years. Hand-enter. |

### RED — skip
- Facebook-events-only clubs. Not worth the fight.

### Not yet checked (add in v1 pass)
Mount Rainier Scenic RR (Elbe WA), Chelatchie Prairie RR (Yacolt WA — closest to Vancouver), Sumpter Valley Railway, Oregon Electric Railway Museum / Antique Powerland (Brooks OR), Train Mountain (Chiloquin OR — largest live steam in the world), Lake Whatcom Railway, Yakima Valley Trolleys, Rose City Garden Railway Society, Willamette Shore Trolley, Astoria Riverfront Trolley.

---

## Competitive read

Existing aggregators: `trainshows.net`, `trainshowlist.com`, `railfan.com` timetable, `american-rails.com`.

All of them are **national and category-siloed** — they cover model train shows OR scenic railroads, never both, and never live steam parks or club open houses together. None are regional. None have editorial voice. None tell you which one is worth your Saturday.

**The gap:** one PNW page that puts excursions, museums, live steam, club open houses, and swap meets on the same calendar, written by someone who actually went.

---

## Recommended build (v1)

**Not a directory product. An events page on meatbagmade.com.**

1. `events.yaml` in the train_lore repo — ~40 hand-curated events, each with date/recurrence, org, location, category, link, and a one-line Kevin note.
2. Static page rendered from it. Sorted by date, filterable by category.
3. A monthly SodClaw check-run against the GREEN sources (TEC JSON, Squarespace JSON, FareHarbor, trainshows.net) that diffs against `events.yaml` and opens a "these changed" list for Kevin to ratify. Draft-and-approve, not auto-write.
4. Each event Kevin actually attends becomes a train_lore post. The calendar feeds the blog; the blog feeds the calendar.

**Why this shape:** zero cold-start (no user signups needed), no new project folder, rides an existing autonomous-tier project, and the maintenance burden is quarterly rather than continuous — which is the only kind Kevin will actually do.

**Kill criteria:** if the events page draws no organic traffic in 90 days, it stays a small page and never becomes a product.

---

## Sources

- [Oregon Rail Heritage Foundation](https://orhf.org/)
- [Columbia Gorge Model Railroad Historical Society — Events](https://www.cgmrhs.org/events)
- [Shady Dell Train Park / Pacific NW Live Steamers](https://www.shadydell.org/)
- [Northwest Railway Museum — Upcoming Events](https://trainmuseum.org/upcoming-events/)
- [Mt. Hood Railroad](https://www.mthoodrr.com/)
- [Chehalis-Centralia Railroad & Museum](https://steamtrainride.com/)
- [Oregon Coast Scenic Railroad](https://oregoncoastscenic.org/)
- [2026 Oregon Train Show Calendar — TrainShows.net](https://trainshows.net/calendar/calendar.php?loc=usOR&year=2026)
- [The Train Show List](https://www.trainshowlist.com/)
- [Railfan & Railroad — Portland Oregon Swap Meet](https://railfan.com/wrp_timetable/portland-oregon-swap-meet/)
- [Willamette Model Railroad Club](https://wmrrc.com/)
- [WCMRRC Shows and Events](https://wcmrrc.com/shows-and-events)
