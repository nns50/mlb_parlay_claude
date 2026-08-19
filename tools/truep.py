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
    tools/truep.py --base-prob 56.7 --custom=-2:short-reason
      # ⚠ a NEGATIVE custom with no space in the reason needs the = form (--custom=-2:x) —
      #   argparse reads a bare '-2:x' as an option and errors; a spaced reason also works.
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
#
# REGISTRY REVIEW v2 (2026-08-07 — first formal review; evidence bar = calib.py §1c n≥20,
# counted over UNIQUE legs after the reprice-row dedup, not raw rows):
#   • custom hard-capped at ±3 (was routinely +4..+10): custom n=33 unique decided legs,
#     15-18 (45%), skill −0.0056/leg, CLV net-negative — the aggregate earns nothing, so
#     no single ad-hoc read may claim more pp than the whole class has ever demonstrated.
#     A conviction >3pp must be pre-registered as a NAMED tag here (so it accrues its
#     own §1c record) — that's the split-the-custom-monolith path.
#   • ace_edge STAYS +3 — ⚠ ON WATCH, not rewritten: raw rows hit n=20 but the dedup
#     shows only n=15 unique legs (7-8, 47%, skill −0.0057, CLV 3+/9−). Under the bar →
#     belief unchanged per doctrine; pulse.py already MARKET-SHADEs its per-build
#     exposure. AUTO-REVIEW when §1c shows n≥20 unique: cut to +1 if skill still <0.
#
# Registry v3 (8/19/26 — the scheduled ace_edge auto-review, plus two park/weather
# verdicts, all read off calib.py §1c AFTER the GLOBAL_SHRINK× parsing bug was fixed
# in pulse/calib/settle the same run; before that fix §1c and §1b were scoring a
# BIASED SUBSAMPLE, so these are the first registry calls made on the full ledger):
#   • ace_edge  → OFF WATCH, STAYS +3. The auto-review triggered at n=20 unique and
#     the verdict is the opposite of the watch's expectation: 12-8 (60%), skill
#     +0.0008/leg. Positive, so the scheduled cut-to-+1 does NOT fire. It is the
#     thinnest possible pass (+0.0008 is ~zero) — re-review at n≥30, cut then if it
#     has not separated from zero.
#   • wind_out_over  → CUT +4 → 0 (RETIRED to narrative-only). Second consecutive
#     review past the evidence bar and still negative: n=28, 13-15 (46%) against a
#     ~53% claim, skill −0.0025/leg, and CLV coverage 0+/0− — we have never once seen
#     this tag's close. A tag that is measurably negative AND unmeasurable at the
#     close has no business pricing a leg. Wind-out stays a *reason to look*; it
#     contributes 0.0pp. (It priced 8/18's ATL/MIN Over 8.5, which lost by 3.5.)
#   • hitter_park_over  → HALVED +3 → +1.5, ⚠ ON WATCH. First crossing of the bar
#     (n=20) at exactly 10-10 / 50% vs a 53% claim, skill −0.0030. Graduated action
#     per the ace_edge precedent: halve now, AUTO-CUT to 0 at n≥30 if skill is still
#     <0. Do not stack it with pitcher_park_under's mirror.
#   • custom cap UNCHANGED at ±3 (n=33, 15-18/45%, skill −0.0056 — still the worst
#     class in the registry).
ADJUSTMENTS = {
    "ace_edge":        (+3, "clear SP quality edge for our side (ERA/xFIP/form) "
                            "[✅ off watch 8/19: n=20 unique 12-8/60%, skill +0.0008 — "
                            "auto-review cut did NOT fire; re-review at n≥30]"),
    "own_sp_hi":       (-5, "our fav's OWN SP ERA ~5.00+ / two-bad-SP shootout (fades D4)"),
    "fade_as_fav":     (-5, "team is on fades.md A-list (fade-as-favorite)"),
    "opponent_driven": (-4, "fav number is opponent-SP-driven, our team sub-.500/cold (D4 decompose)"),
    "hot_dog":         (+3, "quietly-hot underdog value (fades.md B-list)"),
    "second_meeting":  (-4, "2nd meeting within ~14d — hitters adjust (~1 tier; K-Over)"),
    "contact_lineup":  (-4, "opposing contact-heavy lineup vs a K-Over (~1 tier)"),
    "tight_zone_ump":  (-3, "tight-zone HP umpire suppresses a K-Over"),
    "opp_bullpen_game":(0,  "opponent is a bullpen/opener game — NO boost (fades D5)"),
    "market_disagrees":(-4, "market price materially below your model on a liquid ML/total (~5+pp gap) — "
                            "market sees something you don't (start-length risk, lineup, injury); "
                            "shade toward the line; re-derive TrueP from BOTH posted prices (CLAUDE.md)"),
    "getaway_spot":    (-2, "getaway / day-after-night / heavy-travel letdown spot"),
    "pen_rested_edge": (+2, "clear bullpen rest/quality edge late"),
    # --- Park / weather / umpire (softer-market signal; NOISIER than SP/lineup —
    #     keep magnitudes modest and don't stack several. Pick the one matching your
    #     BET DIRECTION; each is framed as "aids <this side>". Use mlb_api.sh weather/ump.)
    "wind_out_over":       (0,  "⛔ RETIRED 8/19 (was +4) — wind OUT aids an OVER is a "
                                "REASON TO LOOK, not a price: n=28, 13-15/46% vs a 53% "
                                "claim, skill −0.0025, CLV coverage 0+/0−. Contributes 0.0pp"),
    "wind_in_under":       (+3, "wind IN / cold aids a total/team-total UNDER"),
    "hitter_park_over":    (+1.5, "hitter-friendly park aids an OVER [⚠ HALVED 8/19 from "
                                  "+3: n=20 10-10/50%, skill −0.0030 — auto-cut to 0 at n≥30 "
                                  "if still <0]"),
    "pitcher_park_under":  (+3, "pitcher-friendly park aids an UNDER"),
    "cold_aids_kover":     (+3, "cold / wind-in aids a K-OVER (more whiffs)"),
    "hot_hurts_kover":     (-3, "hot / wind-out hurts a K-OVER"),
    "wide_zone_ump_kover": (+2, "wide-zone / high-K HP umpire aids a K-OVER"),
    # tight_zone_ump (-3, above) is the K-OVER suppressor; for a K/total UNDER a tight
    # zone HELPS — express that with --custom "+2:tight-zone ump aids the Under".
}


def fmt_registry():
    out = ["Adjustment registry (name: pp — description):"]
    for k, (pp, desc) in ADJUSTMENTS.items():
        # magnitudes may be fractional after a halving review (hitter_park_over 8/19)
        out.append(f"  {k:<18} {pp:+g}pp  {desc}")
    out.append("  custom             ±N    ad-hoc, via --custom \"+N:reason\" (repeatable)")
    return "\n".join(out)


def governor_shrink():
    """Ask pulse.py whether GLOBAL SHRINK is armed → (factor, reason) with factor 1.0 or 0.5.

    WHY THIS IS AUTOMATIC (audit 8/12/26). The shrink was a line of prose the build was
    trusted to remember, and the trigger that produces it had a dilution bug that kept it
    from ever firing — so every adjustment ran at full magnitude for 92 decided legs whose
    measured directional accuracy was 53% and whose Brier skill was −0.0007. Both halves of
    that failure were silent. Applying it here means a haircut cannot be forgotten, and it
    shows up in the printed ledger tag so the record says what was actually used.

    Fails OPEN (factor 1.0) if pulse cannot run — a broken governor must not silently
    halve live numbers either.
    """
    try:
        import io
        import contextlib
        import pulse
        buf = io.StringIO()
        argv = sys.argv
        try:
            sys.argv = ["pulse.py"]        # pulse.main() re-parses argv; ours is not its
            with contextlib.redirect_stdout(buf):
                pulse.main()
        finally:
            sys.argv = argv
        for line in buf.getvalue().splitlines():
            if "GLOBAL SHRINK" in line:
                return 0.5, line.strip().lstrip("🌐 ").strip()
    except Exception as exc:                      # noqa: BLE001 — advisory, never fatal
        return 1.0, f"(pulse unavailable: {exc.__class__.__name__} — no shrink applied)"
    return 1.0, ""


def main():
    ap = argparse.ArgumentParser(description="Derive a pre-registered TrueP from baseline + fixed adjustments.")
    ap.add_argument("--base-prob", type=float, help="market NO-VIG prob in %% (from devig.sh)")
    # action="append" (not a bare default) so that BOTH invocation forms work:
    #   --adj a,b,c        (comma-separated, the documented form)
    #   --adj a --adj b    (repeated flag — argparse would otherwise keep only the LAST,
    #                       silently dropping every earlier tag and mis-pricing the leg).
    # That silent drop was a real mis-price on 8/17/26; see results_log.md "TOOLING TRAP".
    ap.add_argument("--adj", action="append", default=[],
                    help="named adjustments (see --list) — comma-separated and/or repeatable")
    ap.add_argument("--custom", action="append", default=[], help='ad-hoc "+N:reason" (repeatable)')
    ap.add_argument("--list", action="store_true", help="print the adjustment registry and exit")
    ap.add_argument("--no-governor", action="store_true",
                    help="print RAW registry magnitudes — skip the pulse.py GLOBAL SHRINK "
                         "haircut. For inspecting the registry itself; never for pricing a "
                         "live leg, because the haircut is the governor's measured verdict "
                         "on whether these magnitudes are currently earning their pp.")
    args = ap.parse_args()

    if args.list:
        print(fmt_registry())
        return
    if args.base_prob is None:
        ap.error("--base-prob is required (the market no-vig prob; run devig.sh first). Use --list to see adjustments.")

    base = args.base_prob
    applied = []  # (label, pp)

    names = [a.strip() for chunk in args.adj for a in chunk.split(",") if a.strip()]
    resolved = []  # (tag_name, signed_pp) — mirrors flip the sign, tag carries the applied sign
    for n in names:
        mirrored = n.startswith("~")
        key = n[1:] if mirrored else n
        if key not in ADJUSTMENTS:
            ap.error(f"unknown adjustment '{key}'. Use --list to see valid names.")
        pp, desc = ADJUSTMENTS[key]
        if mirrored:
            pp = -pp   # e.g. ~own_sp_hi on the DOG side: the fav's −5 becomes our +5
        applied.append((f"{key} ({'MIRRORED: ' if mirrored else ''}{desc})", pp))
        resolved.append((key, pp))

    for c in args.custom:
        if ":" not in c:
            ap.error(f'--custom must look like "+N:reason", got {c!r}')
        mag, _, reason = c.partition(":")
        try:
            pp = float(mag)
        except ValueError:
            ap.error(f"--custom magnitude {mag!r} is not a number")
        if abs(pp) > 3.0:
            ap.error(f"--custom {pp:+g}pp exceeds the ±3 cap (registry review 8/7/26: custom "
                     f"n=47 measures ~zero skill — no ad-hoc read may claim more than the "
                     f"class has demonstrated). Re-run at ≤±3, or register a NAMED tag in "
                     f"ADJUSTMENTS so the claim accrues its own §1c record.")
        applied.append((f"custom: {reason.strip()}", pp))

    factor, shrink_why = (1.0, "") if args.no_governor else governor_shrink()
    if factor != 1.0 and applied:
        applied = [(f"{lab}  [×{factor} GLOBAL SHRINK]", pp * factor) for lab, pp in applied]

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
    if factor != 1.0:
        print(f"⚠ GLOBAL SHRINK APPLIED (×{factor}) — every magnitude above is already halved.")
        print(f"  {shrink_why}")
    elif shrink_why:
        print(f"  {shrink_why}")
    print("─" * 60)
    # Machine-parseable attribution tag: paste it into the ledger leg cell so calib.py's
    # §1c can score each adjustment's skill as decided rows accrue (the prerequisite for
    # ever auto-calibrating these magnitudes instead of trusting the written values).
    tag_parts = [f"{key}{pp:+g}" for key, pp in resolved]
    tag_parts += [f"custom{float(c.partition(':')[0]):+g}" for c in args.custom]
    if factor != 1.0:
        tag_parts = [f"{key}{pp * factor:+g}" for key, pp in resolved]
        tag_parts += [f"custom{float(c.partition(':')[0]) * factor:+g}" for c in args.custom]
        if tag_parts:
            tag_parts.append("GLOBAL_SHRINK×%g" % factor)
    tag = f"[adj: {', '.join(tag_parts)}]" if tag_parts else "[adj: none]"
    print(f"Ledger tag — paste into the leg cell: {tag}")
    print("  (calib.py §1c attributes per-adjustment skill from these; '[adj: none]' rows")
    print("   are the market-anchored control group.)")
    print("─" * 60)
    print("Log this TrueP at BET TIME (never reconstruct). Edge vs the BEST-priced")
    print("no-vig line is the min-edge gate: ≥+2pp standalone / ≥+3-4pp parlay anchor.")


if __name__ == "__main__":
    main()
