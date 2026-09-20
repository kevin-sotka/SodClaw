#!/usr/bin/env python3
"""
sweep-budget — the budget guard for the portfolio-sweep loop.

Two jobs:
  1. tier_for(stage)  -> which model a stage should run on (cheap vs. expensive).
  2. A BudgetRun that tracks cumulative tokens across stages and STOPS the loop
     before a stage if running it would breach the per-run cap — returning a
     partial-result decision instead of silently overspending.

The cap barely matters on a weekly sweep; this exists to build the tiering
muscle for higher-cadence loops (content pipelines) where it bites for real.

Pure logic, no API calls — the loop reports actual tokens used per stage via
.charge(); budget.py just accounts and decides.
"""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))


def load_config(path=None):
    with open(path or os.path.join(_HERE, "budget.json")) as f:
        return json.load(f)


def tier_for(stage, cfg=None):
    cfg = cfg or load_config()
    for s in cfg["stages"]:
        if s["stage"] == stage:
            return s["tier"]
    raise KeyError(f"unknown stage '{stage}'")


def model_for(stage, cfg=None):
    cfg = cfg or load_config()
    return cfg["tiers"][tier_for(stage, cfg)]["model"]


class BudgetRun:
    """
    Accounts tokens across a single sweep run and gates each stage against the cap.

    Usage per stage:
        ok, decision = run.check(stage)   # BEFORE running the stage
        if not ok: stop_with(decision)    # partial result, don't run stage
        ...run the stage...
        run.charge(stage, actual_tokens)  # AFTER, record what it really cost
    """
    def __init__(self, cfg=None):
        self.cfg = cfg or load_config()
        self.cap = self.cfg["caps"]["per_run_tokens"]
        self.spent = 0
        self.log = []
        self._est = {s["stage"]: s["est_tokens"] for s in self.cfg["stages"]}
        self._conditional = {s["stage"] for s in self.cfg["stages"]
                             if s.get("conditional")}

    def check(self, stage):
        """Would running `stage` (at its estimate) breach the cap? Decide BEFORE spend."""
        est = self._est.get(stage)
        if est is None:
            raise KeyError(f"unknown stage '{stage}'")
        projected = self.spent + est
        if projected > self.cap:
            return False, {
                "action": self.cfg["caps"]["on_exceed"],
                "stage_blocked": stage,
                "tier": tier_for(stage, self.cfg),
                "spent": self.spent,
                "stage_estimate": est,
                "projected": projected,
                "cap": self.cap,
                "message": (f"Stopping before '{stage}': projected {projected} tokens "
                            f"> cap {self.cap}. Returning partial result "
                            f"(spent {self.spent} so far)."),
            }
        return True, {"action": "proceed", "stage": stage,
                      "projected": projected, "cap": self.cap}

    def charge(self, stage, actual_tokens):
        """Record actual tokens a stage used."""
        self.spent += actual_tokens
        self.log.append({"stage": stage, "tokens": actual_tokens,
                         "cumulative": self.spent, "tier": tier_for(stage, self.cfg)})
        return self.spent

    def summary(self):
        opus = sum(e["tokens"] for e in self.log
                   if e["tier"] == "opus")
        haiku = sum(e["tokens"] for e in self.log
                    if e["tier"] == "haiku")
        return {
            "total": self.spent, "cap": self.cap, "under_cap": self.spent <= self.cap,
            "opus_tokens": opus, "haiku_tokens": haiku,
            "opus_share": round(opus / self.spent, 3) if self.spent else 0.0,
            "stages_run": [e["stage"] for e in self.log],
        }
