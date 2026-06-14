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
| A1 | **Cubs** | **L15 ~6-9 (.400), −15 run diff (6/11); off today @ SF as a DOG (Assad vs Roupp).** | 5/25/26 | **6/12/26** | **L (6/11: beat COL 9-3 @ COL as −147 fav — fade MISSED, broke a hot streak)** · W (6/10: lost 2-3 @ COL as −147 fav) · W (6/9: lost 3-7 @ COL) · L (6/6: beat SF 3-2) · W (6/5) · L (6/4) | **ACTIVE** — fade-as-fav now 4-2 recent (one miss 6/11); L15 still sub-.450. Today CHC is the DOG @ SF (don't lay anyway). Re-verify run-diff before any future CHC-fav lean. |
| A3 | **Tigers** | L15 ~7-8 (6/10); cooled back | 5/28/26 | **6/11/26** | **L (6/11: DET −122 won 11-0 vs MIN as fav — fade MISSED)** · W (6/10: lost 4-6 vs MIN as fav) · L (6/9: beat MIN 10-4 as fav) · L (6/7: beat SEA 5-4) · W (6/6) · L (6/3 won as DOG) · W (5/29) · W (5/28) | **NEUTRAL→leaning RETIRE** — fade-as-fav now 3-4 recent (11-0 blowout 6/11); DET clearly not fade-worthy as a fav right now. Don't lay against either. Re-verify run-diff before any DET lean. |

> **Corollary (added 6/3/26):** "Fade as FAVORITE" ≠ "safe to bet AGAINST." A fade-list team can
> win outright as a live dog (Tigers swept TB 6/3; TB −1.5 vs DET-class burned 6/1). Never lay a
> run line against a fade-as-fav team — the fade is about not *trusting them when favored*, not
> about treating them as dead money.

## B. Team value — UNDERDOG "quietly hot"
Potential underdog value (good record-vs-form mismatch in our favor). Dogs = lower floor → usually
standalone, not parlay-floor legs.

| ID | Team | Reason | Added | Last val | Value log | Status |
|----|------|--------|-------|----------|-----------|--------|
| B1 | **White Sox** | 37-32; L10 5-5, +10 run diff (6/14) — cooling after the hot run | 5/28/26 | **6/13/26** | **L (6/13: lost 1-7 to LAD as home dog — dog value MISSED, LAD bounced back hard)** · W (6/12: beat LAD 8-2 as +178 home dog) · W (6/10: beat ATL 2-1 as home dog) · W (6/9: beat ATL 6-5 as home dog) · L (6/7) · W (6/6) · L (6/5) · W (6/4) | **ACTIVE (cooling)** — dog value still net-positive (5-2 recent) but L10 back to 5-5 and run diff regressed +31→+10; split the LAD series. Single L is noise, but watch the regression. |
| B2 | **Pirates** | **L15 ~.500; lost to LAD 6/11 as home dog (8-6) — re-heat stalled** | 5/26/26 | **6/12/26** | **L (6/11: lost 8-6 to LAD as +150 home dog — dog value MISSED)** · W (6/10: beat LAD 9-8 walk-off as +150 dog) · L (6/9: lost 3-12 to LAD) · L (6/6) · L (6/5) · W (6/4) | **WATCH (cooling)** — split the LAD series, 2-4 recent dog tests; re-heat didn't hold. Off today (MIA @ PIT, PIT is the −139 fav, not a dog spot). |
| B3 | **Twins** | Still cold — **L10 3-7, −24 run diff (6/4)**; offense quiet, pen ok | 5/28/26 | **6/4/26** | L (6/4: L10 3-7) · L (5/28 lost 6-2) | **NEUTRAL (soft-matchup only)** |
| B4 | **Tigers** | NEW 6/3: heating as a dog — swept TB, beat elite Martínez. Watch for dog-value flip | 6/3/26 | 6/3/26 | W (6/3 won 7-2 as +122 dog) | **WATCH (emerging dog value)** |
| B5 | Angels / Astros | Honorable mention — surging; Astros stay AUTO-FADE K-Over (back on ML/total only) | 5/28/26 | — | _seed_ | **WATCH** |

## C. K-Over fades (lineup / structural / situational)
The signals that suppress a K-Over AND make the K-Under the +EV side. **Critical refinement
(6/3/26): do NOT HARD-fade a genuinely elite-K ace's K-Over off a SINGLE suppressor** — log it as a
live standalone Over and price both lines; stack the fade only when MULTIPLE suppressors pile up.

| ID | Fade | Reason | Added | Last val | Fade log | Status |
|----|------|--------|-------|----------|----------|--------|
| C1 | **Contact lineups: Royals, Astros, Guardians, D-backs** (K-Over against) | Low-K lineups suppress even elite arms; can also beat aces on the scoreboard | 5/25/26 | 6/3/26 | **L (6/3 Burns 9 K vs KC)** · W (5/27 deGrom held to 6 K vs HOU) · W (5/25 Warren 3 K vs KC) | **ACTIVE but variance-heavy** — 2-1; one-suppressor elite arms now LOG the Over, don't hard-fade |
| C2 | **2nd-meeting within 14d** (downgrade K-Over one tier, two if prior went heavily over) | Hitters adjust 2nd look; K rate drops ~10-15% | 5/x/26 | 6/3/26 | **L (6/3 Sanchez 9 K vs SD, faded as HARD on lone 2nd-mtg)** | **DOWNGRADE-ONLY, not a reject** (per 6/3 refinement) |
| C3 | **Structural pitch-count uncertainty** (TJ-return, MLB debut, post-IL, opener-conversion, quick-hook mgr) | Left-tail on start length the K/9 can't see → take deeper alt / off parlay floor | 5/26/26 | — | W (5/26 Strider 5 K, 5.5 would've busted) | **ACTIVE** — START-LENGTH axis only; don't downgrade per-pitch stuff (Cole/Skenes refinement) |
| C4 | **Designated openers** (planned 1-2 IP) | Pitch-count ceiling kills the Over | 5/x/26 | — | _seed_ | **ACTIVE (auto-fade)** |
| C5 | **Tight-zone HP umpire** | Suppresses K-Overs | 5/x/26 | — | _seed_ | **ACTIVE (check each K-Over)** |
| C6 | **Over-fading elite-K aces** (META-fade: fade our own over-fade) | We faded Sanchez 9 K, Burns 9 K (6/3), Harrison 12 K (6/2) — all hit | 6/3/26 | **6/9/26** | **6/9 calibration (didn't bet, observed): Cease 11K ✅over, Skenes 7K ✅over6.5, Chase Burns 7K/5.1IP ✅over6.5 (my Tier-1 standalone rec), Wheeler 5K ❌under. 3 of 4 elite K-Overs CASHED.** · 3 straight fades MISSED 6/2-6/3 → correction installed | **ACTIVE CORRECTION — 3-of-4 on 6/9 reinforces: don't fade elite arms' K-Overs by reflex. NOT a blanket "always play" (Wheeler missed on start-length); price each pre-game + pick by edge** |

## D. Parlay-construction fades
Recipes to avoid when building.

| ID | Fade | Reason | Added | Last val | Log | Status |
|----|------|--------|-------|----------|-----|--------|
| D1 | **The +200-chase 3rd leg** (bolting a leg onto a clean 2-legger to stamp +200) | Drops floor ~15-18pp; the chase leg keeps busting | 5/30/26 | 6/3/26 | **W (6/3 TB chase leg busts, LAD+PHI cashes)** · W (6/2 declining the +270 saved us) · W (6/1 chase cost us) | **ACTIVE — 3-0, strongest fade on the board** |
| D2 | **Heavy-fav ML anchors (-350 or worse)** | ~Zero payout contribution, still ~20% bust | 5/27/26 | 5/27/26 | W (5/27 faded LAD -420, NYY sub cashed) | **ACTIVE** |
| D3 | **−1.5 RL on a heavy fav vs a live dog** | Carries full ML loss prob + win-by-2 risk; dog wins outright ~35-40% | 6/1/26 | 6/1/26 | W (6/1 TB −1.5 lost outright to DET) | **ACTIVE** |
| D4 | **Favorite ML w/ own SP ERA ~5.00+** (esp. two-bad-SP shootouts) | High-variance; favorite can be blown out as the "right" side | 5/28/26 | **6/7/26** | **L (6/7: PHI −161, Nola 5.55 own-SP trap → PHI WON 9-5 vs CWS; trap fav cashed this time)** · W (6/6: PHI −136, Painter 5.74 → lost 3-6) · W (6/5: AZ −134, Kelly 5.06 → 1-14) · W (5/28 DET/Flaherty 5.94 → 7-1) | **ACTIVE — 3-1, still strong** (high-variance gate; the variance cut our way 6/7 — one miss doesn't void it) |
| D5 | **Bullpen-game opponent ≠ ML boost** — do NOT shade a fav UP because the other side has an opener/no real starter | The opposing pen can shut your offense down AND the lineup can tee off on your ace; a no-starter opponent is variance, not a free upgrade | **6/4/26** | **6/9/26** | **W (6/9: ATL −148 vs CWS's Eisert bullpen game; held ATL 60% NOT boosted — still LOST 5-6, killed the user's $30 parlay. The discipline was right but the leg was just thin/-EV-ish; 2nd validation of the spot)** · **W (6/4: bumped ATL 67→69% vs TOR's Fluharty pen game; lost 7-2)** | **ACTIVE — 2-0, CONFIRMED firm rule** (both sightings = ATL fav vs a bullpen-game opponent, both LOST) |

## E. Data / status traps (verification gates — fade the BAD DATA, not a team)
Not team fades, but recurring data errors to actively guard against each run.

| ID | Trap | Reason | Added | Last val | Log | Status |
|----|------|--------|-------|----------|-----|--------|
| E1 | **Search "final" that re-stamps the prior day** (day-of-week mismatch / reused box score) | Engine conflates adjacent games in a series | 6/3/26 | 6/3/26 | Caught 6/3 SEA "8-3 Tuesday" re-stamp (twice) | **ACTIVE GATE** |
| E2 | **Stale SP stat aggregate** (frozen at a prior start) | Season ERA/WHIP can lag 2+ starts in a hot/cold swing | 5/29/26 | 5/29/26 | Caught 5/29 Imanaga 2.32→4.04 | **ACTIVE GATE** |
| E3 | **Carried-over / mis-attributed probables** | Rotations rotate; search surfaces yesterday's matchup; wrong team attribution | 5/26/26 | 6/3/26 | Caught 6/3 Peralta-to-Brewers mislabel; 5/27 Cole/Cameron | **ACTIVE GATE** |
| E4 | **TBA starter** (build leans on an unannounced SP) | Fails SP-freshness gate → no bet | 5/x/26 | 6/3/26 | 6/3 MIL TBA → no bet (correct) | **ACTIVE GATE** |

---

## Retired (kept for history)
- **A2 — Rangers (fade-as-favorite)** — RETIRED **6/4/26**. The "was-hot-now-cold / just-bad" premise no
  longer holds: **L15 8-7, L10 6-4, W5 active streak, +11 run diff.** L15 .533 is a hair under the strict
  .550 retire bar, but the fade was already NEUTRAL, had **missed its last test** (5/29 — TEX blew out KC
  9-1), and the club is clearly trending up — no longer a team to fade when favored. Re-add only if they
  relapse to a sub-.450 last-15. (Validated via `mlb_api.sh standings`/`teamform`.)

---

### Running scoreboard (fades that have been tested)
- **D1 (+200-chase):** 3-0 ✅ — most reliable fade.
- **D2/D3 (construction):** 1-0 each ✅.
- **D4 (own-SP ERA ~5+ fav):** **3-1** — 6/6 PHI/Painter 5.74 lost 3-6, 6/5 AZ/Kelly 5.06 blown out 1-14, 5/28 DET/Flaherty; **first miss 6/7 PHI −161/Nola 5.55 WON 9-5** (the variance cut toward the trap fav — expected occasionally in a high-variance gate). Still a strong reject signal.
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
