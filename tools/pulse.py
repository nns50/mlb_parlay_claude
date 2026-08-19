#!/usr/bin/env python3
"""pulse.py — recent-window strategy governor: exposure adapts to how results are FLOWING.

WHY THIS EXISTS (user-directed 8/1/26: "I shouldn't have to tell you this")
    The measurement stack (calib bands, §1c attribution, CLV) SHOWED ace_edge failing and
    Tier-1's K-prop monoculture going 4-4 — but the nightly builds kept applying static
    doctrine until the USER noticed the losses. Root cause: doctrine has a bar for changing
    BELIEFS (n≥20-30, correctly conservative) but had NO mechanism for changing EXPOSURE
    while a dimension runs cold. Those are different decisions: rewriting the registry on
    n=8 is overfitting; continuing to headline a bet shape that is 1-5 in its last 6 is
    negligence. This tool is the middle gear — mechanical, pre-registered rules that
    convert the RECENT window of results into exposure ACTIONS every build must apply.

MECHANICAL RULES (fixed here so the governor is auditable, not vibes)
    Window: decided legs from the last 14 days; if fewer than 15, the last 25 decided
    legs regardless of date. Dimensions: bet TYPE (normalized), K-prop LINE bucket
    (≥7.5 vs ≤6.5), each [adj: …] tag, TrueP band. For each dimension with enough
    recent sample, compare actual hit% to the dimension's claimed avg TrueP:

      COOL       n≥5 and hit% ≤ claimed − 15pp  → halve this dimension's adjustments;
                                                  BARRED from Tier 1 and from parlay-anchor.
      SUSPEND    n≥6 and hit% ≤ claimed − 25pp  → no new legs in this dimension this build.
      MARKET-SHADE  ≥4 CLV verdicts and −'s > +'s → set TrueP = market no-vig (adjustments
                                                  = 0) for this dimension until CLV recovers.
      GLOBAL SHRINK  recent-25 Brier(TrueP) worse than Brier(market) → halve ALL
                                                  adjustment magnitudes this build.
      (RE-WARM is automatic: the window rolls, so a dimension exits COOL/SUSPEND by
       actually winning recently — ≥3 of its last 5 decided clears it.)

    Actions are EXPOSURE controls for the current build only — the adjustment REGISTRY
    is still only rewritten at the n≥20-30 evidence bar (promoting-lessons doctrine).

USAGE
    tools/pulse.py                 # PULSE block for today (paste into the build; gate row)
    tools/pulse.py --ledger F      # fixture/selftest mode
    tools/pulse.py --today 2026-08-01
"""
import argparse
import os
import re
import sys
from collections import defaultdict
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from calib import (parse_adj_tags, parse_pct, parse_result, table_rows,  # noqa: E402
                   leg_key, dedup_rows)
from settle import parse_hprop, parse_kprop  # noqa: E402

WINDOW_DAYS = 14
MIN_ROWS = 15
FALLBACK_ROWS = 25
FALLBACK_MAX_AGE = 45   # days — the last-25 fallback must not resurrect a prior season
COOL_N, COOL_GAP = 5, 15.0
SUSP_N, SUSP_GAP = 6, 25.0
CLV_MIN = 4
CLV_COVERAGE_MIN = 0.50   # a MARKET-SHADE needs ≥50% of the dimension's decided legs to carry a CLV verdict
SHRINK_MIN_N = 12         # GLOBAL SHRINK needs this many TAGGED (adjusted) decided legs in the window

# Optional season anchor in results_log.md: '<!-- ledger-epoch: 2026 -->'. Without it,
# M/D-only dates are ambiguous at the season anniversary (an Aug 2027 run would re-import
# Aug 2026 rows as 3 days old — audit 8/7/26). With it, years are assigned by a monotonic
# walk from the epoch: the ledger is append-ordered per section, so a big backward M/D
# jump (>120 days) marks a season wrap.
EPOCH_RX = re.compile(r"<!--\s*ledger-epoch:\s*(\d{4})\s*-->")


def norm_type(typ, leg):
    t = (typ or "").lower()
    # Strip the machine-written [adj: …] ledger tag BEFORE the '×' ticket test: truep.py
    # stamps 'GLOBAL_SHRINK×0.5' into it, and the raw '×' test then classified every
    # governed leg as a parlay ticket and dropped it from the window entirely. Since the
    # shrink armed 8/12 that silently hid EVERY tagged leg from the governor — pulse read
    # adj:wind_out_over as 7-7 while calib.py read 13-15 off the same rows. clv_capture.py
    # carried this fix from 8/16; it was never propagated here or to calib/settle.
    # (Found 8/19 Build A.)
    leg = re.sub(r"\[adj:[^\]]*\]", "", leg or "")
    if "parlay" in t or "×" in leg:
        return None                     # tickets are outcomes of legs, not a dimension
    kp = parse_kprop(leg or "")
    if kp or "k-over" in t or "k-under" in t:
        direction = kp[1] if kp else ("Under" if "under" in t else "Over")
        if kp and direction == "Over":
            return "K-Over ≥7.5" if kp[2] >= 7.5 else "K-Over ≤6.5"
        return f"K-{direction}"
    if parse_hprop(leg or "") or "hitter" in t or "hit-prop" in t:
        return "hitter/pitcher prop"
    if "total" in t:
        return "total"
    if "run line" in t or t.strip() == "rl":
        return "run line"
    if "ml" in t:
        return "ML-dog" if "dog" in t else "ML-fav"
    return t or "other"


def parse_rows(text, today):
    """Decided UNIQUE legs → [{date, dims:[...], truep, y, clv}].

    One entry per PHYSICAL leg: reprice/supersede copies collapse to the latest row
    (audit 8/7/26: 131 window rows were only 107 unique legs, and three MARKET-SHADEs
    existed only because copies re-counted the same W/L + CLV). Sections are walked
    Recommended-first so the keep-last dedup prefers a leg's Played row over its scan
    row (the played copy carries the applied [adj:] tags)."""
    epoch_m = EPOCH_RX.search(text)
    epoch_year = int(epoch_m.group(1)) if epoch_m else None
    rows, keys = [], []
    for sec in ("## Recommended but NOT played", "## Played legs"):
        year = epoch_year or today.year
        prev = None
        for c in table_rows(text, sec):
            if len(c) < 8:
                continue
            m = re.match(r"(\d{1,2})/(\d{1,2})", c[0].strip())
            if not m:
                continue
            mo, dy = int(m.group(1)), int(m.group(2))
            d = None
            if epoch_year:
                try:
                    cand = date(year, mo, dy)
                except ValueError:
                    continue
                if prev and (prev - cand).days > 120:   # season wrap (10/xx → 3/xx)
                    year += 1
                    cand = date(year, mo, dy)
                prev = cand
                if cand <= today:
                    d = cand
            else:   # legacy two-candidate inference (ambiguous at the anniversary)
                for yr in (today.year, today.year - 1):
                    try:
                        cand = date(yr, mo, dy)
                    except ValueError:
                        continue
                    if cand <= today:
                        d = cand
                        break
            if d is None:
                continue
            res = parse_result(c[7])
            if res not in ("W", "L"):
                continue
            truep, starred = parse_pct(c[4])
            if truep is None or starred or not (1 <= truep <= 99):
                continue
            base = norm_type(c[2], c[1])
            if base is None:
                continue
            dims = [f"type:{base}"]
            for tag in (parse_adj_tags(c[1]) or []):
                dims.append(f"adj:{tag}")
            band = int(truep // 5 * 5)
            dims.append(f"band:{band}-{band + 4}")
            # CLV verdicts may be bold-wrapped ('**+**', '**− (line moved…)**') — strip
            # markdown before reading the sign (audit 8/7/26: bold verdicts were dropped)
            clv_cell = (c[9] if len(c) > 9 else "").replace("**", "").strip()
            clv = ("+" if clv_cell.startswith("+") else
                   "−" if clv_cell.startswith(("−", "-")) else
                   "=" if clv_cell.startswith("=") else None)
            implp, _ = parse_pct(c[5])
            rows.append({"date": d, "dims": dims, "truep": truep,
                         "implp": implp, "y": 1.0 if res == "W" else 0.0, "clv": clv})
            keys.append(leg_key(c[0].strip(), c[1], c[2]))
    return dedup_rows(rows, keys)


def window_rows(rows, today):
    rows = sorted(rows, key=lambda r: r["date"])
    recent = [r for r in rows if (today - r["date"]).days <= WINDOW_DAYS]
    if len(recent) < MIN_ROWS:
        # last-25 fallback, but never resurrect stale history: a quiet ledger must
        # idle the governor, not govern off a prior season (audit 8/7/26)
        recent = [r for r in rows[-FALLBACK_ROWS:]
                  if (today - r["date"]).days <= FALLBACK_MAX_AGE]
    return recent


def actions_for(recent):
    """Pure: window rows → (per-dim stats, [(severity, dim, message)])."""
    dims = defaultdict(lambda: {"n": 0, "w": 0, "tp": 0.0, "clvN": 0,
                                "clv+": 0, "clv-": 0, "last": []})
    bm = bk = scored = 0.0
    bmT = bkT = scoredT = 0.0
    for r in recent:
        tagged = any(d.startswith("adj:") for d in r["dims"])
        if r["implp"] is not None:
            bm += (r["truep"] / 100 - r["y"]) ** 2
            bk += (r["implp"] / 100 - r["y"]) ** 2
            scored += 1
            # GLOBAL SHRINK asks "are the ADJUSTMENTS earning their pp?" — only rows where
            # one actually fired are evidence. Market-anchored rows have TrueP == ImplP, so
            # they contribute IDENTICAL terms to both Briers and drag the difference toward
            # zero. (Bug fixed 8/12/26: the trigger was computed over the whole window, which
            # on this ledger is ~60% untagged, so it was mathematically near-unreachable —
            # the adjustment stack ran at full magnitude for 92 decided legs at 53%
            # directional accuracy / skill −0.0007 and the shrink never once fired.)
            if tagged:
                bmT += (r["truep"] / 100 - r["y"]) ** 2
                bkT += (r["implp"] / 100 - r["y"]) ** 2
                scoredT += 1
        for dname in r["dims"]:
            e = dims[dname]
            e["n"] += 1
            e["w"] += int(r["y"] == 1.0)
            e["tp"] += r["truep"]
            e["last"].append(r["y"])
            if r["clv"] is not None:
                e["clvN"] += 1
            if r["clv"] == "+":
                e["clv+"] += 1
            elif r["clv"] == "−":
                e["clv-"] += 1
    acts = []
    for dname, e in sorted(dims.items()):
        n, w = e["n"], e["w"]
        hit = w / n * 100
        claimed = e["tp"] / n
        gap = hit - claimed
        rewarmed = sum(e["last"][-5:]) >= 3 and len(e["last"]) >= 5
        if n >= SUSP_N and gap <= -SUSP_GAP and not rewarmed:
            acts.append(("⛔ SUSPEND", dname,
                         f"{w}-{n-w} ({hit:.0f}%) vs claimed {claimed:.0f}% — NO new legs "
                         f"in this dimension this build; re-warms by winning (≥3 of last 5)"))
        elif n >= COOL_N and gap <= -COOL_GAP and not rewarmed:
            acts.append(("🧊 COOL", dname,
                         f"{w}-{n-w} ({hit:.0f}%) vs claimed {claimed:.0f}% — halve its "
                         f"adjustments; barred from Tier 1 and parlay-anchor this build"))
        # margin of ≥2 so a 3−/2+ coin-flip split can't shade a healthy dimension
        if e["clv+"] + e["clv-"] >= CLV_MIN and e["clv-"] - e["clv+"] >= 2:
            # COVERAGE GUARD (added 8/12/26). A MARKET-SHADE zeroes a whole dimension, so it
            # must not fire off a biased sliver. Ledger audit that day: CLV was filled on only
            # 43% of decided legs overall and the rate varied 0-49% BY BET TYPE — hitter props
            # 27%, run lines 0% — i.e. the dimensions being shaded hardest were the ones we
            # measured least. A shade computed from a quarter of the rows is a claim about the
            # rows that happened to get captured, not about the dimension.
            cov = e["clvN"] / e["n"] if e["n"] else 0.0
            if cov < CLV_COVERAGE_MIN:
                acts.append(("⚠ MEASUREMENT-BLIND", dname,
                             f"CLV {e['clv+']}+/{e['clv-']}− WOULD shade, but only "
                             f"{e['clvN']}/{e['n']} decided legs ({cov*100:.0f}%) carry a CLV "
                             f"verdict (<{CLV_COVERAGE_MIN*100:.0f}% floor) — NOT shading. "
                             f"Backfill this dimension's closes before trusting the signal"))
            else:
                acts.append(("📉 MARKET-SHADE", dname,
                             f"CLV {e['clv+']}+/{e['clv-']}− recent ({cov*100:.0f}% covered) — "
                             f"set TrueP = market no-vig (adjustments 0) for this dimension "
                             f"until CLV recovers"))
    if scoredT >= SHRINK_MIN_N and bmT > bkT:
        acts.append(("🌐 GLOBAL SHRINK", "ALL adjustments",
                     f"on TAGGED legs only, recent Brier(TrueP) {bmT/scoredT:.4f} WORSE than "
                     f"market {bkT/scoredT:.4f} over n={scoredT:.0f} adjusted legs — halve "
                     f"every adjustment this build (whole-window n={scored:.0f} reads "
                     f"{bm/scored:.4f} vs {bk/scored:.4f}, diluted by market-anchored rows)"))
    return dims, acts


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", default=os.path.join(HERE, "..", "results_log.md"))
    ap.add_argument("--today", default=date.today().isoformat())
    args = ap.parse_args()
    today = date.fromisoformat(args.today)
    with open(args.ledger, encoding="utf-8") as fh:
        text = fh.read()
    recent = window_rows(parse_rows(text, today), today)
    dims, acts = actions_for(recent)

    print("═" * 74)
    print(f"  PULSE — recent-window strategy governor   ({len(recent)} decided legs in window,"
          f" through {today})")
    print("═" * 74)
    shown = 0
    for dname, e in sorted(dims.items(), key=lambda kv: -kv[1]["n"]):
        if e["n"] < 3:
            continue
        claimed = e["tp"] / e["n"]
        print(f"  {dname:<26} {e['w']}-{e['n']-e['w']:<3} hit {e['w']/e['n']*100:>3.0f}% "
              f"vs claimed {claimed:>3.0f}%   CLV {e['clv+']}+/{e['clv-']}−")
        shown += 1
    if not shown:
        print("  (window too thin — no dimension has 3 decided legs)")
    print("─" * 74)
    if acts:
        print("  ACTIONS (mechanical — the build MUST apply these; they override static")
        print("  registry magnitudes for THIS build; registry itself changes only at n≥20):")
        for sev, dname, msg in acts:
            print(f"  {sev}  {dname} — {msg}")
    else:
        print("  ✓ no dimension breaches the cool/suspend/shade thresholds — build normally.")
    print("═" * 74)


if __name__ == "__main__":
    main()
