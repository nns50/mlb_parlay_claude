# Fade Registry — living list of active fades + validation log

**Purpose.** One canonical, tracked place for every fade we lean on — team fades, K-Over
fades, parlay-construction fades, and data/status traps — each with its **reason**, the
**date added**, and a **running W/L validation log** so we can see which fades are actually
working and which have gone stale. This replaces having these scattered across `CLAUDE.md`
prose and individual `parlays/*.md` files. `CLAUDE.md` holds the *doctrine* (why a fade
exists); **this file holds the *live entries + tallies* and is the source of truth for what is
active right now.**

**A "fade W" = the fade was correct** (the team we faded lost / the K-Over we faded went Under /
the construction we avoided would have lost). **A "fade L" = the fade missed** (the thing we
faded won / hit anyway).

---

## Validation protocol (run EVERY session)

1. **Consult before building.** Read this file at session start. Do NOT bet against an entry's
   direction (e.g. lay a price on a fade-list team, or fade an elite ace's K-Over) without first
   checking that entry's recent log and status.
2. **Validate on the 09:00 / prior-day-review run.** When settling the prior day's finals, for
   EVERY active entry that touched a game played yesterday, append a dated **W or L** to its log,
   bump the tally, and update **Last validated**.
3. **Validate on any settle.** When the user reports a played ticket or you self-settle a result,
   update any entries that were in play.
4. **Status transitions:**
   - **ACTIVE → NEUTRAL** when an entry's recent log goes ~.500 or worse over its last ~4-5 tests
     (the edge has decayed). Keep it listed as NEUTRAL with a note; don't delete history.
   - **NEUTRAL → RETIRED** after the reason no longer holds (e.g. a fade-as-fav team's last-15
     climbs back above .550 w/ positive run diff). Move to the Retired section with the date + why.
   - **NEW** entries: add when a run identifies a fresh pattern (a "was hot, now cold" team, a
     newly contact-heavy lineup, etc.). Seed the log with the triggering game.
5. **Commit the update** (commit → push → PR → squash-merge) every time this file changes, same as
   the parlay files.

---

## A. Team fades — FADE AS FAVORITE ("was hot now cold" / just bad)
Do not lay a price on these as favorites. Re-verify last-15 form each session.

| ID | Team | Reason | Added | Last val | Fade log (most-recent first) | Status |
|----|------|--------|-------|----------|------------------------------|--------|
| A3 | **Tigers** | L15 7-8 (7/31), +7 run diff — mediocre, not clearly hot or cold | 5/28/26 | **8/1/26** | **L (7/31: DET −132 fav beat ATH 13-1 — no fade lean was applied (correctly, per NEUTRAL status), but a hypothetical fade would have MISSED big)** · (7/31: L15 recomputed via teamform — 7-8, +7 run diff, mixed 6/10 stretch vs CHC/KC/BAL) · L (6/11: DET −122 won 11-0 vs MIN as fav — fade MISSED) · W (6/10: lost 4-6 vs MIN as fav) · L (6/9: beat MIN 10-4 as fav) · L (6/7: beat SEA 5-4) · W (6/6) · L (6/3 won as DOG) · W (5/29) · W (5/28) | **NEUTRAL** — L15 7-8/+7 is genuinely mediocre; the 13-1 blowout as fav is one data point, not enough to re-flag as a fade-fav candidate. Re-verify next check. |

> **Corollary (added 6/3/26):** "Fade as FAVORITE" ≠ "safe to bet AGAINST." A fade-list team can
> win outright as a live dog (Tigers swept TB 6/3; TB −1.5 vs DET-class burned 6/1). Never lay a
> run line against a fade-as-fav team — the fade is about not *trusting them when favored*, not
> about treating them as dead money.

## B. Team value — UNDERDOG "quietly hot"
Potential underdog value (good record-vs-form mismatch in our favor). Dogs = lower floor → usually
standalone, not parlay-floor legs.

| ID | Team | Reason | Added | Last val | Value log | Status |
|----|------|--------|-------|----------|-----------|--------|
| B1 | **White Sox** | 58-51 (.532), L15 9-6 (+17 run diff) — genuine dog value, currently leads AL Central | 5/28/26 | **8/7/26** | **L (8/6: lost 11-12 @ BOS as a road dog — THIRD straight Fenway loss, but this one by a single run in a 23-run game; dog value MISSED narrowly, recent dog tests now 2-3)** · **L (8/5: SHUT OUT 0-4 @ BOS — the +1.5 RL expression of this entry died by a 4-run margin and killed the recommended ticket; SECOND straight Fenway blowout loss)** · **L (8/4: lost 2-14 @ BOS as a +120 road dog — blown out; dog value MISSED)** · **W (8/2: beat TB 9-1 as a road dog at the Trop — 2nd blowout dog win over TB in 3 days; entry reaffirmed, CWS 59-52 / +55 run diff)** · **W (7/31: beat TB 6-1 as ~+123 road dog vs Nick Martinez — dog value HIT big)** · (7/31: L15 recomputed — 9-6, +17 run diff, took 2 of 3 vs NYY 7/28-7/30) · W (6/18: beat NYY 5-1 @ NYY as +180 road dog — dog value HIT) · L (6/17: lost 5-10 @ NYY as +135 road dog) · L (6/16: lost 2-12 @ NYY as +161 road dog) · W (6/14: beat LAD 6-4 as home dog) · L (6/13: lost 1-7 to LAD) · W (6/12: beat LAD 8-2 as +178 dog) · W (6/10: beat ATL 2-1) · W (6/9: beat ATL 6-5) · L (6/7) · W (6/6) · L (6/5) · W (6/4) | **NEUTRAL (transitioned 8/6/26 from WATCH).** Dog value validated 7/31 + 8/2 (both vs TB), then CWS were hammered 2-14 at Fenway on 8/4. Recent dog tests now 2-1. Run diff is still the anchor (+43, first in the AL Central at 59-53), so the entry HOLDS and `hot_dog +3pp` stays live — but on 8/5 the entry is expressed on the **+1.5 run line**, not the ML, because the 45-49% band is PULSE-COOLED. Keep scanning CWS road-dog spots as a value candidate. **8/6 UPDATE: two straight losses at Fenway by 12 and 4 runs (2-14, 0-4) take recent dog tests to 2-2 and the entry to NEUTRAL. `hot_dog+3` is NOT to be expressed again until the entry wins a test.** Not retired: run diff (+43, still first in the AL Central at 59-54) is the doctrine-mandated anchor and it has not moved — a two-game streak is exactly the noise the run-diff rule exists to ignore. |
| B2 | **Pirates** | **L10 2-8, re-heat dead; blown out 2-11 @ ATH 6/15 as a road dog** | 5/26/26 | **6/16/26** | **L (6/15: lost 2-11 @ ATH as +124 road dog — dog value MISSED, shelled)** · L (6/11: lost 8-6 to LAD as +150 home dog) · W (6/10: beat LAD 9-8 walk-off as +150 dog) · L (6/9: lost 3-12 to LAD) · L (6/6) · L (6/5) · W (6/4) | **RETIRED 8/6/26** — 2-6 recent dog tests after 8/5 (PIT lost 2-4 @ MIL as a road dog). The re-heat premise has been dead for seven weeks and the entry has not been actionable since 6/16; PIT are 57-60 with L10 3-7. Kept here for history; no dog-value lean on Pittsburgh. |
| B3 | **Twins** | Still cold — **L10 3-7, −24 run diff (6/4)**; offense quiet, pen ok | 5/28/26 | **6/4/26** | L (6/4: L10 3-7) · L (5/28 lost 6-2) | **NEUTRAL (soft-matchup only)** |
| B4 | **Tigers** | dog value cooling — lost 2-4 @ HOU 6/16 AND 2-4 @ HOU 6/17 (Mize) | 6/3/26 | **6/17/26** | **L (6/17: lost 2-4 @ HOU again — dog value MISSED 2nd straight)** · L (6/16: lost 2-4 @ HOU as road dog) · W (6/15: won 9-3 @ HOU as +159 road dog) · W (6/3 won 7-2 as +122 dog) | **WATCH→leaning RETIRE (dog value 2-2)** — dropped both back-to-back @ HOU; the HOU series re-heat is over. Standalone-only; retire next run if it stays cold. |
| B5 | Angels / Astros | Honorable mention — surging; Astros stay AUTO-FADE K-Over (back on ML/total only) | 5/28/26 | — | _seed_ | **WATCH** |

## C. K-Over fades (lineup / structural / situational)
The signals that suppress a K-Over AND make the K-Under the +EV side. **Critical refinement
(6/3/26): do NOT HARD-fade a genuinely elite-K ace's K-Over off a SINGLE suppressor** — log it as a
live standalone Over and price both lines; stack the fade only when MULTIPLE suppressors pile up.

| ID | Fade | Reason | Added | Last val | Fade log | Status |
|----|------|--------|-------|----------|----------|--------|
| C1 | **Contact lineups: Royals, Astros, Guardians, D-backs** (K-Over against) | Low-K lineups suppress even elite arms; can also beat aces on the scoreboard | 5/25/26 | **8/5/26** | **W (8/4: Joe Ryan 3 K vs KC — the C1 contact-lineup suppression landed hard on a 5.5 line; `second_meeting −4` also validated on the same leg)** · **L (8/2: Gavin Williams 10 K vs AZ — the contact premise missed badly; the C1-backed K-UNDER scan candidate lost)** · L (6/3 Burns 9 K vs KC) · W (5/27 deGrom held to 6 K vs HOU) · W (5/25 Warren 3 K vs KC) | **ACTIVE but variance-heavy — 3-2 after the 8/4 Joe Ryan/KC hit; still burned in BOTH directions** (8/3 refinement: the 8/2 slate split K-Unders 2-2 and the split was clean — *form-collapse / capped-start* Unders WON (Kirby 3K, Sheehan 4K) while *contact-lineup* Unders LOST (Burns 9K, Williams 10K). Prefer the start-length thesis over the contact thesis when choosing a K-Under.) (suppression missed on Overs 6/3 AND on an Under 8/2); treat C1 as a ±1-tier modifier only, never the primary thesis of a leg |
| C2 | **2nd-meeting within 14d** (downgrade K-Over one tier, two if prior went heavily over) | Hitters adjust 2nd look; K rate drops ~10-15% | 5/x/26 | 6/3/26 | **L (6/3 Sanchez 9 K vs SD, faded as HARD on lone 2nd-mtg)** | **DOWNGRADE-ONLY, not a reject** (per 6/3 refinement) |
| C3 | **Structural pitch-count uncertainty** (TJ-return, MLB debut, post-IL, opener-conversion, quick-hook mgr) | Left-tail on start length the K/9 can't see → take deeper alt / off parlay floor | 5/26/26 | — | W (5/26 Strider 5 K, 5.5 would've busted) | **ACTIVE** — START-LENGTH axis only; don't downgrade per-pitch stuff (Cole/Skenes refinement) |
| C4 | **Designated openers** (planned 1-2 IP) | Pitch-count ceiling kills the Over | 5/x/26 | — | _seed_ | **ACTIVE (auto-fade)** |
| C5 | **Tight-zone HP umpire** | Suppresses K-Overs | 5/x/26 | — | _seed_ | **ACTIVE (check each K-Over)** |
| C6 | **Over-fading elite-K aces** (META-fade: fade our own over-fade) | We faded Sanchez 9 K, Burns 9 K (6/3), Harrison 12 K (6/2) — all hit | 6/3/26 | **8/7/26** | **8/6 (settled 8/7): Dylan Cease struck out 10 vs TOR. BOTH governed-out expressions cashed — the COOLed O7.5K (−105) and the SUSPENDED O6.5K alt (−196). This is the SECOND consecutive slate on which an elite-K-rate arm (13.12 K/9) with ZERO active suppressors beat the exposure governor. Re-warm counter: this is win #2 of the ≥3-of-5 needed to un-suspend.** · **8/5: the two sides of C6 landed on the SAME game. Skenes went 6 K vs a 6.5 line — the FIFTH one-strikeout-short miss in nine days, validating the `K-Over ≤6.5` SUSPENSION — while Kyle Harrison, whose U6.5 we declined at −150, struck out 10 after a 28-day layoff. Read together: the suspension is protecting us on the Over side, and the elite-arm-Under is still the more dangerous side to take. Also 8/5: Sonny Gray 8 K (the shaded-out U5.5 would have LOST — shade correct) and Pallante 4 K (the shaded-out U4.5 would have WON — shade cost us), i.e. the K-Under shade went 1-1 on the night.** · **8/4: FOUR more one-short misses in a single night — Skubal 6 vs O7.5 ❌, Luzardo 7 vs O7.5 ❌, Cantillo 5 vs O5.5 ❌, and our own anchor Holmes 5 vs U4.5 ❌; Singer 6 vs O4.5 ✅ was the lone K-Over hit. `pulse.py` escalated `type:K-Over ≤6.5` from COOL to **SUSPEND** (2-6, 25% vs 55% claimed) and holds ≥7.5 at COOL (1-4, 20%).** · **7/25: Cease O7.5K (Tier-1 standalone) ✅ 9.0 IP CG shutout, 12 K — dominant, no suppressors active, biggest edge of the slate (+8.8pp).** · 6/24: Ryan O5.5K (Tier-1 standalone) ✅ 9 K in 6.0 IP · 6/16: Cease O6.5K (Tier-1 standalone) ✅ 7 K in only 5.0 IP — cashed despite the short start; elite K-RATE (13.63 K9) carried it past 6.5 · 6/9: Cease 11K ✅, Skenes 7K ✅over6.5, Chase Burns 7K/5.1IP ✅over6.5 (Tier-1 rec), Wheeler 5K ❌under — 3 of 4 cashed · 3 straight fades MISSED 6/2-6/3 → correction installed | **⚠ ACTIVE CORRECTION — AND NOW IN OPEN CONFLICT WITH `pulse.py` (8/6/26).** **8/6: Dylan Cease struck out 10. BOTH rejected expressions would have cashed — the COOLed O7.5K (-105, rated 0.0pp after shading) and the SUSPENDED O6.5K alt (-196).** Elite K-rate arm (**13.12 K/9**, 2.41 ERA, 1.08 WHIP), zero active suppressors, and the exposure governor talked us out of both sides of it. **This is the second straight elite-arm K-Over the governor has killed that then cashed**, and it means C6's original warning (don't reflex-fade an elite ace — price it and play by edge) and `pulse.py`'s live COOL/SUSPEND are now contradicting each other on a *specific, repeatable, identifiable* class of leg. ⚠ **Held as a FLAG, not a doctrine flip:** the suspension is 2-6 (25% vs 55% claimed) and re-warms mechanically at ≥3 of the last 5 — **this is win #1**, and one winner does not un-suspend a dimension. But if the elite-arm/zero-suppressor subclass keeps cashing inside a cold aggregate, the right fix is to *split the dimension* (elite-K-rate arms vs the rest) rather than keep faded a subclass that is winning. Revisit at the n≥20 registry review. — **8/4/26 counterweight:** **The one-strikeout-short misses have spread below the 7.5 line: Schlittler 6 K vs 6.5 on 8/3 (Tier-1 standalone AND both parlay tickets died on it), after Cease 7 vs 7.5 and Skenes 7 vs 7.5 on 8/1 and Gilbert 4 vs 5.5 on 7/26.** After this run's ledger repair `pulse.py` fires a **COOL on `type:K-Over ≤6.5` (2-3, 40% vs 56% claimed)** on top of the standing ≥7.5 warning (1-3, 25% vs 58%) — i.e. **both** K-Over line buckets are now running well under their claimed rates, while `type:K-Under` runs **5-2 (71% vs 53%)**. C6's original point still holds (don't *reflex-fade* an elite arm's Over), but the live exposure reading is the opposite of a green light: a K-Over now needs its edge to survive a halved adjustment, and the K-UNDER is the side the recent ledger rewards. Re-warms by winning ≥3 of 5. — 7/25 Cease (12K CG) is the strongest validation yet: elite K-rate arms with zero suppressors clear the line comfortably. Don't fade elite arms' K-Overs by reflex; price each + play by edge (NOT a blanket "always play" — Wheeler missed on start-length, and 7/26 Gilbert 4K/5.2IP missed with NO pre-flagged suppressor: a 63% TrueP leg losing is the 37% side, but it's the second reminder that even clean elite-arm K-Overs carry more one-night variance than an ML at the same TrueP — weight that when choosing the PARLAY leg vs the STANDALONE expression).** **7.5-LINE REFINEMENT (8/1/26 — Cease 7K + Skenes 7K one short the SAME night, + Gilbert 7/26): played K-Overs at the 7.5 STANDARD line are 1-3; at ≤6.5 they are 4-1. A 7.5 line on even an elite arm is a ~coin-flip start-length bet, not a 60% leg — when the standard line is 7.5, the PARLAY leg should be the one-lower alt (price via kprice.py) or the stack's ML side; reserve the 7.5 Over for standalone expression. Early signal, small n — directional.** |

## D. Parlay-construction fades
Recipes to avoid when building.

| ID | Fade | Reason | Added | Last val | Log | Status |
|----|------|--------|-------|----------|-----|--------|
| D1 | **The +200-chase 3rd leg** (bolting a leg onto a clean 2-legger to stamp +200) | Drops floor ~15-18pp; the chase leg keeps busting | 5/30/26 | **7/29/26** | **W (7/26: STL ML −132 chase leg busted — CIN 5-3; Tier 3 +440 dead twice over while the flagged floor drop 39.7%→22.6% was exactly the trade rejected)** · L (7/25: LAD ML chase leg on top of Cease K-Over + TB ML WON — Tier 3 cashed at +416 despite the flagged floor drop 36.1%→22.0%) · W (6/3 TB chase leg busts, LAD+PHI cashes) · W (6/2 declining the +270 saved us) · W (6/1 chase cost us) | **ACTIVE — 4-1 (80%), still the strongest fade on the board. The answer to "hit +200 more often" is NOT a 3rd leg — it's a 2-leg construction whose product already reaches the band (`tools/ticket.py` searches for exactly that).** |
| D2 | **Heavy-fav ML anchors (-350 or worse)** | ~Zero payout contribution, still ~20% bust | 5/27/26 | 5/27/26 | W (5/27 faded LAD -420, NYY sub cashed) | **ACTIVE** |
| D3 | **−1.5 RL on a heavy fav vs a live dog** | Carries full ML loss prob + win-by-2 risk; dog wins outright ~35-40% | 6/1/26 | 6/1/26 | W (6/1 TB −1.5 lost outright to DET) | **ACTIVE** |
| D4 | **Favorite ML w/ own SP ERA ~5.00+** (esp. two-bad-SP shootouts) | High-variance; favorite can be blown out as the "right" side | 5/28/26 | **8/6/26** | **W (8/5: PHI −180 with Painter at 6.72 ERA / 1.61 WHIP → PHI LOST 4-10 at home to WSH; the textbook version of the trap, and the +175 dog we logged-but-declined was the money side)** · **W (8/3: HOU −130, Javier 7.17 own-SP trap → HOU LOST 1-3 to TOR)** · **W (8/3: MIL −146, Sproat 5.05 → MIL LOST 3-4 to PIT)** · **L (8/3: PHI −146, Nola 5.61 → PHI WON 6-3 anyway)** · L (8/1: SD −138, Buehler 5.13 own-SP trap → SD WON 6-5 anyway vs SF) · **W (6/17: WSH −130, Littell 5.32 own-SP trap + KC/Avila 6.19 two-bad-SP → WSH LOST 2-6 to KC; reject vindicated)** · L (6/16: MIL −148, Gasser 6.38 → MIL WON 2-1 vs CLE) · L (6/15: LAD −166, Lauer 5.47 → LAD WON 4-3) · L (6/7: PHI −161, Nola 5.55 → PHI WON 9-5) · W (6/6: PHI −136, Painter 5.74 → lost 3-6) · W (6/5: AZ −134, Kelly 5.06 → 1-14) · W (5/28 DET/Flaherty 5.94 → 7-1) | **ACTIVE — 7-5, REJECT-AS-ANCHOR ONLY** (8/3 tested it three times on one slate and went 2-1: both two-bad-SP shootouts, MIL and HOU, lost as favourites; the lone miss was PHI/Nola winning anyway. Still just above a coin flip — keep declining these as a clean parlay ANCHOR since the process risk is real, but do not treat a reject as a confident bet-against.) |
| D5 | **Bullpen-game opponent ≠ ML boost** — do NOT shade a fav UP because the other side has an opener/no real starter | The opposing pen can shut your offense down AND the lineup can tee off on your ace; a no-starter opponent is variance, not a free upgrade | **6/4/26** | **6/9/26** | **W (6/9: ATL −148 vs CWS's Eisert bullpen game; held ATL 60% NOT boosted — still LOST 5-6, killed the user's $30 parlay. The discipline was right but the leg was just thin/-EV-ish; 2nd validation of the spot)** · **W (6/4: bumped ATL 67→69% vs TOR's Fluharty pen game; lost 7-2)** | **ACTIVE — 2-0, CONFIRMED firm rule** (both sightings = ATL fav vs a bullpen-game opponent, both LOST) |
| D6 | **NYM ML favored vs MIA, priced beyond team-quality** — REJECT-as-anchor (NEW 8/1/26) | Recurring series pattern: NYM (47-64, RDiff −52) keeps getting priced as home fav vs MIA (56-55, RDiff +7) regardless of which NYM starter (McLean, Peralta, now Thornton) — the number looks driven by home field/recency, not a real team-quality edge | **8/1/26** | **8/2/26** | **W (8/2: Stock REJECT correct — MIA 2-0 NYM, Alcantara shut them out; 5th sighting)** · **W (8/1: Thornton REJECT correct, MIA won 6-2 — the MIA ML +118 value side also cashed)** · W (7/31: Peralta REJECT correct, MIA won 5-2) · L (7/30: REJECT missed, NYM won 4-2) · W (7/26: McLean REJECT correct, MIA won 5-2) | **ACTIVE (promoted 8/3/26) — 5 sightings, 4-1 (80%).** Past the 2-3× process-lesson bar; NYM-favored-vs-MIA is now a confirmed matchup trap: never anchor it, and price the MIA side as the live value. 8/1 build correctly took the actual +EV side (MIA ML +118, custom+4pp, WON) rather than just rejecting NYM. |

## E. Data / status traps (verification gates — fade the BAD DATA, not a team)
Not team fades, but recurring data errors to actively guard against each run.

| ID | Trap | Reason | Added | Last val | Log | Status |
|----|------|--------|-------|----------|-----|--------|
| E1 | **Search "final" that re-stamps the prior day** (day-of-week mismatch / reused box score) | Engine conflates adjacent games in a series | 6/3/26 | 6/3/26 | Caught 6/3 SEA "8-3 Tuesday" re-stamp (twice) | **ACTIVE GATE** |
| E2 | **Stale SP stat aggregate** (frozen at a prior start) | Season ERA/WHIP can lag 2+ starts in a hot/cold swing | 5/29/26 | 5/29/26 | Caught 5/29 Imanaga 2.32→4.04 | **ACTIVE GATE** |
| E3 | **Carried-over / mis-attributed probables** | Rotations rotate; search surfaces yesterday's matchup; wrong team attribution | 5/26/26 | **8/4/26** | Caught 6/3 Peralta-to-Brewers mislabel; 5/27 Cole/Cameron. **8/4 16:00: `recheck.py` fired on WSH @ PHI — Zack Littell → Carson Palmquist.** No leg was built on that game so nothing was invalidated, but the replacement changes it completely (Palmquist 7.31/1.63 with his last six outings at 3.0/0.1/1.2/1.1/1.1/2.0 IP = an opener profile, i.e. a WSH bullpen game → D5, no PHI boost). The mechanical snapshot-diff caught it without any judgment call | **ACTIVE GATE** |
| E4 | **TBA starter** (build leans on an unannounced SP) | Fails SP-freshness gate → no bet | 5/x/26 | **8/4/26** | 6/3 MIL TBA → no bet (correct). **8/4: both gated games lifted at 16:00 and the gate paid off in an unexpected direction** — DET@SEA (Melton posted, 1.75/0.93) produced a genuine +3.0pp Under read, but LAA@BAL, which the 11:00 build had called "a screaming Over signal" pending the other arm, priced at **+0.8pp** once Povich (5.12/1.34 but 3 GS and last logged 5/07) and a 7 mph wind-IN were actually known. **Calibration note: a loud ERA on one side is not a total read** — the gate protected us from a leg the pre-gate narrative wanted | **ACTIVE GATE** |

---

## Retired (kept for history)
- **A1 — Cubs (fade-as-favorite)** — RETIRED **7/31/26**. The "was-hot-now-cold" premise no longer
  holds at all: **L15 10-5 (.667), +43 run diff (teamform 7/31)**, well clear of the .550 retire bar
  the doctrine sets, and the fade-as-fav log had already drifted to 5-6 (coin-flip) with two straight
  misses (6/17, 6/19 blowouts). CHC (62-47, .569, +89 season run diff) is now a legitimately good team —
  no longer a team to fade when favored. Re-add only if they relapse to a sub-.450 last-15.
- **A2 — Rangers (fade-as-favorite)** — RETIRED **6/4/26**. The "was-hot-now-cold / just-bad" premise no
  longer holds: **L15 8-7, L10 6-4, W5 active streak, +11 run diff.** L15 .533 is a hair under the strict
  .550 retire bar, but the fade was already NEUTRAL, had **missed its last test** (5/29 — TEX blew out KC
  9-1), and the club is clearly trending up — no longer a team to fade when favored. Re-add only if they
  relapse to a sub-.450 last-15. (Validated via `mlb_api.sh standings`/`teamform`.)

---

### Running scoreboard (fades that have been tested)
- **🆕 8/7/26 — NEW observation, 1 sighting, NOT promoted: MECHANICAL kills beat DISCRETIONARY kills.**
  On 8/6 the corrected `pulse.py` mechanically withdrew SD@AZ Over 9.0 — it **lost by 3** (kill correct).
  The same day, the 16:00 run *discretionarily* killed two legs on fresh narrative — WSH@PHI Over 9.0 on a
  new weather read and CWS@BOS Over 9.0 on a line move away from us — and they finished **10 runs** and
  **23 runs**, the biggest total of the slate. **Governor 1-0, in-run human kills 0-2 on a single slate.**
  One sighting of a process claim; needs 2-3 to promote. Logged now so it is graded on its own ledger
  rather than remembered selectively.
- **8/7/26 — Angle B (opposing-SP hits-allowed Over): the honest ALL-candidate record is 6-3 would-have,
  NOT the "5-0 / every candidate has cashed" previously written here.** ⚠ **CORRECTED 8/7/26 (deep-dive
  audit):** the 5-0 chain (6/6 Kochanowicz, 8/3 Nola 6 H + Lorenzen 7 H, 8/6 Mikolas 12 H + Castillo 6 H)
  silently excluded the FOUR 8/5 candidates logged in `results_log.md` the day before — Kremer O5.5 (**3 H,
  would-L**), Bratt O4.5 (**1 H, would-L**), Irvin O4.5 (**would-L**), Anderson O2.5 (**would-W**). Full
  record: **6-3 (67%)** — a real positive lean, but the left tail (hook/short start) bit 3 of 9, which is
  exactly what the shade prices. The candidate set for this record is now FIXED as "every Angle B row
  logged in results_log.md User-angle tracking" — no narrative selection. N=9, under the 20-30 bar; the
  shade-magnitude question stays open for the registry review but the "one-sided for two months" framing
  was an artifact of the skipped rows.
- **D1 (+200-chase):** 3-0 ✅ — most reliable fade.
- **8/6/26 — a NEW fade-shaped observation, logged but NOT yet promoted (1 sighting):** the pulse
  **band-shade produced its cleanest single validation to date.** LAA@BAL Over 9.5 was the loudest
  thesis of the day (Ryan Johnson **7.63 ERA / 1.59 WHIP**, 88°F, 8 mph out to CF), rated **+4.0pp
  pre-governor** and killed by the COOLed+SHADED 55-59 band. **The game finished 4-1 — five runs.**
  The disclosed baseline-shop that would have revived it at +4.0pp, the biggest edge on the board,
  **would have lost.** Counterweight in the same session: the governor was *wrong* twice on Cease
  (see C6). Net 1-2 on the day's governor calls. Recorded so the band-shade is graded on its own
  ledger rather than on whichever direction stings most recently.
- **✅ PROMOTED 8/7/26 (3rd sighting) — `hitter_park_over` / `pitcher_park_under` may NOT be the primary
  thesis of a leg; they are TIEBREAKERS ONLY.** The third sighting arrived on 8/6 and it was emphatic:
  `pitcher_park_under+3` lost **NYM@CLE Under 7.5 by 11.5 runs** (19 total) *and* **DET@SEA Under 8.0 by 3**,
  while `hitter_park_over+3` lost **SD@AZ Over 9.0 by 3**. The two park-tagged legs that DID win that day
  (CWS@BOS 23 runs, WSH@PHI 10 runs) each had an independent *matchup* thesis carrying them — Castillo and
  Mikolas are contact-manager profiles who gave up 6 and 12 hits respectively. Per the tiered bar this is a
  **process/logical lesson at 3 sightings → promoted to doctrine**, not a hit-rate claim needing n≥20.
  **Rule: a park tag may break a tie between two legs that each already have a real matchup thesis. It may
  never manufacture an edge where no thesis exists, and it may never anchor a Tier 1.** `calib.py` §1c
  corroborates: `hitter_park_over` 4-4 / −0.0005 skill, `pitcher_park_under` 2-3 / −0.0066 skill.
- **8/6/26 — `hitter_park_over` / `pitcher_park_under` as a THESIS (not a tiebreaker) — the 2-sighting
  entry that produced the promotion above (kept for history).** 8/5's review found
  `hitter_park_over` went 1-2 with its lone winner driven by bullpen innings rather than the park.
  8/6: **NYM@CLE Under 7.5 carrying `pitcher_park_under+3` lost by 11.5 runs (19 total) through the
  slate's best matched WHIP pair (1.12 / 1.07)** — the second blowout in two days on that same
  total. Both park tags are on notice: use them to break a tie between two real matchup theses, not
  to manufacture an edge where no thesis exists.
- **D2/D3 (construction):** 1-0 each ✅.
- **D4 (own-SP ERA ~5+ fav):** **3-3** — now 3 straight misses (6/7 PHI/Nola 9-5; 6/15 LAD/Lauer 4-3; 6/16 MIL/Gasser 2-1) after 3 early hits (6/6, 6/5, 5/28). At .500 it's **reject-as-anchor only** — no longer a "bet against the trap fav" edge.
- **A1 (Cubs as fav):** **5-6** — 6/19 missed AGAIN (CHC 16-2 blowout vs TOR, 7-run 1st); L15 recovered to 8-7/+5. **Transitioning to NEUTRAL → leaning RETIRE.** CHC is no longer clearly "was hot now cold" — they've stabilized.
- **C6 (don't over-fade elite K-aces):** re-validated 6/16 — Cease O6.5K (played Tier-1) hit 7K in 5 IP; elite K-rate clears the line even on a short start.
- **D5 (bullpen-game ≠ ML boost):** 1-0 ✅ NEW 6/4 — ATL bumped to 69% vs TOR's pen game, lost 7-2.
- **C1 (contact-lineup K-Over):** 2-1 — real but variance-heavy; don't hard-fade one-suppressor aces.
- **C2 (2nd-meeting K-Over):** 0-1 — downgrade-only, not a reject.
- **C6 (meta — over-faded aces):** correction installed after 3 straight misses (Sanchez, Burns, Harrison).
  ⚠️ **Counter-data 6/4: Sale O6.5K (one mild suppressor, TOR 19% vs LHP) MISSED — 6 K in 5.2 IP.** C6
  still stands (don't *hard-fade* an ace's over off one suppressor), but the right expression vs one
  suppressor is the **one-tier-deeper alt (O5.5 would've cashed)**, not the full standard line.
- **A1 (Cubs as fav):** reaffirmed 6/5 — −158 fav crushed 3-18 by SF. Strongest active team-fade.
- **Anchor-decompose / dog-value misses (6/5, logged, no rule change):** Braves −142 anchor-fade MISSED
  (ATL won 6-3); B2 Pirates dog lost 3-6 @ ATL; B1 CWS dog lost 6-8 (close). All within variance — dog-value
  tags are standalone-only and a single dog L is not a signal.
- **A2 (Rangers as fav):** **RETIRED 6/4** — recovered (L15 8-7, L10 6-4, W5, +11).
- **A3 (Tigers as fav):** 2-1 — but now winning as a dog (do not lay runs against).
- **B1 (White Sox dog value):** confirmed 6/4 — L15 9-6 (.600), +23 run diff.
- **B2 (Pirates dog value):** **COOLED 6/7** → NEUTRAL — lost both @ ATL 6/5-6/6 (3-6, 3-6), L15 8-7/+5, L2; re-heat faded.

- **6/8 slate (8 games): no A/B fade team played** (Cubs/Tigers/White Sox/Pirates/Twins all off or absent),
  so no team-fade validation this date. **D4 note:** HOU's Arrighetti was 1.94 (NOT a 5+ trap) — correctly
  played, not faded. **settle.py team-side parser bug** surfaced (mis-flagged HOU-away "vs LAA" as an L) —
  caught by the StatsAPI cross-check, reinforcing E1 (always verify the raw final before settling).

> _6/4/26: the A/B re-verifications above were run deterministically via the new `tools/mlb_api.sh
> standings` + `teamform` (last-15 W-L + run differential), not WebSearch — first live use of the helper._

> _Seed note (6/3/26): logs marked "_seed_" had no clean test yet; fill them on the next run that
> touches the entry. Tallies will firm up as the registry accrues dated results._

> **7/31 slate note:** B1 (White Sox dog value) validated again — CWS 6-1 TB as a road dog. A3 (Tigers,
> NEUTRAL) saw DET blow out ATH 13-1 as fav; no fade lean was applied (correct call given NEUTRAL status),
> logged as a single data point, not enough to re-flag. No other active A/B/C/D entries touched a
> played leg that day (Skenes/Cease K-Over misses were played on their own edge, not a fade signal).

> **8/3 slate note (written 8/4).** **Favourites went 3-5 on an 8-game board** while the pulse
> `type:ML-fav` MARKET-SHADE had every one of them at 0.0pp edge — the shade's best single-day
> vindication so far (NYY −203 lost 7-13). **D4 tested 3× and went 2-1** (MIL/Sproat and HOU/Javier both
> lost as favs; PHI/Nola won anyway) → tally 4-4 to **6-5**. **E4 validated twice by outcome:** both TBA
> starters that resolved mid-slate produced losing lifted legs (Wrobleski O5.5K → 4 K; SF@TEX Over 8.0 →
> 6 runs). **No D1 test** — the ticket was a clean 2-legger, no chase leg. No A/B team entry played.
>
> **NEW counter-data, NOT promoted (1 sighting):** `wind_in_under` **at Coors is 0-1** — TB @ COL went
> **22 runs** on a 13 mph in-from-CF reading, the same reading that fired the 18:45 contingency to drop
> the Over 11.5. Per the tiered bar this is a single sighting of a *probabilistic* claim, so it stays a
> logged data point, not a fade. The lesson that IS promotable at 2-3 sightings is narrower: **do not let
> a wind reading alone move a Coors total without pulling the live line** — the market at Coors already
> prices wind, and our 8/3 model had the SP read pointing the other way.

