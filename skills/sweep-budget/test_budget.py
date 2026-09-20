#!/usr/bin/env python3
"""
Proof for the budget guard.

Scenario 1: a normal sweep run fits under the cap, and Opus is the minority of
            spend (cheap-checker principle holds).
Scenario 2: a runaway crawl (10x tokens) trips the cap and the loop STOPS before
            the next expensive stage runs — partial result, no overspend.
Scenario 3: tier routing is correct (crawl/verify/gate=haiku, reconcile=opus).

Run: python3 test_budget.py
"""
from budget import BudgetRun, tier_for, model_for, load_config

cfg = load_config()


def scenario_1():
    print("=" * 60, "\nSCENARIO 1 — normal run fits, Opus stays minority\n", "=" * 60, sep="")
    run = BudgetRun(cfg)
    # Realistic per-stage actuals (near the estimates), no escalation needed.
    plan = [("crawl", 11000), ("reconcile", 17000), ("verify", 9000), ("gate", 3000)]
    for stage, actual in plan:
        ok, decision = run.check(stage)
        assert ok, f"unexpected stop at {stage}: {decision}"
        run.charge(stage, actual)
    s = run.summary()
    print("summary:", s)
    assert s["under_cap"]
    assert s["opus_share"] < 0.5, "Opus should be the minority of a healthy run"
    print(f"✓ run fit under cap ({s['total']}/{s['cap']}); "
          f"Opus only {int(s['opus_share']*100)}% of spend\n")


def scenario_2():
    print("=" * 60, "\nSCENARIO 2 — runaway crawl trips the cap, STOP before next stage\n", "=" * 60, sep="")
    run = BudgetRun(cfg)
    # Crawl explodes (e.g. node_modules slipped the exclusions): 85k instead of ~12k.
    ok, _ = run.check("crawl")
    assert ok
    run.charge("crawl", 85000)
    # Now the expensive reconcile stage is checked BEFORE it runs:
    ok, decision = run.check("reconcile")
    print("decision:", decision["message"])
    assert ok is False, "should have stopped before reconcile"
    assert decision["action"] == "stop_before_next_stage"
    assert decision["stage_blocked"] == "reconcile"
    # Critical: the expensive Opus stage never got charged.
    assert "reconcile" not in [e["stage"] for e in run.log]
    print("✓ stopped before the Opus stage ran — partial result, no silent overspend\n")


def scenario_3():
    print("=" * 60, "\nSCENARIO 3 — tier routing correct\n", "=" * 60, sep="")
    expect = {"crawl": "haiku", "reconcile": "opus", "verify": "haiku",
              "gate": "haiku", "escalated_call": "opus"}
    for stage, tier in expect.items():
        got = tier_for(stage, cfg)
        print(f"  {stage:15} -> {got:6} ({model_for(stage, cfg)})")
        assert got == tier, f"{stage} should be {tier}, got {got}"
    print("✓ cheap models on crawl/verify/gate; Opus only on judgment\n")


if __name__ == "__main__":
    scenario_1()
    scenario_2()
    scenario_3()
    print("=" * 60)
    print("RESULT: normal run fits with Opus minority; runaway trips the cap")
    print("        before the expensive stage; tiers route correctly.")
    print("=" * 60)
