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
| A3 | **Tigers** | L15 7-8 (7/31), +7 run diff — mediocre, not clearly hot or cold | 5/28/26 | **8/8/26** | **L (8/8: DET −112 fav WON 8-0 @ SF behind Jackson Jobe's 5.0 shutout IP — a fade lean would have MISSED badly; no lean was applied, correctly, per NEUTRAL status)** · **W (8/7: DET −126 fav LOST 2-5 @ SF — a fade lean would have HIT; but the game was D5-blocked on SF's bullpen game so no lean was applied either way)** · | **L (7/31: DET −132 fav beat ATH 13-1 — no fade lean was applied (correctly, per NEUTRAL status), but a hypothetical fade would have MISSED big)** · (7/31: L15 recomputed via teamform — 7-8, +7 run diff, mixed 6/10 stretch vs CHC/KC/BAL) · L (6/11: DET −122 won 11-0 vs MIN as fav — fade MISSED) · W (6/10: lost 4-6 vs MIN as fav) · L (6/9: beat MIN 10-4 as fav) · L (6/7: beat SEA 5-4) · W (6/6) · L (6/3 won as DOG) · W (5/29) · W (5/28) | **NEUTRAL** — L15 7-8/+7 is genuinely mediocre; the 13-1 blowout as fav is one data point, not enough to re-flag as a fade-fav candidate. Re-verify next check. |

> **Corollary (added 6/3/26):** "Fade as FAVORITE" ≠ "safe to bet AGAINST." A fade-list team can
> win outright as a live dog (Tigers swept TB 6/3; TB −1.5 vs DET-class burned 6/1). Never lay a
> run line against a fade-as-fav team — the fade is about not *trusting them when favored*, not
> about treating them as dead money.

## B. Team value — UNDERDOG "quietly hot"
Potential underdog value (good record-vs-form mismatch in our favor). Dogs = lower floor → usually
standalone, not parlay-floor legs.

| ID | Team | Reason | Added | Last val | Value log | Status |
|----|------|--------|-------|----------|-----------|--------|
| B1 | **White Sox** | 58-51 (.532), L15 9-6 (+17 run diff) — genuine dog value, currently leads AL Central | 5/28/26 | **8/8/26** | ✅ **W (8/8: BEAT CLE 6-3 as a +120 home dog — dog value HIT, the entry's first winning test since 8/2; recent dog tests now 3-4)** · **L (8/7: lost 2-8 to CLE as a +130 home dog — dog value MISSED again; recent dog tests now 2-4 and the entry has not won a test since 8/2)** · | **L (8/6: lost 11-12 @ BOS as a road dog — THIRD straight Fenway loss, but this one by a single run in a 23-run game; dog value MISSED narrowly, recent dog tests now 2-3)** · **L (8/5: SHUT OUT 0-4 @ BOS — the +1.5 RL expression of this entry died by a 4-run margin and killed the recommended ticket; SECOND straight Fenway blowout loss)** · **L (8/4: lost 2-14 @ BOS as a +120 road dog — blown out; dog value MISSED)** · **W (8/2: beat TB 9-1 as a road dog at the Trop — 2nd blowout dog win over TB in 3 days; entry reaffirmed, CWS 59-52 / +55 run diff)** · **W (7/31: beat TB 6-1 as ~+123 road dog vs Nick Martinez — dog value HIT big)** · (7/31: L15 recomputed — 9-6, +17 run diff, took 2 of 3 vs NYY 7/28-7/30) · W (6/18: beat NYY 5-1 @ NYY as +180 road dog — dog value HIT) · L (6/17: lost 5-10 @ NYY as +135 road dog) · L (6/16: lost 2-12 @ NYY as +161 road dog) · W (6/14: beat LAD 6-4 as home dog) · L (6/13: lost 1-7 to LAD) · W (6/12: beat LAD 8-2 as +178 dog) · W (6/10: beat ATL 2-1) · W (6/9: beat ATL 6-5) · L (6/7) · W (6/6) · L (6/5) · W (6/4) | **NEUTRAL (transitioned 8/6/26 from WATCH).** Dog value validated 7/31 + 8/2 (both vs TB), then CWS were hammered 2-14 at Fenway on 8/4. Recent dog tests now 2-1. Run diff is still the anchor (+43, first in the AL Central at 59-53), so the entry HOLDS and `hot_dog +3pp` stays live — but on 8/5 the entry is expressed on the **+1.5 run line**, not the ML, because the 45-49% band is PULSE-COOLED. Keep scanning CWS road-dog spots as a value candidate. **8/6 UPDATE: two straight losses at Fenway by 12 and 4 runs (2-14, 0-4) take recent dog tests to 2-2 and the entry to NEUTRAL. `hot_dog+3` is NOT to be expressed again until the entry wins a test.** Not retired: run diff (+43, still first in the AL Central at 59-54) is the doctrine-mandated anchor and it has not moved — a two-game streak is exactly the noise the run-diff rule exists to ignore. |
| B2 | **Pirates** | **L10 2-8, re-heat dead; blown out 2-11 @ ATH 6/15 as a road dog** | 5/26/26 | **6/16/26** | **L (6/15: lost 2-11 @ ATH as +124 road dog — dog value MISSED, shelled)** · L (6/11: lost 8-6 to LAD as +150 home dog) · W (6/10: beat LAD 9-8 walk-off as +150 dog) · L (6/9: lost 3-12 to LAD) · L (6/6) · L (6/5) · W (6/4) | **RETIRED 8/6/26** — 2-6 recent dog tests after 8/5 (PIT lost 2-4 @ MIL as a road dog). The re-heat premise has been dead for seven weeks and the entry has not been actionable since 6/16; PIT are 57-60 with L10 3-7. Kept here for history; no dog-value lean on Pittsburgh. |
| B3 | **Twins** | Still cold — **L10 3-7, −24 run diff (6/4)**; offense quiet, pen ok | 5/28/26 | **6/4/26** | L (6/4: L10 3-7) · L (5/28 lost 6-2) | **NEUTRAL (soft-matchup only)** |
| B4 | **Tigers** | dog value cooling — lost 2-4 @ HOU 6/16 AND 2-4 @ HOU 6/17 (Mize) | 6/3/26 | **6/17/26** | **L (6/17: lost 2-4 @ HOU again — dog value MISSED 2nd straight)** · L (6/16: lost 2-4 @ HOU as road dog) · W (6/15: won 9-3 @ HOU as +159 road dog) · W (6/3 won 7-2 as +122 dog) | **WATCH→leaning RETIRE (dog value 2-2)** — dropped both back-to-back @ HOU; the HOU series re-heat is over. Standalone-only; retire next run if it stays cold. |
| B5 | Angels / Astros | Honorable mention — surging; Astros stay AUTO-FADE K-Over (back on ML/total only) | 5/28/26 | **8/9/26** | **L (8/8: BOTH halves LOST as dogs — LAA shut out 0-7 by MIA (Ureña 2.1 IP / 4 ER) and HOU lost 2-3 at SD; the one-night 8/7 dog sweep did not repeat, which is what a STALE seed row looks like)** · **W (8/7: BOTH cashed as dogs — LAA +146 beat MIA 4-3 and HOU +110 beat SD 6-3)** | **⚠ STALE — DO NOT APPLY AS WRITTEN; re-verified 8/8/26.** The 5/28 premise ('surging') is dead for one half and alive for the other, so the entry can no longer be cited as a unit. **Angels are 45-71 (−75 run diff), tied for the worst record in the AL** — the surge premise is falsified and no `hot_dog` lean is justified on LAA regardless of a one-night dog win. **Astros are 60-57 on an L10 of 8-2** but with a **−22 run diff**, i.e. hot by streak and mediocre by the run-differential anchor that doctrine says must gate team-form transitions — so HOU is a WATCH, not a `hot_dog` fire. **Neither half was expressed on 8/7 and neither should be today.** Split or retire this entry at the next review; a seed row covering two unrelated teams is not usable. |

## C. K-Over fades (lineup / structural / situational)
The signals that suppress a K-Over AND make the K-Under the +EV side. **Critical refinement
(6/3/26): do NOT HARD-fade a genuinely elite-K ace's K-Over off a SINGLE suppressor** — log it as a
live standalone Over and price both lines; stack the fade only when MULTIPLE suppressors pile up.

| ID | Fade | Reason | Added | Last val | Fade log | Status |
|----|------|--------|-------|----------|----------|--------|
| C1 | **Contact lineups: Royals, Astros, Guardians, D-backs** (K-Over against) | Low-K lineups suppress even elite arms; can also beat aces on the scoreboard | 5/25/26 | **8/5/26** | **W (8/7: Kevin Gausman 4 K in 7.0 IP vs KC — a 8.98 K/9 arm held to 4 over a full seven innings; the contact-lineup suppression landed again, C1 now 4-2)** · | **W (8/4: Joe Ryan 3 K vs KC — the C1 contact-lineup suppression landed hard on a 5.5 line; `second_meeting −4` also validated on the same leg)** · **L (8/2: Gavin Williams 10 K vs AZ — the contact premise missed badly; the C1-backed K-UNDER scan candidate lost)** · L (6/3 Burns 9 K vs KC) · W (5/27 deGrom held to 6 K vs HOU) · W (5/25 Warren 3 K vs KC) **L (8/10, settled 8/11: `splits TB` returned 18% K vs LHP — contact-heavy — and Jacob Lopez still struck out 5 in 7.0 IP, busting a 4.5 line. The contact read was correct about contact and wrong about the leg, because C1 prices whiffs and the Over was carried by START LENGTH. Third time a C1 signal has been beaten by innings rather than by stuff.)** | **ACTIVE but variance-heavy — **4-3** after 8/7 (Gausman 4 K in 7.0 IP vs KC, on top of the 8/4 Joe Ryan hit); still burned in BOTH directions** (8/3 refinement: the 8/2 slate split K-Unders 2-2 and the split was clean — *form-collapse / capped-start* Unders WON (Kirby 3K, Sheehan 4K) while *contact-lineup* Unders LOST (Burns 9K, Williams 10K). Prefer the start-length thesis over the contact thesis when choosing a K-Under.) (suppression missed on Overs 6/3 AND on an Under 8/2); treat C1 as a ±1-tier modifier only, never the primary thesis of a leg |
| C2 | **2nd-meeting within 14d** (downgrade K-Over one tier, two if prior went heavily over) | Hitters adjust 2nd look; K rate drops ~10-15% | 5/x/26 | 6/3/26 | **L (6/3 Sanchez 9 K vs SD, faded as HARD on lone 2nd-mtg)** | **DOWNGRADE-ONLY, not a reject** (per 6/3 refinement) |
| C3 | **Structural pitch-count uncertainty** (TJ-return, MLB debut, post-IL, opener-conversion, quick-hook mgr) | Left-tail on start length the K/9 can't see → take deeper alt / off parlay floor | 5/26/26 | — | W (5/26 Strider 5 K, 5.5 would've busted) | **ACTIVE** — START-LENGTH axis only; don't downgrade per-pitch stuff (Cole/Skenes refinement) |
| C4 | **Designated openers** (planned 1-2 IP) | Pitch-count ceiling kills the Over | 5/x/26 | — | _seed_ | **ACTIVE (auto-fade)** |
| C5 | **Tight-zone HP umpire** | Suppresses K-Overs | 5/x/26 | — | _seed_ | **ACTIVE (check each K-Over)** |
| C6 | **Over-fading elite-K aces** (META-fade: fade our own over-fade) | We faded Sanchez 9 K, Burns 9 K (6/3), Harrison 12 K (6/2) — all hit | 6/3/26 | **8/9/26** | **8/9 (settled 8/10) — the OTHER side of C6 landed the same night: Randy Vásquez struck out ONE in 5.0 IP and the U2.5 K we wrote at +116 (best of six books) cashed at a canter.** The read was pure recent-form-over-season-number (3.88 K/9 across his last 12 outings vs a 5.79 season line) and it was unbettable for the **sixth consecutive slate** — five of those on instrument availability, this one on the `custom` MARKET-SHADE pinning TrueP to the market. ⚠ **Read together with the Misiorowski row below, 8/9 killed BOTH an elite-arm K-Over and a weak-arm K-Under on the same board — the two opposite expressions of the same dimension — which is the clearest statement yet that the K market is currently excluded by construction rather than by judgement.** · **8/9: Jacob Misiorowski struck out 9 in 6.0 IP (3 ER) and MIL won 4-3 — BOTH unusable expressions cashed.** A **1.63 ERA / 0.73 WHIP / 13.82 K/9** arm, the best line on the board by a distance, and the build had no legal instrument for it in ANY market: `ace_edge` MARKET-SHADED to 0 killed the ML, and both K-Over buckets were COOLed and Tier-1-barred. **⚠ FIFTH consecutive slate on which an elite-K arm's edge was unbettable by construction rather than by judgement** (8/5 Skenes/Harrison, 8/6 Cease, 8/7 Tolle 14 K, 8/8 Jump 11 K, 8/9 Misiorowski 9 K). The pattern is no longer 'the governor was wrong about a leg' — it is that the elite-K subclass has been structurally excluded for a working week while continuing to cash. **Still held as a FLAG and resolved at the n≥20 registry review, not overridden in-build** — but the dimension-split fix (elite-K-rate arms vs the rest) proposed on 8/6 now has five sightings behind it and should be the first item at that review.** · **8/8: Gage Jump (ATH) struck out 11 in 6.0 IP at Fenway — the slate's biggest K game, again from a starter our scan never priced, and again in the ATH/BOS series that 8/7 flagged. ⚠ THIRD consecutive slate on which the sharpest prop on the board sat inside a game dismissed at its ML price. This is now PROMOTED past the 2-3× process bar: heavy chalk is a reason to skip a game's MONEYLINE, never a reason to skip its PROPS. Acted on 8/9 — the build ran a `core` prop sweep on ATH@BOS specifically because of this entry.** · **8/7: Payton Tolle struck out 14 in 6.0 IP (2 H, 1 ER) vs ATH — the largest K game of the night by a distance, from a starter our scan never priced because ATH@BOS was written off as a −260 chalk / total-only look. No leg was lost (the K-Over dimension is COOLed and the arm was off our board entirely), but it is the THIRD consecutive slate on which an elite-K performance landed outside what the governor would allow. ⚠ The distinct lesson here is not about the governor at all — it is that a game dismissed as chalk still had the slate's sharpest prop in it, and the scan never looked.** · | **8/6 (settled 8/7): Dylan Cease struck out 10 vs TOR. BOTH governed-out expressions cashed — the COOLed O7.5K (−105) and the SUSPENDED O6.5K alt (−196). This is the SECOND consecutive slate on which an elite-K-rate arm (13.12 K/9) with ZERO active suppressors beat the exposure governor. Re-warm counter: this is win #2 of the ≥3-of-5 needed to un-suspend.** · **8/5: the two sides of C6 landed on the SAME game. Skenes went 6 K vs a 6.5 line — the FIFTH one-strikeout-short miss in nine days, validating the `K-Over ≤6.5` SUSPENSION — while Kyle Harrison, whose U6.5 we declined at −150, struck out 10 after a 28-day layoff. Read together: the suspension is protecting us on the Over side, and the elite-arm-Under is still the more dangerous side to take. Also 8/5: Sonny Gray 8 K (the shaded-out U5.5 would have LOST — shade correct) and Pallante 4 K (the shaded-out U4.5 would have WON — shade cost us), i.e. the K-Under shade went 1-1 on the night.** · **8/4: FOUR more one-short misses in a single night — Skubal 6 vs O7.5 ❌, Luzardo 7 vs O7.5 ❌, Cantillo 5 vs O5.5 ❌, and our own anchor Holmes 5 vs U4.5 ❌; Singer 6 vs O4.5 ✅ was the lone K-Over hit. `pulse.py` escalated `type:K-Over ≤6.5` from COOL to **SUSPEND** (2-6, 25% vs 55% claimed) and holds ≥7.5 at COOL (1-4, 20%).** · **7/25: Cease O7.5K (Tier-1 standalone) ✅ 9.0 IP CG shutout, 12 K — dominant, no suppressors active, biggest edge of the slate (+8.8pp).** · 6/24: Ryan O5.5K (Tier-1 standalone) ✅ 9 K in 6.0 IP · 6/16: Cease O6.5K (Tier-1 standalone) ✅ 7 K in only 5.0 IP — cashed despite the short start; elite K-RATE (13.63 K9) carried it past 6.5 · 6/9: Cease 11K ✅, Skenes 7K ✅over6.5, Chase Burns 7K/5.1IP ✅over6.5 (Tier-1 rec), Wheeler 5K ❌under — 3 of 4 cashed · 3 straight fades MISSED 6/2-6/3 → correction installed | **⚠ ACTIVE CORRECTION — AND NOW IN OPEN CONFLICT WITH `pulse.py` (8/6/26).** **8/6: Dylan Cease struck out 10. BOTH rejected expressions would have cashed — the COOLed O7.5K (-105, rated 0.0pp after shading) and the SUSPENDED O6.5K alt (-196).** Elite K-rate arm (**13.12 K/9**, 2.41 ERA, 1.08 WHIP), zero active suppressors, and the exposure governor talked us out of both sides of it. **This is the second straight elite-arm K-Over the governor has killed that then cashed**, and it means C6's original warning (don't reflex-fade an elite ace — price it and play by edge) and `pulse.py`'s live COOL/SUSPEND are now contradicting each other on a *specific, repeatable, identifiable* class of leg. ⚠ **Held as a FLAG, not a doctrine flip:** the suspension is 2-6 (25% vs 55% claimed) and re-warms mechanically at ≥3 of the last 5 — **this is win #1**, and one winner does not un-suspend a dimension. But if the elite-arm/zero-suppressor subclass keeps cashing inside a cold aggregate, the right fix is to *split the dimension* (elite-K-rate arms vs the rest) rather than keep faded a subclass that is winning. Revisit at the n≥20 registry review. — **8/4/26 counterweight:** **The one-strikeout-short misses have spread below the 7.5 line: Schlittler 6 K vs 6.5 on 8/3 (Tier-1 standalone AND both parlay tickets died on it), after Cease 7 vs 7.5 and Skenes 7 vs 7.5 on 8/1 and Gilbert 4 vs 5.5 on 7/26.** After this run's ledger repair `pulse.py` fires a **COOL on `type:K-Over ≤6.5` (2-3, 40% vs 56% claimed)** on top of the standing ≥7.5 warning (1-3, 25% vs 58%) — i.e. **both** K-Over line buckets are now running well under their claimed rates, while `type:K-Under` runs **5-2 (71% vs 53%)**. C6's original point still holds (don't *reflex-fade* an elite arm's Over), but the live exposure reading is the opposite of a green light: a K-Over now needs its edge to survive a halved adjustment, and the K-UNDER is the side the recent ledger rewards. Re-warms by winning ≥3 of 5. — 7/25 Cease (12K CG) is the strongest validation yet: elite K-rate arms with zero suppressors clear the line comfortably. Don't fade elite arms' K-Overs by reflex; price each + play by edge (NOT a blanket "always play" — Wheeler missed on start-length, and 7/26 Gilbert 4K/5.2IP missed with NO pre-flagged suppressor: a 63% TrueP leg losing is the 37% side, but it's the second reminder that even clean elite-arm K-Overs carry more one-night variance than an ML at the same TrueP — weight that when choosing the PARLAY leg vs the STANDALONE expression).** **7.5-LINE REFINEMENT (8/1/26 — Cease 7K + Skenes 7K one short the SAME night, + Gilbert 7/26): played K-Overs at the 7.5 STANDARD line are 1-3; at ≤6.5 they are 4-1. A 7.5 line on even an elite arm is a ~coin-flip start-length bet, not a 60% leg — when the standard line is 7.5, the PARLAY leg should be the one-lower alt (price via kprice.py) or the stack's ML side; reserve the 7.5 Over for standalone expression. Early signal, small n — directional.** |

## D. Parlay-construction fades
Recipes to avoid when building.

| ID | Fade | Reason | Added | Last val | Log | Status |
|----|------|--------|-------|----------|-----|--------|
| D1 | **The +200-chase 3rd leg** (bolting a leg onto a clean 2-legger to stamp +200) | Drops floor ~15-18pp; the chase leg keeps busting | 5/30/26 | **7/29/26** | **W (7/26: STL ML −132 chase leg busted — CIN 5-3; Tier 3 +440 dead twice over while the flagged floor drop 39.7%→22.6% was exactly the trade rejected)** · L (7/25: LAD ML chase leg on top of Cease K-Over + TB ML WON — Tier 3 cashed at +416 despite the flagged floor drop 36.1%→22.0%) · W (6/3 TB chase leg busts, LAD+PHI cashes) · W (6/2 declining the +270 saved us) · W (6/1 chase cost us) | **ACTIVE — 4-1 (80%), still the strongest fade on the board. The answer to "hit +200 more often" is NOT a 3rd leg — it's a 2-leg construction whose product already reaches the band (`tools/ticket.py` searches for exactly that).** |
| D2 | **Heavy-fav ML anchors (-350 or worse)** | ~Zero payout contribution, still ~20% bust | 5/27/26 | 5/27/26 | W (5/27 faded LAD -420, NYY sub cashed) | **ACTIVE** |
| D3 | **−1.5 RL on a heavy fav vs a live dog** | Carries full ML loss prob + win-by-2 risk; dog wins outright ~35-40% | 6/1/26 | 6/1/26 | W (6/1 TB −1.5 lost outright to DET) | **ACTIVE** |
| D4 | **Favorite ML w/ own SP ERA ~5.00+** (esp. two-bad-SP shootouts) | High-variance; favorite can be blown out as the "right" side | 5/28/26 | **8/8/26** | **W (8/8: PHI −156 with Nola at 5.55 → PHI LOST 5-7 to TOR; both starters over 5.00, the textbook two-bad-SP shootout, 12 runs scored)** · ⚠ **NEW COROLLARY (promoted 8/9, 2nd sighting — 8/3 MIL/Sproat 5.05 was the first): when `~own_sp_hi` fires on OUR side because the OPPONENT's starter is bad, check whether OUR OWN starter is within ~0.3 of the 5.00 threshold. On 8/8 the mirror put us on STL −148 off Freeland's 6.81 — and Freeland threw 4.1 IP / 1 ER while STL's own Liberatore (4.97, three hundredths under the threshold) was tagged for 5 ER on 9 hits. A mirror stacked on a near-threshold own SP is not an edge; it is D4 pointed at us.** · **W (8/5: PHI −180 with Painter at 6.72 ERA / 1.61 WHIP → PHI LOST 4-10 at home to WSH; the textbook version of the trap, and the +175 dog we logged-but-declined was the money side)** · **W (8/3: HOU −130, Javier 7.17 own-SP trap → HOU LOST 1-3 to TOR)** · **W (8/3: MIL −146, Sproat 5.05 → MIL LOST 3-4 to PIT)** · **L (8/3: PHI −146, Nola 5.61 → PHI WON 6-3 anyway)** · L (8/1: SD −138, Buehler 5.13 own-SP trap → SD WON 6-5 anyway vs SF) · **W (6/17: WSH −130, Littell 5.32 own-SP trap + KC/Avila 6.19 two-bad-SP → WSH LOST 2-6 to KC; reject vindicated)** · L (6/16: MIL −148, Gasser 6.38 → MIL WON 2-1 vs CLE) · L (6/15: LAD −166, Lauer 5.47 → LAD WON 4-3) · L (6/7: PHI −161, Nola 5.55 → PHI WON 9-5) · W (6/6: PHI −136, Painter 5.74 → lost 3-6) · W (6/5: AZ −134, Kelly 5.06 → 1-14) · W (5/28 DET/Flaherty 5.94 → 7-1) **L (8/10, settled 8/11: PHI −114 with Andrew Painter at 6.48 ERA / 1.57 WHIP — the textbook D4 shape — WON 6-5 at STL. Painter went 5.0 IP / 3 ER, i.e. the own-SP read was not even wrong, the fade simply missed. Our own Tier-1 was the mirror side (STL +108) and lost with it.)** | **ACTIVE — **8-6**, REJECT-AS-ANCHOR ONLY** (8/8 added the cleanest sighting yet: PHI −156 / Nola 5.55 vs TOR / Scherzer 7.92 → PHI lost 5-7 in a 12-run game, and the OVER out of the same analysis cashed. See the NEW COROLLARY in the log — the mirror form of this trap cost us the 8/8 Tier-1 leg.) (8/3 tested it three times on one slate and went 2-1: both two-bad-SP shootouts, MIL and HOU, lost as favourites; the lone miss was PHI/Nola winning anyway. Still just above a coin flip — keep declining these as a clean parlay ANCHOR since the process risk is real, but do not treat a reject as a confident bet-against.) |
| D5 | **Bullpen-game opponent ≠ ML boost** — do NOT shade a fav UP because the other side has an opener/no real starter | The opposing pen can shut your offense down AND the lineup can tee off on your ace; a no-starter opponent is variance, not a free upgrade | **6/4/26** | **8/9/26** | **W (8/9, and it extends the rule to TOTALS: BOS ran a full bullpen game — Erik Miller opening, 0 GS in 35.0 IP — and the ATH@BOS Over 9.5 we published as the search's #2 ticket finished 4-3, SEVEN runs.** The build cited D5 correctly to refuse an ATH ML boost and then expressed the game as an Over anyway, on the reasoning that a bullpen game means more runs. **It does not.** A no-real-starter opponent is variance in BOTH directions, and tonight the pen suppressed. ⚠ **Rule extended on this sighting: 'a bullpen game is not a free ML upgrade' is now 'a bullpen game is not a free anything' — it is not a reason to take the Over either.** Tally 4-0)** · **W (8/7: DET −126 BLOCKED off SF's Brubaker bullpen game (0 GS in 54.0 IP) — **DET LOST 5-2**; the no-boost rule paid a third time, tally now 3-0)** · | **W (6/9: ATL −148 vs CWS's Eisert bullpen game; held ATL 60% NOT boosted — still LOST 5-6, killed the user's $30 parlay. The discipline was right but the leg was just thin/-EV-ish; 2nd validation of the spot)** · **W (6/4: bumped ATL 67→69% vs TOR's Fluharty pen game; lost 7-2)** **W (8/10, settled 8/11: HOU @ SF Under 8.5 −109 CLEARED the gate at +3.0pp and was rejected on D5 because SF ran a bullpen game — the game finished 9 runs and the Under LOST. Second time in five that a D5 reject saved a full leg rather than merely avoiding one.)** | **ACTIVE — **5-0**, CONFIRMED firm rule, and BROADENED 8/9 from ML-only to any market** (8/7 added a non-ATL sighting: DET fav vs SF's bullpen game, DET lost 5-2 — the rule now has a data point outside the original ATL pair, which is what it needed) |
| D6 | **NYM ML favored vs MIA, priced beyond team-quality** — REJECT-as-anchor (NEW 8/1/26) | Recurring series pattern: NYM (47-64, RDiff −52) keeps getting priced as home fav vs MIA (56-55, RDiff +7) regardless of which NYM starter (McLean, Peralta, now Thornton) — the number looks driven by home field/recency, not a real team-quality edge | **8/1/26** | **8/2/26** | **W (8/2: Stock REJECT correct — MIA 2-0 NYM, Alcantara shut them out; 5th sighting)** · **W (8/1: Thornton REJECT correct, MIA won 6-2 — the MIA ML +118 value side also cashed)** · W (7/31: Peralta REJECT correct, MIA won 5-2) · L (7/30: REJECT missed, NYM won 4-2) · W (7/26: McLean REJECT correct, MIA won 5-2) | **ACTIVE (promoted 8/3/26) — 5 sightings, 4-1 (80%).** Past the 2-3× process-lesson bar; NYM-favored-vs-MIA is now a confirmed matchup trap: never anchor it, and price the MIA side as the live value. 8/1 build correctly took the actual +EV side (MIA ML +118, custom+4pp, WON) rather than just rejecting NYM. |

## E. Data / status traps (verification gates — fade the BAD DATA, not a team)
Not team fades, but recurring data errors to actively guard against each run.

| ID | Trap | Reason | Added | Last val | Log | Status |
|----|------|--------|-------|----------|-----|--------|
| E1 | **Search "final" that re-stamps the prior day** (day-of-week mismatch / reused box score) | Engine conflates adjacent games in a series | 6/3/26 | 6/3/26 | Caught 6/3 SEA "8-3 Tuesday" re-stamp (twice) | **ACTIVE GATE** |
| E2 | **Stale SP stat aggregate** (frozen at a prior start) | Season ERA/WHIP can lag 2+ starts in a hot/cold swing | 5/29/26 | 5/29/26 | Caught 5/29 Imanaga 2.32→4.04 | **ACTIVE GATE** |
| E3 | **Carried-over / mis-attributed probables** | Rotations rotate; search surfaces yesterday's matchup; wrong team attribution | 5/26/26 | **8/4/26** | Caught 6/3 Peralta-to-Brewers mislabel; 5/27 Cole/Cameron. **8/4 16:00: `recheck.py` fired on WSH @ PHI — Zack Littell → Carson Palmquist.** No leg was built on that game so nothing was invalidated, but the replacement changes it completely (Palmquist 7.31/1.63 with his last six outings at 3.0/0.1/1.2/1.1/1.1/2.0 IP = an opener profile, i.e. a WSH bullpen game → D5, no PHI boost). The mechanical snapshot-diff caught it without any judgment call | **ACTIVE GATE** |
| E4 | **TBA starter** (build leans on an unannounced SP) | Fails SP-freshness gate → no bet | 5/x/26 | **8/4/26** | 6/3 MIL TBA → no bet (correct). **8/4: both gated games lifted at 16:00 and the gate paid off in an unexpected direction** — DET@SEA (Melton posted, 1.75/0.93) produced a genuine +3.0pp Under read, but LAA@BAL, which the 11:00 build had called "a screaming Over signal" pending the other arm, priced at **+0.8pp** once Povich (5.12/1.34 but 3 GS and last logged 5/07) and a 7 mph wind-IN were actually known. **Calibration note: a loud ERA on one side is not a total read** — the gate protected us from a leg the pre-gate narrative wanted | **ACTIVE GATE** |
| E5 | **Undetected opener / bullpen game** — `slate` names a "probable" who is not a starter | `mlb_api.sh slate` prints a probable pitcher with no indication of ROLE; an arm with 0-2 GS across 35-55 IP is an opener, and the whole leg (ML *or* total) is built on a starter who does not exist | **8/10/26** | **8/10/26** | **Promoted 8/10 on the 3rd sighting.** 8/9 ran **three** undetected bullpen games on one 15-game board — BOS (Erik Miller, 1.0 IP opener), WSH (Brad Lord, 2.2 IP, 1 GS in 59.0 IP) and **both** sides of CLE@CWS (1.0 IP each) — and the ATH@BOS Over 9.5 we published lost *because* of the shape (7 runs). Prior sightings: 8/7 (SF/Brubaker, 0 GS in 54.0 IP, caught by hand) and 8/4 (WSH/Palmquist, caught by `recheck.py`). ⚠ **The two caught sightings were caught by a human remembering to check; the three missed ones were missed on the same day the check was skipped.** | **ACTIVE GATE — mechanical check required: for EVERY SP in a scanned leg, read `GS` from `mlb_api.sh pitcher <id>`; GS ≤ 2 with IP ≥ 30 = opener/bullpen flag, and D5 then applies to EVERY market in that game, not just the ML · ✅ **W 8/11** — CLE @ DET. `wind_in_under+3` had qualified the Under 8.0 at **+3.0pp** and it was heading for the card. Drew Anderson's aggregate reads **3 GS / 67.1 IP**, which reads like a starter at a glance; `gamelog` shows his last twelve appearances are **1.0 · 2.0 · 1.0 · 1.0 · 1.1 · 1.1 · 1.0 · 1.0 · 1.2 · 1.1 · 1.1 · 3.2 IP** — all relief. Detroit is an opener/bullpen game and the leg was dropped. ⚠ **REFINEMENT — the written trigger (`GS ≤ 2 with IP ≥ 30`) would NOT have fired here: Anderson has 3 GS, one over the bar.** The ratio is what gives it away — **67.1 IP / 3 GS = 22 IP per "start", an impossible number for a real starter.** Trigger updated below. Tally **2-0** — ✅ **W 8/11 (settled 8/12): the leg it killed LOST.** CLE @ DET finished **4-6 = 10 runs** vs the Under 8.0 the gate removed at +3.0pp. Second live test, second save.

**Trigger (updated 8/11/26):** flag when `GS ≤ 3` **OR** `IP / GS ≥ 8` (i.e. the innings cannot have come from those starts). Either condition → read `gamelog` before using ANY market in that game. The IP/GS ratio catches the swingman with a handful of spot starts that the raw GS count lets through.** |

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
- **❌ 8/12/26 (settled same day) — `own_sp_hi` (mirrored) takes its FIRST LOSS, and the leg died on the
  tag's own axis rather than on any counter-signal.** BAL ML +101 was the day's Tier 1 at +5.0pp: the mirror
  fired because Minnesota's **Zebby Matthews (5.23 / 1.34, and 7.28 over his last six)** cleared the 5.00
  threshold, against Baltimore's **Shane Baz (3.76 / 1.32, 2.55 over his last six)**, in a game the market
  priced pick'em. **Minnesota won 7-5 — and the starting-pitcher gap inverted completely: Baz went 3.0 IP /
  9 H / 5 ER / 2 K, his worst start in six, while Matthews went 5.0 IP / 4 ER.** Baltimore's pen then held
  Minnesota to 2 ER over 4.2 IP, so the starter lost the game outright. `calib.py` §1c moves **2-0 → 2-1
  across three unique rows** (`pulse.py`'s wider window reads 2-2). **Three rows is a story, not evidence** —
  the +5pp registry magnitude is nowhere near the n≥20 bar and must not be treated as established.
  ⚠ **Explicitly NOT promoted to a fade, and the reason matters:** one losing leg on an n=3 tag is exactly
  the noise the tiered bar exists to ignore, and the recorded cause is a single bad start rather than a
  defect in the tag's logic.
- **⚠ 8/12/26 — the published counter-signal was RIGHT and was NOT the cause, and conflating the two would be
  the retrospective error the doctrine forbids.** Counter-signal #1 on the card read *"Baltimore's last 15 is
  7-8 with a −21 run differential; Minnesota's is 7-8 with −4. On recent form Minnesota is the marginally
  better team, and the model is buying the worse one."* Minnesota did win. But the leg lost on a three-inning,
  nine-hit start, not on team form, so **the counter-signal and the loss coincided without one causing the
  other** — and reading a team-form conclusion out of this result would be scoring a signal on an outcome it
  did not produce. ✅ **The doctrine that team-form transitions anchor on RUN DIFFERENTIAL over a window, not
  W-L streaks, held up under a direct challenge today:** Minnesota's L10 was 3-7 and their L15 run diff was
  −4, i.e. the streak said "cold" and the run differential said "fine" — the run differential was the useful
  number and it was the one on the card.
- **✅ 8/12/26 — thesis-conflict decline is 2-for-2 and is becoming a real gate (2 sightings).** BAL @ MIN
  Under 9.0 had qualified at **+3.0pp** on `wind_in_under+3` and was declined because it contradicted the same
  build's Tier 1 (backing Baltimore *because* Minnesota's starter is bad argues Over, not Under). **The game
  finished 12 runs — the Under would have lost by three.** Second consecutive day an internal-consistency
  check has removed a losing leg. ⚠ Not yet promoted to doctrine: the process bar is 2-3 sightings and this is
  the second, so one more clean sighting promotes it.
- **✅ 8/12/26 — E5 held again on a live board.** HOU @ SF was killed outright on the gate (Bryan King, **0 GS
  across 49.1 IP**) and the game was 0-1 into the 5th at settle time — the low-scoring shape the gate implies.
  Logged as directional; the full settle lands on tomorrow's 11:00 run.
- **⚠ 8/12/26 — `type:ML-dog` is one loss from re-cooling and that, not the anecdote, is the signal to carry.**
  It came off COOL this morning at **3-5 (38%) vs a 44% claim** — a narrow clearance the build flagged at the
  time — and after today's loss it reads **3-6 (33%) vs 44%, i.e. −11pp against a −15pp trigger.** The next
  losing dog leg re-arms the COOL.
- **⛔ 8/11/26 (settled 8/12) — THE CORROBORATION CITED FOR THE 8/7 PARK-TAG PROMOTION WAS A PARSER BUG.
  1 sighting; the promotion is NOT overturned, but the §1c citation is WITHDRAWN.** `calib.py`'s
  `parse_adj_tags` could not read a tag name wrapped in bold, and `results_log.md` bolds every tag
  (`[adj: **hitter_park_over+3 (full magnitude)**]`) — so every tagged row was silently filed under
  `(none — market-anchored)`. After the fix (asserted in `selftest.sh` 8/12): **`hitter_park_over` 15 rows
  9-6 skill +0.0005** (was "6-5, −0.0034"), **`pitcher_park_under` 14 rows 9-5 skill +0.0004** (was "3-4,
  −0.0092"), **`wind_out_over` 15 rows 9-6 skill +0.0032** (was n=1). Both park tags measure **at or slightly
  above zero**, not below it. **The 8/7 promotion was made on the process bar (3 sightings) and stands on that
  basis alone** — it is not being reversed on one day's finding, and the tiered bar forbids rewriting doctrine
  off a single re-read. But the sentence in the promotion entry that says "`calib.py` §1c corroborates" was
  reading a broken parser and is struck. **Carry to the n≥20 review: if the tags keep measuring ≥0, the
  tiebreaker-only restriction needs re-argument from the three sightings alone.** A second bug found the same
  day: an aggregate ledger row naming two lines minted a real leg's `leg_key` and swallowed a settled 16-run
  WIN out of the bands, §1b, §1c and the governor's window; `leg_key` now returns `aggregate` for multi-line
  cells. Both are the silent-measurement class and both now have selftest assertions.
- **🆕 8/11/26 (settled 8/12) — the park-tag strike COST two winning legs and SAVED the ticket. Both halves
  recorded; 1 sighting.** Build C struck TB@ATH O8.5 (**16 runs ✅**), TB@ATH O10.5 (**✅**) and MIL@SD U7.5
  (**❌**) — struck set **2-1 against the strike**. But Build B's actual recommendation was TB O8.5 × MIL U7.5,
  Milwaukee lost, and **the +182 ticket would have lost anyway**. Quoting only the leg-level half would say the
  doctrine cost us; quoting only the ticket-level half would say it saved us. Neither alone is true.
- **🆕 8/11/26 (settled 8/12) — the band-55-59 shade was a WASH across the full day, and the morning-only
  read was misleading.** Kill-list at 11:00/16:00 went **3-1 against** the shade (TB O9.5 ✅, TB O10.0 ✅,
  BOS@TOR O6.5 ✅, MIL U8.0 ❌) — identical to 8/10 and the tempting headline. The three rungs it killed at
  **18:00 went 0-3 for it** (PHI@STL O7.5 ❌ 2 runs, TEX@LAA O9.0 ❌ 5, CIN@CWS U8.5 ❌ 9). **Full-day net 3-4 —
  a coin flip.** This is the pre-registered-candidate-set rule doing real work: the narrative subset would have
  manufactured a two-slate losing streak the complete set does not support. Applied unchanged; far under n≥20.
- **✅ 8/11/26 (settled 8/12) — E5 is 2-0 and remains the cleanest gate on the board.** CLE@DET Under 8.0 had
  qualified at +3.0pp, was killed on the bullpen-game gate, and the game went **10 runs**. See the E5 row for
  the IP-per-GS refinement that caught it.
- **❌ 8/11/26 (settled 8/12) — two rejections missed winners, same shape both times.** HOU@SF Under 8.0 was
  rejected at 11:00 (E4/TBA) and again at 16:00 (Whisenhunt 7.25 ERA) — the game went **5 runs**, so it wins
  twice over. BOS@TOR Over 7.0 **qualified at 11:00 and was withdrawn at 16:00** when a fresh `wind_in_under`
  mirror cancelled its park tag — it went **8 runs**. `wind_in_under` as a *cancelling* device is now **1-1**
  (n=2, directional only). ⚠ **Watch item, 1 sighting: un-qualifying an already-qualified leg on a newly-posted
  tag is a different and less-tested operation than qualifying one.**
- **🆕 8/11/26 (settled 8/12) — `type:ML-fav` MARKET-SHADE, second control slate: favourites went 7-8 (47%)**
  against a market price of roughly 58-60% (W: DET, CHC, NYY, TOR, ATL, TB, LAD; L: PIT, MIN, CWS, PHI, TEX,
  AZ, MIL, HOU). With 8/10's 6-4 that is two slates at 13-12 combined. Not evidence; measured either way.
- **🆕 8/10/26 (settled 8/11) — the governor was a WASH on a slate where it was loud, and both halves are recorded.**
  The band-55-59 COOL+MARKET-SHADE **saved two bets** — KC@LAD Under 7.5 (game went **11**) and Jacob Lopez
  Under 4.5 K (**5 K**) — and **cost three**, because the four alternate-total rungs it zeroed would have gone
  **3-1** (ATH O9.5 ✅ 16 runs, TOR O8.0 ❌ 3, SD U7.5 ✅ 5, STL O8.5 ✅ 11). Net **+2 / −3**. Separately the
  `type:ML-fav` MARKET-SHADE's ten-favourite control group came in **6-4 (60%)**, i.e. **exactly what the market
  priced** — which is the cleanest statement yet that this shade is not a hit-rate claim at all and the whole
  disagreement is about CLV. 1 sighting each; **neither promoted**, and deliberately logged together so the
  flattering half is not the half that gets remembered (the 8/7 audit finding).
- **🆕 8/10/26 (settled 8/11) — `ticket.py`'s best-floor pick and its band pick were the SAME ticket for the
  second consecutive slate, and it cashed. 2 sightings — PROMOTED as a process lesson.** PHI@STL Over 9.0 ×
  TB@ATH Over 9.0 reached **+225** at a **32.9%** floor with **no floor paid to reach the payout band**. Both
  legs won. The rule this supports is already in doctrine (construction is a SEARCH, not an assembly); what is
  new is the specific shape — **when the qualifying pool is all alternate-total rungs off the same tag, the
  band is reachable without a chase leg**, because the ladder lets you buy payout by moving the number rather
  than by adding a game. Worth reaching for first the next time the pool is thin.
- **🆕 8/9/26 — the exposure governor's KILLS went 0-4 on a single 15-game board. 1 sighting, NOT promoted.**
  Every leg `pulse.py` halved or zeroed below the gate on 8/9 then won: **STL ML −157** (band 60-64 COOL
  cut +2.5→+1.25) won 7-4; **COL@STL Over 9.0** (rejected at exactly +2.0pp) hit 11 runs; **CHC@KC Over
  10.5** (rejected at +2.0pp, on the slate's highest number) hit 12; **LAA@MIA — MIA ML −138** (double-
  governed to 0.0pp) won 12-3. Meanwhile the two legs the governor DID allow split 1-1 (TOR@PHI Over 8.5 ✅,
  ATL@NYY Over 8.5 ❌) and the published +184 ticket lost. **This is the mirror image of the 8/6 entry above,
  where the governor's kills were the correct ones — which is exactly why neither is promoted on one slate.**
  Logged the same day it happened so it is graded on its own ledger rather than remembered when convenient.
- **🆕 8/9/26 — the governor's state depends on WHEN we settle, not only on what happened. 1 sighting.**
  At 18:20 the only pre-game leg on the board (SD ML −111) cleared at +2.5pp. Settling the day's eight
  decided legs — which is a *bookkeeping* action — moved `type:ML-fav` recent CLV from 6+/7− to 6+/8−,
  crossing the ≥2-net-negative trigger, and the mandated post-settle `pulse.py` re-run MARKET-SHADED the
  dimension and zeroed the leg. **Whether the leg was bettable depended on whether we had settled yet.**
  Not a bug and not an argument for settling late — the shade is presumably as correct at 18:28 as it
  would have been at 11:00 tomorrow — but the ordering sensitivity is real and worth a second sighting.
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

