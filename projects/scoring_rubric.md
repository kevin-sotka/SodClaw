# Portfolio Scoring Rubric

> How SodClaw scores every project so the dashboard can rank, sort, and surface decisions. All sub-scores are **1–5** (1 = low, 5 = high). The composite is the simple mean of the four sub-scores. `portfolio.json` is the source of truth; this file explains what the numbers mean.

---

## VALUE — "Is this worth Kevin's hour?"

| Metric | 1 | 3 | 5 |
|---|---|---|---|
| **Consumer potential** | Niche / personal | A real but small audience wants it | Broad market appeal |
| **Personal satisfaction** | A chore | Pleasant | Recharges Kevin / pure joy |
| **Reach** | Handful of people | Hundreds | Thousands+ potential users |
| **Profitability** | No revenue path | Indirect (audience → clients later) | Direct, clear revenue |

**Value composite** = mean of the four. Higher = more worth defending against the 80% wall.

## COMPLEXITY — "What will it cost to run?"

| Metric | 1 | 3 | 5 |
|---|---|---|---|
| **Engineering** | Write text / edit a file | Standard web app | Novel/hard stack (3D, crypto, ML) |
| **Review frequency** | Set-and-forget | Periodic check-ins | Kevin must approve every output |
| **Integrations** | Self-contained | 2–3 systems | Many systems wired together |
| **Manual burden** | Fully automatable | Some hand-work | Heavy ongoing manual effort |

**Complexity composite** = mean of the four. Higher = harder for SodClaw to run autonomously and more likely to stall.

---

## How the dashboard uses these

- **Value vs. Complexity quadrant** plots every project. The sweet spot is **high value / low complexity** (top-left) — those are the "just ship it" projects SodClaw should push hardest.
- **High value / high complexity** = worth doing but needs a real plan and protected time.
- **Low value / high complexity** = shelve candidates.
- **Review frequency** and **manual burden** specifically drive the **"Needs your attention"** panel and the autonomy level — a project can't be full-auto if it scores high on review frequency.
- **Progress %** is a separate, judgment-based estimate of how far the project is toward its current goal. It feeds the **80% Watch**: anything ≥80% gets flagged hard.

## Updating scores

Scores are deliberately subjective and are **Kevin's to ratify.** SodClaw proposes; Kevin adjusts. Re-score whenever a project materially changes (ships a milestone, gains/loses a revenue path, gets simpler to run). Update `portfolio.json`, then regenerate the dashboard.
