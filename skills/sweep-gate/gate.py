#!/usr/bin/env python3
"""
sweep-gate — the in-app approval gate for the portfolio-sweep loop.

The verifier produces HELD proposals (shelve X, re-score Y, onboard Z). Those
must never be written unattended — only Kevin may ratify them. This module is
the durable half of "reply in the thread": it persists held proposals to a
pending ledger so an unanswered proposal survives across runs, parses Kevin's
natural-language reply into per-proposal decisions, and applies ONLY the ones
he explicitly approved.

Design contract:
  * A proposal applies if and only if it was EXPLICITLY approved. Silence != yes.
  * Rejected proposals are dropped (logged). Unanswered ones carry forward.
  * The gate writes to portfolio.json only for approved proposals, and only the
    fields that proposal names. It can never edit an approval rule or the gate.

Ledger entry shape (portfolio_proposals.json):
  {
    "id": 1,
    "kind": "shelve" | "rescore" | "progress" | "onboard",
    "target": "<project id or folder name>",
    "summary": "human-readable one-liner shown in the thread",
    "change": { ...kind-specific payload the apply step needs... },
    "status": "pending" | "approved" | "rejected" | "applied",
    "raised": "YYYY-MM-DD",
    "decided": "YYYY-MM-DD" | null
  }
"""
import json
import re
from datetime import date

# Fields the gate is ALLOWED to touch when applying, per kind. Anything outside
# this map is refused — the gate cannot become a general-purpose writer.
ALLOWED_CHANGE = {
    "shelve":   {"status"},                 # status -> "shelved"
    "rescore":  {"value", "complexity"},    # score dicts
    "progress": {"progress"},               # int
    "onboard":  {"__new_stub__"},           # adds a new project stub
}
# Hard-forbidden no matter what a proposal claims — the constitutional boundary.
FORBIDDEN_FIELDS = {"autonomy", "gate", "approval_rule"}


# ---------------------------------------------------------------- ledger I/O
def load_ledger(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"_meta": {"description": "Pending held proposals awaiting Kevin's "
                          "in-app ratification. The sweep gate reads/writes this."},
                "proposals": []}


def save_ledger(ledger, path):
    with open(path, "w") as f:
        json.dump(ledger, f, indent=2)
        f.write("\n")


def add_proposals(ledger, new_proposals, today):
    """Append freshly-held proposals, assigning stable ids after the current max."""
    existing = ledger["proposals"]
    next_id = max([p["id"] for p in existing], default=0) + 1
    for p in new_proposals:
        p = dict(p)
        p.setdefault("status", "pending")
        p.setdefault("raised", today)
        p.setdefault("decided", None)
        p["id"] = next_id
        next_id += 1
        existing.append(p)
    return ledger


# ------------------------------------------------------------- reply parsing
_YES = {"yes", "y", "approve", "approved", "ok", "okay", "do", "ship", "apply"}
_NO = {"no", "n", "skip", "reject", "rejected", "drop", "don't", "dont"}


def parse_reply(reply, pending_ids):
    """
    Turn a natural-language reply into {id: 'approved'|'rejected'}.
    Handles: 'yes 1 and 3, no 2'  /  'approve all'  /  'reject all'  /
             '1 yes 2 no'  /  'yes to 1, 3-5'. Only ids in pending_ids count.
    Anything not mentioned stays undecided (carries forward).
    Ambiguous -> left undecided (safe default: no application).
    """
    text = reply.lower().strip()
    decisions = {}

    if re.search(r"\b(approve|yes|ship|apply)\s+all\b", text):
        return {i: "approved" for i in pending_ids}
    if re.search(r"\b(reject|no|skip|drop)\s+all\b", text):
        return {i: "rejected" for i in pending_ids}

    # Split into clauses on commas/semicolons only. "and" stays INSIDE a clause
    # so "yes 1 and 3" keeps both ids under the same verb. Within a clause, the
    # verb carries left-to-right and re-arms if a new verb word appears, so
    # "1 yes 2 no" still works.
    clauses = re.split(r"[,;]", text)
    for clause in clauses:
        # Walk tokens in order; assign each number the most recent verb seen.
        verb = None
        for tok in re.findall(r"[a-z']+|\d+\s*-\s*\d+|\d+", clause):
            if tok in _YES:
                verb = "approved"
            elif tok in _NO:
                verb = "rejected"
            elif verb is not None:
                m = re.match(r"(\d+)\s*-\s*(\d+)$", tok)
                if m:
                    for i in range(int(m.group(1)), int(m.group(2)) + 1):
                        if i in pending_ids:
                            decisions[i] = verb
                elif tok.isdigit():
                    i = int(tok)
                    if i in pending_ids:
                        decisions[i] = verb
    return decisions


def record_decisions(ledger, decisions, today):
    for p in ledger["proposals"]:
        if p["id"] in decisions and p["status"] == "pending":
            p["status"] = decisions[p["id"]]
            p["decided"] = today
    return ledger


# --------------------------------------------------------------- apply step
def _refuse(p, reason):
    raise ValueError(f"gate refused proposal {p['id']} ({p['kind']} {p['target']}): {reason}")


def apply_approved(ledger, portfolio, today):
    """
    Apply every status=='approved' proposal to the portfolio dict (in memory).
    Returns (portfolio, applied_log). Caller persists portfolio + ledger.
    Enforces the allow-list: a proposal can only touch its kind's allowed fields,
    never a forbidden one. Silence/rejection never reaches here.
    """
    projects = portfolio.get("projects", [])
    by_id = {pr.get("id"): pr for pr in projects}
    applied = []

    for p in ledger["proposals"]:
        if p["status"] != "approved":
            continue
        kind, change = p["kind"], p.get("change", {})

        # Constitutional refusal: no proposal may name a forbidden field.
        if FORBIDDEN_FIELDS & set(change.keys()):
            _refuse(p, f"names forbidden field(s) {FORBIDDEN_FIELDS & set(change.keys())}")
        allowed = ALLOWED_CHANGE.get(kind)
        if allowed is None:
            _refuse(p, f"unknown kind '{kind}'")

        if kind == "shelve":
            pr = by_id.get(p["target"]) or _refuse(p, "target not found")
            pr["status"] = "shelved"
            applied.append(f"shelved {p['target']}")
        elif kind == "rescore":
            pr = by_id.get(p["target"]) or _refuse(p, "target not found")
            for k in ("value", "complexity"):
                if k in change:
                    pr[k] = change[k]
            applied.append(f"re-scored {p['target']}")
        elif kind == "progress":
            pr = by_id.get(p["target"]) or _refuse(p, "target not found")
            pr["progress"] = int(change["progress"])
            applied.append(f"set {p['target']} progress -> {change['progress']}%")
        elif kind == "onboard":
            stub = change["__new_stub__"]
            stub.setdefault("status", "unknown")
            stub.setdefault("tier", "exploratory")
            projects.append(stub)
            applied.append(f"onboarded {stub.get('id', p['target'])} as stub")

        p["status"] = "applied"
        p["decided"] = p.get("decided") or today

    portfolio["projects"] = projects
    portfolio.setdefault("_meta", {})["last_updated"] = today
    return portfolio, applied


def carried_forward(ledger):
    """Proposals still pending after a round — these survive to next run."""
    return [p for p in ledger["proposals"] if p["status"] == "pending"]


def prune_resolved(ledger):
    """Drop applied + rejected entries once recorded; keep only pending."""
    ledger["proposals"] = [p for p in ledger["proposals"] if p["status"] == "pending"]
    return ledger


def render_for_thread(ledger):
    """The numbered list the sweep posts for Kevin to reply to."""
    pend = [p for p in ledger["proposals"] if p["status"] == "pending"]
    if not pend:
        return "No held proposals — nothing needs your ratification this week."
    lines = ["**Needs your yes/no** (reply e.g. \"yes 1 and 3, no 2\"):"]
    for p in pend:
        age = (date.fromisoformat(date.today().isoformat())
               - date.fromisoformat(p["raised"])).days
        tag = f" _(raised {p['raised']}, {age}d ago)_" if age > 0 else ""
        lines.append(f"{p['id']}. {p['summary']}{tag}")
    return "\n".join(lines)
