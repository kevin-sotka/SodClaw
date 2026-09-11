#!/usr/bin/env python3
"""
sweep-verifier — executable core of the checker half of the portfolio-sweep loop.

Given (a) ground truth: per-folder real last-modified date + git state, and
(b) a maker's draft: the projects it claims "moved", proposed shelve-candidates,
and proposed auto-writes — grade the draft against truth on five checks.

This is the deterministic spine the Haiku SKILL.md follows. Pure functions,
no I/O against the live tracker, no writes. Returns a verdict dict.

Checks:
  1. Completeness            — every truly-moved folder is reported as moved
  2. No hallucinated movement— every "moved" claim has a real change since last sweep
  3. Number provenance       — every changed last_touched traces to a real mtime
  4. Stale-rule correctness  — shelve-candidates are really 60+ idle, active/exploratory,
                               and have no uncommitted work
  5. Gate-safety             — no proposed auto-write touches status/score/progress/gate
                               (CONSTITUTIONAL: a fail here never auto-corrects)
"""
from datetime import date

IGNORED_DELTA_FILES = {".DS_Store", "package-lock.json", "yarn.lock", "Cargo.lock"}
SHELVEABLE_STATUSES = {"active", "exploratory"}
# Fields that may NEVER be written automatically — only proposed for Kevin to ratify.
HELD_FIELDS = {"status_to_shelved", "score", "progress", "value", "complexity"}
GATE_FIELDS = {"approval_rule", "gate", "autonomy"}


def _days_between(iso_a, iso_b):
    return (date.fromisoformat(iso_a) - date.fromisoformat(iso_b)).days


def verify(ground_truth, draft, last_swept, today):
    """
    ground_truth: { folder: {"last_modified": "YYYY-MM-DD", "delta_file": str,
                             "uncommitted": int, "status": str} }
    draft: {
        "moved":            [folder, ...],                # claimed moved this week
        "last_touched":     {folder: "YYYY-MM-DD"},       # proposed last_touched writes
        "shelve_candidates":[{"folder":..., "idle_days":...}, ...],
        "auto_writes":      [{"folder":..., "field":...}, ...],  # what it wants to write unattended
    }
    """
    results = {}

    # --- Check 1: Completeness -------------------------------------------------
    truly_moved = {
        f for f, gt in ground_truth.items()
        if _days_between(gt["last_modified"], last_swept) > 0
        and gt.get("delta_file") not in IGNORED_DELTA_FILES
    }
    missed = sorted(truly_moved - set(draft["moved"]))
    results["1_completeness"] = {
        "status": "PASS" if not missed else "FAIL",
        "detail": "all moved folders reported" if not missed
        else f"moved but unreported: {missed}",
    }

    # --- Check 2: No hallucinated movement ------------------------------------
    halluc = []
    for f in draft["moved"]:
        gt = ground_truth.get(f)
        if gt is None:
            halluc.append(f"{f} (no ground truth)")
        elif _days_between(gt["last_modified"], last_swept) <= 0:
            halluc.append(f"{f} (newest {gt['last_modified']} <= last sweep {last_swept})")
        elif gt.get("delta_file") in IGNORED_DELTA_FILES:
            halluc.append(f"{f} (only change is ignored file {gt['delta_file']})")
    results["2_no_hallucinated_movement"] = {
        "status": "PASS" if not halluc else "FAIL",
        "detail": "every moved claim has a real change" if not halluc
        else "hallucinated: " + "; ".join(halluc),
    }

    # --- Check 3: Number provenance -------------------------------------------
    bad_dates = []
    for f, claimed in draft.get("last_touched", {}).items():
        gt = ground_truth.get(f)
        if gt is None or claimed != gt["last_modified"]:
            real = gt["last_modified"] if gt else "none"
            bad_dates.append(f"{f}: claimed {claimed}, real mtime {real}")
    results["3_number_provenance"] = {
        "status": "PASS" if not bad_dates else "FAIL",
        "detail": "every date traces to a real mtime" if not bad_dates
        else "; ".join(bad_dates),
    }

    # --- Check 4: Stale-rule correctness --------------------------------------
    bad_stale = []
    for cand in draft.get("shelve_candidates", []):
        f = cand["folder"]
        gt = ground_truth.get(f)
        if gt is None:
            bad_stale.append(f"{f} (no ground truth)")
            continue
        real_idle = _days_between(today, gt["last_modified"])
        if real_idle < 60:
            bad_stale.append(f"{f} (only {real_idle}d idle, not 60+)")
        if gt.get("status") not in SHELVEABLE_STATUSES:
            bad_stale.append(f"{f} (status {gt.get('status')} not shelveable)")
        if gt.get("uncommitted", 0) > 0:
            bad_stale.append(f"{f} ({gt['uncommitted']} uncommitted files = active work)")
    results["4_stale_rule_correctness"] = {
        "status": "PASS" if not bad_stale else "FAIL",
        "detail": "shelve candidates valid" if not bad_stale else "; ".join(bad_stale),
    }

    # --- Check 5: Gate-safety (CONSTITUTIONAL) ---------------------------------
    violations = []
    for w in draft.get("auto_writes", []):
        field = w.get("field")
        if field in HELD_FIELDS or field in GATE_FIELDS:
            violations.append(f"{w.get('folder','?')}: auto-write to held/gate field '{field}'")
    results["5_gate_safety"] = {
        "status": "PASS" if not violations else "FAIL",
        "detail": "no held/gate field auto-written" if not violations
        else "; ".join(violations),
        "constitutional": True,
    }

    # --- Overall ---------------------------------------------------------------
    statuses = [r["status"] for r in results.values()]
    gate_failed = results["5_gate_safety"]["status"] == "FAIL"
    overall = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"
    failed = [k for k, r in results.items() if r["status"] == "FAIL"]

    if overall == "PASS":
        action = "post report + apply safe writes; held proposals to in-app gate"
    elif gate_failed:
        action = "STOP — gate-safety fail is constitutional, never auto-corrected. Flag Kevin."
    else:
        action = "send back for ONE corrective re-run; stop+flag if it fails again"

    return {"overall": overall, "checks": results, "failed": failed, "action": action}


def render(verdict, run_date):
    lines = [f"SWEEP VERIFIER — {run_date}", f"Overall: {verdict['overall']}", ""]
    names = {
        "1_completeness": "Completeness",
        "2_no_hallucinated_movement": "No hallucinated movement",
        "3_number_provenance": "Number provenance",
        "4_stale_rule_correctness": "Stale-rule correctness",
        "5_gate_safety": "Gate-safety",
    }
    for i, key in enumerate(names, 1):
        r = verdict["checks"][key]
        dots = "." * max(2, 28 - len(names[key]))
        line = f"{i}. {names[key]} {dots} {r['status']}"
        if r["status"] != "PASS":
            line += f" — {r['detail']}"
        lines.append(line)
    lines += ["", f"Action: {verdict['action']}"]
    return "\n".join(lines)
