#!/usr/bin/env python3
"""parlay.py — true combined probability of a parlay, correlation-aware, vs the offered price.

WHY THIS EXISTS
    Stacking legs multiplies the bust rate (we measured it: parlay LEGS hit ~68% while
    parlay TICKETS hit ~42%). The only way a parlay keeps a real win chance is POSITIVE
    CORRELATION — same-game legs that tend to win together have a true combined prob ABOVE
    the naive product. CLAUDE.md says to use that ("take the better of SGP vs the independent
    product") but it's been done by hand and guessed. This computes it:
      • naive independent combined prob (Π of leg TruePs),
      • correlation-adjusted combined prob (for a 2-leg same-game pair),
      • fair odds for the true combined,
      • EV vs the offered independent-product price AND vs an offered SGP price,
      • a recommendation (independent vs SGP) + the min-edge-gate verdict.

CORRELATION MODEL (2 legs)
    For two binary events with marginals p1,p2 and correlation ρ:
        joint = p1*p2 + ρ*sqrt(p1(1-p1)·p2(1-p2)),  clamped to the Fréchet bounds.
    ρ comes from a qualitative tier (--corr) because we never know it exactly — these are
    deliberately rough; positive when legs win together (team ML + their team-total Over;
    F5 Under + game Under), negative when they fight (team ML + opposing SP K-Over).

USAGE
    tools/parlay.py --leg 59:-120 --leg 66:-188                 # independent 2-leg
    tools/parlay.py --leg 59:-120 --leg 66:-188 --corr moderate # same-game, +correlated
    tools/parlay.py --leg 60:-130 --leg 55:+110 --corr moderate --sgp +320
    tools/parlay.py --leg 59 --leg 66 --leg 56                  # TrueP-only, 3-leg (independent)

    Each --leg is  TrueP%[:americanPrice]  (price optional; needed for the payout/EV math).
"""
import argparse
import math
import sys

CORR = {
    "strong":      0.45,   # F5 Under + game Under; team total Over + that team ML (clear)
    "moderate":    0.30,   # team ML + their team-total Over; team ML + their SP K-Over
    "weak":        0.15,   # loosely linked same-game legs
    "none":        0.00,   # independent (different games)
    "neg-weak":   -0.15,
    "neg-moderate":-0.30,  # team ML + OPPOSING SP K-Over (fight each other)
    "neg-strong": -0.45,
}


def dec_from_american(a):
    return 1 + (a / 100.0 if a > 0 else 100.0 / -a)


def american_from_dec(d):
    if d <= 1:
        return float("nan")
    return (d - 1) * 100 if d >= 2 else -100 / (d - 1)


def parse_leg(s):
    """'59:-120' -> (0.59, -120.0) ; '59' -> (0.59, None)."""
    tp, _, price = s.partition(":")
    p = float(tp) / 100.0
    if not (0 < p < 1):
        raise ValueError(f"leg TrueP {tp!r} must be a percent in (0,100)")
    return p, (float(price) if price else None)


def joint2(p1, p2, rho):
    cov = rho * math.sqrt(p1 * (1 - p1) * p2 * (1 - p2))
    j = p1 * p2 + cov
    return max(max(0.0, p1 + p2 - 1.0), min(j, min(p1, p2)))  # Fréchet clamp


def gate(edge_pp):
    if edge_pp >= 3:
        return "✓ clears the +3-4pp parlay-anchor bar"
    if edge_pp >= 0:
        return "✗ positive but under the parlay bar — thin, near-fair"
    return "✗ NEGATIVE edge — the price is worse than the true odds (-EV)"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--leg", action="append", required=True, help="TrueP%%[:americanPrice], repeatable")
    ap.add_argument("--corr", default="none", choices=sorted(CORR), help="correlation tier (2-leg same-game only)")
    ap.add_argument("--sgp", type=float, default=None, help="offered same-game-parlay American price")
    args = ap.parse_args()

    try:
        legs = [parse_leg(x) for x in args.leg]
    except ValueError as e:
        ap.error(str(e))

    probs = [p for p, _ in legs]
    prices = [pr for _, pr in legs]
    naive = math.prod(probs)

    rho = CORR[args.corr]
    if len(legs) == 2 and args.corr != "none":
        true_comb = joint2(probs[0], probs[1], rho)
        corr_note = f"correlation '{args.corr}' (ρ≈{rho:+.2f})"
    else:
        true_comb = naive
        corr_note = "independent (product)"
        if len(legs) != 2 and args.corr != "none":
            corr_note += "  ⚠ --corr only models a 2-leg pair; 3+ legs treated independent"

    print("─" * 64)
    print(f"legs: {', '.join(f'{p*100:.0f}%' + (f'@{pr:+.0f}' if pr else '') for p, pr in legs)}")
    print(f"naive independent combined : {naive*100:5.1f}%")
    print(f"true combined ({corr_note}) : {true_comb*100:5.1f}%")
    if len(legs) == 2 and rho > 0:
        print(f"  → positive correlation ADDS {(true_comb-naive)*100:+.1f}pp of win prob vs independent")
    elif len(legs) == 2 and rho < 0:
        print(f"  → negative correlation REMOVES {(naive-true_comb)*100:.1f}pp — these legs fight; usually skip")

    fair_dec = 1 / true_comb if true_comb > 0 else float("inf")
    print(f"fair odds for true combined: {fair_dec:.3f} dec ({american_from_dec(fair_dec):+.0f})")

    # Payout / EV — needs every leg's price for the independent product.
    print("─" * 64)
    if all(pr is not None for pr in prices):
        indep_dec = math.prod(dec_from_american(pr) for pr in prices)
        be_indep = 1 / indep_dec
        ev_indep = true_comb * indep_dec - 1
        edge_indep = (true_comb - be_indep) * 100
        print(f"INDEPENDENT product price  : {indep_dec:.3f} dec ({american_from_dec(indep_dec):+.0f})")
        print(f"  breakeven {be_indep*100:.1f}%  | edge {edge_indep:+.1f}pp | EV {ev_indep*100:+.1f}%  → {gate(edge_indep)}")

        if args.sgp is not None:
            sgp_dec = dec_from_american(args.sgp)
            be_sgp = 1 / sgp_dec
            ev_sgp = true_comb * sgp_dec - 1
            edge_sgp = (true_comb - be_sgp) * 100
            print(f"SGP offered price          : {sgp_dec:.3f} dec ({args.sgp:+.0f})")
            print(f"  breakeven {be_sgp*100:.1f}%  | edge {edge_sgp:+.1f}pp | EV {ev_sgp*100:+.1f}%  → {gate(edge_sgp)}")
            better = "SGP" if ev_sgp > ev_indep else "INDEPENDENT product"
            print("─" * 64)
            print(f"➡ TAKE THE {better} — higher EV ({max(ev_sgp, ev_indep)*100:+.1f}% vs {min(ev_sgp, ev_indep)*100:+.1f}%).")
            if args.corr.startswith("none") and args.sgp is not None:
                print("  (note: an SGP usually IS correlated — set --corr so the true-combined/EV is honest.)")
        else:
            print("─" * 64)
            print(f"➡ Verdict: {gate(edge_indep)}.  Add --sgp <price> to compare a same-game-parlay quote.")
    else:
        print("(add :price to each --leg for the payout / breakeven / EV / SGP comparison.)")
    print("─" * 64)


if __name__ == "__main__":
    main()
