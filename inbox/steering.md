# Steering inbox

Kevin steers SodClaw and DoClaw from the Claude app. Each reply he gives there is added to the **Open** list below, one line per item, newest at the bottom. Slack is send-only for now, so this file is how direction reaches the nightly run.

## How runs use this file

1. Every DoClaw run (6pm Pacific, 7pm on Fridays after the sweep) and every SodClaw sweep reads this file before doing anything else.
2. The run acts on each open item that belongs to it, then moves that item to **Handled** with the date and a few words on what it did.
3. The next 6am digest lists every item handled since the last digest, so Kevin knows each one was heard.
4. An item a run can't act on stays open, and the digest says why.

## Commands

Every proposal and decision posted to Slack carries a short ID, such as `LL-014` (LL = The Lookout Logs, TL = Train Lore, HF = hitfactory.games, S22 = Simulation 22, TG = touchgrass.guru).

| Command | What it does |
| --- | --- |
| `go LL-014` | Approves a proposal now instead of waiting 24 hours |
| `veto LL-014` | Cancels it; the crew picks the next-best option |
| `hold LL-014` | Parks the item until Kevin says go |
| `redo LL-014: <note>` | Sends the work back with that direction |
| `note <project>: <guidance>` | Adds standing direction to that project's CLAUDE.md |
| `pause all` / `resume` | Turns the PAUSE switch on or off for every project |

Plain sentences are fine too. If an item doesn't match a command, the run treats it as direction for the project it names and says in the digest how it read it.

## Open

<!-- Add new items below this line, one per line, as: - YYYY-MM-DD: <command or note> -->

## Handled

<!-- Runs move items here as: - YYYY-MM-DD handled YYYY-MM-DD: <item> -> <what was done> -->
