#!/usr/bin/env python3
"""
Round-trip proof for the sweep gate.

Scenario 1: 3 held proposals, reply 'yes 1 and 3, no 2'
  -> #1 and #3 apply to a test portfolio, #2 dropped, none carried (all decided).
Scenario 2: 3 proposals, reply only mentions #1
  -> #1 applies, #2/#3 carry forward as pending.
Scenario 3: an approved proposal that names a forbidden field
  -> gate REFUSES, nothing written (constitutional boundary).

Run: python3 test_gate.py
"""
import copy
from gate import (load_ledger, add_proposals, parse_reply, record_decisions,
                  apply_approved, carried_forward, prune_resolved)

TODAY = "2026-06-29"

# A minimal fake portfolio
PORTFOLIO = {
    "_meta": {"last_updated": "2026-06-26"},
    "projects": [
        {"id": "oregon_fail", "status": "exploratory", "progress": 10},
        {"id": "train_lore", "status": "active", "progress": 40,
         "value": {"reach": 3}, "complexity": {"engineering": 1}},
        {"id": "the_wall", "status": "active", "progress": 55},
    ],
}

HELD = [
    {"kind": "shelve", "target": "oregon_fail",
     "summary": "Shelve Oregon Fail — 138 days idle?", "change": {"status": "shelved"}},
    {"kind": "progress", "target": "the_wall",
     "summary": "Bump The Wall 55% → 60%?", "change": {"progress": 60}},
    {"kind": "rescore", "target": "train_lore",
     "summary": "Re-score train_lore reach 3 → 4?",
     "change": {"value": {"reach": 4}}},
]


def fresh_ledger():
    led = load_ledger("/nonexistent-so-empty.json")
    return add_proposals(led, copy.deepcopy(HELD), TODAY)


def scenario_1():
    print("=" * 60, "\nSCENARIO 1 — 'yes 1 and 3, no 2'\n", "=" * 60, sep="")
    led = fresh_ledger()
    pf = copy.deepcopy(PORTFOLIO)
    pending = [p["id"] for p in led["proposals"]]
    decisions = parse_reply("yes 1 and 3, no 2", pending)
    print("parsed:", decisions)
    assert decisions == {1: "approved", 3: "approved", 2: "rejected"}
    record_decisions(led, decisions, TODAY)
    pf, applied = apply_approved(led, pf, TODAY)
    print("applied:", applied)
    by = {p["id"]: p for p in pf["projects"]}
    assert by["oregon_fail"]["status"] == "shelved"          # #1 applied
    assert by["train_lore"]["value"]["reach"] == 4           # #3 applied
    assert by["the_wall"]["progress"] == 55                  # #2 NOT applied (rejected)
    assert carried_forward(led) == []                        # all decided
    print("✓ #1 shelved, #3 re-scored, #2 left untouched (rejected), nothing carried\n")


def scenario_2():
    print("=" * 60, "\nSCENARIO 2 — reply only mentions #1 (silence on 2,3)\n", "=" * 60, sep="")
    led = fresh_ledger()
    pf = copy.deepcopy(PORTFOLIO)
    pending = [p["id"] for p in led["proposals"]]
    decisions = parse_reply("yes 1", pending)
    print("parsed:", decisions)
    assert decisions == {1: "approved"}                      # 2 and 3 NOT decided
    record_decisions(led, decisions, TODAY)
    pf, applied = apply_approved(led, pf, TODAY)
    print("applied:", applied)
    carried = carried_forward(led)
    carried_ids = sorted(p["id"] for p in carried)
    print("carried forward:", carried_ids)
    assert carried_ids == [2, 3]                             # silence => carry, not apply
    assert pf["projects"][2]["progress"] == 55               # the_wall untouched (silence)
    print("✓ #1 applied; #2 and #3 carried forward as pending (silence is never a yes)\n")


def scenario_3():
    print("=" * 60, "\nSCENARIO 3 — approved proposal names a FORBIDDEN field\n", "=" * 60, sep="")
    led = load_ledger("/nonexistent-so-empty.json")
    bad = [{"kind": "rescore", "target": "train_lore",
            "summary": "sneaky autonomy flip",
            "change": {"value": {"reach": 5}, "autonomy": "full-auto"}}]  # forbidden!
    add_proposals(led, bad, TODAY)
    record_decisions(led, {1: "approved"}, TODAY)
    pf = copy.deepcopy(PORTFOLIO)
    try:
        apply_approved(led, pf, TODAY)
        raise SystemExit("FAIL: gate applied a forbidden-field proposal!")
    except ValueError as e:
        print("refused as expected:", e)
        # portfolio untouched
        assert pf["projects"][1].get("autonomy") is None
    print("✓ gate refused the forbidden-field write; portfolio untouched\n")


if __name__ == "__main__":
    scenario_1()
    scenario_2()
    scenario_3()
    print("=" * 60)
    print("RESULT: approvals apply, rejections drop, silence carries forward,")
    print("        forbidden-field writes are refused. Gate round-trip holds.")
    print("=" * 60)
