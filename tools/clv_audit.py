#!/usr/bin/env python3
"""clv_audit.py — how much of the ledger actually carries a closing line? (READ-ONLY)

WHY THIS EXISTS (audit 8/12/26)
    Doctrine says CLV is MANDATORY and calls it "the best +EV signal at this sample size".
    The ledger disagreed with the doctrine and nobody was counting: on 8/12/26 only **43%**
    of decided legs carried a CLV verdict, and the rate varied enormously by bet type —
    ML 49%, totals 42%, K-props 46%, hitter props 27%, aggregate/'other' 22%, run lines 0%.

    That is not a cosmetic gap. `pulse.py`'s MARKET-SHADE — the action that zeroes an entire
    dimension for a build — triggers on the CLV sign count. So the dimensions we measured
    LEAST were being governed HARDEST, off whichever rows happened to get captured. A
    governor reading a 27%-covered dimension is not measuring that dimension; it is
    measuring the capture process.

    `clv_capture.py` fills rows automatically and `clv_backfill.py` closes historical holes,
    but neither reports whether the ledger as a whole is adequately covered. This does, so
    the hole is visible on every session start instead of being rediscovered by an audit.

USAGE
    tools/clv_audit.py                 # coverage table + the worst-covered dimensions
    tools/clv_audit.py --min 50        # exit 1 if overall coverage is under 50% (CI/selftest)
    tools/clv_audit.py --dates         # per-date coverage, newest first (find the dropped runs)
"""
import argparse
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from calib import (dedup_rows, leg_key, parse_adj_tags,  # noqa: E402
                   parse_result, table_rows)

LEDGER = os.path.join(HERE, "..", "results_log.md")
BLANK = ("", "—", "-", "n/a", "tbd", "?")


def verdict(cell):
    """'+ 52%cl' → '+';  '− (moved)' → '−';  '= 47%cl' → '=';  blank/— → None."""
    v = (cell or "").replace("**", "").strip()
    if v.lower() in BLANK:
        return None
    if v.startswith("+"):
        return "+"
    if v.startswith(("−", "-")):
        return "−"
    if v.startswith("="):
        return "="
    return None


def bet_type(raw):
    t = (raw or "").strip().lower()
    if t.startswith("ml"):
        return "ML"
    if "run line" in t or t == "rl":
        return "run line"
    if "total" in t:
        return "total"
    if t.startswith("k-"):
        return "K-prop"
    if "prop" in t:
        return "hitter prop"
    if "nrfi" in t:
        return "NRFI"
    if "verdict" in t or "mixed" in t or "integrity" in t:
        return "aggregate/verdict"
    return t or "(untyped)"


def load(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    rows = (table_rows(text, "## Recommended but NOT played")
            + table_rows(text, "## Played legs"))
    rows = dedup_rows(rows, [leg_key(c[0], c[1], c[2]) for c in rows])
    out = []
    for c in rows:
        if len(c) < 10:
            continue
        if parse_result(c[7]) not in ("W", "L"):
            continue          # only DECIDED legs: an open leg has no close to be missing yet
        out.append({"date": c[0].strip(), "type": bet_type(c[2]),
                    "tags": parse_adj_tags(c[1]) or [],
                    "clv": verdict(c[9])})
    return out


def table(rows, keyfn, label):
    buckets = defaultdict(lambda: {"n": 0, "f": 0, "+": 0, "−": 0, "=": 0})
    for r in rows:
        for k in keyfn(r):
            b = buckets[k]
            b["n"] += 1
            if r["clv"]:
                b["f"] += 1
                b[r["clv"]] += 1
    if not buckets:
        return
    print(f"\n-- coverage by {label} --")
    print(f"   {'':22} {'filled':>10}  {'cov':>5}   {'+':>3} {'=':>3} {'−':>3}   net")
    for k, b in sorted(buckets.items(), key=lambda kv: (kv[1]["f"] / kv[1]["n"], -kv[1]["n"])):
        cov = b["f"] / b["n"] * 100
        net = b["+"] - b["−"]
        flag = "  ⚠ SHADE-BLIND" if cov < 50 else ""
        print(f"   {k:22} {b['f']:>4}/{b['n']:<5} {cov:>4.0f}%   "
              f"{b['+']:>3} {b['=']:>3} {b['−']:>3}   {net:>+3}{flag}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ledger", nargs="?", default=LEDGER)
    ap.add_argument("--min", type=float, default=None,
                    help="exit 1 if overall coverage %% is below this (for selftest/CI)")
    ap.add_argument("--dates", action="store_true", help="per-date coverage, newest first")
    a = ap.parse_args()

    rows = load(a.ledger)
    if not rows:
        print("no decided legs found — nothing to audit")
        return 0
    filled = sum(1 for r in rows if r["clv"])
    cov = filled / len(rows) * 100
    plus = sum(1 for r in rows if r["clv"] == "+")
    minus = sum(1 for r in rows if r["clv"] == "−")

    print("=" * 62)
    print("  CLV COVERAGE AUDIT  (decided legs only, deduped)")
    print(f"  source: {os.path.relpath(a.ledger)}")
    print("=" * 62)
    print(f"\n   decided legs {len(rows)}   CLV filled {filled}   "
          f"COVERAGE {cov:.0f}%   blank {len(rows)-filled}")
    print(f"   sign among filled:  +{plus}  −{minus}  net {plus-minus:+d}")
    if plus - minus < 0:
        print("   ⚠ NET NEGATIVE CLV — on the rows we DO measure, the market moved against"
              "\n     us more often than with us. That is the single most important number"
              "\n     on this page and it is not a rounding artifact.")

    table(rows, lambda r: [r["type"]], "bet type")
    table(rows, lambda r: (["adj:" + t for t in r["tags"]] or ["(market-anchored)"]),
          "adjustment tag")

    if a.dates:
        table(rows, lambda r: [r["date"]], "date")

    print("\n   Fill holes with:  tools/clv_capture.py --apply       (live, near first pitch)")
    print("                     tools/clv_backfill.py <date>       (historical, 30cr/snapshot)")
    print("   A dimension under 50% cannot be MARKET-SHADED by pulse.py — it is measured")
    print("   too thinly to govern off, and pulse now says so instead of shading it.")

    if a.min is not None and cov < a.min:
        print(f"\n   ⛔ FAIL: coverage {cov:.0f}% is below the required {a.min:.0f}%")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
