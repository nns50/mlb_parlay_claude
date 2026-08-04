# First-Inning Run Tracker — NRFI / YRFI (Over/Under 0.5 runs in the 1st)

**The market.** A bet on whether **any run scores in the first inning** of a game.
- **NRFI** = **N**o **R**un **F**irst **I**nning = **Under 0.5** total 1st-inning runs (neither team scores in the 1st).
- **YRFI** = **Y**es **R**un **F**irst **I**nning = **Over 0.5** (at least one run scores in the 1st).

Separate, standalone tracker — **not** part of the daily 3-tier parlay build and **not** in `results_log.md`.
Its own ledger lives here; the dashboard renders it from this file.

---

## Doctrine (how to read a 1st-inning O/U)
- **It's a battle of two half-innings.** A run only needs to score in EITHER team's top-of-order to bust
  NRFI. So NRFI needs BOTH starters to put up a clean 1st AND both 1-2-3 hitters to go quiet. That's why
  the **YRFI bias is real** and books shade NRFI to ~−130/−140 (public also loves "a run will score").
- **Drivers, in order:**
  1. **Both SPs' 1st-inning run rate / quality** — aces and ground-ball/sinker arms (weak early contact)
     are the NRFI backbone; homer-prone or slow-starting arms are YRFI flags.
  2. **Both top-of-order trios (slots 1-2-3)** — OBP + power. Loaded tops (LAD, ATL, NYY) push YRFI even
     vs a good arm; cold/weak tops (current MIN, etc.) support NRFI.
  3. **Park / weather** — hitter parks + wind-out lean YRFI (Coors = auto-YERFI tilt); pitcher parks NRFI.
- **NEVER estimate the price** (same gate as every leg) — pull the live 1st-inning total
  (`totals_1st_1_innings`) at a book and devig before betting. The reads below are **model leans only**
  until a real number is pulled.
- **Edge gate + staking** same as the rest of the routine: devig the real line, require ≥ +2pp, size by
  ¼-Kelly. **TrueP pre-registered** (write it before first pitch — no back-fill).
- **Correlation:** NRFI stacks cleanly with a **game Under / F5 Under** (positive) and is roughly
  independent of either ML. Don't pair NRFI with a YRFI-leaning total.

---

## Tonight's reads — 2026-08-04 (15-game slate; **4 reads clear +2pp on a real 1st-inning line**)

> 11:00 ET morning reads — full 15-game slate, all first pitches 18:35 ET or later, every game
> `Preview/Scheduled`. One model-lean per game with a pre-registered TrueP. Weather PENDING for all games
> at build time (Wrigley and Coors are the two that matter). **Two games carry a TBD starter** (BAL home,
> DET away) → E4 gate, leans held deliberately mild. **Unlike recent slates, four reads were priced against
> a live `totals_1st_1_innings` market and cleared the +2pp gate** — flagged ✅ below.

| # | Matchup | Starters (ERA/WHIP) | Lean | TrueP | Line pulled | Edge | Why (1st-inning read) |
|---|---------|---------------------|------|-------|-------------|------|------------------------|
| 1 | LAA @ BAL | G. Rodriguez 7.98/1.75 / **TBD** | **YRFI** | 56% | _model-only_ | — | ⚠ E4 — BAL's starter is TBA, so half the read is unknown. G-Rod's line is the worst on the board (7.98 ERA, 1.75 WHIP) and he has not gone past 5 innings; a 1.75 WHIP means baserunners in the 1st. Lean held mild for the E4. |
| 2 | ATH @ CIN | Ginn 3.46/1.22 / Singer 4.68/1.43 | **YRFI** | 56% | _model-only_ | — | GABP is a hitter park and Singer carries a 1.43 WHIP. Cuts the other way: ATH's road offense is the worst on the slate (.244/.325, L10 2-8, RDiff −154), so the top half of the 1st is quiet. Net mild YRFI on the park + Singer traffic. |
| 3 | NYM @ CLE | Manaea 4.42/1.34 / Cantillo 3.88/1.45 | **YRFI** | 55% | _model-only_ | — | Both WHIPs ≥1.34 — this is a traffic game, and Cantillo's 1.45 is the higher. Offsetting: NYM's top is .231/.301 vs RHP, among the weakest tops in the league, and Progressive Field plays neutral-to-pitcher. Mild. |
| 4 | WSH @ PHI | Littell 4.94/1.34 / Luzardo 3.57/1.19 | **YRFI** | 57% | _model-only_ | — | Asymmetric: Luzardo (3.57/1.19, 10.98 K/9) is the stabilising side, but Littell at 4.94/1.34 faces PHI's top in a hitter park (CBP). The YRFI equity is almost entirely the bottom of the 1st. |
| 5 | STL @ NYY | Dobbins 3.74/1.34 / Weathers 3.99/1.24 | **YRFI** | 57% | _model-only_ | — | Yankee Stadium plus NYY's top of order against a 4-start rookie (Dobbins, 33.2 IP, 1.34 WHIP). STL's own top is contact-heavy (18% K vs LHP) so it puts balls in play against Weathers too. |
| 6 | CWS @ BOS | Martin 3.62/1.26 / Sandoval 3.32/1.58 | **YRFI** ✅ | **56%** | **Over 0.5 +102 (FanDuel)** · no-vig **48.6%** | **+7.4pp** | **Priced read, gate cleared.** Sandoval is 4 starts / 19 IP into a return and carries a **1.58 WHIP** — the highest on the board — at Fenway, against a BOS-hot slate context (L10 8-2, W5). Shaded down from a 60% first pass because CWS's top strikes out 24% vs LHP; the market's 48.6% is the reason for the shade, not a reason to abandon the read. |
| 7 | MIA @ ATL | Gusto 5.31/1.44 / Holmes 3.88/1.36 | **YRFI** | 59% | _model-only_ | — | Gusto's 5.31/1.44 against the hottest top-of-order on the slate (ATL 67-45, W5, L10 7-3, +108 run diff) at Truist. The strongest un-priced YRFI on the board. |
| 8 | MIN @ KC | J. Ryan 3.52/1.11 / Dobnak 1.04/1.19 | **NRFI** ✅ | **55%** | **Under 0.5 −104 (FanDuel)** · no-vig **48.8%** | **+6.2pp** | **Priced read, gate cleared, and the market is on the other side.** Two of the lowest WHIPs on the board (1.11, 1.19) and two weak tops (KC .313 OBP, MIN .319) in a big park (Kauffman). Shaded 57% → 55% precisely *because* the market prices this YRFI-side (48.8% NRFI) — Dobnak is a 3-start, 26-IP sample and a 4.85 K/9, so the market may be reading a short/opener-ish outing we can't see. Best available price is a near-pick-em at −104. |
| 9 | PIT @ MIL | Jones 3.81/**1.02** / Henderson 2.66/**0.91** | **NRFI** ✅ | **58%** | **Under 0.5 −129 (BetRivers)** · no-vig **54.7%** | **+3.3pp** | **The cleanest NRFI premise of the day.** The two best WHIPs on the entire slate face each other (1.02 and 0.91) in a dome, and PIT's top is the weaker of the two (.263/.345 vs RHP but 23% K). The market agrees — hence the smallest edge of the four; we are getting paid a little, not a lot, for the correct side. |
| 10 | LAD @ CHC | Skubal 2.79/**0.91** / Assad 3.75/1.16 | **NRFI** | 55% | _model-only_ | — | Skubal's 0.91 WHIP is elite and Assad is competent, but **both tops are strong** (CHC .333 OBP vs RHP, .355 vs LHP; LAD's is the best in baseball) and Wrigley wind is **PENDING** — the one park where a wind reading would move this materially. Held at a mild NRFI. |
| 11 | SF @ TEX | Tidwell 3.00/1.08 (**0 GS**) / Gore 4.77/1.26 | **YRFI** | 55% | _model-only_ | — | ⚠ **C4-adjacent:** Tidwell has **0 starts** in 12 IP — role is a swingman/opener question mark, which adds variance to the top of the 1st rather than resolving it. Gore's 4.77 ERA is the firmer YRFI signal. Dome, so no weather risk. |
| 12 | TOR @ HOU | Yesavage 3.73/1.16 / Wesneski 4.76/**1.59** | **YRFI** | 58% | _model-only_ | — | Wesneski has **5.2 IP all season across 1 start** — a rust/short-leash profile with a 1.59 WHIP, effectively a bullpen game for HOU. Yesavage on the other side is the steadier arm, so like WSH@PHI the equity is one-sided. |
| 13 | TB @ COL | Peralta 4.99/**1.48** / Hughes 3.33/1.19 | **YRFI** ✅ | **61%** | **Over 0.5 −130 (FanDuel)** · no-vig **54.9%** | **+6.1pp** | **Day's strongest read, and it is at Coors.** Peralta's 1.48 WHIP and 4.5 IP/start meet a TB top that is the most contact-heavy on the slate (18-19% K, .264 avg vs RHP) at altitude. **Directly informed by yesterday:** this exact park produced 22 runs on a 13 mph wind-IN reading, so the wind-suppression story is not being applied here. Coors weather still PENDING. |
| 14 | SD @ AZ | Vásquez 4.45/**1.47** / E. Rodriguez 2.48/1.21 | **YRFI** | 55% | _model-only_ | — | Vásquez's 1.47 WHIP against AZ's top is the YRFI half; E-Rod (2.48 ERA, the best mark on the board) is a genuine NRFI arm on the other side, which caps the lean. Dome. |
| 15 | DET @ SEA | **TBD** / Hancock 3.26/1.04 | **NRFI** | 55% | _model-only_ | — | ⚠ E4 — DET's starter is TBA. Hancock (3.26/1.04) in T-Mobile Park is close to an archetypal NRFI side, but with half the matchup unknown the lean stays mild. |

**Day's strongest NRFI:** PIT @ MIL (58%, +3.3pp on a real line — two sub-1.05 WHIPs in a dome)
**Day's strongest YRFI:** TB @ COL (61%, +6.1pp on a real line — Coors + Peralta's 1.48 WHIP)
**Slate split:** 4 NRFI / 11 YRFI leans. **4 priced reads clear +2pp** (PIT@MIL NRFI, MIN@KC NRFI, TB@COL YRFI, CWS@BOS YRFI); the other 11 stay model-only/no-bet.

---

## Tonight's reads — 2026-08-03 (model leans, un-priced; pull `totals_1st_1_innings` at the book)

> 11:00 ET morning reads — 8-game slate, all first pitches 18:40 ET or later. One model-lean per game,
> model-only/no-bet (pull the real 1st-inning total at the book; promote only a read clearing +2pp after
> devig). Weather PENDING for all games at build time. Two games carry a TBD starter (LAD away, TEX home)
> → E4 gate, leans held deliberately mild.

| # | Matchup | Starters | Lean | TrueP | Why (1st-inning read) |
|---|---------|----------|------|-------|------------------------|
| 1 | WSH @ PHI | Alvarez / Nola | **YRFI** | ~56% | Nola's line has collapsed (5.61 ERA / 1.45 WHIP) and he averages just 5.2 IP; Alvarez carries a 1.51 WHIP and has gone past 5 IP once in 6 starts. Traffic on both sides early, in a hitter park. |
| 2 | STL @ NYY | McGreevy / Schlittler | **NRFI** | ~55% | Schlittler is the best arm on the board (2.04 ERA / 0.91 WHIP) and should retire a 21%-K STL top cleanly; McGreevy is contact-prone (5.90 K/9) but his damage usually comes later, not in the 1st. |
| 3 | PIT @ MIL | Chandler / Sproat | **YRFI** | ~57% | Both arms are walk-prone and short (Chandler 4.56 / 1.41 WHIP, Sproat 5.05 / 1.39); MIL's top is .260/.341 vs RHP and PIT's is .263/.345. Two shaky arms vs two live tops. |
| 4 | LAD @ CHC | TBD / Boyd | **YRFI** | ~55% | ⚠ E4 — LAD's starter is TBA, so half the read is unknown. Boyd (3.41 ERA) is the stabilizing side, but LAD's 1-2-3 (.267/.346 vs RHP, the best top on the slate) is the reason the lean stays YRFI at Wrigley. |
| 5 | SF @ TEX | Webb / TBD | **NRFI** | ~54% | ⚠ E4 — TEX starter TBA. Webb is the archetypal NRFI arm (3.93 ERA, 1.12 WHIP, heavy ground-ball profile) and SF's top is a weak .255/.313 vs RHP inside a dome. Mild lean. |
| 6 | TOR @ HOU | Bieber / Javier | **YRFI** | ~60% | **Day's strongest YRFI.** Bieber's command is gone (last start 0.2 IP / 4 ER / **6 BB**; 5.74 ERA / 1.63 WHIP) and Javier is 4 starts into a ramp-up at 7.17 ERA / 1.83 WHIP. Both sides are live in the 1st. |
| 7 | TB @ COL | Seymour / Lorenzen | **YRFI** | ~60% | Coors + Lorenzen at 6.54 ERA / 1.81 WHIP (last two: 3.2 IP/6 ER, 4.0 IP/3 ER); TB's top is .262/.335 vs RHP. Seymour's 10.34 K/9 is the only NRFI argument and he's averaged 4.4 IP over his last five. |
| 8 | SD @ AZ | King / Pfaadt | **NRFI** | ~55% | **Day's strongest NRFI.** King is steady (3.38 ERA, 1.17 WHIP, 6.0 IP in four of five) and Pfaadt has been sharp lately (7.0 IP / 0 ER last out, 4.00 ERA). Two competent arms in a dome. |

**Day's strongest NRFI:** SD @ AZ (two competent arms in a dome, ~55%); STL @ NYY (Schlittler elite, ~55%)
**Day's strongest YRFI:** TOR @ HOU (Bieber's command gone + Javier ramp-up, ~60%); TB @ COL (Coors + Lorenzen, ~60%)

> **16:00 ET re-verify (Build B).** `nrfi_settle.py 2026-08-03 --apply` → all 8 games still pre-game,
> nothing to settle. Lineups now posted for **PHI (home), STL + NYY (both), LAD (away), TEX (home)**;
> PIT/MIL, TOR/HOU, TB/COL, SD/AZ still PENDING. **No lean flipped:** NYY's posted top
> (Grisham / Rice / Vientos) keeps the STL@NYY NRFI premise intact, LAD's confirmed 1-2-3
> (Ohtani / Pages / Edman) keeps the Wrigley YRFI, and PHI's posted top keeps the WSH@PHI YRFI.
> LAD's starter is **still TBA** at 16:12, so game 4 stays E4-flagged and its lean stays mild.
> **No read clears +2pp on a real `totals_1st_1_innings` line, so all 8 remain model-only / no-bet.**
> Coors weather still PENDING (populates near the 20:40 ET first pitch) — the TB@COL YRFI lean is
> held at ~60% but is the one read a wind-in reading would move.

> **18:45 ET update (Build C-2).** Coors weather populated: **89°F, wind 13 mph, In From CF.** The
> TB @ COL **YRFI ~60%** lean rested on the same Coors-plus-Lorenzen premise as the (now dropped)
> Over 11.5 leg, and wind-in is exactly the switch that moves Coors toward its low-scoring mode —
> supporting context: COL home games since 6/1 (n=28) are **bimodal**, 9 of them at ≤8 total runs.
> **Lean downgraded 60% → ~54% (NEUTRAL).** Still model-only/no-bet; no read on the slate clears
> +2pp on a real `totals_1st_1_innings` line. All other leans unchanged.

---

## Tonight's reads — 2026-06-22 (model leans, un-priced; pull `totals_1st_1_innings` at the book)

> 11:00 ET morning reads — 13-game slate. One model-lean per game, all model-only/no-bet (pull the real 1st-inning total at the book; promote only a read clearing +2pp after devig). All PENDING lineup confirmation.

| # | Matchup | Starters | Lean | TrueP | Why (1st-inning read) |
|---|---------|----------|------|-------|------------------------|
| 1 | KC @ TB | Wacha / Rasmussen | **NRFI** | ~57% | Rasmussen dominates 1st inning with elite stuff (2.59 ERA, 9.45 K9); KC mediocre top-of-order. Strong NRFI lean. |
| 2 | NYY @ DET | Cole / Valdez | **NRFI** | ~53% | Both SPs tend to work efficiently early. Cole's early-inning efficiency historically solid; DET top quiet. |
| 3 | CHC @ NYM | Imanaga / Senga | **NRFI** | ~55% | Imanaga and Senga (when healthy) both tend to be clean first-inning arms. |
| 4 | BOS @ COL | Bennett / Feltner | **YRFI** | ~63% | **Coors Field + both leaky arms (Bennett 4.79, Feltner 5.05) = auto-YRFI tilt. Strongest lean of the day.** |
| 5 | LAD @ MIN | Lauer / Matthews | **YRFI** | ~58% | Lauer 5.37 ERA shaky early; LAD elite top (Ohtani/Betts/Freeman) likely to score in 1st. |
| 6 | ATL @ SD | Holmes / King | **YRFI** | ~55% | Holmes only 2.0 IP last start (volatile early); ATL top-of-order explosive. |
| 7 | CLE @ CWS | Williams / Kay | **NRFI** | ~53% | Williams K-heavy (10.11 K9); typically efficient early even when rough later. |
| 8 | PHI @ WSH | TBD / Griffin | **YRFI** | ~55% | PHI TBD SP risk; PHI's lineup vs any weaker arm YRFI-lean. |
| 9 | MIL @ CIN | TBD / Singer | NEUTRAL | ~50% | MIL TBD SP = opener/high variance 1st inning. |
| 10 | BAL @ LAA | Bradish / Aldegheri | NEUTRAL | ~52% | Bradish decent early; LAA bottom-tier offense. |
| 11 | HOU @ TOR | Brown / TBD | **YRFI** | ~55% | TOR TBD SP = elevated 1st-inning variance; HOU scores in bunches. |
| 12 | TEX @ MIA | Rocker / Phillips | NEUTRAL | ~52% | Phillips's 1st-inning vulnerability (ERA 3.10 season but 8 ER last start); Rocker unverified. |
| 13 | AZ @ STL | Kelly / Pallante | NEUTRAL | ~51% | Kelly ERA 5.81 is the risk; Pallante unverified. |

**Day's strongest NRFI:** KC @ TB (Rasmussen first-inning dominance)
**Day's strongest YRFI:** BOS @ COL (Coors + two leaky arms)

> Pull the real 1st-inning total + devig at first pitch; promote any read clearing +2pp into the ledger
> below with a pre-registered TrueP and the book price. Re-check lineups (a rested leadoff bat flips a read).

---

## Ledger (every NRFI/YRFI bet OR tracked read, append-only)

| Date | Matchup | Pick | TrueP | Price | Result | Reasoning (why this pick) |
|------|---------|------|-------|-------|--------|----------------------------|
| 6/17 | NYM @ CIN (McLean/Lodolo) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | GABP hitter park + two live tops; 1st-inning risk despite McLean K-stuff. |
| 6/17 | KC @ WSH (Avila/Littell) | YRFI | 56% | _model-only_ | **W** (1st 1-0 → YRFI) | Two-bad-SP shootout (6.19 / 5.32) — strongest YRFI lean. |
| 6/17 | MIA @ PHI (Alcantara/Painter) | NRFI | 54% | _model-only_ | **L** (1st 2-2 → YRFI) | Alcantara clean 1sts; rookie Painter the lone risk. |
| 6/17 | DET @ HOU (Mize/Lambert) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Two league-avg arms, contact-ish tops; mild NRFI. |
| 6/17 | SD @ STL (Rodriguez/Leahy) | YRFI | 53% | _model-only_ | **W** (1st 1-0 → YRFI) | Rookie B.Rodriguez 1st-inning variance + hittable Leahy. |
| 6/17 | TB @ LAD (McClanahan/Ohtani) | NRFI | 56% | _model-only_ | **W** (1st 0-0 → NRFI) | Ohtani 1.06 mows the 1st; two strong arms — cleanest NRFI. |
| 6/17 | LAA @ AZ (Aldegheri/E.Rodriguez) | NRFI | 54% | _model-only_ | **L** (1st 1-0 → YRFI) | E-Rod 2.55 clean early + quiet LAA top; rookie Aldegheri the risk. |
| 6/17 | TOR @ BOS (Scherzer/Bennett) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Scherzer mows early; rookie Bennett vs TOR top the YRFI risk. |
| 6/17 | CWS @ NYY (Kay/Rodón) | NRFI | 54% | _model-only_ | **L** (1st 0-2 → YRFI) | Rodón 9.87 K9 clean vs weak CWS top; NYY top vs Kay the live half. |
| 6/17 | SF @ ATL G2 (TBD/Ritchie) | YRFI | 53% | _model-only (SP TBD — provisional)_ | **W** (1st 1-0 → YRFI) | Rookie Ritchie 1st-inning risk; SF away SP unannounced. |
| 6/17 | CLE @ MIL (Williams/Sproat) | NRFI | 53% | _model-only_ | **L** (1st 0-3 → YRFI) | G.Williams K-stuff early; rookie Sproat the risk. |
| 6/17 | COL @ CHC (Sullivan/Assad) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | Wrigley + rookie Sullivan 1st-inning variance vs live CHC top. |
| 6/17 | PIT @ ATH (Ashcraft/Civale) | NRFI | 53% | _model-only_ | **L** (1st 3-0 → YRFI) | Two contact-ish arms, league-avg tops; mild NRFI. |
| 6/17 | BAL @ SEA (Bradish/Kirby) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Kirby clean early at home; BAL top vs Bradish the only risk. |
| 6/18 | TOR @ BOS (Yesavage/Gray) | YRFI | 53% | _model-only_ | **W** (1st 1-0 → YRFI) | Gray clean early but rookie Yesavage vs a live BOS top is the 1st-inning risk. |
| 6/18 | CLE @ MIL (Messick/Drohan) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | Two rookie SPs + MIL strong top; both tops can jump early. Strongest YRFI. |
| 6/18 | MIN @ TEX (Ryan/Leiter) | NRFI | 53% | _model-only_ | **L** (1st 4-0 → YRFI) | Joe Ryan (10.06 K9) mows the 1st; Leiter vs a cold MIN top the lone risk. |
| 6/18 | BAL @ SEA (Baz/Woo) | YRFI | 54% | _model-only_ | **W** (1st 0-3 → YRFI) | Woo gave up early runs lately (7 ER vs BAL 6/11); BAL top live 2nd look. |
| 6/18 | NYM @ PHI (Manaea/Nola) | YRFI | 56% | _model-only_ | **W** (1st 2-1 → YRFI) | Nola shaky early + CBP hitter park + live PHI top. Strongest YRFI on the board. |
| 6/18 | CWS @ NYY (Burke/Weathers) | YRFI | 53% | _model-only_ | **L** (1st 0-0 → NRFI) | NYY elite top vs Burke can cash early; Weathers avg, CWS top slumping. |
| 6/18 | SF @ ATL (Roupp/Pérez) | NRFI | 54% | _model-only_ | **VOID** (SF@ATL postponed 6/18) | Pérez (2.90) clean 1sts; SF road top weak; ATL top vs Roupp lone risk. |
| 6/19 | TOR @ CHC (Gausman/Brown) | NRFI | 53% | _model-only_ | **L** (1st 0-7 → YRFI) | Two competent arms; both tops league-avg early. Mild NRFI. |
| 6/19 | CWS @ DET (Fedde/Skubal) | NRFI | 55% | _model-only_ | **L** (1st 1-2 → YRFI) | Skubal (2.81 ace) mows the 1st; CWS top slumping. |
| 6/19 | CIN @ NYY (Lowder/Schlittler) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | NYY elite top vs rookie-ish Schlittler can cash early. |
| 6/19 | WSH @ TB (Cavalli/Jax) | YRFI | 53% | _model-only_ | **L** (1st 0-0 → NRFI) | Two uncertain arms; both tops can jump. |
| 6/19 | SF @ MIA (Roupp/Bachar) | YRFI | 53% | _model-only_ | **W** (1st 0-1 → YRFI) | Two back-end arms; slight early-run lean. |
| 6/19 | MIL @ ATL (Misiorowski/Pérez) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | ATL elite top vs a wild rookie flamethrower is the live half. |
| 6/19 | SD @ TEX (Vásquez/deGrom) | NRFI | 55% | _model-only_ | **L** (1st 5-6 → YRFI) | deGrom (10.45 K9) mows the 1st; SD top vs Vásquez lone risk. Strongest NRFI. |
| 6/19 | CLE @ HOU (Bibee/Imai) | YRFI | 53% | _model-only_ | **W** (1st 0-1 → YRFI) | Imai (NPB import, 1st-inning uncertain) vs a live CLE top. |
| 6/19 | STL @ KC (McGreevy/Lugo) | NRFI | 53% | _model-only_ | **L** (1st 1-0 → YRFI) | Lugo contact arm + McGreevy; both tops quiet early. |
| 6/19 | PIT @ COL (Chandler/Freeland) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | Coors + Freeland + rookie Chandler — strongest YRFI. |
| 6/19 | LAA @ ATH (Soriano/Springs) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Springs clean early; both tops quiet. |
| 6/19 | MIN @ AZ (Prielipp/Soroka) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Soroka (3.11) clean 1sts; MIN top vs rookie Prielipp lone risk. |
| 6/19 | BAL @ LAD (Gibson/Sasaki) | YRFI | 56% | _model-only_ | **W** (1st 0-2 → YRFI) | LAD elite top vs rookie Gibson; Sasaki volatile early. Strong YRFI. |
| 6/19 | BOS @ SEA (Suárez/Miller) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Two quality arms, both clean 1sts; quiet early. |
| 6/18 | STL @ KC (Liberatore/Cameron) | NRFI | 52% | _model-only_ | **L** (1st 2-1 → YRFI) | Two lefties, both tops league-avg; quiet early frames. |
| 6/18 | LAA @ ATH (TBD/Jump) | NRFI | 53% | _model-only_ | **L** (1st 0-5 → YRFI) | Provisional (LAA SP TBD, E4); Jump clean early vs a quiet LAA top. |
| 6/10 | ATL @ CWS (Sale/Martin) | NRFI | 60% | _model-only (no bet)_ | **W** | **Pitching:** Sale ace (2.23 ERA / 10.65 K9) routinely retires a contact-average CWS top 1-2-3 in order. **Bats:** CWS top is league-avg (23% K vs LHP), no early-power threat. **YRFI risk:** ATL's strong top (Harris/Albies/Olson) vs back-end Davis Martin — the one half that can break NRFI. **Net:** lean NRFI ~60%, but Martin is the swing factor (not a lock). **Result:** 1st inning 0-0 → NRFI occurred, **lean correct (W).** |
| 6/10 | MIN @ DET (Paredes/Valdez) | NRFI | 61% | _model-only (no bet)_ | **W** | **Pitching:** Valdez is an elite sinker/ground-ball arm — weak early contact, low 1st-inning run rate; the cleanest NRFI starter on the board. **Bats:** MIN's offense is cold (L10 3-7), unlikely to manufacture vs a GB arm. **YRFI risk:** Paredes (weak) means DET's top could score, but they'd have to string it together in the 1st. **Net:** cleanest NRFI of the three ~61%. **Result:** 1st inning 0-0 → NRFI occurred, **lean correct (W)** — note DET still won the game 11-... blowout, but the 1st was clean. |
| 6/10 | LAD @ PIT (Ohtani/Jones) | YRFI | 56% | _model-only (no bet)_ | **L** | **Thesis (YRFI):** LAD's top is the board's most dangerous (Ohtani leadoff, Betts, Freeman) vs hittable Jared Jones — a real 1st-inning run threat, and it only takes that one half-inning. Ohtani shuts PIT's weak top down, so the over rode entirely on the LAD side. **Result:** 1st inning 0-0 (LAD 0, PIT 0) — NRFI occurred, **lean MISSED.** Both starters threw clean 1sts; LAD's elite top didn't cash early. Calibration: the pitching-first bias beat the bats-first read. |
| 6/11 | LAD @ PIT (Wrobleski/Keller) | YRFI | 57% | _model-only (no bet)_ | **L** (1st 0-0 → NRFI) | LAD's elite top (Ohtani/Betts/Freeman) vs hittable Keller (4.81); wind 11 out to LF @ PNC. Wrobleski quiets PIT's weak top → over rides the LAD side. Slight YRFI. **⚠ Note the 6/10 LAD@PIT YRFI MISSED (1st 0-0) — same LAD-top thesis; downgraded confidence accordingly.** |
| 6/11 | ATL @ CWS (Pérez/Kay) | YRFI | 56% | _model-only (no bet)_ | TBD | Two soft-contact/back-end arms; ATL top + hot CWS home offense (L15 10-5/+27) both live in the 1st. Mild YRFI. |
| 6/11 | SEA @ BAL (Woo/Bradish) | NRFI | 55% | _model-only (no bet)_ | **L** (1st 1-0 → YRFI) | Cleanest NRFI of the three — Woo + Bradish both work fast early, neither top is loaded. Mild NRFI. |
| 6/12 | MIA @ PIT (Alcantara/Ashcraft) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Alcantara GB/sinker arm; both tops league-avg. |
| 6/12 | SEA @ WSH (Miller/Littell) | NRFI | 58% | _model-only_ | **W** (1st 0-0 → NRFI) | Cleanest read — Miller dominant early + Littell low-BB; no loaded top. |
| 6/12 | SD @ BAL (Canning/Baz) | NRFI | 55% | _model-only_ | **L** (1st 1-3 → YRFI) | Baz K-stuff; SD top slumping (L10 3-7). |
| 6/12 | DET @ CLE (Flaherty/Bibee) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Two mid-rotation arms, league-avg tops. |
| 6/12 | TEX @ BOS (Leiter/Gray) | NRFI | 55% | _model-only_ | **L** (1st 1-2 → YRFI) | Gray works clean 1sts; TEX top average. |
| 6/12 | AZ @ CIN (Rodriguez/Lodolo) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | GABP hitter park, two contact LHP. |
| 6/12 | ATL @ NYM (Strider/McLean) | YRFI | 54% | _model-only_ | **W** (1st 0-2 → YRFI) | ATL elite top vs McLean is the live half. |
| 6/12 | NYY @ TOR (Weathers/TBD) | YRFI | 55% | _model-only (TBD SP)_ | **W** (1st 0-3 → YRFI) | NYY top vs TBD/opener; soft, TBD arm. |
| 6/12 | LAD @ CWS (Sasaki/Kay) | YRFI | 57% | _model-only_ | **W** (1st 0-1 → YRFI) | LAD elite top vs Kay; CWS hot top vs walk-prone Sasaki. |
| 6/12 | PHI @ MIL (Painter/Misiorowski) | YRFI | 54% | _model-only_ | **W** (1st 0-1 → YRFI) | Miso wild; PHI top strong. |
| 6/12 | HOU @ KC (Imai/Avila) | NRFI | 53% | _model-only_ | **L** (1st 9-5 → YRFI) | Two rookies but KC low-power; hair NRFI. |
| 6/12 | STL @ MIN (Leahy/Ryan) | NRFI | 57% | _model-only_ | **L** (1st 1-1 → YRFI) | Joe Ryan quiets STL early; Leahy vs weak MIN top. |
| 6/12 | TB @ LAA (McClanahan/Aldegheri) | NRFI | 55% | _model-only_ | **L** (1st 0-2 → YRFI) | McClanahan shuts a weak LAA top early. |
| 6/12 | COL @ ATH (TBD/Jump) | YRFI | 53% | _model-only (TBD SP)_ | **L** (1st 0-0 → NRFI) | ATH bats vs uncertain COL arm; soft. |
| 6/12 | CHC @ SF (Assad/Roupp) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Pitcher-friendly Oracle, two mid arms. |
| 6/13 | STL @ MIN (Liberatore/Prielipp) | NRFI | 54% | _model-only_ | **L** (1st 2-0 → YRFI) | Two contact arms; weak MIN top. |
| 6/13 | NYY @ TOR (Schlittler/Gausman) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | NYY loaded top is the live half. |
| 6/13 | SD @ BAL (Vásquez/Gibson) | NRFI | 53% | _model-only_ | **L** (1st 4-2 → YRFI) | SD top slumping; rookie Gibson. |
| 6/13 | SEA @ WSH (Castillo/Cavalli) | NRFI | 54% | _model-only_ | **L** (1st 0-3 → YRFI) | Castillo clean 1sts; tops not loaded. |
| 6/13 | MIA @ PIT (Bachar/Chandler) | YRFI | 53% | _model-only_ | **W** (1st 0-1 → YRFI) | Uncertain arms + MIA hot bats. |
| 6/13 | AZ @ CIN (Soroka/Lowder) | NRFI | 54% | _model-only_ | **L** (1st 1-0 → YRFI) | Soroka clean early; CIN cold (GABP caveat). |
| 6/13 | DET @ CLE (Skubal/Cantillo) | NRFI | 56% | _model-only_ | **L** (1st 1-0 → YRFI) | Skubal K-stuff + weak CLE top. |
| 6/13 | TEX @ BOS (deGrom/Suarez) | NRFI | 57% | _model-only_ | **W** (1st 0-0 → NRFI) | deGrom mows tops early; cleanest read. |
| 6/13 | ATL @ NYM (Pérez/TBD) | YRFI | 55% | _model-only (TBD SP)_ | **L** (1st 0-0 → NRFI) | ATL elite top vs a TBD/opener. |
| 6/13 | LAD @ CWS (Yamamoto/Burke) | YRFI | 54% | _model-only_ | **W** (1st 3-0 → YRFI) | LAD elite top vs Burke is the live half. |
| 6/13 | HOU @ KC (Burrows/Cameron) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Two soft arms, both tops low-power. |
| 6/13 | PHI @ MIL (Nola/Drohan) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | PHI top strong; Nola 5.55 shaky early. |
| 6/13 | COL @ ATH (Freeland/Estes) | YRFI | 56% | _model-only_ | **W** (1st 0-2 → YRFI) | Two poor/unproven arms (Estes unverified). |
| 6/13 | CHC @ SF (Brown/McDonald) | NRFI | 54% | _model-only_ | **L** (1st 1-0 → YRFI) | Oracle pitcher park, two mid arms. |
| 6/13 | TB @ LAA (Jax/Soriano) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Soriano clean + Jax K-stuff vs weak LAA top. |
| 6/14 | MIA @ PIT (Meyer/Skenes) | NRFI | 57% | _model-only_ | **W** (1st 0-0 → NRFI) | Two elite-early arms; cleanest NRFI of the board. |
| 6/14 | SD @ BAL (Buehler/Rogers) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Buehler vet + Rogers LHP; SD top average. |
| 6/14 | SEA @ WSH (Hancock/Mikolas) | NRFI | 53% | _model-only_ | **L** (1st 1-1 → YRFI) | Mikolas control arm clean early. |
| 6/14 | NYY @ TOR (Warren/Corbin) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | NYY loaded top vs shaky Corbin = the live half. |
| 6/14 | AZ @ CIN (Gallen/Abbott) | YRFI | 53% | _model-only_ | **W** (1st 0-1 → YRFI) | GABP hitter park; two beatable arms. |
| 6/14 | DET @ CLE (Mize/G.Williams) | NRFI | 53% | _model-only_ | TBD | Williams K-stuff + league-avg tops. |
| 6/14 | ATL @ NYM (Elder/Peralta) | YRFI | 54% | _model-only_ | **W** (1st 1-4 → YRFI) | ATL elite top vs GB-arm Elder is the live half. |
| 6/14 | HOU @ KC (Arrighetti/Kolek) | NRFI | 53% | _model-only_ | **L** (1st 0-1 → YRFI) | Two mid arms, both tops low-power. |
| 6/14 | STL @ MIN (McGreevy/Bradley) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | McGreevy GB + weak MIN top. |
| 6/14 | LAD @ CWS (Sheehan/Fedde) | YRFI | 56% | _model-only_ | **W** (1st 1-0 → YRFI) | LAD elite top + hot CWS top — both halves live. |
| 6/14 | PHI @ MIL (Sánchez/Harrison) | YRFI | 53% | _model-only_ | **W** (1st 0-1 → YRFI) | PHI top vs LHP Harrison. |
| 6/14 | COL @ ATH (Sugano/Springs) | YRFI | 54% | _model-only_ | **W** (1st 2-4 → YRFI) | Two shaky arms; both tops can cash. |
| 6/14 | CHC @ SF (Rolison/Webb) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Webb GB-ace + Oracle park; Rolison opener. |
| 6/14 | TB @ LAA (Legumina/G.Rodriguez) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | G-Rod decent early; neither top loaded. |
| 6/14 | TEX @ BOS (Eovaldi/Early) | NRFI | 54% | _model-only_ | **L** (1st 1-0 → YRFI) | Eovaldi vet clean vs rookie Early. |
| 6/15 | MIA @ PHI (Gusto/Wheeler) | NRFI | 58% | _model-only_ | **W** (1st 0-0 → NRFI) | Wheeler mows tops early; cleanest NRFI of the board. |
| 6/15 | KC @ WSH (Spence/Alvarez) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Two contact arms, KC top low-power. |
| 6/15 | NYM @ CIN (Myers/Burns) | YRFI | 54% | _model-only_ | **W** (1st 0-3 → YRFI) | GABP + rookie Burns variance vs live NYM top. |
| 6/15 | SD @ STL (TBD/May) | NRFI | 53% | _model-only (TBD SP)_ | **W** (1st 0-0 → NRFI) | May clean early; SD top slumping. Provisional. |
| 6/15 | COL @ CHC (Lorenzen/Imanaga) | NRFI | 55% | _model-only_ | **L** (1st 0-1 → YRFI) | Imanaga clean 1sts + weak COL road top. |
| 6/15 | MIN @ TEX (TBD/Gore) | YRFI | 53% | _model-only (TBD SP)_ | **W** (1st 3-0 → YRFI) | Gore K-stuff but TEX top can cash. Provisional. |
| 6/15 | DET @ HOU (Melton/Teng) | YRFI | 54% | _model-only_ | **W** (1st 1-0 → YRFI) | Two uncertain arms, both tops league-avg. |
| 6/15 | LAA @ ARI (Ureña/Nelson) | YRFI | 54% | _model-only_ | **W** (1st 1-1 → YRFI) | Rookie Ureña 1st-inning risk vs ARI top. |
| 6/15 | PIT @ ATH (Jones/Ginn) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Jared Jones K-stuff + ATH top low-power. |
| 6/15 | TB @ LAD (Martinez/Lauer) | YRFI | 56% | _model-only_ | **W** (1st 2-0 → YRFI) | LAD elite top vs shaky Lauer (5.47) is the live half. |
| 6/16 | MIA @ PHI (Phillips/Luzardo) | YRFI | 54% | _model-only_ | **W** (1st 0-3 → YRFI) | PHI top (Schwarber/Harper) can score early on Phillips; wind 7mph Out To RF at CBP. |
| 6/16 | KC @ WSH (Wacha/Griffin) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Wacha contact arm + weak KC top; mild NRFI. |
| 6/16 | TOR @ BOS (Cease/Tolle) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Cease (13.63 K9) mows the 1st clean; rookie Tolle the only YRFI risk. |
| 6/16 | CWS @ NYY (Martin/Cole) | NRFI | 53% | _model-only_ | **L** (1st 1-0 → YRFI) | Cole clean 1sts + CWS avg top; NYY top vs Martin the swing. |
| 6/16 | NYM @ CIN (Senga/Singer) | YRFI | 57% | _model-only_ | **W** (1st 0-4 → YRFI) | Senga post-IL shaky (9.00 ERA) + GABP hitter park; the live half. |
| 6/16 | SF @ ATL (Houser/Holmes) | YRFI | 53% | _model-only_ | **W** (1st 1-2 → YRFI) | ATL top can cash early vs Houser; SF top weak. Mild YRFI. |
| 6/16 | CLE @ MIL (Cecconi/Gasser) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | Gasser shaky (6.38 ERA) early; CLE top can jump. |
| 6/16 | SD @ STL (King/Pallante) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | King clean early; SD top slumping. |
| 6/16 | COL @ CHC (Feltner/Cabrera) | YRFI | 57% | _model-only_ | **W** (1st 0-1 → YRFI) | Wrigley wind 17mph OUT + two hittable arms — strongest YRFI lean. |
| 6/16 | MIN @ TEX (Matthews/Rocker) | NRFI | 53% | _model-only_ | **L** (1st 2-0 → YRFI) | Rocker K-stuff, dome, cold MIN top; mild NRFI. |
| 6/16 | DET @ HOU (Valdez?/Brown) | NRFI | 53% | _model-only (SP attribution uncertain — E3)_ | **W** (1st 0-0 → NRFI) | Brown clean early; SP label disputed → provisional. |
| 6/16 | LAA @ AZ (Detmers/Kelly) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Kelly clean 1sts; LAA top quiet. |
| 6/16 | PIT @ ATH (Keller/Perkins) | NRFI | 54% | _model-only_ | **L** (1st 0-4 → YRFI) | Keller clean early + ATH low-power top. |
| 6/16 | BAL @ SEA (Young/Gilbert) | NRFI | 56% | _model-only_ | **L** (1st 1-0 → YRFI) | Gilbert ace mows the 1st; BAL top vs Young the only risk. |
| 6/16 | TB @ LAD (Rasmussen/Wrobleski) | YRFI | 56% | _model-only_ | **L** (1st 0-0 → NRFI) | LAD elite top vs back-end Wrobleski is the live half. |
| 6/19 | TOR @ CHC (Gausman/Brown) | NRFI | 53% | _model-only_ | **L** (1st 0-7 → YRFI) | CHC erupted for 7 in the 1st off Gausman — blowout YRFI; NRFI read badly missed. |
| 6/19 | CWS @ DET (Fedde/Skubal) | NRFI | 55% | _model-only_ | **L** (1st 1-2 → YRFI) | Skubal conceded an early run to CWS top despite ace edge. |
| 6/19 | CIN @ NYY (Lowder/Schlittler) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | NYY top went quiet in the 1st vs Schlittler — both arms clean. |
| 6/19 | WSH @ TB (Cavalli/Jax) | YRFI | 53% | _model-only_ | **L** (1st 0-0 → NRFI) | Two uncertain arms both produced clean 1sts. |
| 6/19 | SF @ MIA (Roupp/Bachar) | YRFI | 53% | _model-only_ | **W** (1st 0-1 → YRFI) | MIA scored in the 1st; mild YRFI lean validated. |
| 6/19 | MIL @ ATL (Misiorowski/Pérez) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | Pérez (2.90) clean — even Misiorowski's first inning was quiet. |
| 6/19 | SD @ TEX (Vásquez/deGrom) | NRFI | 55% | _model-only_ | **L** (1st 5-6 → YRFI) | Both sides scored heavily in the 1st (deGrom gave up 5); strongest NRFI lean missed badly. |
| 6/19 | CLE @ HOU (Bibee/Imai) | YRFI | 53% | _model-only_ | **W** (1st 0-1 → YRFI) | Imai gave up an early run as expected vs live CLE top. |
| 6/19 | STL @ KC (McGreevy/Lugo) | NRFI | 53% | _model-only_ | **L** (1st 1-0 → YRFI) | STL scored in the 1st vs Lugo; contact-arm lean missed. |
| 6/19 | PIT @ COL (Chandler/Freeland) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | Coors + Freeland + rookie Chandler still produced a clean 1st. Strongest YRFI missed. |
| 6/19 | LAA @ ATH (Soriano/Springs) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Springs clean; quiet 1st as expected. |
| 6/19 | MIN @ AZ (Prielipp/Soroka) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Soroka clean 1st; MIN top quiet vs rookie. |
| 6/19 | BAL @ LAD (Gibson/Sasaki) | YRFI | 56% | _model-only_ | **W** (1st 0-2 → YRFI) | LAD top cashed early vs rookie Gibson as expected. |
| 6/19 | BOS @ SEA (Suárez/Miller) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Both quality arms produced clean 1sts; lean validated. |
| 6/20 | CWS @ DET (Fedde/Melton) | NRFI | 53% | _model-only_ | **L** (1st 1-0 → YRFI) | Melton young but works clean; CWS top volatile. |
| 6/20 | CIN @ NYY (Abbott/Warren) | YRFI | 54% | _model-only_ | **W** (1st 0-1 → YRFI) | NYY elite top vs Abbott; Warren gives up early contact. |
| 6/20 | TOR @ CHC (Corbin/Rea) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Rea decent early; Corbin veteran. Neutral. |
| 6/20 | SD @ TEX (Buehler/Eovaldi) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Both capable early-frame control arms; no loaded tops. |
| 6/20 | WSH @ TB (Cavalli/Seymour) | YRFI | 53% | _model-only_ | **W** (1st 0-1 → YRFI) | Seymour uncertain; WSH top live. |
| 6/20 | SF @ MIA (McDonald/Meyer) | NRFI | 55% | _model-only_ | **L** (1st 0-1 → YRFI) | Meyer (2.75 ERA) mows early — best NRFI arm on core. |
| 6/20 | MIL @ ATL (Harrison/Sale) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Sale elite early; Harrison also clean. Both aces. |
| 6/20 | CLE @ HOU (Cantillo/Arrighetti) | NRFI | 53% | _model-only_ | **L** (1st 1-0 → YRFI) | Arrighetti decent; dome suppression. |
| 6/20 | NYM @ PHI (Peralta/Sánchez) | NRFI | 55% | _model-only_ | **L** (1st 0-1 → YRFI) | Sánchez (1.82 ERA) dominant early; strong NRFI. |
| 6/20 | PIT @ COL (Skenes/Sugano) | YRFI | 60% | _model-only_ | **W** (1st 1-1 → YRFI) | Coors + Sugano 4.54 ERA = strongest YRFI on board. |
| 6/20 | LAA @ ATH (Ureña/Ginn) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | Ginn unverified; Ureña back-end. Both tops live. |
| 6/20 | MIN @ AZ (Bradley/Gallen) | YRFI | 55% | _model-only_ | **W** (1st 2-0 → YRFI) | Gallen struggling (5.35 ERA); MIN top can score early. |
| 6/20 | BAL @ LAD (Rogers/Yamamoto) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Yamamoto (2.52 ERA) elite early; LAD top vs Rogers only risk. |
| 6/20 | BOS @ SEA (Early/Hancock) | YRFI | 53% | _model-only_ | **W** (1st 0-1 → YRFI) | Both young arms; slight early-run lean. |
| 6/22 | KC @ TB (Wacha/Rasmussen) | NRFI | ~57% | _model-only_ | **W** (1st 0-0 → NRFI) | Rasmussen dominates 1st inning (2.59 ERA, 9.45 K9); KC mediocre top-of-order. Strong NRFI lean. |
| 6/22 | NYY @ DET (Cole/Valdez) | NRFI | ~53% | _model-only_ | **W** (1st 0-0 → NRFI) | Both SPs efficient early. Cole clean 1sts; DET top quiet. |
| 6/22 | CHC @ NYM (Imanaga/Senga) | NRFI | ~55% | _model-only_ | TBD | Both arms tend to be clean first-inning starters. |
| 6/22 | BOS @ COL (Bennett/Feltner) | YRFI | ~63% | _model-only_ | **L** (1st 0-0 → NRFI) | **Coors Field + Bennett 4.79 + Feltner 5.05 = strongest YRFI lean of the day.** |
| 6/22 | LAD @ MIN (Lauer/Matthews) | YRFI | ~58% | _model-only_ | **W** (1st 1-1 → YRFI) | Lauer 5.37 ERA shaky early; LAD elite top (Ohtani/Betts/Freeman) likely to score in 1st. |
| 6/22 | ATL @ SD (Holmes/King) | YRFI | ~55% | _model-only_ | **L** (1st 0-0 → NRFI) | Holmes only 2.0 IP last start (volatile early); ATL top explosive. |
| 6/22 | CLE @ CWS (Williams/Kay) | NRFI | ~53% | _model-only_ | **W** (1st 0-0 → NRFI) | Williams K-heavy (10.11 K9); typically efficient early. |
| 6/22 | PHI @ WSH (TBD/Griffin) | YRFI | ~55% | _model-only_ | **W** (1st 0-1 → YRFI) | PHI TBD SP risk; PHI lineup vs any weaker arm YRFI-lean. |
| 6/22 | MIL @ CIN (TBD/Singer) | NEUTRAL | ~50% | _model-only_ | TBD | MIL TBD SP = opener/high variance 1st inning. |
| 6/22 | BAL @ LAA (Bradish/Aldegheri) | NEUTRAL | ~52% | _model-only_ | TBD | Bradish decent early; LAA bottom-tier offense. |
| 6/22 | HOU @ TOR (Brown/TBD) | YRFI | ~55% | _model-only_ | **W** (1st 1-0 → YRFI) | TOR TBD SP = elevated 1st-inning variance; HOU scores in bunches. |
| 6/22 | TEX @ MIA (Rocker/Phillips) | NEUTRAL | ~52% | _model-only_ | TBD | Phillips's 1st-inning vulnerability; Rocker unverified. |
| 6/22 | AZ @ STL (Kelly/Pallante) | NEUTRAL | ~51% | _model-only_ | TBD | Kelly ERA 5.81 is the risk; Pallante unverified. |
| 6/21 | LAA @ ATH (Detmers/Perkins) | NRFI | 53% | _model-only_ | **L** (1st 0-4 → YRFI) | Detmers decent LHP; ATH back-end Perkins uncertain but both tops quiet. |
| 6/21 | BAL @ LAD (Young/Sheehan) | YRFI | 57% | _model-only_ | **W** (1st 2-1 → YRFI) | LAD elite top (Ohtani/Betts/Freeman) vs rookie Young — live half. Strongest YRFI lean. |
| 6/21 | BOS @ SEA (Tolle/Gilbert) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Gilbert ace dominant early frames; BOS avg top vs Gilbert. |
| 6/21 | NYM @ PHI (Peterson/Wheeler) | YRFI | 53% | _model-only_ | **W** (1st 0-2 → YRFI) | PHI top strong vs shaky Peterson; CBP hitter park. |
| 6/24 | LAD @ MIN (Ohtani/Ryan) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Ohtani (1.47 ERA) surgical early; Ryan (2.99/10.20 K9) also efficient. Both elite; clean 1st innings as expected. |
| 6/24 | ATH @ SF (Jump/Mahle) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | Mahle (6.04 ERA, 1-7) was expected to be vulnerable early but worked a clean 1st; ATH top didn't cash. |
| 6/24 | ATL @ SD (Pérez/Sears) | NEUTRAL | 52% | _model-only_ | (1st 0-0 → NRFI, excluded — neutral) | Pérez (2.78 ERA) clean early; Sears 0 GS in 2026 (IL return) = coin-flip. Petco/wind-in tempers YRFI. |
| 6/24 | AZ @ STL (Bratt/Liberatore) | YRFI | 56% | _model-only_ | **L** (1st 0-0 → NRFI) | Liberatore struggled badly last start but worked a clean 1st this time; AZ top didn't cash early either. |
| 7/25 | KC @ DET (Wacha/Mize) | NEUTRAL | 52% | _model-only_ | (1st 0-0 → NRFI, excluded — neutral) | Both quality journeyman arms; Comerica suppresses offense slightly. |
| 7/25 | AZ @ WSH (Bratt/Griffin) | YRFI | 56% | _model-only_ | **L** (1st 0-0 → NRFI) | Both moderate arms produced a clean 1st; AZ's active offense didn't cash early. |
| 7/25 | LAA @ SF (Johnson/Ray) | YRFI | 60% | _model-only_ | **L** (1st 0-0 → NRFI) | Oracle wind-out lean missed — both starters worked a clean opening frame. |
| 7/25 | TOR @ BOS (Cease/Gray) | NRFI | 57% | _model-only_ | **W** (1st 0-0 → NRFI) | Cease (13.37 K/9) mowed the order; Gray also clean. Elite-arm NRFI thesis held. |
| 7/25 | SD @ MIA (Vásquez/Pérez) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Dome + Pérez dominant early + cold MIA offense — clean NRFI as leaned. |
| 7/25 | NYY @ PHI (Weathers/TBD) | YRFI | 60% | _model-only_ | **W** (1st 0-1 → YRFI) | PHI TBD-SP variance thesis hit — PHI scored in the 1st. |
| 7/25 | CLE @ TB (Bibee/Martinez) | NRFI | 56% | _model-only_ | **W** (1st 0-0 → NRFI) | Martinez's elite contact management + cold CLE offense held the 1st clean. |
| 7/25 | CHC @ PIT (Imanaga/Skenes) | NRFI | 62% | _model-only_ | **W** (1st 0-0 → NRFI) | Strongest NRFI lean of the day — both elite arms delivered clean 1sts as expected. |
| 7/25 | ATL @ BAL (Elder/Young) | YRFI | 58% | _model-only_ | **L** (1st 0-0 → NRFI) | ATL's explosive top stayed quiet in the 1st; Young worked clean. |
| 7/25 | ATH @ MIN (Basso/TBD) | YRFI | 58% | _model-only_ | **L** (1st 0-0 → NRFI) | TBD-SP variance thesis missed — 1st stayed clean on both sides. |
| 7/25 | HOU @ CWS (Brown/Burke) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | Brown's rough recent form didn't translate to a 1st-inning run; HOU's big lineup went quiet early too. |
| 7/25 | COL @ MIL (Feltner/Gasser) | NEUTRAL | 52% | _model-only_ | (1st 0-0 → NRFI, excluded — neutral) | Dome-controlled; near-neutral read as leaned. |
| 7/25 | LAD @ NYM (Yamamoto/McLean) | NRFI | 60% | _model-only_ | **W** (1st 0-0 → NRFI) | Both hot elite arms delivered clean 1sts as leaned. |
| 7/25 | CIN @ STL (Greene/Pallante) | NRFI | 58% | _model-only_ | **L** (1st 0-1 → YRFI) | Greene's K-heavy profile didn't prevent an early run against him. |
| 7/25 | SEA @ TEX (Woo/Eovaldi) | NEUTRAL | 51% | _model-only_ | (1st 0-3 → YRFI, excluded — neutral) | Coin-flip read; TEX offense broke through early (3 runs), well outside the neutral lean either way. |
| 7/26 | CLE @ TB (Messick/Rasmussen) | NRFI | 58% | _model-only_ | **W** (1st 0-0 → NRFI) | Both elite arms (Messick 2.68 ERA, Rasmussen 3.28 ERA); Tropicana dome controlled. |
| 7/26 | AZ @ WSH (Drake/Mikolas) | YRFI | 57% | _model-only_ | **W** (1st 1-0 → YRFI) | Mikolas struggling (5.61 ERA); wind out to LF at Nats Park. |
| 7/26 | CHC @ PIT (Taillon/Ashcraft) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | Wind out to RF at PNC; Ashcraft's command unproven at this level. |
| 7/26 | TOR @ BOS (Gausman/Suarez) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Suarez's first start back from IL (groin) — likely on a pitch-count leash; wind in from RF at Fenway suppresses. |
| 7/26 | ATL @ BAL (López/Baz) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | López inconsistent vs ATL's dynamic top-of-order. |
| 7/26 | KC @ DET (Avila/Valdez) | YRFI | 57% | _model-only_ | **W** (1st 2-0 → YRFI) | Both shaky arms (Avila 4.86, Valdez 4.57 post-bereavement disaster start). |
| 7/26 | LAD @ NYM (Sheehan/Peralta) | YRFI | 60% | _model-only_ | **W** (1st 0-1 → YRFI) | Two-bad-SP shootout — both own-SP-ERA traps (5.13/5.01), recent multi-run 1st/2nd-inning blowups. |
| 7/26 | SD @ MIA (Buehler/Junk) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | Buehler's control has deteriorated (5 BB last start) — walks invite early trouble. |
| 7/26 | ATH @ MIN (Springs/Prielipp) | YRFI | 54% | _model-only_ | **W** (1st 0-3 → YRFI) | Wind out to LF + 92°F heat at Target Field boosts offense mildly. |
| 7/26 | HOU @ CWS (Blanco/Fedde) | NRFI | 53% | _model-only_ | **L** (1st 1-2 → YRFI) | Wind in from RF at Rate Field suppresses; near coin-flip on SP quality. |
| 7/26 | COL @ MIL (Freeland/Misiorowski) | NRFI | 58% | _model-only_ | **L** (1st 0-3 → YRFI) | Misiorowski elite (1.57 ERA, 13.54 K/9) even on a workload-managed pitch count; dome neutralizes Coors tilt. |
| 7/26 | CIN @ STL (Abbott/Leahy) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | Wind out to CF + 94°F heat at Busch; both mid-tier arms without a clean-1st track record. |
| 7/26 | SEA @ TEX (Gilbert/deGrom) | NRFI | 60% | _model-only_ | **L** (1st 0-1 → YRFI) | Both elite K-arms (9.68/10.94 K9) in a neutral dome; typically retire the order cleanly early. |
| 7/26 | LAA @ SF (Soriano/Whisenhunt) | NEUTRAL | 52% | _model-only_ | TBD | Weather pending at build time; no strong SP signal identified. |
| 7/26 | NYY @ PHI (Warren/Sánchez) | YRFI | 55% | _model-only_ | **W** (1st 0-1 → YRFI) | Sánchez should retire NYY clean, but Warren shaky/short-outing prone — PHI's own bats live vs him. |
| 7/30 | TEX @ TB (Winn/McClanahan) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | Winn on an alarming short-leash pattern (0.1-1.1 IP last 6 outings) — command/health risk. Dome neutral. |
| 7/30 | KC @ MIN (Cameron/Ober) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | Both mediocre arms; wind out to LF at Target Field boosts carry mildly. |
| 7/30 | NYY @ CWS (Weathers/Burke) | NRFI | 58% | _model-only_ | **W** (1st 0-0 → NRFI) | Burke dominant recent form (10 K last start); wind in from CF suppresses. |
| 7/30 | CHC @ STL (Assad/Pallante) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Pallante shutout last start; Assad on a short leash but avoiding damage. |
| 7/30 | PIT @ CIN (Ramírez/Lowder) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | Both shaky/short-leash (Ramírez essentially an opener; Lowder 5.61 ERA). |
| 7/30 | MIA @ NYM (Pérez/McLean) | NRFI | 58% | _model-only_ | **W** (1st 0-0 → NRFI) | McLean elite and metronomic (exactly 6.0 IP 6 straight starts); Pérez also sharp recently. |
| 7/30 | WSH @ ATL (Irvin/Holmes) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | Irvin hasn't pitched since 5/23 (IL return, C3 rust risk); Holmes moderate. |
| 7/30 | BOS @ ATH (Gray/Barnett) | NRFI | 58% | _model-only_ | **W** (1st 0-0 → NRFI) | Gray is a legitimate ace; ATH's punchless lineup limits early damage. |
| 7/30 | SF @ SD (TBA/Sears) | NRFI | 54% | _model-only_ | **L** (1st 1-0 → YRFI) | SF SP TBA (E4 gate, no bet); Sears reliable, Petco a pitcher's park. |
| 7/30 | SEA @ LAD (Woo/Sasaki) | NRFI | 57% | _model-only_ | **L** (1st 0-2 → YRFI) | Sasaki's best form of the season his last two starts (5K/0ER, 9K/1ER). |
| 7/31 | NYY @ CHC (Warren/Imanaga) | YRFI | 56% | _model-only_ | **L** (1st 0-0 → NRFI) | Warren shaky last 2 outings; Imanaga clean recent form. |
| 7/31 | PIT @ CIN (Skenes/Greene) | NRFI | 58% | _model-only_ | **L** (1st 2-2 → YRFI) | Skenes elite/consistent; Greene wildly volatile in a 4-GS sample. |
| 7/31 | PHI @ BAL (TBA/Young) | NEUTRAL | 52% | _model-only_ | TBD | PHI SP still TBA (E4 gate) — no SP-quality read. |
| 7/31 | STL @ TOR (Leahy/Cease) | NRFI | 60% | _model-only_ | **W** (1st 0-0 → NRFI) | Cease dominant (CG shutout last start) — should retire STL's top clean. |
| 7/31 | AZ @ CLE (Bratt/Bibee) | YRFI | 56% | _model-only_ | **W** (1st 0-1 → YRFI) | Bratt small-sample rookie (4 GS), never past 5.0 IP. |
| 7/31 | CWS @ TB (Fedde/Martinez) | YRFI | 55% | _model-only_ | **W** (1st 1-0 → YRFI) | Fedde swingman on short outings; Martinez's side is fine. |
| 7/31 | MIA @ NYM (Junk/Peralta) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | Peralta's recent starts have leaked early runs despite high K/9. |
| 7/31 | WSH @ ATL (Griffin/Elder) | NRFI | 54% | _model-only_ | **L** (1st 0-1 → YRFI) | Both solid arms, no strong signal either way. |
| 7/31 | TEX @ HOU (Eovaldi/Brown) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Both good arms, dome-neutral park. |
| 7/31 | KC @ COL (Wacha/Sugano) | YRFI | 58% | _model-only_ | **W** (1st 0-1 → YRFI) | Sugano 3.5-wk rust gap + Coors amplifies early damage. |
| 7/31 | MIL @ LAA (Drohan/R. Johnson) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | R. Johnson's last start was a disaster (3.1 IP/8 ER). |
| 7/31 | DET @ ATH (UNCONFIRMED/Springs) | YRFI | 55% | _model-only_ | **W** (1st 0-1 → YRFI) | Springs' last start a disaster (1.1 IP/4 ER/0K); DET SP unconfirmed. |
| 7/31 | SF @ SD (Whisenhunt/Rodriguez) | YRFI | 54% | _model-only_ | **W** (1st 0-2 → YRFI) | Rodriguez effectively an opener; Whisenhunt unstable; Petco tempers it. |
| 7/31 | BOS @ LAD (Suarez/Henriquez) | YRFI | 58% | _model-only_ | **L** (1st 0-0 → NRFI) | Henriquez a full-time reliever run as LAD's "starter" — bullpen game. |
| 7/31 | MIN @ SEA (Matthews/Miller) | YRFI | 57% | _model-only_ | **W** (1st 0-2 → YRFI) | Miller's last start alarming (0 K in 5.1 IP); Matthews also inconsistent. |
| 8/1 | STL @ TOR (Mathews/Gausman) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | Mathews likely MLB debut (zero 2026 data) — 1st-inning jitters risk. |
| 8/1 | MIN @ SEA (Prielipp/Gilbert) | NRFI | 57% | _model-only_ | **L** (1st 0-2 → YRFI) | Gilbert ace-quality (3.44 ERA/0.99 WHIP) should retire MIN's top clean. |
| 8/1 | CWS @ TB (Hicks/Rasmussen) | YRFI | 58% | _model-only_ | **L** (1st 0-0 → NRFI) | Hicks (0 GS all season) running as CWS's opener — real bulk-role volatility. |
| 8/1 | MIA @ NYM (T.Phillips/Thornton) | NRFI | 53% | _model-only_ | **L** (1st 1-0 → YRFI) | Both reasonably clean arms; mild lean. |
| 8/1 | PIT @ CIN (Ashcraft/Abbott) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Both mid-tier consistent starters; mild lean. |
| 8/1 | PHI @ BAL (Sánchez/Baz) | NRFI | 57% | _model-only_ | **W** (1st 0-0 → NRFI) | Sánchez dominant (2.73 ERA/10.19 K9) should keep BAL's top quiet. |
| 8/1 | TEX @ HOU (deGrom/Blanco) | YRFI | 56% | _model-only_ | **L** (1st 0-0 → NRFI) | Blanco on just his 2nd start back (8.10 ERA, tiny sample) — real 1st-inning risk. |
| 8/1 | AZ @ CLE (Drake/Messick) | YRFI | 56% | _model-only_ | **W** (1st 0-2 → YRFI) | Drake making his 2nd career MLB start — extreme small-sample risk. |
| 8/1 | WSH @ ATL (Mikolas/López) | YRFI | 56% | _model-only_ | **W** (1st 0-2 → YRFI) | Mikolas 5.65 ERA, weak recent K/9 (2.92) — contact-prone early-run risk. |
| 8/1 | NYY @ CHC (Fried/Peterson) | YRFI | 57% | _model-only_ | **W** (1st 0-1 → YRFI) | Fried's apparent IL-return gap + Peterson's rough season line (5.80 ERA). |
| 8/1 | KC @ COL (Avila/Feltner) | YRFI | 59% | _model-only_ | **L** (1st 0-0 → NRFI) | Both shaky arms (4.95/5.73 ERA) at Coors — strongest YRFI lean of the day. |
| 8/1 | SF @ SD (Mahle/Buehler) | YRFI | 54% | _model-only_ | **W** (1st 0-2 → YRFI) | Both mediocre this season (4.96/5.13 ERA). |
| 8/1 | BOS @ LAD (Tolle/Yamamoto) | NRFI | 58% | _model-only_ | **L** (1st 1-0 → YRFI) | Yamamoto elite (2.72 ERA/0.90 WHIP); Tolle solid — strongest NRFI of the day. |
| 8/1 | MIL @ LAA (Gasser/Suter) | NRFI | 52% | _model-only_ | **L** (1st 0-1 → YRFI) | **SP CHANGED (16:00 recheck): José Soriano → Brent Suter** (E3 gate) — Suter is a soft-tossing lefty reliever/swingman, not the announced Soriano; downgraded lean slightly (contact-prone but not a hard-thrower, first-inning read stays mild NRFI). |
| 8/1 | DET @ ATH (Valdez/Perkins) | YRFI | 55% | _model-only_ | **W** (1st 2-0 → YRFI) | Perkins a recent bullpen-to-rotation convert (31% GS, 6.45 ERA) — real risk. |
| 8/2 | PHI @ BAL (Wheeler/Bradish) | NRFI | 58% | _model-only_ | **W** (1st 0-0 → NRFI) | Wheeler elite (2.53 ERA/10.75 K9) should retire BAL's top clean; Bradish (3.74 ERA) decent too. |
| 8/2 | WSH @ ATL (Cavalli/Ritchie) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | Ritchie a small-sample rookie (7 GS, 4.50 ERA) — real 1st-inning risk; Cavalli (3.55 ERA) solid. |
| 8/2 | STL @ TOR (Liberatore/Scherzer) | YRFI | 59% | _model-only_ | **L** (1st 0-0 → NRFI) | Scherzer's decline is stark this year (9.49 ERA in just 24.2 IP over 7 GS) — real injury/command risk; Liberatore also shaky (5.26 ERA). Strongest YRFI lean of the day. |
| 8/2 | AZ @ CLE (Kelly/Williams) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Williams sharp (3.71 ERA/11.34 K9); Kelly middling (4.86 ERA). Mild lean. |
| 8/2 | PIT @ CIN (Keller/Burns) | NRFI | 58% | _model-only_ | **L** (1st 0-3 → YRFI) | Burns elite (2.40 ERA/10.22 K9) should keep PIT's top quiet; Keller middling (4.83 ERA). |
| 8/2 | CWS @ TB (Kay/Jax) | YRFI | 54% | _model-only_ | **W** (1st 2-0 → YRFI) | Both middling (4.25/3.74 ERA) — mild lean toward early contact. |
| 8/2 | MIA @ NYM (Alcantara/Stock) | NEUTRAL | 52% | _model-only_ | TBD | Stock still has no verifiable 2026 gamelog (E4 gate) — no reliable SP-quality read either way; Alcantara (3.82 ERA) solid. |
| 8/2 | TEX @ HOU (Rocker/Lambert) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Lambert sharp (3.06 ERA); Rocker middling (4.03 ERA). Mild lean. |
| 8/2 | NYY @ CHC (Cole/Rea) | NRFI | 56% | _model-only_ | **W** (1st 0-0 → NRFI) | Cole elite when on the mound (3.57 ERA/9.66 K9); Rea middling (4.67 ERA). |
| 8/2 | KC @ COL (Lugo/Freeland) | YRFI | 60% | _model-only_ | **W** (1st 0-1 → YRFI) | Freeland's line has collapsed (7.34 ERA) at Coors; Lugo also middling (4.22 ERA). Strongest YRFI lean of the day besides STL@TOR. |
| 8/2 | MIL @ LAA (Misiorowski/Ureña) | NRFI | 60% | _model-only_ | **W** (1st 0-0 → NRFI) | Misiorowski dominant (1.58 ERA/13.88 K9) and Ureña also sharp (2.70 ERA) — both elite arms, strongest NRFI of the day. |
| 8/2 | DET @ ATH (Montero/Jump) | NRFI | 55% | _model-only_ | **L** (1st 2-0 → YRFI) | Montero solid (3.34 ERA); Jump middling small-sample (12 GS, 4.00 ERA). Mild lean. |
| 8/2 | SF @ SD (Roupp/King) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | King sharp (3.38 ERA); Roupp middling (4.12 ERA). Mild lean. **⚠ 16:00 recheck: HOME SP CHANGED King → Kyle Hart (E3 gate)** — read premised on King is invalid; game already Live/Warmup at flag time, unbettable either way. |
| 8/2 | MIN @ SEA (Bradley/Kirby) | YRFI | 55% | _model-only_ | **W** (1st 0-2 → YRFI) | Kirby was just shelled last start (4.0 IP/7 ER/3 K) — recent-form risk despite a decent season line; Bradley solid (3.65 ERA). |
| 8/2 | BOS @ LAD (Bennett/Sheehan) | YRFI | 55% | **Over 0.5 −102 (FanDuel)** | **W** (1st 2-0 → YRFI) | Sheehan's ERA has climbed (4.95); Bennett a small-sample rookie (11 GS) — real variance on both sides. **16:00: real line pulled, no-vig YRFI(Over) 49.1% vs model 55% = +5.9pp, clears the +2pp gate — promoted from model-only to a priced read** (lineups locked, hot/wind-out weather also supports early contact). |
| 8/3 | WSH @ PHI (Alvarez/Nola) | YRFI | 56% | _model-only_ | **W** (1st 1-0 → YRFI) | Nola collapsed (5.61 ERA/1.45 WHIP, 5.2 IP/start) and Alvarez runs a 1.51 WHIP — traffic early on both sides in a hitter park. |
| 8/3 | STL @ NYY (McGreevy/Schlittler) | NRFI | 55% | _model-only_ | **L** (1st 2-0 → YRFI) | Schlittler is the slate's best arm (2.04 ERA/0.91 WHIP) vs a 21%-K STL top; McGreevy's damage usually comes late, not in the 1st. |
| 8/3 | PIT @ MIL (Chandler/Sproat) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | Two walk-prone, short arms (4.56/1.41 and 5.05/1.39) vs two live tops (MIL .260/.341, PIT .263/.345 vs RHP). |
| 8/3 | LAD @ CHC (TBD/Boyd) | YRFI | 55% | _model-only_ | **W** (1st 3-2 → YRFI) | ⚠ E4 — LAD starter TBA. Boyd (3.41) steadies one side, but LAD's .267/.346-vs-RHP top is the best on the slate. |
| 8/3 | SF @ TEX (Webb/TBD) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | ⚠ E4 — TEX starter TBA. Webb is a prototypical NRFI ground-ball arm (1.12 WHIP) and SF's top is weak (.255/.313 vs RHP), in a dome. Mild lean. |
| 8/3 | TOR @ HOU (Bieber/Javier) | YRFI | 60% | _model-only_ | **L** (1st 0-0 → NRFI) | Day's strongest YRFI: Bieber's command gone (0.2 IP/4 ER/6 BB last out) and Javier 4 starts into a ramp-up at 7.17 ERA/1.83 WHIP. |
| 8/3 | TB @ COL (Seymour/Lorenzen) | YRFI | 60% | _model-only_ | **W** (1st 2-0 → YRFI) | Coors + Lorenzen 6.54 ERA/1.81 WHIP (3.2 IP/6 ER and 4.0 IP/3 ER his last two) vs a .262/.335 TB top. |
| 8/3 | SD @ AZ (King/Pfaadt) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Day's strongest NRFI: King steady (3.38/1.17, 6.0 IP in four of five) and Pfaadt sharp lately (7.0 IP/0 ER last out), in a dome. |

| 8/4 | LAA @ BAL (G.Rodriguez/TBD) | YRFI | 56% | _model-only_ | TBD | ⚠ E4 — BAL TBA. G-Rod 7.98 ERA / 1.75 WHIP is the worst line on the board; lean held mild for the unknown half |
| 8/4 | ATH @ CIN (Ginn/Singer) | YRFI | 56% | _model-only_ | TBD | GABP hitter park + Singer 1.43 WHIP, offset by the worst road offense on the slate (ATH .244/.325, RDiff −154) |
| 8/4 | NYM @ CLE (Manaea/Cantillo) | YRFI | 55% | _model-only_ | TBD | Both WHIPs ≥1.34 (Cantillo 1.45) = traffic game; capped by NYM's .231/.301 top and a neutral park |
| 8/4 | WSH @ PHI (Littell/Luzardo) | YRFI | 57% | _model-only_ | TBD | One-sided: Littell 4.94/1.34 vs PHI's top at CBP; Luzardo (3.57/1.19) stabilises the other half |
| 8/4 | STL @ NYY (Dobbins/Weathers) | YRFI | 57% | _model-only_ | TBD | Yankee Stadium + NYY top vs a 4-start rookie (1.34 WHIP); STL's 18%-K top puts balls in play vs Weathers |
| 8/4 | **CWS @ BOS (Martin/Sandoval)** | **YRFI** | **56%** | **Over 0.5 +102 (FanDuel)** — no-vig 48.6%, **+7.4pp** | TBD | ✅ gate cleared. Sandoval 1.58 WHIP, 4 starts / 19 IP into a return, at Fenway vs a BOS side on W5/L10 8-2. Shaded 60%→56% on CWS's 24% K vs LHP and the market's YRFI-side price |
| 8/4 | MIA @ ATL (Gusto/Holmes) | YRFI | 59% | _model-only_ | TBD | Gusto 5.31/1.44 vs the hottest top on the slate (ATL 67-45, W5, +108). Strongest un-priced YRFI |
| 8/4 | **MIN @ KC (J.Ryan/Dobnak)** | **NRFI** | **55%** | **Under 0.5 −104 (FanDuel)** — no-vig 48.8%, **+6.2pp** | TBD | ✅ gate cleared, market on the other side. Two sub-1.20 WHIPs + two weak tops (.313/.319 OBP) at Kauffman; shaded 57%→55% because Dobnak is a 26-IP/4.85-K/9 sample the market may be reading as short |
| 8/4 | **PIT @ MIL (Jones/Henderson)** | **NRFI** | **58%** | **Under 0.5 −129 (BetRivers)** — no-vig 54.7%, **+3.3pp** | TBD | ✅ gate cleared. Cleanest premise of the day: the slate's two best WHIPs (1.02, 0.91) in a dome vs PIT's 23%-K top. Market agrees → smallest edge of the four |
| 8/4 | LAD @ CHC (Skubal/Assad) | NRFI | 55% | _model-only_ | TBD | Skubal 0.91 WHIP elite, Assad competent — but two strong tops (CHC .333/.355 OBP) and **Wrigley wind PENDING**, the one park a wind reading would move |
| 8/4 | SF @ TEX (Tidwell/Gore) | YRFI | 55% | _model-only_ | TBD | ⚠ C4-adjacent: Tidwell has **0 GS in 12 IP** (swingman/opener question). Gore's 4.77 ERA is the firmer signal. Dome |
| 8/4 | TOR @ HOU (Yesavage/Wesneski) | YRFI | 58% | _model-only_ | TBD | Wesneski: **5.2 IP all season, 1 GS**, 1.59 WHIP — rust + short leash, effectively a HOU bullpen game; Yesavage steadier, so equity is one-sided |
| 8/4 | **TB @ COL (Peralta/Hughes)** | **YRFI** | **61%** | **Over 0.5 −130 (FanDuel)** — no-vig 54.9%, **+6.1pp** | TBD | ✅ gate cleared, day's strongest. Peralta 1.48 WHIP / 4.5 IP-per-start vs the slate's most contact-heavy top (TB 18-19% K, .264) at Coors. **Yesterday's 22-run game on a wind-IN reading is why no suppression is applied** |
| 8/4 | SD @ AZ (Vásquez/E.Rodriguez) | YRFI | 55% | _model-only_ | TBD | Vásquez 1.47 WHIP is the YRFI half; E-Rod (2.48 ERA, best on board) caps it. Dome |
| 8/4 | DET @ SEA (TBD/Hancock) | NRFI | 55% | _model-only_ | TBD | ⚠ E4 — DET TBA. Hancock 3.26/1.04 in T-Mobile is an archetypal NRFI side but half the matchup is unknown |

---

## Running totals (update on every settle)
- **Record:** **132-108** (tracker opened 6/10/26). **NRFI:** **65-56** · **YRFI:** **67-52**.
- **Staked:** $0 · **P/L:** $0.00 (model leans only — no priced bets yet; tracking calibration).
- **Open:** **8/3 SETTLED** (auto via `nrfi_settle.py --apply` at this session's start — all 8 reads stamped,
  **5W-3L**: WSH@PHI YRFI ✅, LAD@CHC YRFI ✅, SF@TEX NRFI ✅, TB@COL YRFI ✅, SD@AZ NRFI ✅; STL@NYY NRFI ❌
  (1st went 2-0), PIT@MIL YRFI ❌ (0-0), TOR@HOU YRFI ❌ (0-0). Record moved to **132-108**. The 18:45
  downgrade of TB@COL YRFI 60%→54% on the wind-IN reading was in the *wrong* direction — the 1st went 2-0
  and the game went 22 runs; the lean would have been better left at 60%.) **8/4: 15 games, all pre-game at
  build time** — today's reads above; **4 of them are priced reads clearing +2pp** (PIT@MIL NRFI −129,
  MIN@KC NRFI −104, TB@COL YRFI −130, CWS@BOS YRFI +102), the other 11 model-only. Settle next session via
  `nrfi_settle.py --apply`.
- **Settled 7/26** (auto via `nrfi_settle.py --apply`, run 7/30): 14 decided, 7W-7L (NRFI 2-3, YRFI 5-4).
  Record updated from 91-74 to 98-81. LAA@SF (Soriano/Whisenhunt, NEUTRAL) still TBD — game likely
  postponed/unresolved, left open. **No parlay builds ran 7/27-7/29** (session gap) — those slates have
  no NRFI reads logged; resuming the daily cadence today (7/30).
- **Settled 6/24 + 7/25** (backfilled 7/26 — these reads were logged in "Tonight's reads" but never copied into
  the Ledger table in their build sessions, so `nrfi_settle.py` had nothing to match; fixed by hand this run
  using `mlb_api.sh raw schedule?...hydrate=linescore` for the 1st-inning score). 6/24: 3 decided (1W-2L,
  1 neutral excluded). 7/25: 12 decided (6W-6L, 3 neutral excluded) — NRFI 5-1, YRFI 1-5 on the day (the
  elite-arm NRFI theses (Cease, Skenes/Imanaga, Yamamoto/McLean) all held; the YRFI TBD-SP-variance thesis
  missed repeatedly — TBD/uncertain-SP alone isn't a reliable YRFI driver without a live bat trio also firing).
- **Settled 6/22** (auto via `nrfi_settle.py --apply`): 8 reads settled 5W-3L (NRFI 3-0, YRFI 2-3). Record updated from 78-64 to **84-66**. Neutral reads (MIL@CIN, BAL@LAA, TEX@MIA, AZ@STL) excluded (lean ~50/51%). CHC@NYM postponed → left open. Strong NRFI (Rasmussen/Cole) both hit; the Coors YRFI missed badly (total only 5 runs, wind In suppressed it — calibration lesson confirmed).
- **Settled 6/21** (auto via `nrfi_settle.py --apply` in session_start.sh): 4 reads → 3W-1L.
  - LAA@ATH NRFI ❌ L (1st 0-4 → YRFI — Perkins/ATH exploded 4 runs)
  - BAL@LAD YRFI ✅ W (1st 2-1 → YRFI — LAD top cashed early vs Young)
  - BOS@SEA NRFI ✅ W (1st 0-0 → NRFI — Gilbert dominated early; BOS top quiet)
  - NYM@PHI YRFI ✅ W (1st 0-2 → YRFI — PHI top scored 2 early vs Peterson)
  Record updated from 75-63 to **78-64**. 6/21 NRFI 1-1, YRFI 2-0. Good YRFI day.
- **Settled 6/20:** 14 reads settled 9W-5L (NRFI 4-4, YRFI 5-1) — solid YRFI day. Record updated from 66-58 to 75-63.
- **Settled 6/11** (auto via `nrfi_settle.py --apply`): LAD@PIT YRFI **L** (1st 0-0 → NRFI), SEA@BAL NRFI **L**
  (1st 1-0 → YRFI). **Calibration:** YRFI on LAD's top missed AGAIN (2nd straight 0-0 LAD 1st) — the
  pitching-first/NRFI bias keeps beating the bats-first LAD-top read; the SEA@BAL NRFI lean missed on a lone
  early run. NRFI leans 2-1, YRFI 0-2 so far — small n, but the doctrine's NRFI bias is holding.
- **Settled 6/10:** ATL@CWS NRFI **W** (1st 0-0), MIN@DET NRFI **W** (1st 0-0), LAD@PIT YRFI **L** (1st 0-0).

> Tracked like `fades.md` / `bankroll.md`: any change → commit → push → PR → squash-merge.
> **Settling is automated:** `tools/nrfi_settle.py [date] --apply` stamps W/L from the 1st-inning line score
> (auto-run in `session_start.sh` for yesterday + today every session). Run it by hand for any other date.
</content>
</invoke>
