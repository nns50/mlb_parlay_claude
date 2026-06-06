#!/usr/bin/env python3
"""truep.py — derive a pre-registered TrueP from a market baseline + FIXED adjustments.

WHY THIS EXISTS
    CLAUDE.md's TrueP method (codified 6/4): "derive it, don't vibe it" — anchor to the
    market no-vig prob, then apply PRE-SET, written adjustments with fixed magnitudes, so
    calibration measures the ADJUSTMENTS (the thing worth measuring) instead of a gut
    number. A bare gut TrueP is the `*`-equivalent and is calibration-invalid. This makes
    the method mechanical and reproducible: feed the no-vig baseline (from devig.sh) +
    the named adjustments that apply, get a TrueP you can log with a clear audit trail.

USAGE
    tools/truep.py --base-prob 54.3 --adj ace_edge
    tools/truep.py --base-prob 64.1 --adj own_sp_hi,fade_as_fav
    tools/truep.py --base-prob 56.7 --custom "-2:Sonny Gray duel caps the floor"
    tools/truep.py --list          # print the adjustment registry and exit

NOTES
    • --base-prob is the MARKET NO-VIG prob (run devig.sh first). The whole point is to
      anchor on the market and adjust from there, not to invent a number.
    • Adjustments are in percentage points (pp). Combine named (--adj) + ad-hoc (--custom).
    • K-prop "tiers" are NOT pp and are handled by moving the alt line, not here — this
      tool is for ML / spread / total / team-total style pp adjustments.
"""
import argparse
import sys

# Registry: name -> (pp, description). Magnitudes are the doctrine's written values.
ADJUSTMENTS = {
    "ace_edge":        (+3, "clear SP quality edge for our side (ERA/xFIP/form)"),
    "own_sp_hi":       (-5, "our fav's OWN SP ERA ~5.00+ / two-bad-SP shootout (fades D4)"),
    "fade_as_fav":     (-5, "team is on fades.md A-list (fade-as-favorite)"),
    "opponent_driven": (-4, "fav number is opponent-SP-driven, our team sub-.500/cold (D4 decompose)"),
    "hot_dog":         (+3, "quietly-hot underdog value (fades.md B-list)"),
    "second_meeting":  (-4, "2nd meeting within ~14d — hitters adjust (~1 tier; K-Over)"),
    "contact_lineup":  (-4, "opposing contact-heavy lineup vs a K-Over (~1 tier)"),
    "tight_zone_ump":  (-3, "tight-zone HP umpire suppresses a K-Over"),
    "opp_bullpen_game":(0,  "opponent is a bullpen/opener game — NO boost (fades D5)"),
    "getaway_spot":    (-2, "getaway / day-after-night / heavy-travel letdown spot"),
    "pen_rested_edge": (+2, "clear bullpen rest/quality edge late"),
}


def fmt_registry():
    out = ["Adjustment registry (name: pp — description):"]
    for k, (pp, desc) in ADJUSTMENTS.items():
        out.append(f"  {k:<18} {pp:+d}pp   {desc}")
    out.append("  custom             ±N    ad-hoc, via --custom \"+N:reason\" (repeatable)")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Derive a pre-registered TrueP from baseline + fixed adjustments.")
    ap.add_argument("--base-prob", type=float, help="market NO-VIG prob in %% (from devig.sh)")
    ap.add_argument("--adj", default="", help="comma-separated named adjustments (see --list)")
    ap.add_argument("--custom", action="append", default=[], help='ad-hoc "+N:reason" (repeatable)')
    ap.add_argument("--list", action="store_true", help="print the adjustment registry and exit")
    args = ap.parse_args()

    if args.list:
        print(fmt_registry())
        return
    if args.base_prob is None:
        ap.error("--base-prob is required (the market no-vig prob; run devig.sh first). Use --list to see adjustments.")

    base = args.base_prob
    applied = []  # (label, pp)

    names = [a.strip() for a in args.adj.split(",") if a.strip()]
    for n in names:
        if n not in ADJUSTMENTS:
            ap.error(f"unknown adjustment '{n}'. Use --list to see valid names.")
        pp, desc = ADJUSTMENTS[n]
        applied.append((f"{n} ({desc})", pp))

    for c in args.custom:
        if ":" not in c:
            ap.error(f'--custom must look like "+N:reason", got {c!r}')
        mag, _, reason = c.partition(":")
        try:
            pp = float(mag)
        except ValueError:
            ap.error(f"--custom magnitude {mag!r} is not a number")
        applied.append((f"custom: {reason.strip()}", pp))

    total = sum(pp for _, pp in applied)
    truep = max(1.0, min(99.0, base + total))

    print("─" * 60)
    print(f"baseline (market no-vig)         {base:6.1f}%")
    if applied:
        print("adjustments:")
        for label, pp in applied:
            print(f"  {pp:+5.1f}pp  {label}")
    else:
        print("adjustments:                     (none — TrueP = market no-vig)")
    print("─" * 60)
    print(f"net adjustment                   {total:+6.1f}pp")
    print(f"TrueP (clamped 1–99)             {truep:6.1f}%")
    print(f"pre-registered edge vs baseline  {truep - base:+6.1f}pp")
    print("─" * 60)
    print("Log this TrueP at BET TIME (never reconstruct). Edge vs the BEST-priced")
    print("no-vig line is the min-edge gate: ≥+2pp standalone / ≥+3-4pp parlay anchor.")


if __name__ == "__main__":
    main()
