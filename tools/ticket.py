#!/usr/bin/env python3
"""ticket.py — exhaustive +200-band ticket search: the max-floor construction, not the first hand-built one.

WHY THIS EXISTS (the ledger earned it)
    The legs are fine; the CONSTRUCTION is the leak. As of 7/29/26 the ledger reads:
      • recommended legs hit ~68-70%, parlay TICKETS sit ~50% — multiplication is where win prob dies;
      • D1 (the +200-chase 3rd leg) is 4-1 — the bolted-on leg keeps busting (7/26 STL, 6/17 SEA, ...);
      • the same-game POSITIVE-correlation stack is the best-performing route to ~+200
        (6/8 PHI×Sánchez, 6/12 SEA×Miller, 6/16 SEA×Cease, 6/17 NYY×Rodón, 6/19 TEX×deGrom);
      • swapping a high-edge K-prop for a thin ML at the SAME payout flips -EV to +EV
        (6/9: MIA+ATL +1.5pp lost; MIA+Burns O6.5K +7.3pp would have cashed — user-caught).
    Hand-building tiers finds ONE ticket. This enumerates EVERY legal 1-3-leg construction from the
    day's gate-cleared candidates, prices each honestly (correlation-aware via parlay.py's model), and
    ranks the payout band by TRUE COMBINED PROB — so "the +200" is the best-floor +200 that exists,
    not the first one assembled. It cannot beat the math of stacking legs; it stops floor from being
    left on the table.

LEG FORMAT (repeatable --leg, or one per line in --file; '#' comments ok)
    TrueP:price:game[:label[:tier]]
      TrueP  whole-number percent (63, not 0.63) — the PRE-REGISTERED true prob
      price  American (-110, +207) — the BEST shopped price
      game   any id shared by legs of the same game (SEA-TEX)
      label  free text ("Gilbert O6.5K")
      tier   correlation tier vs the OTHER declared leg of the same game:
             strong/moderate/weak (positive) or neg-weak/neg-moderate/neg-strong
    Same-game rules (doctrine): two legs of one game combine ONLY if BOTH declare the same tier
    (unclear correlation = one leg per game); at most ONE correlated pair per ticket; the pair is
    priced via joint2 (parlay.py), remaining legs multiply independently. Negative-tier pairs are
    shown as rejected, not recommended.

USAGE
    tools/ticket.py --leg "63:-110:SEA-TEX:Gilbert O6.5K" --leg "63:-164:NYY-PHI:PHI ML" \\
                    --leg "57:-132:CIN-STL:STL ML"
    tools/ticket.py --file legs.txt --min-price 180 --max-price 260 --top 5
    tools/ticket.py --leg "63:-164:NYY-PHI:PHI ML:moderate" --leg "55:-125:NYY-PHI:Sánchez O6.5K:moderate"
                    # same-game pos-corr pair — output includes the min acceptable SGP quote

OUTPUT
    1. the leg pool (edge vs each price's breakeven — legs are assumed ALREADY devig-gated upstream);
    2. the payout/floor FRONTIER (what +200 costs vs +150 — the honest Tier-2-vs-Tier-3 view);
    3. the target band (default +180..+260) ranked by true combined prob, with EV, ¼-Kelly stake,
       and for corr pairs the minimum SGP quote worth taking;
    4. rejected constructions with reasons (negative pair, undeclared same-game, thin leg).
"""
import argparse
import itertools
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parlay import CORR, american_from_dec, dec_from_american, joint2  # single source of truth

POS_TIERS = {t for t, r in CORR.items() if r > 0}
NEG_TIERS = {t for t, r in CORR.items() if r < 0}


def parse_leg(spec):
    """'63:-110:SEA-TEX:Gilbert O6.5K[:moderate]' -> dict. TrueP is whole-number percent."""
    parts = spec.split(":")
    if len(parts) < 3:
        raise ValueError(f"leg {spec!r}: need TrueP:price:game[:label[:tier]]")
    tp = float(parts[0])
    if tp < 1:
        raise ValueError(f"leg {spec!r}: TrueP looks like a fraction — use whole-number percent (63, not 0.63)")
    if not (0 < tp < 100):
        raise ValueError(f"leg {spec!r}: TrueP must be in (0,100)")
    price = float(parts[1])
    if abs(price) < 100:
        raise ValueError(f"leg {spec!r}: price {parts[1]!r} isn't American odds (|price| >= 100)")
    game = parts[2].strip()
    if not game:
        raise ValueError(f"leg {spec!r}: empty game id")
    label = parts[3].strip() if len(parts) > 3 and parts[3].strip() else f"{tp:.0f}%@{price:+.0f}"
    tier = parts[4].strip() if len(parts) > 4 and parts[4].strip() else None
    if tier is not None and tier not in CORR:
        raise ValueError(f"leg {spec!r}: unknown tier {tier!r} (choose from {', '.join(sorted(CORR))})")
    dec = dec_from_american(price)
    return {"p": tp / 100.0, "price": price, "dec": dec, "game": game, "label": label,
            "tier": tier, "edge_pp": (tp / 100.0 - 1.0 / dec) * 100}


def ticket_prob(legs):
    """True combined prob + notes. Legality is enforced by caller (≤1 declared same-game pair)."""
    by_game = {}
    for l in legs:
        by_game.setdefault(l["game"], []).append(l)
    p, note = 1.0, None
    for game_legs in by_game.values():
        if len(game_legs) == 1:
            p *= game_legs[0]["p"]
        else:
            a, b = game_legs
            rho = CORR[a["tier"]]
            p *= joint2(a["p"], b["p"], rho)
            note = f"same-game pair ρ{rho:+.2f} ({a['tier']})"
    return p, note


def legality(legs):
    """Return (ok, reason). Doctrine: unclear same-game corr = one leg per game; ≤1 pair/ticket;
    negative pairs fight each other — computed but never recommended."""
    by_game = {}
    for l in legs:
        by_game.setdefault(l["game"], []).append(l)
    pairs = 0
    for game, gl in by_game.items():
        if len(gl) > 2:
            return False, f"{game}: >2 legs in one game"
        if len(gl) == 2:
            a, b = gl
            if a["tier"] is None or b["tier"] is None:
                return False, f"{game}: same-game legs without a declared corr tier (one leg per game)"
            if a["tier"] != b["tier"]:
                return False, f"{game}: contradictory tiers ({a['tier']} vs {b['tier']})"
            if a["tier"] in NEG_TIERS:
                return False, f"{game}: negatively-correlated pair ({a['tier']}) — legs fight; skip"
            pairs += 1
    if pairs > 1:
        return False, "more than one correlated pair (model supports one pair per ticket)"
    return True, None


def quarter_kelly(p, dec, cap=2.0):
    """¼-Kelly units on the ticket's own edge (doctrine: parlays are staked on the ticket's edge,
    usually small/negative — most parlays are near-EV chalk+vig)."""
    b = dec - 1.0
    if b <= 0:
        return 0.0
    f = (p * dec - 1.0) / b
    return max(0.0, min(cap, f * 25.0))  # fraction*100 units → /4


def min_sgp_price(p, floor_edge_pp=3.0):
    """The worst SGP quote still worth taking for a corr pair: price where edge = floor_edge_pp."""
    be = p - floor_edge_pp / 100.0
    if be <= 0:
        return None
    return american_from_dec(1.0 / be)


def fmt_ticket(t, show_kelly=True):
    legs = " × ".join(f"{l['label']} {l['price']:+.0f}" for l in t["legs"])
    line = (f"{t['payout']:+.0f}  floor {t['p']*100:5.1f}%  edge {t['edge_pp']:+5.1f}pp  "
            f"EV {t['ev']*100:+6.1f}%  | {legs}")
    if t["note"]:
        line += f"  [{t['note']}]"
    if show_kelly:
        line += f"  | ¼-Kelly {quarter_kelly(t['p'], t['dec']):.2f}u"
    return line


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--leg", action="append", default=[], help="TrueP:price:game[:label[:tier]], repeatable")
    ap.add_argument("--file", help="file with one leg spec per line ('#' comments ok)")
    ap.add_argument("--min-price", type=float, default=180, help="target band lower bound, American (default +180)")
    ap.add_argument("--max-price", type=float, default=260, help="target band upper bound, American (default +260)")
    ap.add_argument("--max-legs", type=int, default=3, choices=(1, 2, 3, 4), help="max legs per ticket (default 3)")
    ap.add_argument("--min-edge", type=float, default=0.0,
                    help="drop legs whose TrueP−breakeven edge (vig INCLUDED) is below this many pp. "
                         "Default 0.0 = drop only legs that are -EV at the offered price; the no-vig "
                         "+2pp/+3-4pp doctrine gate happens UPSTREAM via devig.sh before legs get here")
    ap.add_argument("--top", type=int, default=5, help="how many band tickets to print (default 5)")
    args = ap.parse_args()

    specs = list(args.leg)
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            specs += [ln.strip() for ln in fh
                      if ln.strip() and not ln.strip().startswith("#")]
    if len(specs) < 2:
        ap.error("need at least 2 legs (via --leg / --file)")

    try:
        pool = [parse_leg(s) for s in specs]
    except ValueError as e:
        ap.error(str(e))

    print("═" * 78)
    print("LEG POOL  (edge = TrueP − price breakeven, vig INCLUDED — smaller than the no-vig edge;"
          " negative = -EV at this price)")
    thin = []
    for l in pool:
        gate = "✓" if l["edge_pp"] >= args.min_edge else "✗ thin"
        print(f"  {gate}  {l['label']:<28} {l['price']:+7.0f}  TrueP {l['p']*100:4.1f}%  "
              f"be {100/l['dec']:4.1f}%  edge {l['edge_pp']:+5.1f}pp  game {l['game']}"
              + (f"  tier={l['tier']}" if l["tier"] else ""))
        if l["edge_pp"] < args.min_edge:
            thin.append(l["label"])
    kept = [l for l in pool if l["edge_pp"] >= args.min_edge]
    if thin:
        print(f"  → dropped {len(thin)} thin leg(s): {', '.join(thin)} "
              f"(--min-edge {args.min_edge:g}; the D1 lesson is that these sink tickets)")
    if len(kept) < 1:
        print("  NO legs clear the bar → NO BET is the honest output.")
        return

    # Enumerate every construction
    tickets, rejected = [], []
    for n in range(1, min(args.max_legs, len(kept)) + 1):
        for combo in itertools.combinations(kept, n):
            ok, why = legality(combo)
            if not ok:
                rejected.append((combo, why))
                continue
            p, note = ticket_prob(list(combo))
            dec = math.prod(l["dec"] for l in combo)
            payout = american_from_dec(dec)
            tickets.append({"legs": combo, "p": p, "dec": dec, "payout": payout,
                            "ev": p * dec - 1.0, "edge_pp": (p - 1.0 / dec) * 100,
                            "note": note or ("SINGLE" if n == 1 else None)})

    # Payout/floor frontier (Pareto: nothing else has both ≥floor and ≥payout)
    frontier = []
    for t in sorted(tickets, key=lambda t: (-t["p"], -t["payout"])):
        if not any(f["payout"] >= t["payout"] and f["p"] >= t["p"] and f is not t for f in frontier):
            frontier.append(t)
    frontier.sort(key=lambda t: t["payout"])
    print("─" * 78)
    print("PAYOUT / FLOOR FRONTIER  (what each payout band truly costs in win prob)")
    for t in frontier:
        print("  " + fmt_ticket(t, show_kelly=False))

    band = sorted((t for t in tickets if args.min_price <= t["payout"] <= args.max_price),
                  key=lambda t: (-t["p"], -t["ev"]))
    print("─" * 78)
    print(f"TARGET BAND {args.min_price:+.0f}..{args.max_price:+.0f} — ranked by TRUE COMBINED PROB "
          f"(the max-floor route to the payout)")
    if not band:
        print("  ∅ no construction reaches the band from these legs.")
        near = min(tickets, key=lambda t: abs(t["payout"] - (args.min_price + args.max_price) / 2),
                   default=None)
        if near:
            print("  closest: " + fmt_ticket(near))
        print("  Honest options: take the best-floor ticket BELOW the band (doctrine: highest floor even"
              " at +120-180) or NO BET — do NOT bolt on a thin leg to reach the number (D1, 4-1).")
    else:
        for i, t in enumerate(band[:args.top]):
            tag = "➡ RECOMMENDED" if i == 0 else f"  #{i+1}"
            print(f"{tag}  {fmt_ticket(t)}")
            if t["note"] and "pair" in (t["note"] or ""):
                msp = min_sgp_price(t["p"])
                if msp is not None:
                    print(f"      corr pair books as an SGP — worth taking only if the quote beats "
                          f"{msp:+.0f} (edge ≥ +3pp); else bet the legs separately.")
        best_any = max(tickets, key=lambda t: t["p"])
        if best_any["p"] > band[0]["p"] + 1e-9:
            print(f"  ⚖ floor cost of the band: best ANY-payout construction is "
              f"{best_any['p']*100:.1f}% at {best_any['payout']:+.0f} "
              f"({(best_any['p']-band[0]['p'])*100:.1f}pp higher floor than the band pick).")

    if rejected:
        print("─" * 78)
        print("REJECTED CONSTRUCTIONS")
        seen = set()
        for combo, why in rejected:
            key = why
            if key in seen:
                continue
            seen.add(key)
            print(f"  ✗ {' × '.join(l['label'] for l in combo)} — {why}")
    print("═" * 78)
    print("Reminder: a parlay is still chalk×vig — the Tier-1 standalone is where the measured edge"
          " lives. This tool only stops the +200 from being WORSE than it has to be.")


if __name__ == "__main__":
    main()
