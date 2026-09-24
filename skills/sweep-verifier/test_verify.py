#!/usr/bin/env python3
"""
Seeded-error proof for the sweep verifier.

Builds synthetic ground truth, then runs TWO drafts through the verifier:
  A) a CLEAN report that matches truth   -> must come back PASS
  B) a SEEDED-BAD report with 4 planted errors -> must catch all 4

Run: python3 test_verify.py
"""
from verify import verify, render

LAST_SWEPT = "2026-06-19"
TODAY = "2026-06-28"

# --- Ground truth: what actually happened on disk -------------------------
GROUND_TRUTH = {
    "train_lore":  {"last_modified": "2026-06-25", "delta_file": "post6.md",
                    "uncommitted": 0, "status": "active"},      # really moved
    "gridiron":    {"last_modified": "2026-06-22", "delta_file": "week3.html",
                    "uncommitted": 0, "status": "active"},      # really moved
    "riventide":   {"last_modified": "2026-04-02", "delta_file": ".DS_Store",
                    "uncommitted": 0, "status": "exploratory"}, # did NOT move (old + ignored file)
    "gerlok":      {"last_modified": "2026-06-16", "delta_file": "notes.md",
                    "uncommitted": 3, "status": "exploratory"}, # 12d idle, has uncommitted work
    "oregon_fail": {"last_modified": "2026-02-10", "delta_file": "main.js",
                    "uncommitted": 0, "status": "exploratory"}, # genuinely stale (138d)
}

# --- Draft A: CLEAN — matches truth ---------------------------------------
CLEAN = {
    "moved": ["train_lore", "gridiron"],
    "last_touched": {"train_lore": "2026-06-25", "gridiron": "2026-06-22"},
    "shelve_candidates": [{"folder": "oregon_fail", "idle_days": 138}],
    "auto_writes": [
        {"folder": "train_lore", "field": "last_touched"},
        {"folder": "gridiron", "field": "last_touched"},
        {"folder": "_meta", "field": "last_swept"},
    ],
}

# --- Draft B: SEEDED-BAD — 4 planted errors -------------------------------
SEEDED_BAD = {
    # ERROR 1 (Check 2): claims riventide moved — its only change is a .DS_Store from April
    # ERROR also feeds Check 1: gridiron really moved but is omitted here
    "moved": ["train_lore", "riventide"],
    # ERROR 2 (Check 3): train_lore last_touched dated wrong (claims 28th, real is 25th)
    "last_touched": {"train_lore": "2026-06-28"},
    # ERROR 3 (Check 4): gerlok proposed for shelve but it's 12d idle w/ uncommitted work
    "shelve_candidates": [{"folder": "gerlok", "idle_days": 71}],
    # ERROR 4 (Check 5, CONSTITUTIONAL): auto-write flips a status to shelved unattended
    "auto_writes": [
        {"folder": "oregon_fail", "field": "status_to_shelved"},
    ],
}


def main():
    print("=" * 64)
    print("DRAFT A — CLEAN REPORT (expect: PASS on all 5)")
    print("=" * 64)
    va = verify(GROUND_TRUTH, CLEAN, LAST_SWEPT, TODAY)
    print(render(va, TODAY))
    assert va["overall"] == "PASS", "CLEAN report should PASS but didn't!"
    print("\n  ✓ clean report passed, as expected\n")

    print("=" * 64)
    print("DRAFT B — SEEDED-BAD REPORT (expect: catch 4 planted errors)")
    print("=" * 64)
    vb = verify(GROUND_TRUTH, SEEDED_BAD, LAST_SWEPT, TODAY)
    print(render(vb, TODAY))

    # Prove each planted error was caught by the right check
    expected_fails = {
        "1_completeness",              # gridiron moved but omitted
        "2_no_hallucinated_movement",  # riventide didn't really move
        "3_number_provenance",         # train_lore date wrong
        "4_stale_rule_correctness",    # gerlok wrongly flagged stale
        "5_gate_safety",               # unattended status->shelved
    }
    got = set(vb["failed"])
    print("\n  Planted errors the verifier was expected to catch:")
    for c in sorted(expected_fails):
        hit = "✓ caught" if c in got else "✗ MISSED"
        print(f"    {hit}: {c}")
    assert expected_fails.issubset(got), f"missed: {expected_fails - got}"
    assert vb["overall"] == "FAIL"
    # gate-safety fail must route to STOP, not a retry
    assert "STOP" in vb["action"], "gate-safety fail must stop the loop, not retry"
    print("\n  ✓ all 4 seeded errors caught (across 5 checks)")
    print("  ✓ gate-safety violation correctly routed to STOP (no auto-retry)\n")

    print("=" * 64)
    print("RESULT: verifier passes the clean report and catches every seeded error.")
    print("=" * 64)


if __name__ == "__main__":
    main()
