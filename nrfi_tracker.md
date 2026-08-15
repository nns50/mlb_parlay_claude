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

## Tonight's reads — 2026-08-15 (15-game slate; model-only at 11:00 — the priced `totals_1st_1_innings` sweep is the 16:00 run)

> **✅ 8/14 AUTO-SETTLED at session start** — 13 rows stamped off `linescore.innings[0]` by
> `nrfi_settle.py --apply`. **Record now 207-174 (54%)** (NRFI 107-87 · YRFI 100-87).
>
> ---
>
> ### ⚠ 16:00 RUN — the priced sweep, and why the one big number is NOT being promoted
>
> **CWS @ DET settled: 1st inning 1-1 → YRFI, our NRFI 60% read LOST.** Today's daily line is **0-1**;
> **14 reads remain open**; lineups are now CONFIRMED for every pre-game game and **no scratch flips any
> read** (the tracker's leans are SP-driven, and `recheck.py` reports no SP change beyond SD's TBA
> resolving — see below).
>
> **1 credit was spent pricing the single strongest read rather than sweeping all fifteen:**
> **MIL @ LAD NRFI (Misiorowski, 0.74 WHIP — the lowest on the board).** Best **Under 0.5 −136
> (BetRivers)**, devigged against that book's own Over 0.5 −105 → **market no-vig 52.9%, hold 8.9%.**
>
> **Model 61% vs market 52.9% = a raw +8.1pp gap — and it is being DECLINED. Three reasons, in order of
> weight:**
> 1. ⛔ **The 61% is not a derived TrueP.** It is a model-only number, pre-registered but *not* built from
>    the market no-vig baseline plus registered tags — which is precisely what CLAUDE.md calls the
>    `*`-equivalent of TrueP. **No registered tag exists for NRFI at all**, so under the 8/12 audit's
>    finding #3 this thesis prices at market: **52.9%, edge 0.0pp.**
> 2. ⛔ **`market_disagrees` fires.** An ~8pp gap on a liquid market is the doctrine's own warning sign —
>    *a surprisingly long price is information; defer to the line.* The registered magnitude is −4pp,
>    halved to **−2pp** by GLOBAL SHRINK, which alone cuts the gap to +6.1pp before the point above
>    zeroes it.
> 3. ⚠ **The hold is 8.9%** — roughly triple a main-market total. Even were the edge real, the vig on the
>    best of five books eats most of it, and **−136 is an expensive price for a 52.9% event.**
>
> ⚠ **Named plainly because it is the tracker's own trap:** the rule says *promote if a real line clears
> +2pp*, and read literally this clears by four times that. **A +8.1pp gap against a liquid market is far
> more likely to be a model artifact than an edge** — the tracker's model numbers have never been
> calibrated against prices, because until today essentially none of them were ever priced. **This is the
> first data point in that calibration, and it says the model runs hot.** Logged, not bet.
>
> ⚠ **Two data flags on today's board, named before the numbers.** (1) **SD @ CLE carries a TBA starter**
> (San Diego's), so that row has half an input and is marked **LOW CONFIDENCE** rather than quietly
> modelled as complete (E4). (2) **TWO games are bullpen/opener constructions on one side** — **Braydon
> Fisher (TOR)** has thrown **1.0, 1.0, 1.0, 2.0, 1.0, 1.0 IP in his last six outings, every other day**,
> and **Brad Lord (WSH)** has **2 GS in 61.2 IP** with his last eight outings all ≤3.0 IP. Both are listed
> as probables and neither is a starter. **A fresh 1-inning opener is a different 1st-inning object than a
> bad starter** — it usually suppresses the first frame rather than inflating it — so neither row is given
> a reflex YRFI lean on "the starter is weak."
>
> ✅ **The lineup gate stays on: these are model leans at 11:00, not locks.** The 8/13 MIL@LAD row remains
> the standing example — priced at +6.6pp, refused for an unposted lineup, and the first inning went 0-0.

| Matchup (SP) | Lean | TrueP | Price | Why |
|---|---|---|---|---|
| CWS @ DET (Kay 3.96/1.34 · Melton **1.46/0.90**) | **NRFI** | **60%** | _model-only_ | Slate's best 1st-inning suppressor pair-half; Comerica + wind **7mph IN** |
| MIL @ LAD (Misiorowski **1.76/0.74** · Wrobleski 3.44/1.11) | **NRFI** | **61%** | _model-only_ | **0.74 WHIP** is the lowest on the board — baserunners are the input |
| AZ @ ATL (E-Rodriguez 2.70/1.23 · Holmes 3.47/1.32) | NRFI | 57% | _model-only_ | Two sub-3.50 ERA arms, no park or air help for the bats |
| SEA @ HOU (Hancock 3.35/1.12 · Wesneski 3.86/1.18) | NRFI | 56% | _model-only_ | Dome, neutral air, two 1.1x WHIPs |
| STL @ CHC (McGreevy 3.64/1.22 · Boyd 3.50/1.22) | NRFI | 56% | _model-only_ | Matched 1.22 WHIPs; ⚠ Wrigley wind PENDING at a 14:20 first pitch |
| BAL @ TB (Bradish 3.69/1.34 · Seymour 4.08/**1.13**) | NRFI | 54% | _model-only_ | Seymour 10.56 K/9 in a dome; Bradish's 1.34 is the drag |
| NYY @ TOR (Schlittler **2.21/0.93** · Fisher — **OPENER**) | NRFI | 54% | _model-only_ | Schlittler 0.93 WHIP; fresh 1-inning opener ≠ soft first frame |
| KC @ LAA (Dobnak 2.00/1.33 · Detmers 4.00/**1.10**) | NRFI | 54% | _model-only_ | Detmers 10.40 K/9 vs a KC offence at −113 run diff |
| PHI @ MIN (Luzardo 3.32/1.14 · Prielipp 4.79/1.32) | NRFI | 53% | _model-only_ | Luzardo 11.03 K/9 carries it; Prielipp vs the PHI top is the risk |
| BOS @ PIT (Gray **2.79/1.15** · Jones 5.03/1.20) | NRFI | 53% | _model-only_ | PNC suppresses; ⚠ Jones gave **8 ER in 3.0 IP** last out — the live YRFI half |
| COL @ SF (Lorenzen **6.83/1.88** · Webb 3.59/1.08) | YRFI | 53% | _model-only_ | 1.88 WHIP is a first-inning traffic magnet; Oracle + a 50-72 SF bat is the counter |
| SD @ CLE (**TBA** · Cantillo 3.91/**1.48**) | YRFI | 54% ⚠LOW-CONF | _model-only_ | Cantillo 1.48 WHIP; **E4 — half the input is missing** |
| TEX @ ATH (Gore 4.43/1.24 · Ginn 3.41/1.21) | YRFI | 54% | _model-only_ | Sutter Health is a hot small-park; both arms are mid |
| WSH @ NYM (Lord — **BULLPEN GAME** · Manaea 4.13/1.32) | YRFI | 55% | _model-only_ | Manaea's 1.32 is the real input; Lord's 1-2 innings are fresh, not soft |
| MIA @ CIN (Gusto 4.78/1.33 · Singer 4.66/**1.43**) | **YRFI** | **58%** | _model-only_ | Weakest pair on the board in the NL's best hitter's park |

**Model-only, no bet:** no `totals_1st_1_innings` line was pulled at 11:00 — the priced sweep belongs to the
16:00 run, and per doctrine a read is bet only if a real line clears +2pp. ⚠ **MIA @ CIN is flagged as the
row most likely to be already priced** (two 4.6+ ERAs in GABP is not a secret), so a fair price there is the
one to check first, not assumed.

## Tonight's reads — 2026-08-14 (14-game slate; model-only at 11:00 — the priced `totals_1st_1_innings` sweep is the 16:00 run)

> **✅ 8/13 CLOSED 6W-3L (67%).** The three late rows auto-settled off `linescore.innings[0]` at session
> start and the stamps are verified present. **Record now 202-165 (55%)** (NRFI 104-84 · YRFI 98-81).
> **NRFI leans went 4-1; YRFI leans went 2-2** — the third straight slate the NRFI side carried the board.
>
> ⚠ **The −5pp YRFI correction's eighth graded slate was a MISS on the row pre-flagged as its most likely
> miss** (BOS @ TOR, flipped raw YRFI 56% → NRFI 51%, first inning went 1-0). Eight graded slates: 8/6
> neutral, 8/7 neutral, 8/8 strongly positive, 8/9 strongly negative, 8/10 mildly negative, 8/11 neutral,
> 8/12 positive, 8/13 negative-on-the-flip. **Today is slate nine; not tapered, not extended.**
>
> ✅ **The clearest vindication of the lineup gate this tracker has produced:** MIL @ LAD was priced at
> **+6.6pp** on 8/13 and refused a lock because Milwaukee's lineup was unposted and Betts was scratched.
> **The first inning went 0-0 and the YRFI lost.** A qualifying price is not a qualifying leg.
>
> ⚠ **Three data flags on today's board, named before the numbers.** (1) **Three starters are TBA** —
> BAL's, ATL's and the Athletics' — so those rows carry only half an input and are marked LOW CONFIDENCE
> rather than quietly modelled as if complete (E4). (2) **CWS @ DET is a bullpen game on one side and a
> 5-inning sample on the other**: Sean Newcomb has **1 GS in 64.1 IP** and his last twelve outings are all
> 0.2–2.0 IP relief, while Jackson Jobe's 0.00 ERA / 0.40 WHIP is **5.0 IP across a single start** — an E2
> stale/small-sample line in the flattering direction. Both used at heavy discount. (3) **Robert Stock
> (NYM) carries a 10.13 ERA / 2.13 WHIP over 2 GS and 8.0 IP** — the worst line on the board by a wide
> margin and itself a small sample, but small-sample-bad in a direction his 3.0 IP / 8 ER outing on 8/8
> corroborates, so it is used rather than discarded.
>
> **No priced line pulled at 11:00** (the 1st-inning market is thin pre-lineup and the sweep is the 16:00
> duty), so all fourteen rows go to the ledger as model-only calibration. Raw model splits the board
> **5 NRFI / 9 YRFI**; the −5pp correction pulls it to **6 / 8**, reversing exactly one read —
> **MIL @ LAD** — marked below.

| # | Matchup | SPs (WHIP) | Lean | TrueP | Price | Reasoning |
|---|---|---|---|---|---|---|
| 1 | SD @ CLE | King 1.17 / **G. Williams 1.04** | **NRFI** | **58%** | _model-only_ | **The strongest read of either kind today, and the best combined arms on the board.** King is 3.37 / 1.17 over 24 GS; Williams 3.55 / **1.04** over 24 GS with **11.51 K/9**, the highest strikeout rate on the slate — and whiffs are the cleanest first-inning suppressant there is. **Progressive Field is a genuine suppressant venue.** Neither top-of-order is an engine (SD +1, CLE −30). ⚠ Counter recorded: Williams struck out 10 vs AZ on 8/2, so his half is dominant, but King's 1.17 allows more traffic than the pair's headline suggests. |
| 2 | WSH @ NYM | Alvarez 1.40 / **Stock 2.13** | **YRFI** | **57%** | _model-only_ | **Raw YRFI 62% → 57%, and it is comfortably the strongest YRFI of the day.** **Robert Stock's 2.13 WHIP is the worst on the board by nearly half a run of baserunners** — a pitcher allowing 2.13 per inning is, by definition, putting the leadoff man on. His last start was **3.0 IP / 8 ER / 5 BB @ PIT**, so the season line is corroborated rather than a fluke of two outings. Alvarez's 1.40 does not suppress either. ⚠ Held at 57 rather than higher because the sample is genuinely 2 GS and 8.0 IP, and because neither top-of-order is an engine (WSH +23, NYM −47). |
| 3 | MIA @ CIN | Alcantara 1.17 / **Burns 1.12** | **NRFI** | **55%** | _model-only_ | Two sub-1.20 WHIPs, and **Chase Burns at 2.61 / 1.12 with 10.38 K/9 over 22 GS (13-2)** is the second-best arm on the slate. Alcantara's 3.52 / 1.17 across **163.2 IP** is the most durable line on the board. ⚠ **The counter is the park and it is a big one — Great American is the best hitter's venue in the National League**, which is why this sits at 55 and not at the ~60 the arms alone would say. Weather PENDING at 11:00. |
| 4 | BOS @ PIT | **Bennett 1.04** / Chandler 1.38 | **NRFI** | **55%** | _model-only_ | **Jake Bennett's 1.04 WHIP is tied for the best on the board** (3.17 ERA over 13 GS), and **PNC Park is one of the two strongest suppressant venues in the league.** Bennett's half of the inning is close to a lockout. ⚠ **Chandler's 1.38 is the whole drag** — 4.26 ERA over 22 GS — and Boston's 1-2-3 at +86 run differential is a real top-of-order, which is why a 1.04/pitcher-park combination only produces 55. |
| 5 | NYY @ TOR | **Cole 1.08** / **Bieber 1.66** | **YRFI** | **55%** | _model-only_ | Raw **YRFI 60% → 55%.** **Bieber's 1.66 WHIP is the worst qualified line on the board** (5.48 ERA over 9 GS, still working back and averaging under 5 IP/start), and **the Yankee 1-2-3 is a standing YRFI engine at +89** — the single best top-of-order/bad-arm pairing on the slate. Rogers Centre with the roof is a hitter's venue. ⚠ **Cole's half is the counter and it is severe** — 3.35 / 1.08 with 9.71 K/9 — so this is a one-sided YRFI, entirely dependent on Toronto's half of the inning. |
| 6 | KC @ LAA | Lugo 1.37 / **G. Rodriguez 1.62** | **YRFI** | **55%** | _model-only_ | Raw **YRFI 60% → 55%. The weakest pair of arms on the board:** Grayson Rodriguez at **7.20 ERA / 1.62 WHIP** over 12 GS and Seth Lugo at 4.41 / 1.37 over 24 GS. Neither suppresses and both allow first-inning traffic. ⚠ **Two counters keep it at 55 rather than higher:** neither top-of-order is remotely an engine — **KC −114 and LAA −83 are two of the four worst run differentials in the AL** — and Angel Stadium is a neutral-to-suppressing venue, not a bandbox. |
| 7 | STL @ CHC | **Liberatore 1.52** / Holmes 1.10 | **YRFI** | **54%** | _model-only_ | Raw **YRFI 59% → 54%.** **Matthew Liberatore's 1.52 WHIP is the second-worst qualified line on the slate** (5.15 ERA, 5-9 over 23 GS) and **the Cubs' 1-2-3 is the second-best top-of-order on the board at +108.** That is the YRFI case and it is a clean one. ⚠ **Clay Holmes at 2.39 / 1.10 is the counter** and it is why this is not 58 — his half of the inning is close to shut. ⚠ **Wrigley is the one park on the board where the wind can move this read several points in either direction, and weather is PENDING at 11:00** — this row is the most likely of the fourteen to want re-reading at 16:00. **First pitch 14:20 ET, so the 16:00 run will be too late** — flagged rather than fixed. |
| 8 | SEA @ HOU | Kirby 1.27 / Lambert 1.15 | **NRFI** | **54%** | _model-only_ | Two competent arms in a dome with weather removed: Peter Lambert at **3.09 / 1.15 over 20 GS** is quietly the better half, Kirby 3.68 / 1.27 over 22 GS the softer one. Neither top-of-order is an engine (SEA −26, HOU −27, both negative). ⚠ **Kirby's 1.27 is the drag** and Houston's lineup makes a lot of contact (21% K vs RHP), which puts balls in play early — contact is not the same as suppression. |
| 9 | TEX @ ATH | Rocker 1.38 / **TBA** | **YRFI** | **53%** | _model-only_ | ⚠ **LOW CONFIDENCE — the Athletics' starter is TBA (E4), so half this read's input does not exist.** What is known: Kumar Rocker at 4.46 / 1.38 over 20 GS does not suppress, and **Sutter Health Park is the most hitter-friendly venue on the board** — a temporary minor-league park that has played small all season. Both point YRFI, which is why the lean stands, but **it is a lean on one starter and a park, not on a matchup**, and it is logged at 53 to say so. |
| 10 | MIL @ LAD | Gasser 1.22 / **Yamamoto 0.89** | **NRFI** | **52%** | _model-only_ | ⚠ **FLIPPED READ — the only one the correction reverses today.** Raw model says **YRFI 53%** on the strength of the two best tops-of-order in baseball (**MIL +131 and LAD +141**, exactly as on 8/13), and the −5pp correction pulls it to a bare NRFI. **The case for the flip is Yoshinobu Yamamoto's 0.89 WHIP — the best on the board and the only sub-1.00 on the slate** (2.65 ERA over 21 GS); his half of the first is as close to a lockout as this board offers, and Dodger Stadium suppresses. ⚠ **Recorded against ourselves: this exact game read YRFI 56% yesterday and the first inning went 0-0**, so the flip is in the direction yesterday's result argues for — which is a reason to be careful, not confident, since one inning is not evidence. Gasser's 1.22 is the live YRFI half. |
| 11 | CWS @ DET | **Newcomb (opener)** / Jobe 0.40 | **NRFI** | **52%** | _model-only_ | ⚠ **LOW CONFIDENCE — this is a bullpen game on one side and a 5-inning sample on the other.** **Sean Newcomb has 1 GS in 64.1 IP and his last twelve appearances are all 0.2–2.0 IP relief outings** — he is an opener, and an opener's *first* inning is often his best (fresh arm, 2.66 ERA in that role), which is the entire NRFI case here. **Jackson Jobe's 0.00 ERA / 0.40 WHIP is 5.0 IP across one start** and is treated as an E2 small-sample line, not as a true talent read. Held at a bare 52 because **the honest answer is that neither half of this inning is well estimated.** |
| 12 | COL @ SF | **Freeland 1.50** / Roupp 1.29 | **YRFI** | **52%** | _model-only_ | Raw **YRFI 57% → 52%.** Kyle Freeland at **6.63 ERA / 1.50 WHIP (3-10 over 21 GS)** is the third-worst line on the board and does not miss bats (7.67 K/9). ⚠ **Two counters pull this most of the way back:** **Oracle Park is the strongest suppressant venue in baseball**, and **Colorado's top-of-order is the second-weakest on the slate at −116** — a bad arm facing a bad lineup in a huge park is a coin flip, not a YRFI. Roupp's 1.29 is unremarkable in both directions. |
| 13 | AZ @ ATL | Pfaadt 1.20 / **TBA** | **YRFI** | **52%** | _model-only_ | ⚠ **LOW CONFIDENCE — Atlanta's starter is TBA (E4).** The YRFI case is **Atlanta's 1-2-3, which at +124 is the best top-of-order in the National League** and the second-best on the board. ⚠ **Brandon Pfaadt is the counter and he is a real one** — 3.36 / 1.20 over 11 GS — though **his 5.67 K/9 is the lowest on the slate**, meaning he works through the inning on contact rather than shutting it, which is exactly the profile that concedes a first-inning run to a good lineup. Lean is on the Braves' half alone. |
| 14 | BAL @ TB | **TBA** / Matz 1.23 | **YRFI** | **52%** | _model-only_ | ⚠ **LOW CONFIDENCE — Baltimore's starter is TBA (E4), so the away half is unmodelled.** Steven Matz at **5.46 ERA / 1.23 WHIP over 10 GS** is the known half: the WHIP says he limits traffic but the ERA says what traffic he allows scores, which is a homer-prone profile and a first-inning risk. Tropicana is a dome, so weather is removed. **Neither run differential is strong from the Orioles' side (−36)**; Tampa Bay's +62 and L10 of 9-1 are the YRFI push. Logged at a bare 52 to reflect the missing input. |

---

## Tonight's reads — 2026-08-13 (9-game slate; model-only at 11:00 — the priced `totals_1st_1_innings` sweep is the 16:00 run)

> **✅ 8/12 CLOSED 9W-6L (60%).** All fifteen rows auto-settled off `linescore.innings[0]` by
> `nrfi_settle.py --apply` at session start; stamps verified present. **Record now 196-162 (55%)**
> (NRFI 100-83 · YRFI 96-79). **NRFI leans went 6-2; YRFI leans went 3-4** — the second straight slate
> where the NRFI side carried the board and the third in four where the YRFI side did not.
>
> **The −5pp YRFI correction's seventh graded slate — and its cleanest win.** It flipped exactly one read,
> **NYM @ ATL** (raw YRFI 56% → NRFI 51%), and the first inning went **0-0 → NRFI ✅**. The 8/12 note had
> named that specific row as *"the row I most expect the correction to be wrong on tonight"* — it was right
> instead, on the row we had least confidence in. Seven graded slates: 8/6 neutral, 8/7 neutral, 8/8 strongly
> positive, 8/9 strongly negative, 8/10 mildly negative, 8/11 neutral, **8/12 positive**. Runs to the
> ~10-slate review per the pre-registration; **not tapered, not extended.**
>
> ⚠ **The two 8/12 NRFI misses are worth naming because both were reads on quality arms**: **SEA @ NYY NRFI
> 53%** (Bryce Miller's 0.95 WHIP) and **CLE @ DET NRFI 55%** (Foster Griffin's 1.11) both busted. That is the
> same shape as the main build's thesis-conflict problem yesterday — **a very good season WHIP is not a
> first-inning guarantee**, and the tracker keeps paying for treating it as one.
>
> **Today's board is nine games and unusually pitcher-heavy.** Four of the eighteen listed starters carry a
> sub-1.10 WHIP (Montero 1.01, Messick 1.04, Fried 0.97, Gilbert 1.00) and two entire games are made of them.
> ⚠ **Two data flags, named before the numbers:** (1) **Max Scherzer's 7.25 ERA / 1.53 WHIP is the worst line
> on the board but it is a STALE AGGREGATE** — his last two starts are 6.0 IP / 1 ER and 5.1 IP / 2 ER, and
> the season number is dragged by two April outings of 2.1 IP before a long absence. It is used at half
> weight. (2) **PHI @ MIN is at Field of Dreams, Dyersville** — a temporary park with essentially no
> park-factor history, so no park input is applied in either direction rather than guessed.
>
> **No priced line pulled at 11:00** (the 1st-inning market is thin pre-lineup and the sweep is the 16:00
> duty), so all nine rows go to the ledger as model-only calibration. Raw model splits the board **4 NRFI /
> 5 YRFI**; the −5pp correction pulls it to **5 / 4**, reversing one read — **BOS @ TOR** — marked below.

> **✅ 16:00 BUILD B — the priced sweep ran and produced the day's two best legs.** All three still-pre-game
> games had `totals_1st_1_innings` pulled across 3 books (3 credits) and devigged against the TruePs
> pre-registered above at 11:00, **before any price for this market existed**. **Two of three clear the
> +2pp gate**: **MIL @ LAD YRFI −105 at +5.9pp** (the biggest edge on the whole board, promoted to the
> build's Tier 1 but ⚠ **PENDING LINEUP** — the entire thesis is the top-of-order, so the 18:00 run locks
> or drops it) and **PHI @ MIN YRFI −110 at +2.3pp** (lineups CONFIRMED both sides, promoted into the
> build's Tier 2 same-game pair). **TEX @ LAA NRFI −140 fails at +0.9pp**, and its two sides sum to a
> **5.9% overround** — the 2nd sighting of the hold finding, which that promotes to doctrine.
> ⚠ **Both promotions are YRFI, the side the −5pp correction penalises**, so the correction is working
> against today's card rather than for it and both rows grade cleanly tonight.
> ⚠ **Recorded honestly: this tracker is a separate ledger that `pulse.py` does not govern and `calib.py`
> does not score for Brier skill vs market.** Its TrueP has never been tested against the market the way
> `results_log.md` rows are, so a +5.9pp claim here is weaker evidence than the same number would be there.
> The six earlier games are **In Progress or Final** and unbettable; their reads settle at 11:00 tomorrow.

| # | Matchup | SPs (WHIP) | Lean | TrueP | Price | Reasoning |
|---|---|---|---|---|---|---|
| 1 | CLE @ DET | **Messick 1.04** / **Montero 1.01** | **NRFI** | **59%** | _model-only_ | **The strongest read of either kind today and the best WHIP pair on the board.** Messick is 2.57 ERA / 1.04 over 23 GS with 8.96 K/9; Montero 3.38 / **1.01** over 19 GS. Comerica is a genuine suppressant venue and the wind is a harmless 4 mph left-to-right at 77°F. ⚠ Counter recorded honestly: **this exact game read NRFI 55% yesterday and busted**, and Detroit's +87 differential is the third-best in the AL. Held at 59 rather than higher for that reason. |
| 2 | TEX @ LAA | **deGrom 1.13** / Ureña 1.29 | **NRFI** | **56%** | **−140 Caesars → no-vig 55.1%, +0.9pp — ⛔ NO BET (under gate)** | deGrom's **10.92 K/9 is the highest on the slate** and strikeouts are the cleanest first-inning suppressant there is; his half of the inning is close to a lockout. Ureña's 2.83 ERA is real but the 1.29 WHIP says traffic, and **the Angels strike out 25% vs both hands** — a lineup that whiffs is a lineup that does not string a first-inning rally. Weather PENDING at 11:00; re-read at 18:00. |
| 3 | PIT @ MIA | Ashcraft 1.16 / Phillips 1.36 | **NRFI** | **56%** | _model-only_ | **Roof closed at loanDepot, 72°F, wind 0** — weather removed entirely, at the National League's second-best suppressant venue. Ashcraft's 9.86 K/9 over 23 GS is the whiff half. **Neither top-of-order is an engine** (PIT +13, MIA +23, 17th and 15th by differential). Phillips' 1.36 is the drag and is why this is not higher. |
| 4 | SEA @ NYY | **Gilbert 1.00** / **Fried 0.97** | **NRFI** | **55%** | _model-only_ | **Two sub-1.00 WHIPs, the only such pair on the board** — Fried at 2.88 / 0.97 and Gilbert at 3.42 / 1.00 with 9.37 K/9. Held five points below what those numbers alone would say, by the two biggest counters on the slate: **the Yankee 1-2-3 is a standing YRFI engine at +90**, and **83°F with the wind 9 mph out to right** is the most carry-friendly reading posted. ⚠ **This game read NRFI 53% yesterday and busted 5-10**; the arms are better today but the caution is logged rather than forgotten. |
| 5 | BOS @ TOR | **Tolle 1.10** / Scherzer **1.53** | **NRFI** | **51%** | _model-only_ | ⚠ **FLIPPED READ.** Raw model says **YRFI 56%** on Scherzer's 1.53 WHIP — the worst on the board — and the −5pp correction reverses it to a bare NRFI. **Two things hold the YRFI case down:** Scherzer's season line is a **stale aggregate** (last two starts 6.0 IP / 1 ER and 5.1 IP / 2 ER), and **Toronto hit .218 / .292 against left-handed pitching**, which is who they face in Tolle — a 10.43 K/9 lefty who struck out **14** on 8/7. Marked for row-level grading; **this is the row I most expect the correction to be wrong on tonight**, because a 41-year-old arm's first inning is its least reliable. |
| 6 | MIL @ LAD | Drohan 1.25 / Sasaki 1.28 | **YRFI** | **56%** | ⭐ **−105 BetMGM → no-vig 50.1%, +5.9pp — PROMOTED, ⚠ PENDING LINEUP** | Raw **YRFI 61%** → 56%, and it is still the strongest YRFI of the day. **This is the only game on the board where BOTH tops-of-order are engines** — Milwaukee +130 and the Dodgers +142 are the two best run differentials in baseball — facing two starters in the 1.25-1.28 WHIP band, neither of whom suppresses. Sasaki's 4.54 ERA is the softer half. Weather PENDING; re-read at 18:00. |
| 7 | PHI @ MIN | Nola **1.45** / Bradley 1.25 | **YRFI** | **54%** | ✓ **−110 BetMGM → no-vig 51.7%, +2.3pp — PROMOTED, lineups CONFIRMED** | Raw **YRFI 59%** → 54%. **Nola's 5.47 ERA / 1.45 WHIP is the worst qualified line on the board once Scherzer's stale aggregate is set aside**, and a 3-9 record across 24 GS says it is not a small-sample artifact. Bradley's 10.12 K/9 is the genuine counter and is why this is not higher. ⚠ **No park input applied** — Field of Dreams has essentially no park-factor history and guessing one would be inventing data. |
| 8 | CHC @ WSH | Gausman 1.26 / Cavalli 1.30 | **YRFI** | **52%** | _model-only_ | Raw **YRFI 57%** → 52%. Two starters either side of a 1.28 WHIP, neither suppressing, and **Chicago's 1-2-3 is the third-best on the board at +115**. Cavalli's 9.86 K/9 over 25 GS is the reason this is not higher — he misses bats even while allowing traffic. Weather PENDING at 11:00. |
| 9 | CIN @ CWS | Abbott **1.39** / Martin 1.33 | **YRFI** | **51%** | _model-only_ | Raw **YRFI 56%** → 51%. Two 1.3+ WHIPs with ERAs of 3.92 and 4.17 — the weakest pair on the board, and the same venue that hosted yesterday's worst read. ⚠ **Two counters keep it at a coin flip:** **the wind is 6 mph IN from left field** at 77°F, the only suppressing weather reading posted this morning, and **neither top-of-order is an engine** (CIN −78, CWS +41). ⚠ Recorded against ourselves: this game read **YRFI 54% yesterday and the first inning went 0-0** while Castillo threw seven shutout innings. |

---

## Tonight's reads — 2026-08-12 (15-game slate; model-only at 11:00 — the priced `totals_1st_1_innings` sweep is the 16:00 run)

> **✅ 8/11 CLOSED 10W-5L (67%) — the tracker's second-best slate on record.** All fifteen rows auto-settled off
> `linescore.innings[0]` by `nrfi_settle.py --apply` at session start; stamps verified present. **Record now
> 187-156** (NRFI 94-81 · YRFI 93-75). NRFI leans went **7-3**, YRFI leans **3-2** — both sides of the board
> contributed, which is the first slate in a week where that is true.
>
> **The −5pp YRFI correction's sixth graded slate: it flipped two reads and they went 1-1.** CLE @ DET (raw
> YRFI 58% → NRFI 53%) went **0-0 → NRFI ✅**; BAL @ MIN (raw YRFI 57% → NRFI 52%) went **2-0 → YRFI ❌**, and
> the 8/11 note had explicitly named BAL @ MIN as "the row I most expect the correction to be wrong on." Six
> graded slates now: 8/6 neutral, 8/7 neutral, 8/8 strongly positive, 8/9 strongly negative, 8/10 mildly
> negative, **8/11 neutral on the flips and strongly positive on the slate**. Runs to the ~10-slate review per
> the pre-registration; **not tapered, not extended.**
>
> ⭐ **The one promoted bet settled W** — PIT @ MIA NRFI −155 (no-vig 59.3%, +3.7pp) and the first inning went
> **0-0**. ⚠ It is recorded as a **correct read on an unbettable leg**: the game had reached Warmup by the time
> the 18:00 run reached it, so it was never actually available. The W is calibration, not money.
>
> ⚠ **Today's data traps, named before the numbers:** (1) **HOU @ SF is a Houston BULLPEN GAME** — Bryan King
> has **0 GS across 49.1 IP**, so the "probable" is an opener and the first inning is the least predictable one
> on the board (E5). (2) **CHC @ WSH — Jackson Kent has no 2026 StatsAPI pitching record**, so half that read
> is missing and the number is deliberately flattened rather than guessed (E4-equivalent). (3) **KC @ LAD —
> Daniel Lynch IV's 1.01 WHIP is relief data**: 1 GS across 47.2 IP. It is not used as a starter's WHIP.
>
> **No priced line pulled at 11:00** (the 1st-inning market is thin pre-lineup and the sweep is the 16:00
> duty), so all fifteen rows go to the ledger as model-only calibration. Raw model splits the board
> **7 NRFI / 8 YRFI**; the −5pp correction pulls it to **8 / 7**, reversing one read — **NYM @ ATL** — marked below.

| # | Matchup | SPs (WHIP) | Lean | TrueP | Price | Reasoning |
|---|---|---|---|---|---|---|
| 1 | PHI @ STL | **Wheeler 0.98** / Leahy 1.34 | **NRFI** | **58%** | _model-only_ | Strongest read of either kind today. **Wheeler's 0.98 WHIP and 10.77 K/9 over 19 GS are the best first-inning profile on the board** and strikeouts are the cleanest first-inning suppressant there is. Held under 60% by Leahy's 1.34 and by **94°F with the wind 6 mph out to right** at Busch — the one park condition posted this early, and it cuts against this read. |
| 2 | BOS @ TOR | Suarez 1.17 / Soriano 1.26 | **NRFI** | **56%** | _model-only_ | Two genuinely competent arms (3.32 and 3.24 ERA, 9.44 and 9.16 K/9) under a closed roof, so no weather input either way. Neither top-of-order is a standing engine — Boston are +81 and Toronto −56. |
| 3 | MIL @ SD | May 1.27 / **Ray 1.33** | **NRFI** | **55%** | _model-only_ | Petco, the most reliable first-inning suppressant venue in the National League. Ray's 3.24 ERA is the better half; May at 4.30 / 1.27 with 8.69 K/9 is the drag but still gets whiffs. Milwaukee's top-of-order (+131, best in baseball) is the live YRFI half. |
| 4 | CLE @ DET | **Griffin 1.11** / Valdez 1.37 | **NRFI** | **55%** | _model-only_ | Griffin's 1.11 over 23 GS and 133.1 IP is real and is the reason this reads NRFI at all; Valdez at 4.17 / 1.37 with a 7.28 K/9 gets his outs on the ground, which is less reliable in the first than whiffs. Detroit's +89 differential is the best in the division and is the counter. |
| 5 | PIT @ MIA | Mlodzinski 1.36 / Junk 1.36 | **NRFI** | **53%** | _model-only_ | Identical mediocre WHIPs, but **neither top-of-order is dangerous** — Pittsburgh +19 and Miami +17 are 17th and 18th by run differential — and loanDepot's roof takes weather out. Held to a coin-flip-plus because contact-dependent outs in the first are exactly what this tracker keeps getting burned on. |
| 6 | SEA @ NYY | **Miller 0.95** / Warren 1.37 | **NRFI** | **53%** | _model-only_ | Miller's **0.95 WHIP over 13 GS** is the second-best profile of the day. Held to a coin flip by the single biggest counter on the board: **the Yankee 1-2-3 is a standing YRFI engine at +85**, and Warren's 1.37 is the half they will be hitting against. |
| 7 | TB @ ATH | **Rasmussen 0.91** / Perkins 1.45 | **NRFI** | **53%** | _model-only_ | The board's best WHIP (0.91 over 22 GS, 9.41 K/9) against **the most hitter-friendly venue in the majors** and a 7.04 ERA opposing starter. ⚠ Genuinely two-sided: Rasmussen's half of the first is close to a lockout, Perkins' half is the softest on the slate, and Sutter Health amplifies whatever happens. Sits barely above the line for that reason, not from confidence. |
| 8 | NYM @ ATL | Thornton 1.07 / Mahle 1.36 | **NRFI** | **51%** | _model-only_ | ⚠ **FLIPPED READ.** Raw model says **YRFI 56%** — **Atlanta's top-of-order is the best on the board (+121)**, Mahle is at 4.83 / 1.36, and Thornton's tidy 1.07 comes with **7 GS across only 39.1 IP**, i.e. a short-role arm whose first inning is a larger share of his outing than usual. The −5pp correction takes that to 51% and reverses the lean. Marked for row-level grading; **this is the row I most expect the correction to be wrong on tonight.** |
| 9 | BAL @ MIN | Baz 1.32 / **Matthews 1.34** | **YRFI** | **52%** | _model-only_ | Raw **YRFI 57%**, corrected to 52%. Two 1.3+ WHIPs, and **Matthews at 5.23 ERA is the softest qualified starter of the early window** — the same reason the main build's Tier 1 is on Baltimore's moneyline. ⚠ Counter: **82°F with the wind 5 mph IN from centre** at Target Field, the only suppressing weather reading posted this morning. |
| 10 | HOU @ SF | **King — opener, 0 GS** / Houser 1.37 | **YRFI** | **51%** | _model-only_ | ⚠ **E5 — HOUSTON IS RUNNING A BULLPEN GAME.** Bryan King has **0 GS across 49.1 IP**, so the "probable" is an opener and an opener's first inning is the single least predictable one on any board — it cuts both ways and the number is flattened accordingly rather than pushed. **Oracle Park is the strongest suppressant venue on the slate** and is why this does not read higher. Re-read at 16:00. |
| 11 | CHC @ WSH | Peterson **1.50** / **Kent — no 2026 record** | **YRFI** | **51%** | _model-only_ | ⚠ **HALF THE READ IS MISSING.** Peterson at **5.35 ERA / 1.50 WHIP** is the worst qualified WHIP on the board and the Cubs' opponent-side case is strong on its own; but **Jackson Kent returns no 2026 StatsAPI pitching line at all**, so rather than guess a debut profile the number is deliberately flattened to near-coin-flip. Chicago's +109 top-of-order is the live half. Re-read at 16:00. |
| 12 | KC @ LAD | **Lynch — 1 GS / 47.2 IP** / Lauer 1.26 | **YRFI** | **52%** | _model-only_ | Raw **YRFI 57%** → 52%. ⚠ **The WHIP column is a trap here and is not being used:** Lynch's 1.01 is relief data across **1 start in 47.2 IP** — he is a swingman, not a starter, and this is E5-adjacent. The read rests on the two things that are real: **the Dodger 1-2-3 is a top-two YRFI engine (+140)** facing a **4.89 ERA / 5.58 K/9 Lauer**, whose low strikeout rate means his clean innings depend on contact luck. |
| 13 | CIN @ CWS | Lowder **1.48** / Castillo **1.41** | **YRFI** | **54%** | _model-only_ | Raw **YRFI 59%** → 54%. **Both starters are over 5.20 ERA and over 1.40 WHIP** — the second-worst pair on the slate and the only game where neither half suppresses. Rate Field's carry is a live first-inning HR risk. ⚠ Counter: neither top-of-order is an engine (CIN −73, CWS +36). |
| 14 | COL @ AZ | Feltner **1.45** / Kelly **1.47** | **YRFI** | **55%** | _model-only_ | Raw **YRFI 60%** → 55%. **The worst ERA pair on the board** (5.71 and 4.88) with two 1.45+ WHIPs and two low strikeout rates (6.48 and 6.00 K/9) — both arms need contact to go their way in the inning where they have the least feel. Chase Field with the roof shut is the only thing holding this down. |
| 15 | TEX @ LAA | Quantrill 1.19 / **Klassen 2.88 (8.2 IP)** | **YRFI** | **58%** | _model-only_ | Raw **YRFI 63%** → 58% — **the strongest YRFI of the day, and by the widest margin of any read this week.** George Klassen has a **2.88 WHIP across 8.2 IP in 3 GS**: that is roughly three baserunners per inning, the most extreme number in either direction on this board. ⚠ Two honest caveats: **8.2 innings is a tiny sample** (the E2 trap with the sign flipped), and **Quantrill's 3.56 / 1.19 half is genuinely competent**, so only one side of this game is soft. |

> **🔄 16:00 ET Build B — priced sweep (lineups locked).** The two strongest pre-game reads were pulled
> against a real `totals_1st_1_innings` market (2 credits). **Neither is promoted to a bet.**
>
> | Read | Model TrueP | Priced | no-vig | Edge | Verdict |
> |---|---|---|---|---|---|
> | **TEX @ LAA YRFI** (Over 0.5) | 58% | −136 / +106 FanDuel · best Over **−130** BetOnline | 54.3% | **+3.7** | ⛔ **model-only** — TrueP 58% lands in the **COOL + MARKET-SHADED 55-59 band** → zeroed; lineups also still PENDING |
> | **BOS @ TOR NRFI** (Under 0.5) | 56% | −160 / +130 Caesars | 58.6% | **−2.6** | ⛔ **negative edge** — the market has this richer than the model |
>
> **TEX @ LAA is the painful one:** it clears the raw +2pp gate at +3.7pp and dies purely on the band shade —
> the same mechanism that ran **3-1 against itself on 8/10 and again on 8/11**. Applied unchanged anyway,
> because one slate is far under the n≥20 belief bar and the governor governs EXPOSURE on recency, not belief.
> **BOS @ TOR is the cleaner decline:** the model said 56%, the market says 58.6%, and the honest read is that
> the market is right about two 3.2-ERA arms under a roof. All 15 rows stay model-only calibration.
>
> **No read was changed by the lineup lock** — no scratched or rested leadoff bat turned up in the seven
> confirmed pre-game line-ups. KC @ LAD and TEX @ LAA are still PENDING and belong to the 18:00 run.

---

## Tonight's reads — 2026-08-11 (15-game slate; model-only at 11:00 — the priced `totals_1st_1_innings` sweep is the 16:00 run)

> **✅ 8/10 CLOSED 4W-6L (40%)** — all ten rows auto-settled off `linescore.innings[0]` by `nrfi_settle.py --apply`
> at session start; stamps verified present. **Record now 177-151** (NRFI 87-78 · YRFI 90-73).
>
> **The −5pp YRFI correction was RIGHT on the row it actually changed.** 8/10's one flipped read was
> **BOS @ TOR** (raw YRFI 53% → corrected NRFI 52%) and the first inning went **0-0 → NRFI ✅**. The rest of the
> slate was unkind to the NRFI side the correction favours: NRFI leans **3-5**, YRFI leans **1-1**.
> **Five graded slates now: 8/6 neutral, 8/7 neutral, 8/8 strongly positive, 8/9 strongly negative, 8/10 mildly
> negative on the slate but positive on the flipped row.** It runs to the ~10-slate review per the
> pre-registration and is **not** tapered.
>
> ⚠ **Two rows are E4-gated tonight** — CHC @ WSH and HOU @ SF have **TBD probables** on StatsAPI at 11:14 ET.
> Both are written at a deliberately flat number off the one known starter and marked; the 16:00 run re-reads them.
> ⚠ **KC @ LAD carries a data trap worth naming: Blake Snell's whole 2026 line is 3.0 IP in one start.** His
> WHIP of 2.67 is noise, not information, so the read is built off the LAD top-of-order and his **rust**, not off
> the number.
>
> **No priced line pulled at 11:00** (the 1st-inning market is thin pre-lineup and the sweep is the 16:00 duty), so
> all fifteen rows go to the ledger as model-only calibration. Raw model splits the board **8 NRFI / 7 YRFI**; the
> −5pp correction pulls it to **10 / 5**, reversing two reads — **CLE @ DET** and **BAL @ MIN** — both marked.

| # | Matchup | SPs (WHIP) | Lean | TrueP | Price | Reasoning |
|---|---|---|---|---|---|---|
| 1 | PIT @ MIA | Skenes **1.12** / E. Pérez 1.13 | **NRFI** | **63%** | _model-only_ | Strongest read of either kind tonight. Two genuine front-line arms (11.24 and 9.93 K/9) in **loanDepot park**, and strikeouts are the cleanest first-inning suppressant there is. Neither top-of-order is dangerous — PIT and MIA are 21st and 15th by run differential. |
| 2 | MIL @ SD | Harrison **1.04** / Buehler 1.46 | **NRFI** | **59%** | _model-only_ | Petco, and Harrison's 1.04 WHIP / 11.27 K/9 is the best first-inning profile on the board. Held under 62% purely by **Buehler at 1.46** — the Brewers' 1-2-3 against a 5.07 ERA arm is the live YRFI half of this game. Same game the main build took an Under 7.5 in. |
| 3 | BOS @ TOR | Sandoval 1.67 / **Cease 1.04** | **NRFI** | **57%** | _model-only_ | Cease is the best arm on the slate (2.28 ERA, 13.11 K/9) and his half of the first is close to a lockout. ⚠ Discounted from a higher raw read because **Sandoval's 1.67 WHIP is the worst of any arm here with a real role** — the Toronto top-of-order is the whole YRFI case. |
| 4 | CIN @ CWS | Lodolo 1.47 / Burke **1.12** | **NRFI** | **54%** | _model-only_ | Burke (3.08 / 10.07 K/9) is quietly one of the better arms on the board; Lodolo's 1.47 is the drag. Neither top-of-order scares. Rate Field's carry is a first-inning HR risk. |
| 5 | PHI @ STL | Sánchez 1.22 / Pallante 1.22 | **NRFI** | **54%** | _model-only_ | Two identical WHIPs and two sub-3.65 ERAs. Sánchez at 2.65 / 10.46 K/9 is the better arm by a distance; Pallante's 6.53 K/9 means his clean innings come from weak contact, which is less reliable in the first than whiffs. |
| 6 | CLE @ DET | Bibee 1.13 / Anderson 1.29 | **NRFI** | **53%** | _model-only_ | ⚠ **FLIPPED READ #1.** Raw model says **YRFI 58%** — Anderson has **3 GS in 67.1 IP**, so he is a converted reliever whose first inning is the least predictable one he throws, and Detroit's +87 run differential is the best in the division. The −5pp correction takes that to 53% and reverses the lean to NRFI. Marked for row-level grading. |
| 7 | SEA @ NYY | Woo 1.12 / Weathers 1.22 | **NRFI** | **52%** | _model-only_ | Two tidy WHIPs, and Woo's 1.12 over 22 GS is real. Held to a coin flip by **the Yankee 1-2-3, which is a standing YRFI engine at +82 run differential** — the same reason this matchup rarely reads cleanly either way. |
| 8 | BAL @ MIN | Young 1.31 / Ober 1.22 | **NRFI** | **52%** | _model-only_ | ⚠ **FLIPPED READ #2.** Raw model says **YRFI 57%** — Ober at **4.45 ERA / 6.10 K/9** is the lowest-strikeout arm on the slate and gets to his outs via contact, and this exact pairing produced **14 runs** yesterday. The −5pp correction lands it at 52% NRFI. Marked; this is the row I most expect the correction to be wrong on. |
| 9 | NYM @ ATL | McLean 1.16 / M. Pérez 1.15 | **NRFI** | **51%** | _model-only_ | Both WHIPs are fine and both ERAs are sub-3.55. ⚠ Sits barely above the line because **Atlanta's top-of-order is the best on the board** (+117 run differential) and it **put up five runs in the first inning of this same series yesterday** — the model is not allowed to forget that. |
| 10 | CHC @ WSH | Imanaga **1.09** / **TBD (E4)** | **NRFI** | **51%** | _model-only_ | ⚠ **E4-GATED.** Imanaga's 1.09 / 3.60 over 23 GS would carry this to the high 50s on its own; with **Washington's starter unannounced**, half the read is missing and the number is deliberately flattened to near-coin-flip rather than guessed. Re-read at 16:00. |
| 11 | COL @ AZ | Sugano 1.26 / Bratt 1.52 | **YRFI** | **52%** | _model-only_ | Raw lean **YRFI 57%**, corrected to 52%. **Bratt has 6 GS / 27.2 IP and a 1.52 WHIP**; Sugano's 5.10 K/9 is the second-lowest here, so both arms need contact to go their way. Chase Field with the roof shut is the only thing holding this down. |
| 12 | HOU @ SF | H. Brown 1.24 / **TBD (E4)** | **YRFI** | **52%** | _model-only_ | ⚠ **E4-GATED**, and the gate matters more here than at CHC@WSH: **San Francisco ran a bullpen game in this same series yesterday**, and an opener's first inning is the single least predictable one on any board. Oracle Park pulls the other way. Flattened and marked; re-read at 16:00. |
| 13 | TEX @ LAA | Bradford 1.62 (**4.1 IP**) / R. Johnson **1.60** | **YRFI** | **56%** | _model-only_ | Raw **YRFI 61%**, corrected to 56%. **The worst WHIP pair on the slate by some way.** Johnson is at **7.11 ERA / 1.60 WHIP over 10 GS** — the worst qualified starter tonight — and Bradford has thrown **4.1 innings all season**, so his first inning is effectively a first inning of the year. |
| 14 | KC @ LAD | Wacha 1.15 / **Snell — 3.0 IP all season** | **YRFI** | **57%** | _model-only_ | Raw **YRFI 62%**, corrected to 57%. ⚠ **The WHIP column is a trap here and is not being used:** Snell's 2.67 is three innings of data. The read is built on the two things that are real — **his first start back carries live rust and a hard pitch cap**, and **the Dodger 1-2-3 is a top-two YRFI engine in baseball** (+139 run differential) facing a 7.00 K/9 Wacha. |
| 15 | TB @ ATH | Martinez **1.10** / Barnett 1.38 | **YRFI** | **58%** | _model-only_ | Raw **YRFI 63%**, corrected to 58% — **the strongest YRFI of the night**, and the same game the main build's Tier 1 Over 8.5 is in. **Sutter Health Park is the most hitter-friendly venue in the majors** and **Barnett (5.56 ERA, 2 GS in 34.0 IP) is a swingman starting**, which is the exact profile that gives up a first-inning crooked number. ⚠ Counter-signal: **Martinez at 2.65 / 1.10 is a real starter**, so only one half of this game is soft — the same caveat the main build logged. |

---

## Tonight's reads — 2026-08-10 (10-game slate; model-only at 11:00 — the priced `totals_1st_1_innings` sweep is the 16:00 run)

> **✅ 8/9 CLOSED 10W-10L (50%)** — the five rows still open at last night's Build C lock were auto-settled off
> `linescore.innings[0]` by `nrfi_settle.py --apply` at session start (DET@SF **W**, TB@SEA **L**, LAD@AZ **L**,
> CLE@CWS **L**, HOU@SD **L**) and the stamps are verified present. **Record now 173-145** (NRFI 84-73 · YRFI 89-72).
>
> ⚠ **The −5pp YRFI correction had its worst full slate yet, and the direction of the failure is the one already
> flagged.** 8/9 finished with the **YRFI leans 5-1** and the **NRFI leans 5-9**. The correction subtracts 5pp from
> YRFI leans only, so it systematically converts marginal YRFI reads into NRFI ones — and on 8/9 every one of the
> five late settles that came in was a game the correction had pushed toward NRFI, four of which went YRFI.
> **Four graded slates now: 8/6 raw-vs-corrected neutral, 8/7 neutral, 8/8 strongly positive, 8/9 strongly negative.**
> Per the pre-registration it keeps running to the ~10-slate review and is **not** tapered after a bad day — the same
> discipline that stopped it being tapered after 8/8's good one.
>
> ⚠ **Ratchet status, today:** the raw model splits this board **7 NRFI / 3 YRFI**; the correction pulls it to
> **8 / 2**, reversing exactly one read — **BOS @ TOR**, from YRFI 53% to a nominal NRFI 52%. That row is marked so
> the correction is graded on the reads it actually flips, not only on the slate total.
>
> **No priced line pulled at 11:00** (the 1st-inning market is thin pre-lineup and the sweep is the 16:00 duty), so
> all ten rows go to the ledger as model-only calibration.

| # | Matchup | SPs (WHIP) | Lean | TrueP | Price | Reasoning |
|---|---|---|---|---|---|---|
| 1 | MIL @ SD | Henderson **0.90** / Mize 1.09 | **NRFI** | **62%** | _model-only_ | Strongest read of either kind today, and it is the same game the main build took an Under 7.0 in. Petco plus **the two lowest WHIPs facing each other anywhere on the slate**; Henderson has walked almost nobody (0.90 WHIP over 10 GS) and Mize's 1.09 is real despite one 8-ER blowup. |
| 2 | KC @ LAD | Skubal **0.92** / Cameron 1.29 | **NRFI** | **59%** | _model-only_ | Skubal is the best arm on the board and Cameron has thrown 23.0 IP / 1 ER across his last three. The only thing holding this under 62% is the Dodger top-of-order, which is a genuine YRFI engine even against elite pitching. |
| 3 | HOU @ SF | Wesneski 1.29 / Tidwell 1.18 | **NRFI** | **57%** | _model-only_ | Oracle Park, the most run-suppressing venue on this slate. ⚠ Discounted from a higher raw read because **Tidwell has 1 GS in 9 appearances** — a converted reliever's first inning is the least predictable one he throws. |
| 4 | TEX @ LAA | Gore 1.24 / Detmers **1.10** | **NRFI** | **56%** | _model-only_ | Two high-K arms (9.79 and 10.47 K/9) in a neutral park. Strikeouts are the cleanest first-inning suppressant there is; neither top-of-order is fearsome. |
| 5 | NYM @ ATL | Scott 1.26 / Elder 1.20 | **NRFI** | **54%** | _model-only_ | Both sub-3.70 ERA with tidy WHIPs. Held down from the high-50s purely by Atlanta's 1-2-3, which is the best top-of-order on the board (+120 run differential, 8-2 L10). |
| 6 | COL @ AZ | Hughes 1.18 / **Soroka — 7 weeks absent** | **NRFI** | **54%** | _model-only_ | The WHIP pair says 58%; **Soroka has not pitched in the majors since 6/19 and `currentTeam` returns Reno Aces**, so the first inning carries live rust risk that the season line cannot see. Discounted to 54% for exactly that. |
| 7 | BAL @ MIN | Rogers 1.24 / Kremer 1.32 | **NRFI** | **52%** | _model-only_ | Two ordinary WHIPs, neutral park, neither top-of-order dangerous. Close to a coin-flip and priced as such. |
| 8 | BOS @ TOR | Gray 1.15 / Taillon 1.39 | **NRFI** | **52%** | _model-only_ | ⚠ **THE FLIPPED READ.** Raw model says **YRFI 53%** — Rogers Centre, and Taillon has not completed five innings since June. The pre-registered **−5pp YRFI correction** takes that to 48%, so the nominal lean becomes NRFI 52%. **Gray's own first innings are the argument for the flip being right; the park and Taillon are the argument against it.** Marked so the correction is graded on this row specifically. |
| 9 | PHI @ STL | **Painter 1.57** / Dobbins 1.30 | **YRFI** | **51%** | _model-only_ | Painter's 1.57 WHIP is the worst on the board outside the TB@ATH pair, and he is the arm the main build's Tier-1 leg is priced against. Raw lean **YRFI 56%**; the −5pp correction lands it at 51%. |
| 10 | TB @ ATH | Peralta 1.52 / **Lopez 1.63** | **YRFI** | **57%** | _model-only_ | The day's clearest YRFI shape: **both starters over a 5.37 ERA**, the two worst WHIPs on the slate, in **the most hitter-friendly park in the majors**. Raw lean **YRFI 62%**, corrected to 57% — still the strongest YRFI of the day, and the same game the main build took an Over 10.0 in. |

---


## Tonight's reads — 2026-08-09 (15-game slate; **11:00 run treated as the LOCK run** — Sunday getaway board, 10 of 15 first pitches precede the scheduled 16:00 run)

> **✅ 8/8 CLOSED 11W-3L (79%)** — 14 rows auto-settled off the 1st-inning line score by
> `nrfi_settle.py --apply` at session start; stamps verified present. **Record now 167-136**
> (NRFI 82-67 · YRFI 85-69). The best single slate this tracker has recorded.
>
> **The −5pp YRFI correction, graded on its second full slate: POSITIVE, but read it carefully.**
> 8/8 was called **4 YRFI / 11 NRFI** *after* the correction and came back **11-3** — however the raw
> model split that slate 8-7, so most of the winning reads were NRFI calls the correction had *created*.
> That is one good slate for a one-way ratchet, not evidence the ratchet is right. Per the
> pre-registration it keeps running for ~10 slates and is graded at the end, not after a hot day.
>
> ⚠ **The ratchet flagged on 8/8 is still live and is now tagged at the row level.** Today the raw model
> splits **7 YRFI / 8 NRFI**; the correction pulls that to **6 / 9**, reversing exactly one read —
> **ATL @ NYY**, from YRFI 55% to a nominal NRFI 51%. That row is marked in the table so the correction
> can be graded on the reads it actually flips rather than only on the slate total.

| # | Matchup | SPs (WHIP) | Lean | TrueP | Price | Reasoning |
|---|---|---|---|---|---|---|
| 1 | TOR @ PHI | Bieber 1.68 / Luzardo 1.16 | **YRFI** | **61%** | _model-only_ | **The board's worst WHIP (1.68) in the board's best hitter park with 9 mph blowing out to the short porch.** Bieber is at **4.6 IP/start across 8 GS** post-injury — a profile that concedes traffic early. Held under 65% because Luzardo (1.16, 10.80 K/9, 8.0 IP / 0 ER last out) is the strongest counterweight of any YRFI read here. Raw 66%. [−5pp applied] |
| 2 | COL @ STL | Lorenzen 1.85 / McGreevy 1.20 | **YRFI** | **58%** | _model-only_ | **Lorenzen's 1.85 WHIP is the worst mark of any starter working today** (23 GS, 6.94 ERA) and Busch is **93°F with 10 mph out to LF**, the hottest reading on the slate. Capped by McGreevy's 1.20 and by Colorado's dire road top. Raw 63%. [−5pp applied] |
| 3 | ATH @ BOS | Ginn 1.21 / Miller 1.34 (opener) | **YRFI** | **55%** | _model-only_ | Asymmetric by design: **Boston is opening with Erik Miller (0 GS in 35.0 IP)**, so the ATH half of the inning faces a fresh 12.60 K/9 arm — that side argues NRFI. The read rests entirely on **Ginn's 1.21 meeting a BOS top on a 9-1 L10 at Fenway with 11 mph out to RF.** Raw 60%. [−5pp applied] |
| 4 | CIN @ WSH | Singer 1.43 / Lord 1.20 | **YRFI** | **52%** | _model-only_ | Singer's **1.43 over 22 GS** is the soft half; Washington counter with **Brad Lord, 1 GS across 59.0 IP** — effectively a long man starting, fresh but unpriceable as a starter. 6 mph crosswind adds nothing. Thin. Raw 57%. [−5pp applied] |
| 5 | CHC @ KC | Boyd 1.22 / Dobnak 1.19 | **YRFI** | **51%** | _model-only_ | **91°F with 13 mph out to CF, the strongest wind of the day**, and Chicago's top is the hotter of the two. But both WHIPs are good (1.22 / 1.19) and **Kauffman's centre field is the deepest in the league** — the wind is blowing to the one direction the park already swallows. Raw 56%. [−5pp applied] |
| 6 | LAA @ MIA | G. Rodriguez 1.59 / Gusto 1.36 | **YRFI** | **53%** | _model-only_ | **The worst ERA on the board (7.24) and a 1.59 WHIP** on one side, 1.36 on the other — the softest matched pair of the slate. Discounted hard because the **roof is closed** (zero weather help) and these are two of the weakest tops in baseball (45-72 and 59-59). Raw 58%. [−5pp applied] |
| 7 | DET @ SF | Melton 0.91 / Webb 1.11 | **NRFI** | **63%** | _model-only_ | **Strongest read of either kind today.** The best matched WHIP pair on the board — **Melton 0.91 / 1.58 ERA** over 12 GS and Webb 1.11 — in **Oracle Park**, and neither top is dangerous (DET and SF are both mid-table offensively). Nothing in the matchup argues the other way. |
| 8 | MIN @ MIL | Prielipp 1.31 / Misiorowski 0.73 | **NRFI** | **61%** | _model-only_ | **Misiorowski's 0.73 WHIP is the best in MLB** (1.63 ERA, 13.82 K/9, 21 GS) and American Family's **roof is closed**. Held off the top spot only because Prielipp's 1.31 is a genuine soft half — the MIN side of the inning is the whole risk. |
| 9 | TB @ SEA | Seymour 1.13 / Hancock 1.07 | **NRFI** | **60%** | _model-only_ | **T-Mobile Park, the most run-suppressing park in MLB**, with a clean 1.13 / 1.07 pair. This read won on 8/7 and again on 8/8; the arms are different but the park and the shape are the same, and unlike the game total (which the market moved to 7.5) the 1st-inning read has not been repriced against us. |
| 10 | LAD @ AZ | Wrobleski 1.07 / E. Rodriguez 1.24 | **NRFI** | **58%** | _model-only_ | Closed dome at Chase, two starters with real command lines (Wrobleski **3.31 / 1.07 over 18 GS**, E-Rod **2.71 / 1.24 over 23 GS**). Capped by the Dodgers' top, which is still the most dangerous 1-2-3 on this board even at 3-7 over their last ten. |
| 11 | NYM @ PIT | Manaea 1.38 / J. Jones 1.11 | **NRFI** | **56%** | _model-only_ | **PNC is a pitcher park** and both tops are poor — NYM are 51-67 (−53) and PIT 58-61 on a 3-7 L10. Jones' 1.11 (9.96 K/9) carries the read; Manaea's 1.38 is the reason it is not 62%. |
| 12 | BAL @ TEX | Povich 1.34 / Rocker 1.33 | **NRFI** | **54%** | _model-only_ | Closed dome at Globe Life and two nearly identical ordinary WHIPs (1.34 / 1.33) against two ordinary tops. ⚠ **Povich has only 4 GS / 25.1 IP**, so half the pair is a thin sample — the number is written near the coin flip rather than dressed up. |
| 13 | CLE @ CWS | Cantillo 1.47 / D. Martin 1.31 | **NRFI** | **53%** | _model-only_ | The one **wind-IN** game on the board — **11 mph in from RF at Rate Field** — which is what drags a hitter park's read under. Working against it: Cantillo's **1.47 is the second-worst WHIP** among today's real starters. Park and wind cancel; the pitching says YRFI. |
| 14 | HOU @ SD | Javier 1.68 / **TBD** | **NRFI** | **52%** | _model-only_ | ⚠ **Lowest-conviction read on the slate and flagged as such — San Diego's starter is unannounced (E4).** Half the matchup is genuinely unpriceable, and Javier's **1.68 WHIP / 6.59 ERA over 5 GS** argues the other way. The number is **Petco Park alone**, written at near-coin-flip. Re-read at 18:00 once the probable posts. |
| 15 | ATL @ NYY | Holmes 1.34 / Schlittler 0.95 | **NRFI** | **51%** | _model-only_ | ⚠ **A FLIPPED READ, and the ratchet flag from 8/8 is exactly why it is being called out.** The raw model has this **YRFI 55%** — 90°F with 8 mph out to the Yankee Stadium porch, and the two best offences on the board (ATL 70-47, NYY 66-51) — but the −5pp YRFI correction pulls it to 50% and tips it to a nominal NRFI 51%. **Schlittler's 0.95 is the best WHIP of any starter here and his last start was 3.0 IP / 5 ER.** This row is logged specifically so the correction's one-way ratchet is graded on a read it reversed, not just on reads it left alone. |

**Pre-registered split: 6 YRFI · 9 NRFI** (raw model 7-8 before the correction; one read reversed).
All 15 rows go to the ledger as model-only. ⚠ **No real `totals_1st_1_innings` line was pulled at 11:00
and none will clear the gate unpriced** — on this getaway board the 16:00 run is post-first-pitch for
ten of these games, so the honest status is **model-only / NO BET for the early slate**, with the 18:00
run able to price only HOU@SD, DET@SF, LAD@AZ and TB@SEA.

---

## Tonight's reads — 2026-08-08 (15-game slate; model-only at 11:00 — priced sweep is the 16:00 run)

> **✅ 8/7 CLOSED 8W-7L (53%)** — YRFI leans **4-4**, NRFI leans **4-3**. All 15 rows auto-settled off the
> 1st-inning line score by `nrfi_settle.py --apply` at session start. Record now **156-132**.
>
> **The −5pp YRFI correction, graded on its first full slate: NEUTRAL.** It was applied to 8/7 as a
> pre-registered experiment and the day came back **8-7 with the two sides splitting evenly (YRFI 4-4,
> NRFI 4-3)** — no evidence for it, none against. Both reads it *flipped* (TOR@PHI, CIN@WSH) went
> **1-1**. Per the pre-registration it keeps running for ~10 slates; one neutral day changes nothing.
>
> ⚠ **But a structural side-effect is now visible and is worth flagging before it becomes a habit.**
> The correction subtracts 5pp from every YRFI lean and nothing from any NRFI lean, so it does not
> merely *rebalance* the split — it **ratchets it toward NRFI on every slate**. On 8/6 the raw model
> split 8 YRFI / 3 NRFI; on 8/7 the correction pulled that to 8/7; **today it pulls a raw 8-7 all the
> way to 4 YRFI / 11 NRFI.** A calibration correction that keeps moving the split in one direction is
> indistinguishable from a directional bet on NRFI, which is not what it was registered to be. Logged
> now, not acted on — the honest resolution is at the graded-experiment review, and pre-emptively
> tapering it after one neutral day would be exactly the result-reading the doctrine forbids.

| # | Matchup | SPs (WHIP) | Lean | TrueP | Price | Reasoning |
|---|---|---|---|---|---|---|
| 1 | TOR @ PHI | Scherzer 1.63 / Nola 1.44 | **YRFI** | **63%** | _model-only_ | **Strongest read of either kind.** The two worst WHIPs among today's non-blind arms, in **Citizens Bank Park** (hitter park), and Scherzer is averaging **3.8 IP across 8 GS** — a profile that gets hit early. Survives the −5pp correction comfortably (raw 68%). [−5pp applied] |
| 2 | HOU @ SD | Lambert 1.13 / King 1.20 | **NRFI** | **61%** | _model-only_ | **Petco Park** — the strongest pitcher park on tonight's board — plus the best matched WHIP pair (1.13/1.20) and two mid-grade tops. This is the same shape as 8/7's TB@SEA read, which won. |
| 3 | COL @ STL | Freeland 1.49 / Liberatore 1.49 | **YRFI** | **61%** | _model-only_ | Identical 1.49 WHIPs — the joint-worst pair on the slate. Held back only by Busch (mild pitcher park) and COL's dire road top. ⚠ Freeland's last start was a **9.0 IP CG, 1 ER** — one start against a 6.81 season. [−5pp applied] |
| 4 | LAA @ MIA | Ureña 1.25 / Alcantara 1.20 | **NRFI** | **59%** | _model-only_ | Two quality arms (2.54 / 3.68 ERA) in a **retractable-roof park**, against two of the weakest tops in the league (LAA 45-71, MIA 58-59). Zero weather variance. |
| 5 | TB @ SEA | Jax 1.21 / Kirby 1.28 | **NRFI** | **58%** | _model-only_ | **T-Mobile Park**, the most run-suppressing park in MLB, roof available. Won this exact read on 8/7 (Rasmussen/Gilbert, 61%). Slightly softer tonight — Kirby's 1.28 is the weaker half. |
| 6 | ATL @ NYY | Sale 1.02 / Cole 1.10 | **NRFI** | **57%** | _model-only_ | **The best WHIP pair on the board** (Sale 2.08 ERA / 11.00 K9; Cole 3.42). Discounted hard from that because **both tops are loaded** — ATL are 70-46 (+120) and NYY 65-51 (+82), the two best offences here. Quality vs quality. |
| 7 | ATH @ BOS | Jump 1.47 / Bennett 1.01 | **YRFI** | **57%** | _model-only_ | Asymmetric: Bennett's 1.01 is elite but Jump's 1.47 faces a **BOS top on a 9-1 L10 / 9-game win streak** at Fenway. The Over needs only the bottom half of the matchup to break. [−5pp applied] |
| 8 | LAD @ AZ | Yamamoto 0.88 / Pfaadt 1.26 | **NRFI** | **57%** | _model-only_ | **Yamamoto's 0.88 is the best WHIP on the slate** and Chase is a closed dome. Capped by AZ's top (7-3 L10) and by LAD being on a **7-game losing streak** — a cold top helps NRFI, which is the rare case where the streak argues *for* the read. |
| 9 | BAL @ TEX | Bradish 1.36 / deGrom 1.14 | **NRFI** | **55%** | _model-only_ | deGrom (1.14, **10.69 K/9**) is the best half of any 1st inning tonight; Globe Life is a closed dome. Bradish's 1.36 is the whole reason this isn't 60%. |
| 10 | NYM @ PIT | Stock 0.60 / Chandler 1.41 | **NRFI** | **54%** | _model-only_ | **PNC is a pitcher park** and both tops are poor (NYM 51-66 / −44, PIT 57-61 on L10 2-8). ⚠ **Stock's 0.60 is a 5.0 IP sample across 1 GS** — effectively unpriced; the read rests on the two weak offences, not on him. |
| 11 | CIN @ WSH | Burns 1.10 / Alvarez 1.45 | **NRFI** | **54%** | _model-only_ | Burns is the class of the matchup (2.35 ERA, **10.39 K/9**, 13-1) but Alvarez's 1.45 over 8 GS is the soft half and WSH's top is live. Thin. |
| 12 | MIN @ MIL | Bradley 1.24 / Gasser 1.17 | **NRFI** | **54%** | _model-only_ | Retractable roof, two ordinary-but-competent arms, two ordinary tops. A genuine coin flip that the dome nudges under. |
| 13 | CHC @ KC | Holmes 1.10 / Lugo 1.39 | **YRFI** | **53%** | _model-only_ | **CHC's top is the hottest on the board** (L10 7-3, W5, beat KC 6-4 last night) against Lugo's 1.39, and Kauffman's gaps turn contact into extra bases. Holmes' 1.10 is what keeps this from being 60%. [−5pp applied] |
| 14 | CLE @ CWS | Williams 1.04 / Kay 1.35 | **NRFI** | **53%** | _model-only_ | Gavin Williams (1.04, **11.53 K/9**) is a legitimate NRFI arm, but **Rate Field is a hitter park** and Kay's 1.35 is exposed. The park is doing most of the work against the read. |
| 15 | DET @ SF | Jobe **n/a** / Roupp 1.29 | **NRFI** | **52%** | _model-only_ | ⚠ **Lowest-conviction read on the slate and flagged as such.** Jackson Jobe has **zero 2026 MLB pitching data** (`stats: []` from StatsAPI) — half this matchup is genuinely unpriceable. The number is **Oracle Park alone**, so it is written at near-coin-flip rather than dressed up. |

**Pre-registered split: 4 YRFI · 11 NRFI** — see the ratchet flag above; the raw model split 8-7 before
the correction. All 15 rows go to the ledger as model-only; the **16:00 run prices them** against a real
`totals_1st_1_innings` line, and only then can any clear the +2pp gate.

---

## Tonight's reads — 2026-08-07 (15-game slate; model-only at 11:00 — priced sweep is the 16:00 run)

> **✅ 8/6 CLOSED 6W-5L** (YRFI leans **5-3**, NRFI leans **1-2**). All 11 rows auto-settled off the
> 1st-inning line score. Record now **148-125**.
>
> ⚠ **THE −5pp YRFI CORRECTION IS APPLIED THIS RUN — as a pre-registered graded experiment, and the
> evidence for it just got weaker.** Yesterday's 16:00 sweep produced the third straight confirmation
> that our YRFI leans price 5-9pp above the market, and the standing recommendation was to apply a
> −5pp correction starting today. **But 8/6 then finished with YRFI leans 5-3 and NRFI leans 1-2** —
> the opposite of what the bias hypothesis predicts. I am applying the correction anyway, because
> abandoning a pre-registered adjustment after one favourable day is exactly the result-reading the
> doctrine forbids, and because the market-disagreement evidence (3 sightings, 4-for-4 on 8/6) is
> independent of one night's outcomes. **Grade it on the ledger, not on 8/6.**
>
> Method: derive raw P(YRFI) from both SPs' 1st-inning quality + both 1-2-3 trios + park, subtract
> **5pp** from the YRFI side, then the lean is whichever side finishes above 50%. Two games flipped
> from a raw YRFI lean to a thin NRFI lean as a direct result (TOR@PHI, CIN@WSH) and one more sits on
> the line (HOU@SD) — that flip is the correction working, and it is what makes it measurable.
>
> **Weather is PENDING on all 15 games at 11:00** (pre-game), so no wind/temp input is in any read.
> **E4 gate:** CHC@KC (CHC starter TBD) and DET@SF (SF starter TBD) are half-blind — flagged below.

| # | Matchup | Starters (ERA/WHIP) | Lean | TrueP | Line | Why (1st-inning read) |
|---|---------|---------------------|------|-------|------|------------------------|
| 1 | TB @ SEA | Rasmussen 2.91/**0.93** / Gilbert 3.46/**0.99** | **NRFI** | **61%** | _model-only_ | **Strongest read of either kind on the board.** The best matched WHIP pair on the slate (0.93 / 0.99) in **T-Mobile, the most run-suppressing park in the majors**, roof available so no weather variance. Rasmussen's last two starts are 7.0 IP / 0 ER / 9 K and 6.0 IP / 0 ER / 10 K; Gilbert went 7.0 IP last out. Both tops are middling (TB +41, SEA −14). Nothing in this game argues for early traffic. |
| 2 | DET @ SF | Montero 3.17/**1.00** / **TBD** | **NRFI** | **58%** | _model-only_ | Montero's **1.00 WHIP** is the second-best number on the board, at **Oracle Park** — extreme pitcher park, cold marine air on a night game. ⚠ **E4-GATED:** the SF starter is unannounced, so half this read is blind; the number reflects Montero + park only and would move on a bad SF arm. |
| 3 | LAA @ MIA | Klassen **11.57/3.64** / Phillips 3.53/1.35 | **YRFI** | **57%** | _model-only_ | **Highest YRFI on the board and it is one number: Klassen's 3.64 WHIP** — roughly 3.6 baserunners per inning across his 4.2 IP / 2 GS. If he takes the mound the bottom of the 1st is traffic. Held to 57% (post-correction) by two real caps: the sample is 4.2 IP, and **MIA's top is mid** (RDiff 0), so traffic ≠ runs. LAA's top is the second-worst offence on the slate, which flattens the other half. |
| 4 | LAD @ AZ | Sasaki 4.64/1.30 / **Kelly 5.04/1.49** | **YRFI** | **56%** | _model-only_ | Two of the four worst WHIPs on the slate in the same game (1.30 / **1.49**) at **Chase Field**, and the board agrees — this carries the joint-highest total (9.5). Kelly's 1.49 faces the **best top-of-order on the board**; Sasaki's 1.30 faces a competent AZ trio. Symmetric equity, which is why it survives the correction better than the one-sided reads. |
| 5 | ATH @ BOS | Perkins **6.72/1.40** / Tolle 3.30/1.15 | **YRFI** | **54%** | _model-only_ | Perkins (6.72 ERA / 1.40 WHIP) opens against a **BOS top that is 9-1 in its last 10 on a 7-game win streak (+77)** at Fenway. But the equity is almost entirely one-sided: Tolle's 1.15 faces **the worst road offence in baseball** (ATH 45-70, **L10 1-9**, −157). One live half only → 54%, not 60%. |
| 6 | BAL @ TEX | Baz 3.86/1.37 / Eovaldi 4.31/1.21 | **NRFI** | **54%** | _model-only_ | **The board's lowest total (7.5/7.0)** and a dome, which is the cleanest market corroboration of an NRFI lean on the slate. Neither arm is elite but neither is a WHIP disaster, and **both tops are weak** (BAL −33, TEX −33). The suppression here is offence-driven rather than pitching-driven. |
| 7 | ATL @ NYY | **Mahle 5.13/1.39** / Fried 3.12/0.99 | **YRFI** | **53%** | _model-only_ | Mahle's 1.39 WHIP faces a strong NYY top (+81) — genuine 1st-inning equity. The counterweight is large: **Fried's 0.99 WHIP** is one of the three best on the board and he caps the ATL half even against the hottest lineup in the NL (70-45, **W8**). Half a live game → a thin lean. |
| 8 | CLE @ CWS | Messick 2.57/1.06 / **Schultz 5.82/1.38** | **YRFI** | **52%** | _model-only_ | Purely asymmetric: **all** the equity is the bottom of the 1st, where Schultz (5.82/1.38) faces the CLE top, in a hitter park. Messick's 1.06 is the third-best WHIP on the slate and should handle the CWS trio. One-sided reads keep underperforming this tracker — hence a thin lean, not a loud one. |
| 9 | MIN @ MIL | **Matthews 5.22/1.31** / Drohan 3.48/1.17 | **YRFI** | **52%** | _model-only_ | Matthews' 1.31 against **the best team in baseball's top** (72-43, +141) is the equity. Drohan's 1.17 against a weak MIN top (−35) is the suppressant, and the dome removes weather. Near coin-flip after the correction. |
| 10 | COL @ STL | **Feltner 5.75/1.46** / Leahy 3.44/1.33 | **YRFI** | **51%** | _model-only_ | Feltner's 1.46 WHIP is the third-worst on the board and STL's top will see it. Pulled back hard by **Busch being a pitcher park** and by COL's road top being one of the two worst offences in the NL (45-70, −108) — Leahy's 1.33 does not need to be good to hold it. |
| 11 | CHC @ KC | **TBD** / Lynch IV 1.96/0.93 — **0 GS in 46.0 IP** | **YRFI** | **51%** | _model-only_ | ⚠ **The least knowable game on the board and it should be read as such.** CHC's starter is unannounced (**E4**), and KC's "starter" Daniel Lynch IV has **zero starts in 46.0 IP** — this is a **bullpen game / opener (C4)**, so his shiny 1.96/0.93 is relief-context and does not describe a first inning against the CHC top. The board carries the **joint-highest total (9.5)**. Thin lean, lowest confidence of the 15. |
| 12 | TOR @ PHI | Soriano 3.29/1.25 / Wheeler 2.49/**0.91** | **NRFI** | **51%** | _model-only_ | ⚠ **FLIPPED BY THE CORRECTION** (raw read was YRFI 54%). Wheeler's 0.91 WHIP / 10.80 K/9 is the single best 1st-inning arm on the slate. Offsetting it: **CBP is a hitter park**, Soriano's 1.25 is ordinary against a PHI top, and — flagged loudly — **Wheeler's last two starts are 3.0 IP / 5 ER and 2.0 IP / 0 ER**, an unexplained short-outing pattern that is a start-length flag but says little about a *first* inning. Thinnest of the NRFI leans. |
| 13 | CIN @ WSH | Petty 4.50/1.23 (2 GS) / Cavalli 3.52/1.29 | **NRFI** | **51%** | _model-only_ | ⚠ **FLIPPED BY THE CORRECTION** (raw read was YRFI 56%). Two ordinary WHIPs and two ordinary tops (CIN −60, WSH +10); the market's 9.0 total is the highest-uncertainty number of the slate. **Petty has 2 GS / 30.0 IP**, so his 1.23 is barely a sample. Genuine coin flip — logged for calibration, not conviction. |
| 14 | HOU @ SD | **Blanco 7.36/1.30 (3 GS)** / Ray 3.08/1.29 | **NRFI** | **51%** | _model-only_ | Sits exactly on the correction line (raw YRFI 56% → 51% the other way). Blanco's 7.36 ERA over **14.2 IP / 3 GS** is a post-layoff sample, not an established profile, and his 1.30 WHIP is unremarkable. **Petco is the strongest pitcher park in the NL** and Ray's 1.29 faces a HOU top with a −25 run diff. Park carries this, narrowly. |
| 15 | NYM @ PIT | Thornton 2.88/1.05 (6 GS) / Mlodzinski 3.15/1.31 | **NRFI** | **56%** | _model-only_ | **PNC is a pitcher park** and both tops are poor — NYM are 50-66 (−46) and PIT 57-60 on **L10 2-8**. Thornton's 1.05 is good but thin (34.1 IP); Mlodzinski's 1.31 is the softer half. The read is driven mostly by **two weak offences**, which is the shape that has been winning for the NRFI side. |

**Pre-registered split: 8 YRFI · 7 NRFI** — versus 8/6's 8-3. **The correction did what it was designed to
do structurally**: it balanced the split and flipped two reads without touching the underlying model.
Whether it was *right* is a question for the ledger, and 8/6's 5-3 YRFI result is already one point
against it. All 15 rows go to the ledger as model-only; the **16:00 run prices them** against a real
`totals_1st_1_innings` line and only then can any clear the +2pp gate.

---

## Tonight's reads — 2026-08-06 (11-game slate; model-only at 11:00 — priced sweep is the 16:00 run)

> 11:00 ET morning reads — full 11-game slate, one model-lean per game with a pre-registered TrueP.
> **Three games are early** (LAA@BAL 12:35, ATH@CIN 12:40, NYM@CLE 13:10 ET) and will be Live before
> Build B, so their leans stay **model-only calibration rows** — they cannot be priced at 16:00.
> Weather is live for those three and PENDING for the other eight. **All 11 rows go to the ledger.**
>
> ⚠ **Standing correction applied this run:** 8/5 finished with **9 of 15 first innings scoreless**
> and NRFI leans beating YRFI leans 6-1, on top of the 16:00 finding that our YRFI lean ran 8-10pp
> above the market on three separate games. Today's YRFI leans are therefore written **2pp lower than
> the raw WHIP model produces**, and the NRFI leans unchanged. This is a directional correction to a
> known bias, pre-registered here so it is measurable — not a re-derivation after the fact.

| # | Matchup | Starters (ERA/WHIP) | Lean | TrueP | Line | Why (1st-inning read) |
|---|---------|---------------------|------|-------|------|------------------------|
| 1 | SD @ AZ | Buehler 5.18/1.45 / Drake 4.85/1.46 | **YRFI** | **61%** | _model-only_ | **Strongest YRFI on the board.** The two worst WHIPs on the slate are in the same game (1.45 / 1.46) at Chase Field. Drake is 3 GS / 13.0 IP — a rookie with no established clean-first pattern — and Buehler's last four outings are 2.0/5.2/5.1/4.1 IP, i.e. he is being hit early. Both tops are competent. |
| 2 | CWS @ BOS | Castillo 5.06/1.39 / Suarez 3.15/1.16 | **YRFI** | **58%** | _model-only_ | Asymmetric but the vulnerable half is the one facing the hot bats: Castillo (5.06/1.39, 3-9) opens against a BOS top that is **9-1 in its last 10 with a 7-game win streak** at Fenway. Suarez caps the other half. Nearly all the YRFI equity is the bottom of the 1st. |
| 3 | MIA @ ATL | Junk 4.58/1.33 / M. Pérez 3.24/1.17 | **YRFI** | **57%** | _model-only_ | Junk's 1.33 WHIP against the hottest top-of-order in baseball (ATL 69-45, **W7**, L10 8-2, +113 run diff) at Truist. Same shape as the CWS@BOS read and one tier milder because Pérez is the better stabiliser. |
| 4 | WSH @ PHI | Mikolas 5.67/1.35 / C. Sánchez 2.61/1.20 | **YRFI** | **56%** | _model-only_ | Mikolas (5.67 ERA, **4.58 K/9** — a pure contact-manager) faces the PHI top in a hitter park. Cuts the other way hard: Sánchez is the best arm on the slate (2.61/1.20, 10.45 K/9, 11 K last out) and WSH's top is weak. Equity is one-sided, hence only 56%. |
| 5 | LAA @ BAL | R. Johnson 7.63/1.59 / B. Young 3.31/1.29 | **YRFI** | **56%** | _model-only_ | **Worst single starter line on the board:** Ryan Johnson 7.63 ERA / **1.59 WHIP**, with 13 ER over his last two starts (7.2 IP). A 1.59 WHIP means baserunners in the 1st. Live weather supports it — **88°F, 8 mph out to CF**. Held at 56% only because the LAA top is the second-worst offence on the slate (43-71, −79). |
| 6 | TOR @ CHC | Cease 2.41/1.08 / Peterson 5.52/1.48 | **YRFI** | **55%** | _model-only_ | The most one-sided game on the board. Peterson's **1.48 WHIP** vs a TOR top is real first-inning traffic; Cease (2.41 ERA, **13.12 K/9**, 1.08 WHIP) is the single most likely arm on the slate to post a clean 1st. Wrigley wind PENDING — the swing factor, and the reason this is not higher. |
| 7 | PIT @ MIL | Ashcraft 3.96/1.16 / May 4.38/1.28 | **YRFI** | **53%** | _model-only_ | Genuinely close to a coin flip. May's 1.28 WHIP against the best team in baseball's top (MIL 71-43, +138) is the equity; Ashcraft's 1.16 is the suppressant. Dome, so no weather variance. Mild lean only. |
| 8 | ATH @ CIN | Barnett 4.85/1.31 / Abbott 3.91/1.39 | **YRFI** | **53%** | _model-only_ | GABP and Abbott's 1.39 WHIP argue Over, but two things pull it back to near-even: **Barnett is a converted reliever** (1 GS in 29.2 IP; his log is 1-2 IP outings until 3.1 and 5.0 in his last two), so the ATH half may be an opener facing the top once and briefly — and **ATH's road offence is the worst in baseball** (−156 run diff, 1-9 L10). |
| 9 | DET @ SEA | Valdez 4.41/1.39 / B. Miller 2.80/0.92 | **NRFI** | **57%** | _model-only_ | **Miller's 0.92 WHIP is the best number on the slate**, in the most run-suppressing park in the majors, under a roof. Valdez's 1.39 is the one-sided risk — and it is a real one (0.2 IP / 6 ER on 7/21) — which is why this is 57% and not 62%. |
| 10 | MIN @ KC | Ober 4.45/1.23 / Wacha 3.51/1.16 | **NRFI** | **56%** | _model-only_ | Two sub-1.25 WHIPs in the biggest outfield in the majors, against two of the weakest tops on the board (MIN −36, KC −102 run diff). Wacha's last out was 6.0 IP / 1 ER / 7 K. Nothing here argues for early traffic. |
| 11 | NYM @ CLE | McLean 3.29/1.12 / F. Griffin 3.06/1.07 | **NRFI** | **60%** | _model-only_ | **Strongest NRFI on the board and the cleanest read of either kind.** The two best matched WHIPs on the slate (1.12 / 1.07) in a pitcher's park; Griffin is 12-3 with a 3.06 ERA and McLean carries 10.60 K/9. Both tops are below average. This is the same shape that went 6-1 for the NRFI side yesterday. |

**Pre-registered NRFI/YRFI split for the day: 8 YRFI · 3 NRFI.** ⚠ Worth flagging honestly — that split
is itself the bias the correction above is meant to fight, and the model still produced it. If the
NRFI side outperforms again tonight, the 2pp shade is too small and the next step is a structural
re-weight, not another nudge.

---

## Tonight's reads — 2026-08-05 (15-game slate; **UPDATED 16:00 ET Build B — 5 reads now priced on a real `totals_1st_1_innings` line; 2 clear +2pp**)

> **16:00 ET UPDATE (Build B).** Lineups are locked, so the priced sweep ran: `totals_1st_1_innings`
> pulled for the five strongest pre-game reads (5 credits). Result — **2 bet-grade, 3 shaded out by
> their own size.** The four early games (TOR@HOU, LAD@CHC, SF@TEX, TB@COL) are now Live and
> unpriceable; their 11:00 model leans stand as calibration rows only.
>
> | Game | 11:00 lean | TrueP after 16:00 | Best price | No-vig | Edge | Verdict |
> |---|---|---|---|---|---|---|
> | **PIT @ MIL** | NRFI 60% | **60%** (unchanged) | **Under 0.5 −145 @Caesars** | **56.0%** | **+4.0** | ✅ **BET-GRADE** |
> | **MIN @ KC** | YRFI 58% | **54%** (`market_disagrees −4`) | **Over 0.5 −110 @BetMGM** | **50.0%** | **+4.0** | ✅ **BET-GRADE** |
> | ATH @ CIN | YRFI 63% | → market 52.6% | Over 0.5 −125 @BetMGM | 52.6% | 0.0 | ✗ shaded |
> | WSH @ PHI | YRFI 61% | → market 52.4% | Over 0.5 −125 @BetMGM | 52.4% | 0.0 | ✗ shaded |
> | CWS @ BOS | NRFI 60% | → market 52.0% | Under 0.5 −125 @Caesars | 52.0% | 0.0 | ✗ shaded |
>
> **Why three of five shaded themselves out.** Each showed an 8–10pp gap between the 11:00 model lean
> and the market's no-vig, which fires `market_disagrees −4pp`; the shaded number then lands in the
> **PULSE-shaded 55-59 band**, which resets TrueP to the market outright. **PIT@MIL survived precisely
> because its gap (4.0pp) was too small to trigger the shade** — the mechanism rewards agreeing with
> the market, which is the point. This is also a calibration finding about our own model: the
> WHIP-driven YRFI lean is systematically higher than the market's, and this tracker's own history
> (6/11, 6/22, 7/25) already recorded that the YRFI side is where the misses cluster.
>
> ⚠ **PIT@MIL carries one un-modelled risk:** Kyle Harrison has not pitched since **7/08 (28 days)**,
> and rust argues for early traffic — i.e. against the NRFI. The 60% was pre-registered at 11:00 with
> that flag already written, so it is not being revised now; but it is the reason this is a 60% and
> not a 64%.


> 11:00 ET morning reads — full 15-game slate. TOR@HOU / LAD@CHC / SF@TEX / TB@COL are early
> (14:10-15:11 ET first pitch); the other 11 are 18:35 ET or later. All games `Preview/Scheduled` at
> build time. One model-lean per game with a pre-registered TrueP, derived from both SPs' WHIP /
> start-quality plus park. **Weather PENDING for every park except Wrigley** (overcast, 78F, 9 mph
> variable — no usable direction). No `totals_1st_1_innings` market was pulled this run (quota
> discipline: the 16:00 run owns the priced prop sweep), so every read below is **model-only / no bet**.

| Game (away SP / home SP) | Lean | TrueP | Why |
|---|---|---|---|
| ATH @ CIN (J.Lopez / Lowder) | **YRFI** | **63%** | Day's strongest. **Both WHIPs are the worst matched pair on the board — Lopez 1.67, Lowder 1.52** — at GABP, the slate's most hitter-friendly non-Coors park. |
| WSH @ PHI (Irvin / Painter) | **YRFI** | **61%** | Two arms 2 starts into post-IL returns: Painter 6.72/1.61, Irvin 5.56/1.32, at Citizens Bank Park. Traffic in the 1st is the base case. |
| CWS @ BOS (Burke / Gray) | **NRFI** | **60%** | The two best matched ERAs on the slate (2.93 / 3.04) and two sub-1.20 WHIPs. Fenway caps it at 60 rather than higher. |
| PIT @ MIL (Skenes / Harrison) | **NRFI** | **60%** | The two lowest WHIPs on the board (1.11 / 1.08) in a dome. ⚠ Harrison has not pitched since 7/08 — rust is the one-sided risk. |
| TB @ COL (Martinez / Sugano) | **YRFI** | **58%** | Coors. Sugano 4.47/1.26 is the YRFI half; Martinez (2.77/1.10) genuinely caps it, which is why 58 and not 62. |
| MIN @ KC (Kremer / Cameron) | **YRFI** | **58%** | Kremer 6.50/1.36 over 7 GS is the worst ERA among tonight's starters; Kauffman's size is the only brake. |
| TOR @ HOU (Taillon / H.Brown) | **YRFI** | **57%** | Wholly one-sided: Taillon 5.92/1.36 vs a HOU top; Brown (3.42) caps the other half. |
| NYM @ CLE (C.Scott / Bibee) | **NRFI** | **57%** | Two competent arms (2.99/1.24, 3.81/1.15) in a pitcher's park vs two below-average tops. |
| SD @ AZ (Mize / Bratt) | **YRFI** | **57%** | **Bratt 5.23 / 1.84 WHIP over 20.2 IP** is the equity; Mize (2.70/0.99) is the best arm on the slate and shuts the other half down. |
| STL @ NYY (Pallante / Warren) | **YRFI** | **56%** | Warren 1.36 WHIP at Yankee Stadium; Pallante is a contact-manager (6.52 K/9) so STL put balls in play early. |
| LAA @ BAL (Detmers / T.Rogers) | **NRFI** | **55%** | Two mid arms (4.03/1.10, 4.27/1.28) but the two weakest offences of the late slate (LAA RDiff −76, BAL −33). |
| MIA @ ATL (E.Perez / Elder) | **NRFI** | **55%** | Perez 3.44/1.10 is the reason; Elder (3.84/1.25) vs a hot ATL-facing MIA top is the risk. |
| SF @ TEX (Whisenhunt / Bradford) | **YRFI** | **55%** | ⚠ **E4-adjacent: Bradford has NO 2026 game data** — unverifiable. Whisenhunt (6.63 / **1.74 WHIP**, 4 GS) alone carries the lean; capped at 55 for the unknown half. |
| LAD @ CHC (Lauer / Imanaga) | **NRFI** | **54%** | Imanaga 1.07 WHIP is elite in the 1st; Lauer 1.19 is fine. Held to 54 because both tops are top-5 offences and Wrigley wind is unreadable. |
| DET @ SEA (D.Anderson / Woo) | **NRFI** | **54%** | T-Mobile, the most run-suppressing park in the majors. ⚠ **DET is effectively a bullpen game** — Anderson has 2 GS in 63.2 IP — so the "starter" half is really an opener, which caps this at 54. |

**Slate split:** 7 NRFI / 8 YRFI leans. **0 priced reads** — no 1st-inning market pulled this run;
all 15 rows go to the ledger as model-only calibration.

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

| 8/4 | LAA @ BAL (G.Rodriguez/Povich) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | **16:00 REVISED (E4 LIFTED, was 56% w/ TBD):** BAL's arm is **Cade Povich — 5.12/1.34 but only 3 GS and last logged 5/07**, i.e. a return with real start-length uncertainty. Two bad arms, but two weak offences (LAA RDiff −74, BAL −35) and **7 mph wind IN from CF** cap it. Nudged +1pp only; the priced Over 0.5 doesn't clear the gate |
| 8/4 | ATH @ CIN (Ginn/Singer) | YRFI | 56% | _model-only_ | **L** (1st 0-0 → NRFI) | GABP hitter park + Singer 1.43 WHIP, offset by the worst road offense on the slate (ATH .244/.325, RDiff −154) |
| 8/4 | NYM @ CLE (Manaea/Cantillo) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | Both WHIPs ≥1.34 (Cantillo 1.45) = traffic game; capped by NYM's .231/.301 top and a neutral park |
| 8/4 | **WSH @ PHI (Palmquist/Luzardo)** | **YRFI** | **60%** | **Over 0.5 −115 (BetMGM)** — no-vig 50.5%, **+9.5pp** | **W** (1st 0-1 → YRFI) | **16:00 REVISED + PROMOTED (was YRFI 57% model-only on Littell).** ⚠ **E3 SP CHANGE: Littell → Carson Palmquist**, who is materially worse *and* materially shorter — **7.31 ERA / 1.63 WHIP**, last six outings **3.0, 0.1, 1.2, 1.1, 1.1, 2.0 IP** (C4-adjacent opener/bulk profile) — facing PHI's top three at CBP. Luzardo (3.57/1.19) still caps the WSH half, which is why 60% and not higher. ✅ gate cleared |
| 8/4 | STL @ NYY (Dobbins/Weathers) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | Yankee Stadium + NYY top vs a 4-start rookie (1.34 WHIP); STL's 18%-K top puts balls in play vs Weathers |
| 8/4 | **CWS @ BOS (Martin/Sandoval)** | **YRFI** | **56%** | **Over 0.5 +102 (FanDuel)** — no-vig 48.6%, **+7.4pp** | **W** (1st 0-6 → YRFI) | ✅ gate cleared. Sandoval 1.58 WHIP, 4 starts / 19 IP into a return, at Fenway vs a BOS side on W5/L10 8-2. Shaded 60%→56% on CWS's 24% K vs LHP and the market's YRFI-side price |
| 8/4 | MIA @ ATL (Gusto/Holmes) | YRFI | 59% | _model-only_ | **L** (1st 0-0 → NRFI) | Gusto 5.31/1.44 vs the hottest top on the slate (ATL 67-45, W5, +108). Strongest un-priced YRFI |
| 8/4 | **MIN @ KC (J.Ryan/Dobnak)** | **NRFI** | **55%** | **Under 0.5 −104 (FanDuel)** — no-vig 48.8%, **+6.2pp** | **L** (1st 0-2 → YRFI) | ✅ gate cleared, market on the other side. Two sub-1.20 WHIPs + two weak tops (.313/.319 OBP) at Kauffman; shaded 57%→55% because Dobnak is a 26-IP/4.85-K/9 sample the market may be reading as short |
| 8/4 | **PIT @ MIL (Jones/Henderson)** | **NRFI** | **58%** | **Under 0.5 −129 (BetRivers)** — no-vig 54.7%, **+3.3pp** | **W** (1st 0-0 → NRFI) | ✅ gate cleared. Cleanest premise of the day: the slate's two best WHIPs (1.02, 0.91) in a dome vs PIT's 23%-K top. Market agrees → smallest edge of the four |
| 8/4 | LAD @ CHC (Skubal/Assad) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Skubal 0.91 WHIP elite, Assad competent — but two strong tops (CHC .333/.355 OBP) and **Wrigley wind PENDING**, the one park a wind reading would move |
| 8/4 | SF @ TEX (Tidwell/Gore) | YRFI | 55% | _model-only_ | **W** (1st 0-2 → YRFI) | ⚠ C4-adjacent: Tidwell has **0 GS in 12 IP** (swingman/opener question). Gore's 4.77 ERA is the firmer signal. Dome |
| 8/4 | TOR @ HOU (Yesavage/Wesneski) | YRFI | 58% | _model-only_ | **L** (1st 0-0 → NRFI) | Wesneski: **5.2 IP all season, 1 GS**, 1.59 WHIP — rust + short leash, effectively a HOU bullpen game; Yesavage steadier, so equity is one-sided |
| 8/4 | **TB @ COL (Peralta/Hughes)** | **YRFI** | **61%** | **Over 0.5 −130 (FanDuel)** — no-vig 54.9%, **+6.1pp** | **W** (1st 0-1 → YRFI) | ✅ gate cleared, day's strongest. Peralta 1.48 WHIP / 4.5 IP-per-start vs the slate's most contact-heavy top (TB 18-19% K, .264) at Coors. **Yesterday's 22-run game on a wind-IN reading is why no suppression is applied** |
| 8/4 | SD @ AZ (Vásquez/E.Rodriguez) | YRFI | 55% | _model-only_ | **W** (1st 3-0 → YRFI) | Vásquez 1.47 WHIP is the YRFI half; E-Rod (2.48 ERA, best on board) caps it. Dome |
| 8/4 | **DET @ SEA (Melton/Hancock)** | **NRFI** | **59%** | **Under 0.5 −125 (FanDuel)** — no-vig 52.4%, **+6.6pp** | **W** (1st 0-0 → NRFI) | **16:00 REVISED + PROMOTED (was NRFI 55%, E4-gated).** E4 lifted: DET's arm is **Troy Melton — 1.75 ERA / 0.93 WHIP, 6.09 IP/start over 11 GS**, opposite **Hancock 3.26 / 1.04**. The two lowest WHIPs on the board in the most run-suppressing park in the majors. Shaded 61%→59% because Hancock carries a 1.2-IP outing in the log and both lineups were still PENDING at 16:08. ✅ gate cleared |

| 8/5 | ATH @ CIN (J.Lopez/Lowder) | YRFI | → market 52.6% *(11:00 lean 63%)* | -125 (BetMGM) — no-vig 52.6% | **W** (1st 1-0 → YRFI) | **16:00 Build B — PRICED, 0.0pp, NO BET.** Worst matched WHIP pair on the board (1.67 / 1.52) at GABP, but a **10.4pp** model-vs-market gap fires `market_disagrees -4` → 59% → PULSE-shaded 55-59 band → TrueP reset to market outright |
| 8/5 | WSH @ PHI (Irvin/Painter) | YRFI | → market 52.4% *(11:00 lean 61%)* | -125 (BetMGM) — no-vig 52.4% | **W** (1st 1-0 → YRFI) | **16:00 Build B — PRICED, 0.0pp, NO BET.** Same mechanism (8.6pp gap → 57% → shaded). Note this game IS the Tier-1 Over 9.5: the full-game total clears the gate while the 1st-inning slice does not — a useful reminder they are different bets |
| 8/5 | CWS @ BOS (Burke/Gray) | NRFI | → market 52.0% *(11:00 lean 60%)* | -125 (Caesars) — no-vig 52.0% | **L** (1st 0-1 → YRFI) | **16:00 Build B — PRICED, 0.0pp, NO BET.** Same mechanism (8.0pp gap → 56% → shaded). Best matched ERAs on the slate (2.93 / 3.04), but Fenway plus a 6.8% hold leave nothing |
| 8/5 | PIT @ MIL (Skenes/Harrison) | **NRFI** | **60%** | **-145 (Caesars)** — no-vig 56.0% | **W** (1st 0-0 → NRFI) | **16:00 Build B — PRICED, +4.0pp, BET-GRADE.** (11:00 model-only lean: NRFI 60%.) Two lowest WHIPs on the board (1.11 / 1.08) in a dome. The 4.0pp model-vs-market gap is UNDER the 5pp `market_disagrees` trigger, so the pre-registered TrueP stands; band 60-64 is unshaded (11-5 / 69% in the pulse window). ⚠ Harrison hasn't pitched since 7/08 (28 d) — rust is the one-sided risk, already written into the 60% at 11:00 |
| 8/5 | TB @ COL (Martinez/Sugano) | YRFI | 58% | _model-only_ | **W** (1st 2-0 → YRFI) | Coors + Sugano 4.47/1.26; Martinez 2.77/1.10 genuinely caps the other half. |
| 8/5 | MIN @ KC (Kremer/Cameron) | **YRFI** | **54%** | **-110 (BetMGM)** — no-vig 50.0% | **L** (1st 0-0 → NRFI) | **16:00 Build B — PRICED, +4.0pp, BET-GRADE.** (11:00 model-only lean: YRFI 58%; `market_disagrees -4` applied on an 8pp gap → 54%.) Kremer 6.50 ERA / 1.36 WHIP over 7 GS is tonight's worst starter line, vs KC — a fades.md C1 contact-heavy lineup. The shaded 54% still clears a dead-even 50.0% market. Band 50-54 unshaded |
| 8/5 | TOR @ HOU (Taillon/H.Brown) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | One-sided: Taillon 5.92/1.36; Hunter Brown 3.42 caps the TOR half. |
| 8/5 | NYM @ CLE (C.Scott/Bibee) | NRFI | 57% | _model-only_ | **W** (1st 0-0 → NRFI) | Two competent arms in a pitcher's park vs two below-average tops. |
| 8/5 | SD @ AZ (Mize/Bratt) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | Bratt 5.23 / 1.84 WHIP is the equity; Mize (2.70/0.99) shuts the other half. |
| 8/5 | STL @ NYY (Pallante/Warren) | YRFI | 56% | _model-only_ | **L** (1st 0-0 → NRFI) | Warren 1.36 WHIP at Yankee Stadium; Pallante a 6.52-K/9 contact-manager. |
| 8/5 | LAA @ BAL (Detmers/T.Rogers) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Two mid arms but the two weakest offences of the late slate. |
| 8/5 | MIA @ ATL (E.Perez/Elder) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Eury Perez 3.44/1.10 is the reason; Elder is the risk half. |
| 8/5 | SF @ TEX (Whisenhunt/Bradford) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | E4-adjacent: Bradford has NO 2026 data. Whisenhunt 6.63 / 1.74 WHIP alone carries it. |
| 8/5 | LAD @ CHC (Lauer/Imanaga) | NRFI | 54% | _model-only_ | **L** (1st 1-1 → YRFI) | Imanaga 1.07 WHIP elite in the 1st; capped by two top-5 offences + unreadable Wrigley wind. |
| 8/5 | DET @ SEA (D.Anderson/Woo) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | T-Mobile suppression, but DET is effectively a bullpen game (Anderson 2 GS / 63.2 IP). |
| 8/6 | SD @ AZ (Buehler/Drake) | YRFI | 61% | _model-only_ — **16:00 market no-vig 52.4%** (BetMGM O-125/U-102) → **model +8.6pp above market; NO BET** | **W** (1st 1-0 → YRFI) | Two worst WHIPs on the slate in one game (1.45/1.46) at Chase; Drake 3 GS, Buehler being hit early. |
| 8/6 | CWS @ BOS (Castillo/Suarez) | YRFI | 58% | _model-only_ — **16:00 market no-vig 50.5%** (BetMGM O-115/U-110) → **model +7.5pp above market; NO BET** | **L** (1st 0-0 → NRFI) | Castillo 5.06/1.39 opens vs a BOS top on a 7-game win streak at Fenway; Suarez caps the other half. |
| 8/6 | MIA @ ATL (Junk/M.Perez) | YRFI | 57% | _model-only_ — **16:00 market no-vig 51.6%** (BetMGM O-120/U-105) → **model +5.4pp above market; NO BET** | **L** (1st 0-0 → NRFI) | Junk 1.33 WHIP vs the hottest top in baseball (ATL W7, +113) at Truist. |
| 8/6 | WSH @ PHI (Mikolas/C.Sanchez) | YRFI | 56% | _model-only_ — **16:00 market no-vig 50.0%** (FanDuel O-113/U-113) → **model +6.0pp above market; NO BET** | **W** (1st 0-2 → YRFI) | Mikolas 5.67/4.58 K9 contact-manager in a hitter park; Sánchez (best arm on the slate) makes it one-sided. |
| 8/6 | LAA @ BAL (R.Johnson/B.Young) | YRFI | 56% | _model-only_ | **L** (1st 0-0 → NRFI) | Worst starter line on the board (7.63/1.59, 13 ER last 2 starts); 88°F, 8 mph out to CF. LAA top is weak. |
| 8/6 | TOR @ CHC (Cease/Peterson) | YRFI | 55% | _model-only_ | **W** (1st 1-0 → YRFI) | Peterson 1.48 WHIP is the equity; Cease (13.12 K/9) the likeliest clean 1st on the slate. Wrigley wind PENDING. |
| 8/6 | PIT @ MIL (Ashcraft/May) | YRFI | 53% | _model-only_ | **W** (1st 0-1 → YRFI) | Near coin-flip: May 1.28 vs the MIL top is the equity, Ashcraft 1.16 the suppressant. Dome. |
| 8/6 | ATH @ CIN (Barnett/Abbott) | YRFI | 53% | _model-only_ | **W** (1st 0-1 → YRFI) | GABP + Abbott 1.39 argue Over, but Barnett is a converted reliever (1 GS/29.2 IP) and ATH's offence is the worst in baseball. |
| 8/6 | DET @ SEA (Valdez/B.Miller) | NRFI | 57% | _model-only_ | **L** (1st 3-0 → YRFI) | Miller's 0.92 WHIP is the best number on the slate, in the top run-suppressing park, under a roof. Valdez 1.39 is the risk half. **18:00 hand-settle: DET hung 3 in the top of the 1st off Miller — the second NRFI lean of the day built on the best WHIP number on the board, and the second to lose.** |
| 8/6 | MIN @ KC (Ober/Wacha) | NRFI | 56% | _model-only_ — **16:00 market no-vig 50.0%** (FanDuel O-113/U-113); TrueP 56% lands in the **⛔ COOLed + SHADED 55-59 band** → reset to market, **NO BET** | **W** (1st 0-0 → NRFI) | Two sub-1.25 WHIPs at Kauffman vs two of the weakest tops on the board. |
| 8/6 | NYM @ CLE (McLean/F.Griffin) | NRFI | 60% | _model-only_ | **L** (1st 0-2 → YRFI) | Best matched WHIP pair on the slate (1.12/1.07) in a pitcher's park; both tops below average. Cleanest read of either kind. |

---

| 8/7 | TB @ SEA (Rasmussen/Gilbert) | NRFI | 61% | _model-only_ | **W** (1st 0-0 → NRFI) | Best matched WHIP pair on the slate (0.93/0.99) at T-Mobile, the most run-suppressing park in MLB, roof available. Strongest read of either kind. |
| 8/7 | DET @ SF (Montero/TBD) | NRFI | 58% | _model-only_ | **L** (1st 1-2 → YRFI) | Montero 1.00 WHIP at Oracle, cold marine night air. ⚠ E4 — SF starter unannounced, half the read is blind. |
| 8/7 | LAA @ MIA (Klassen/Phillips) | YRFI | 57% | _model-only_ | **W** (1st 1-0 → YRFI) | Klassen's **3.64 WHIP** over 4.2 IP is the loudest single number on the board; capped by a 4.2 IP sample and MIA's mid top. [−5pp YRFI correction applied] |
| 8/7 | LAD @ AZ (Sasaki/Kelly) | YRFI | 56% | _model-only_ | **L** (1st 0-0 → NRFI) | Two of the four worst WHIPs on the slate (1.30/1.49) at Chase; joint-highest total. Symmetric equity. [−5pp applied] |
| 8/7 | NYM @ PIT (Thornton/Mlodzinski) | NRFI | 56% | _model-only_ | **L** (1st 1-0 → YRFI) | PNC pitcher park + two weak tops (NYM −46, PIT L10 2-8). Offence-driven suppression. |
| 8/7 | ATH @ BOS (Perkins/Tolle) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | Perkins 6.72/1.40 vs a BOS top 9-1 L10 at Fenway, but equity is one-sided — ATH is the worst road offence in baseball. [−5pp applied] |
| 8/7 | BAL @ TEX (Baz/Eovaldi) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Board's lowest total (7.5/7.0) in a dome; both tops weak. Market corroborates. |
| 8/7 | ATL @ NYY (Mahle/Fried) | YRFI | 53% | _model-only_ | **L** (1st 0-0 → NRFI) | Mahle 1.39 vs a strong NYY top is the equity; Fried's 0.99 caps the other half. [−5pp applied] |
| 8/7 | CLE @ CWS (Messick/Schultz) | YRFI | 52% | _model-only_ | **W** (1st 2-0 → YRFI) | All equity is the bottom of the 1st (Schultz 5.82/1.38) in a hitter park; Messick 1.06 caps the top. [−5pp applied] |
| 8/7 | MIN @ MIL (Matthews/Drohan) | YRFI | 52% | _model-only_ | **W** (1st 0-1 → YRFI) | Matthews 1.31 vs the best top in baseball; Drohan 1.17 vs a weak MIN top. Dome. [−5pp applied] |
| 8/7 | COL @ STL (Feltner/Leahy) | YRFI | 51% | _model-only_ | **L** (1st 0-0 → NRFI) | Feltner 1.46 is the 3rd-worst on the board; pulled back by Busch (pitcher park) + COL's dire road top. [−5pp applied] |
| 8/7 | CHC @ KC (TBD/Lynch IV) | YRFI | 51% | _model-only_ | **W** (1st 0-1 → YRFI) | ⚠ Least knowable game: CHC SP TBD (E4) and Lynch IV has **0 GS in 46.0 IP** = bullpen game (C4). Joint-highest total. [−5pp applied] |
| 8/7 | TOR @ PHI (Soriano/Wheeler) | NRFI | 51% | _model-only_ | **W** (1st 0-0 → NRFI) | ⚠ FLIPPED by the correction (raw YRFI 54%). Wheeler 0.91 is the best 1st-inning arm on the slate; CBP hitter park offsets. Wheeler's last two starts 3.0 and 2.0 IP — start-length flag. |
| 8/7 | CIN @ WSH (Petty/Cavalli) | NRFI | 51% | _model-only_ | **L** (1st 0-3 → YRFI) | ⚠ FLIPPED by the correction (raw YRFI 56%). Two ordinary WHIPs, two ordinary tops; Petty has 2 GS. Genuine coin flip. |
| 8/7 | HOU @ SD (Blanco/Ray) | NRFI | 51% | _model-only_ | **W** (1st 0-0 → NRFI) | Sits exactly on the correction line. Blanco's 7.36 is a 14.2 IP post-layoff sample; Petco carries this narrowly. |

| 8/11 | PIT @ MIA (Skenes 1.12 / E. Pérez 1.13) | NRFI | 63% | **−155 (BetMGM) → no-vig 59.3%, Edge +3.7pp** | **W** (1st 0-0 → NRFI) | ⭐ **PROMOTED TO A BET at 16:00** — the first read in this tracker to clear the +2pp bar. Strongest read of the night: two front-line arms (11.24 / 9.93 K9) at a **roof-closed** loanDepot (wind 0); neither top-of-order dangerous. The 63% was pre-registered here at 11:00 **before any 1st-inning line was pulled**. ⚠ Five books posted, spread **−155 (BetMGM) to −189 (BetOnline)** — a 34-point gap, so the shop is worth more than the model. ¼-Kelly 1.41u. |
| 8/11 | MIL @ SD (Harrison **1.04** / Buehler 1.46) | NRFI | 59% | _model-only_ | **W** (1st 0-0 → NRFI) | Petco; Harrison's 1.04 / 11.27 K9 is the best 1st-inning profile on the board. Held under 62% by Buehler's 1.46. |
| 8/11 | BOS @ TOR (Sandoval 1.67 / **Cease 1.04**) | NRFI | 57% | _model-only_ | **W** (1st 0-0 → NRFI) | Cease (2.28, 13.11 K9) is the slate's best arm; discounted for Sandoval's 1.67 WHIP over 24.0 IP. |
| 8/11 | CIN @ CWS (Lodolo 1.47 / Burke 1.12) | NRFI | 54% | _model-only_ | **L** (1st 0-1 → YRFI) | Burke 3.08 / 10.07 K9 carries it; Lodolo's 1.47 is the drag. |
| 8/11 | PHI @ STL (Sánchez 1.22 / Pallante 1.22) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Identical WHIPs, both sub-3.65 ERA. Sánchez the better arm; Pallante's 6.53 K9 means contact-dependent outs. |
| 8/11 | CLE @ DET (Bibee 1.13 / **bullpen game**) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | ⚠ **FLIPPED #1, and the 16:00 gamelog CONFIRMS why.** Raw YRFI 58% (Anderson has 3 GS in 67.1 IP; DET +87 RDiff) → corrected to NRFI 53%. **E5 check at 16:00: Anderson's last twelve appearances are all relief (1.0–3.2 IP) — Detroit is running an opener/bullpen game**, so the 11:00 suspicion off the odd GS/IP ratio was right. Read HELD at 53% rather than moved: an opener's 1st inning is the least predictable on the board and cuts both ways. Row-level grading. |
| 8/11 | SEA @ NYY (Woo 1.12 / Weathers 1.22) | NRFI | 52% | _model-only_ | **W** (1st 0-0 → NRFI) | Two tidy WHIPs held to a coin flip by the Yankee 1-2-3. |
| 8/11 | BAL @ MIN (Young 1.31 / Ober 1.22) | NRFI | 52% | _model-only_ | **L** (1st 2-0 → YRFI) | ⚠ **FLIPPED #2.** Raw YRFI 57% (Ober 4.45 / 6.10 K9, lowest-K arm on the slate; this pairing went 14 runs yesterday) → corrected to NRFI 52%. The row I most expect the correction to miss. |
| 8/11 | NYM @ ATL (McLean 1.16 / M. Pérez 1.15) | NRFI | 51% | _model-only_ | **W** (1st 0-0 → NRFI) | Both fine; barely above the line because ATL's top-of-order put 5 on the board in the 1st yesterday. |
| 8/11 | CHC @ WSH (Imanaga 1.09 / **Irvin 1.29**) | NRFI | 53% | _model-only_ | **L** (1st 0-2 → YRFI) | ✅ **E4 LIFTED at 16:00** — WSH probable posted: **Jake Irvin, 5.37 ERA / 1.29 WHIP, 13 GS / 62.0 IP**. 51% (flattened) → **53%**: Imanaga's 1.09 is the best half, Irvin's 1.29 is mediocre rather than bad. ⚠ **C3** — Irvin has no start between 5/23 and 7/30; last two went 5.0 and 5.1 IP, so his 1st-inning sample is thin. Nationals Park is untagged, so no bettable side either way. |
| 8/11 | COL @ AZ (Sugano 1.26 / Bratt 1.52) | YRFI | 52% | _model-only_ | **W** (1st 0-2 → YRFI) | Raw YRFI 57% → 52%. Bratt 6 GS / 27.2 IP; Sugano 5.10 K9. Roof-shut Chase is the only suppressant. |
| 8/11 | HOU @ SF (H. Brown 1.24 / **Whisenhunt 1.84**) | YRFI | 56% | _model-only_ | **L** (1st 0-0 → NRFI) | ✅ **E4 LIFTED at 16:00** — SF probable posted: **Carson Whisenhunt, 7.25 ERA / 1.84 WHIP, 5 GS / 22.1 IP = 4.5 IP/start**. 52% (flattened) → **56%**: a 1.84 WHIP is the worst on the slate and the YRFI read strengthens accordingly. ⚠ Oracle Park and Hunter Brown (3.53 / 1.24) are the suppressants holding it under 60%. |
| 8/11 | TEX @ LAA (Bradford 1.62 / **R. Johnson 1.60**) | YRFI | 56% | _model-only_ | **W** (1st 1-0 → YRFI) | Raw YRFI 61% → 56%. Worst WHIP pair on the slate; Johnson 7.11 ERA over 10 GS, Bradford has 4.1 IP all season. |
| 8/11 | KC @ LAD (Wacha 1.15 / **Snell — 3.0 IP all season**) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | Raw YRFI 62% → 57%. ⚠ Snell's WHIP is 3 innings of noise and is NOT used; the read is his rust/pitch cap plus the LAD 1-2-3. |
| 8/11 | TB @ ATH (Martinez **1.10** / Barnett 1.38) | YRFI | 58% | _model-only_ | **W** (1st 2-0 → YRFI) | Raw YRFI 63% → 58%, strongest YRFI of the night. Most hitter-friendly park in MLB; Barnett is a swingman (2 GS / 34.0 IP) starting. ⚠ Martinez at 2.65 / 1.10 is a real arm — only one half is soft. |
| 8/12 | PHI @ STL (**Wheeler 0.98** / Leahy 1.34) | NRFI | 58% | _model-only_ | **W** (1st 0-0 → NRFI) | Strongest read of the day. Wheeler's 0.98 WHIP / 10.77 K9 over 19 GS is the best 1st-inning profile on the board. ⚠ Held under 60% by Leahy's 1.34 and by 94°F / 6 mph out to RF at Busch. |
| 8/12 | BOS @ TOR (Suarez 1.17 / Soriano 1.26) | NRFI | 56% | _model-only_ | **W** (1st 0-0 → NRFI) | Two competent arms (3.32 / 3.24 ERA, 9.44 / 9.16 K9), closed roof, neither top-of-order a standing engine. |
| 8/12 | MIL @ SD (May 1.27 / Ray 1.33) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Petco. Ray (3.24) the better half; May 4.30 / 1.27 the drag. MIL's +131 top-of-order is the live YRFI half. |
| 8/12 | CLE @ DET (**Griffin 1.11** / Valdez 1.37) | NRFI | 55% | _model-only_ | **L** (1st 2-2 → YRFI) | Griffin 1.11 over 23 GS / 133.1 IP is real; Valdez 4.17 / 1.37 with 7.28 K9 gets outs on the ground. DET +89 is the counter. |
| 8/12 | PIT @ MIA (Mlodzinski 1.36 / Junk 1.36) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Identical mediocre WHIPs but neither top-of-order dangerous (PIT +19, MIA +17); roof closed. Contact-dependent outs keep it near the line. |
| 8/12 | SEA @ NYY (**Miller 0.95** / Warren 1.37) | NRFI | 53% | _model-only_ | **L** (1st 3-0 → YRFI) | Miller's 0.95 over 13 GS is the 2nd-best profile today; held to a coin flip by the Yankee 1-2-3 (+85) facing Warren's 1.37. |
| 8/12 | TB @ ATH (**Rasmussen 0.91** / Perkins 1.45) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Board's best WHIP vs the majors' most hitter-friendly park and a 7.04 ERA opponent. Genuinely two-sided — barely above the line by design, not confidence. |
| 8/12 | NYM @ ATL (Thornton 1.07 / Mahle 1.36) | NRFI | 51% | _model-only_ | **W** (1st 0-0 → NRFI) | ⚠ **FLIPPED READ.** Raw YRFI 56% (ATL top-of-order best on the board at +121; Mahle 4.83 / 1.36; Thornton is a short-role arm at 7 GS / 39.1 IP) → corrected to NRFI 51%. Row-level grading; the row I most expect the correction to miss. |
| 8/12 | BAL @ MIN (Baz 1.32 / **Matthews 1.34**) | YRFI | 52% | _model-only_ | **W** (1st 1-1 → YRFI) | Raw YRFI 57% → 52%. Two 1.3+ WHIPs; Matthews 5.23 ERA is the softest qualified starter of the early window. ⚠ Counter: 82°F, wind 5 mph IN from CF. |
| 8/12 | HOU @ SF (**King — opener, 0 GS / 49.1 IP** / Houser 1.37) | YRFI | 51% | _model-only_ | **W** (1st 0-1 → YRFI) | ⚠ **E5 — Houston is a BULLPEN GAME.** An opener's 1st inning is the least predictable on any board and cuts both ways, so the number is flattened rather than pushed. Oracle Park is the strongest suppressant venue on the slate. Re-read at 16:00. |
| 8/12 | CHC @ WSH (Peterson **1.50** / **Kent — no 2026 record**) | YRFI | 51% | _model-only_ | **L** (1st 0-0 → NRFI) | ⚠ Half the read is missing — Jackson Kent returns no 2026 StatsAPI pitching line, so the number is flattened rather than guessed. Peterson's 5.35 / 1.50 is the worst qualified WHIP on the board; CHC +109 is the live half. Re-read at 16:00. |
| 8/12 | KC @ LAD (**Lynch — 1 GS / 47.2 IP** / Lauer 1.26) | YRFI | 52% | _model-only_ | **L** (1st 0-0 → NRFI) | Raw YRFI 57% → 52%. ⚠ Lynch's 1.01 WHIP is relief data and is NOT used — he is a swingman (E5-adjacent). Read rests on the LAD 1-2-3 (+140) vs Lauer's 4.89 ERA / 5.58 K9 contact profile. |
| 8/12 | CIN @ CWS (Lowder **1.48** / Castillo **1.41**) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | Raw YRFI 59% → 54%. Both starters over 5.20 ERA and 1.40 WHIP — the only game where neither half suppresses. Rate Field carry is a 1st-inning HR risk. ⚠ Neither top-of-order is an engine. |
| 8/12 | COL @ AZ (Feltner **1.45** / Kelly **1.47**) | YRFI | 55% | _model-only_ | **W** (1st 0-1 → YRFI) | Raw YRFI 60% → 55%. Worst ERA pair on the board (5.71 / 4.88), two 1.45+ WHIPs, two low K rates (6.48 / 6.00). Roof-shut Chase is the only suppressant. |
| 8/12 | TEX @ LAA (Quantrill 1.19 / **Klassen 2.88 — 8.2 IP**) | YRFI | 58% | _model-only_ | **L** (1st 0-0 → NRFI) | Raw YRFI 63% → 58%, **strongest YRFI of the day.** Klassen's 2.88 WHIP over 8.2 IP / 3 GS is ~3 baserunners per inning, the most extreme number on the board either way. ⚠ 8.2 IP is a tiny sample (E2 with the sign flipped) and Quantrill's 3.56 / 1.19 half is genuinely competent. |
| 8/14 | SD @ CLE (King 1.17 / **G. Williams 1.04**) | NRFI | 58% | _model-only_ | **W** (1st 0-0 → NRFI) | Strongest read of either kind today; best combined arms on the board. Williams 3.55/1.04 over 24 GS with **11.51 K/9** (highest on the slate) and whiffs are the cleanest 1st-inning suppressant; King 3.37/1.17 over 24 GS. Progressive Field suppresses; neither top-of-order an engine (SD +1, CLE −30). |
| 8/14 | WSH @ NYM (Alvarez 1.40 / **Stock 2.13**) | YRFI | 57% | _model-only_ | **L** (1st 0-0 → NRFI) | Raw YRFI 62% → 57%; strongest YRFI of the day. **Stock's 2.13 WHIP is the board's worst by nearly half a baserunner/inning**; last start 3.0 IP / 8 ER / 5 BB @ PIT corroborates the 10.13 ERA. Alvarez's 1.40 does not suppress. ⚠ Held at 57 — the sample is 2 GS / 8.0 IP and neither top-of-order is an engine. |
| 8/14 | MIA @ CIN (Alcantara 1.17 / **Burns 1.12**) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Two sub-1.20 WHIPs; Burns 2.61/1.12 with 10.38 K/9 over 22 GS (13-2) is the 2nd-best arm on the slate, Alcantara's 163.2 IP the most durable line. ⚠ **Great American is the NL's best hitter's park** — that counter is why this is 55 not ~60. Weather PENDING. |
| 8/14 | BOS @ PIT (**Bennett 1.04** / Chandler 1.38) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | Bennett's 1.04 is tied for best on the board (3.17 over 13 GS) and **PNC is a top-two suppressant venue**; his half is near a lockout. ⚠ Chandler's 1.38 (4.26, 22 GS) is the whole drag, and BOS's 1-2-3 at +86 is a real top-of-order. |
| 8/14 | NYY @ TOR (**Cole 1.08** / **Bieber 1.66**) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | Raw YRFI 60% → 55%. **Bieber's 1.66 is the worst qualified line on the board** (5.48 over 9 GS, <5 IP/start) and **the Yankee 1-2-3 is a standing YRFI engine at +89** — best bad-arm/good-lineup pairing on the slate. ⚠ Cole 3.35/1.08, 9.71 K/9 — a one-sided YRFI resting entirely on Toronto's half. |
| 8/14 | KC @ LAA (Lugo 1.37 / **G. Rodriguez 1.62**) | YRFI | 55% | _model-only_ | **L** (1st 0-0 → NRFI) | Raw YRFI 60% → 55%. **Weakest pair of arms on the board** — G-Rod 7.20/1.62 over 12 GS, Lugo 4.41/1.37 over 24 GS. ⚠ Two counters hold it at 55: **KC −114 and LAA −83 are two of the AL's four worst run differentials**, and Angel Stadium is neutral-to-suppressing, not a bandbox. |
| 8/14 | STL @ CHC (**Liberatore 1.52** / Holmes 1.10) | YRFI | 54% | _model-only_ | **L** (1st 0-0 → NRFI) | Raw YRFI 59% → 54%. Liberatore's 1.52 is the 2nd-worst qualified line (5.15, 5-9 over 23 GS) and **the Cubs' 1-2-3 is 2nd-best on the board at +108**. ⚠ Holmes 2.39/1.10 is the counter. ⚠ **Wrigley wind can move this several points and weather is PENDING; first pitch 14:20 ET so the 16:00 run is too late** — flagged, not fixed. |
| 8/14 | SEA @ HOU (Kirby 1.27 / Lambert 1.15) | NRFI | 54% | _model-only_ | **L** (1st 2-1 → YRFI) | Two competent arms in a dome, weather removed. Lambert 3.09/1.15 over 20 GS is quietly the better half; Kirby 3.68/1.27 the softer. Neither top-of-order an engine (SEA −26, HOU −27). ⚠ Kirby's 1.27 is the drag and Houston puts the ball in play early (21% K vs RHP) — contact is not suppression. |
| 8/14 | TEX @ ATH (Rocker 1.38 / **TBA**) | YRFI | 53% | _model-only_ | **W** (1st 0-3 → YRFI) | ⚠ **LOW CONFIDENCE — Athletics SP is TBA (E4), half the input missing.** Rocker 4.46/1.38 over 20 GS does not suppress and **Sutter Health Park is the most hitter-friendly venue on the board**. A lean on one starter and a park, not a matchup — logged at 53 to say so. |
| 8/14 | MIL @ LAD (Gasser 1.22 / **Yamamoto 0.89**) | NRFI | 52% | _model-only_ | **L** (1st 0-1 → YRFI) | ⚠ **FLIPPED READ — the only reversal today.** Raw YRFI 53% on the two best tops-of-order in baseball (MIL +131, LAD +141); −5pp correction pulls it to a bare NRFI. **Yamamoto's 0.89 is the board's only sub-1.00** (2.65 over 21 GS) and Dodger Stadium suppresses. ⚠ Recorded against ourselves: this game read YRFI 56% yesterday and went 0-0 — a reason for care, not confidence. |
| 8/14 | CWS @ DET (**Newcomb — opener** / Jobe 0.40) | NRFI | 52% | _model-only_ | **L** (1st 1-0 → YRFI) | ⚠ **LOW CONFIDENCE — bullpen game one side, 5-inning sample the other.** **Newcomb has 1 GS in 64.1 IP; last twelve outings all 0.2–2.0 IP relief** — an opener, whose *first* inning is often his best (2.66 ERA in relief), which is the NRFI case. **Jobe's 0.00/0.40 is 5.0 IP in one start** — E2 small-sample. Held at a bare 52: neither half is well estimated. |
| 8/14 | COL @ SF (**Freeland 1.50** / Roupp 1.29) | YRFI | 52% | _model-only_ | **L** (1st 0-0 → NRFI) | Raw YRFI 57% → 52%. Freeland 6.63/1.50 (3-10 over 21 GS) is 3rd-worst on the board and misses no bats (7.67 K/9). ⚠ Two counters pull it back: **Oracle is the strongest suppressant venue in baseball** and **COL's top-of-order is 2nd-weakest on the slate at −116**. Bad arm vs bad lineup in a huge park is a coin flip. |
| 8/14 | AZ @ ATL (Pfaadt 1.20 / **TBA**) | YRFI | 52% | _model-only_ | **W** (1st 1-0 → YRFI) | ⚠ **LOW CONFIDENCE — Atlanta SP is TBA (E4).** The case is **Atlanta's 1-2-3, at +124 the best top-of-order in the NL**. ⚠ Pfaadt 3.36/1.20 over 11 GS is a real counter, though **his 5.67 K/9 is the lowest on the slate** — he works on contact rather than shutting the inning, the profile that concedes a run to a good lineup. |
| 8/14 | BAL @ TB (**TBA** / Matz 1.23) | YRFI | 52% | _model-only_ | **L** (1st 0-0 → NRFI) | ⚠ **LOW CONFIDENCE — Baltimore SP is TBA (E4), away half unmodelled.** Matz 5.46/1.23 over 10 GS: the WHIP limits traffic but the ERA says what traffic he allows scores — a homer-prone, 1st-inning-risk profile. Dome removes weather. BAL −36; TB's +62 and L10 9-1 are the push. Logged at 52 for the missing input. |
| 8/13 | CLE @ DET (**Messick 1.04** / **Montero 1.01**) | NRFI | 59% | _model-only_ | **W** (1st 0-0 → NRFI) | Strongest read of the day and the best WHIP pair on the board (2.57/1.04 over 23 GS vs 3.38/1.01 over 19 GS). Comerica suppresses; wind a harmless 4 mph L-to-R at 77°F. ⚠ This game read NRFI 55% yesterday and busted; DET's +87 differential is the counter. |
| 8/13 | TEX @ LAA (**deGrom 1.13** / Ureña 1.29) | NRFI | 56% | _model-only_ | **W** (1st 0-0 → NRFI) | deGrom's 10.92 K/9 is the highest on the slate and his half is close to a lockout. Ureña's 2.83 ERA is real but 1.29 says traffic. LAA whiff 25% vs both hands — a lineup that whiffs does not string a 1st-inning rally. Weather PENDING. |
| 8/13 | PIT @ MIA (Ashcraft 1.16 / Phillips 1.36) | NRFI | 56% | _model-only_ | **W** (1st 0-0 → NRFI) | Roof closed at loanDepot, 72°F, wind 0 — weather removed entirely at the NL's 2nd-best suppressant venue. Ashcraft's 9.86 K/9 is the whiff half. Neither top-of-order is an engine (PIT +13, MIA +23). Phillips' 1.36 is the drag. |
| 8/13 | SEA @ NYY (**Gilbert 1.00** / **Fried 0.97**) | NRFI | 55% | _model-only_ | **W** (1st 0-0 → NRFI) | The only sub-1.00 WHIP pair on the board. Held 5pp below what the arms alone say by the two biggest counters on the slate: the Yankee 1-2-3 is a standing YRFI engine at +90, and 83°F with wind 9 mph out to RF is the most carry-friendly reading posted. ⚠ Read NRFI 53% yesterday and busted 5-10. |
| 8/13 | BOS @ TOR (**Tolle 1.10** / Scherzer **1.53**) | NRFI | 51% | _model-only_ | **L** (1st 1-0 → YRFI) | ⚠ **FLIPPED READ** — raw YRFI 56% on Scherzer's board-worst 1.53, corrected to a bare NRFI. Two things hold the YRFI case down: Scherzer's season line is a STALE AGGREGATE (last two 6.0 IP/1 ER, 5.1 IP/2 ER), and TOR hit .218/.292 vs LHP, which is who they face in a 10.43 K/9 lefty who struck out 14 on 8/7. **The row I most expect the correction to be wrong on tonight.** |
| 8/13 | MIL @ LAD (Drohan 1.25 / Sasaki 1.28) | YRFI | 56% | _model-only_ | **L** (1st 0-0 → NRFI) | Raw YRFI 61% → 56%, strongest YRFI of the day. The only game where BOTH tops-of-order are engines — MIL +130 and LAD +142 are the two best run differentials in baseball — facing two 1.25-1.28 WHIPs, neither suppressing. Sasaki's 4.54 is the softer half. Weather PENDING. |
| 8/13 | PHI @ MIN (Nola **1.45** / Bradley 1.25) | YRFI | 54% | _model-only_ | **W** (1st 2-0 → YRFI) | Raw YRFI 59% → 54%. Nola's 5.47 / 1.45 is the worst qualified line on the board once Scherzer's stale aggregate is set aside, and 3-9 over 24 GS says it is not small-sample. Bradley's 10.12 K/9 is the counter. ⚠ No park input applied — Field of Dreams has no park-factor history. |
| 8/13 | CHC @ WSH (Gausman 1.26 / Cavalli 1.30) | YRFI | 52% | _model-only_ | **L** (1st 0-0 → NRFI) | Raw YRFI 57% → 52%. Two starters either side of a 1.28 WHIP, neither suppressing; CHC's 1-2-3 is 3rd-best on the board at +115. Cavalli's 9.86 K/9 over 25 GS keeps it from going higher. Weather PENDING. |
| 8/13 | CIN @ CWS (Abbott **1.39** / Martin 1.33) | YRFI | 51% | _model-only_ | **W** (1st 3-1 → YRFI) | Raw YRFI 56% → 51%. Weakest pair on the board (3.92 / 4.17, both 1.3+). ⚠ Two counters hold it at a coin flip: wind 6 mph IN from LF at 77°F is the only suppressing reading posted, and neither top-of-order is an engine (CIN −78, CWS +41). ⚠ This game read YRFI 54% yesterday and went 0-0. |

| 8/10 | MIL @ SD (Henderson 0.90 / Mize 1.09) | NRFI | 62% | _model-only_ | **W** (1st 0-0 → NRFI) | Strongest read of the day. Petco plus the two lowest WHIPs facing each other anywhere on the slate. |
| 8/10 | KC @ LAD (Skubal 0.92 / Cameron 1.29) | NRFI | 59% | _model-only_ | **L** (1st 1-0 → YRFI) | Best arm on the board opposite a Cameron at 23.0 IP / 1 ER over three starts; held under 62% by the LAD top-of-order. |
| 8/10 | HOU @ SF (Wesneski 1.29 / Tidwell 1.18) | NRFI | 57% | _model-only_ | **L** (1st 1-0 → YRFI) | Oracle Park, the most run-suppressing venue on the slate; discounted for Tidwell having 1 GS in 9 appearances. |
| 8/10 | TEX @ LAA (Gore 1.24 / Detmers 1.10) | NRFI | 56% | _model-only_ | **L** (1st 0-1 → YRFI) | Two high-K arms (9.79 / 10.47 K9) in a neutral park; strikeouts are the cleanest 1st-inning suppressant. |
| 8/10 | NYM @ ATL (Scott 1.26 / Elder 1.20) | NRFI | 54% | _model-only_ | **L** (1st 5-2 → YRFI) | Both sub-3.70 ERA; held down only by Atlanta's 1-2-3, the best top-of-order on the board. |
| 8/10 | COL @ AZ (Hughes 1.18 / **Soroka — 7 weeks absent**) | NRFI | 54% | _model-only_ | **L** (1st 0-4 → YRFI) | WHIP pair says 58%; Soroka's last MLB outing was 6/19 and currentTeam returns Reno Aces, so live rust risk the season line cannot see. |
| 8/10 | BAL @ MIN (Rogers 1.24 / Kremer 1.32) | NRFI | 52% | _model-only_ | **W** (1st 0-0 → NRFI) | Two ordinary WHIPs, neutral park, neither top dangerous — close to a coin flip. |
| 8/10 | BOS @ TOR (Gray 1.15 / Taillon 1.39) | NRFI | 52% | _model-only_ | **W** (1st 0-0 → NRFI) | ⚠ **THE FLIPPED READ.** Raw lean YRFI 53% (Rogers Centre; Taillon has not finished 5 IP since June); the pre-registered −5pp YRFI correction takes it to 48%, so the nominal lean becomes NRFI 52%. Marked for row-level grading of the correction. |
| 8/10 | PHI @ STL (**Painter 1.57** / Dobbins 1.30) | YRFI | 51% | _model-only_ | **L** (1st 0-0 → NRFI) | Painter's 1.57 is the worst WHIP outside the TB@ATH pair. Raw lean YRFI 56%, corrected to 51%. |
| 8/10 | TB @ ATH (Peralta 1.52 / **Lopez 1.63**) | YRFI | 57% | _model-only_ | **W** (1st 1-2 → YRFI) | Day's clearest YRFI: both SPs over 5.37 ERA, the two worst WHIPs on the slate, in the most hitter-friendly park in MLB. Raw 62% → corrected 57%. |

| 8/9 | TOR @ PHI (Bieber 1.68 / Luzardo 1.16) | YRFI | 61% | _model-only_ | **L** (1st 0-0 → NRFI) | The board's worst WHIP (1. |
| 8/9 | COL @ STL (Lorenzen 1.85 / McGreevy 1.20) | YRFI | 58% | _model-only_ | **W** (1st 1-1 → YRFI) | Lorenzen's 1. |
| 8/9 | ATH @ BOS (Ginn 1.21 / Miller 1.34 opener) | YRFI | 55% | _model-only_ | **W** (1st 1-0 → YRFI) | Asymmetric by design: Boston is opening with Erik Miller (0 GS in 35. |
| 8/9 | CIN @ WSH (Singer 1.43 / Lord 1.20) | YRFI | 52% | _model-only_ | **L** (1st 0-0 → NRFI) | Singer's 1. |
| 8/9 | CHC @ KC (Boyd 1.22 / Dobnak 1.19) | YRFI | 51% | _model-only_ | **W** (1st 1-0 → YRFI) | 91°F with 13 mph out to CF, the strongest wind of the day, and Chicago's top is the hotter of the two. |
| 8/9 | LAA @ MIA (G. Rodriguez 1.59 / Gusto 1.36) | YRFI | 53% | _model-only_ | **W** (1st 1-3 → YRFI) | The worst ERA on the board (7. |
| 8/9 | DET @ SF (Melton 0.91 / Webb 1.11) | NRFI | 63% | _model-only_ | **W** (1st 0-0 → NRFI) | Strongest read of either kind today. |
| 8/9 | MIN @ MIL (Prielipp 1.31 / Misiorowski 0.73) | NRFI | 61% | _model-only_ | **L** (1st 0-1 → YRFI) | Misiorowski's 0. |
| 8/9 | TB @ SEA (Seymour 1.13 / Hancock 1.07) | NRFI | 60% | _model-only_ | **L** (1st 0-1 → YRFI) | T-Mobile Park, the most run-suppressing park in MLB, with a clean 1. |
| 8/9 | LAD @ AZ (Wrobleski 1.07 / E. Rodriguez 1.24) | NRFI | 58% | _model-only_ | **L** (1st 0-2 → YRFI) | Closed dome at Chase, two starters with real command lines (Wrobleski 3. |
| 8/9 | NYM @ PIT (Manaea 1.38 / J. Jones 1.11) | NRFI | 56% | _model-only_ | **L** (1st 2-0 → YRFI) | PNC is a pitcher park and both tops are poor — NYM are 51-67 (−53) and PIT 58-61 on a 3-7 L10. |
| 8/9 | BAL @ TEX (Povich 1.34 / Rocker 1.33) | NRFI | 54% | _model-only_ | **L** (1st 2-0 → YRFI) | Closed dome at Globe Life and two nearly identical ordinary WHIPs (1. |
| 8/9 | CLE @ CWS (Cantillo 1.47 / D. Martin 1.31) | NRFI | 53% | _model-only_ | **L** (1st 2-1 → YRFI) | The one wind-IN game on the board — 11 mph in from RF at Rate Field — which is what drags a hitter park's read under. |
| 8/9 | HOU @ SD (Javier 1.68 / **Vásquez 1.42**) | YRFI | 52% | O0.5 −130 / U0.5 +110 (FD) → YRFI no-vig **54.3%** | **L** (1st 0-0 → NRFI) | ⚠ **FLIPPED at 16:00 (was NRFI 52%).** **E4 CLEARED — San Diego posted Randy Vásquez (4.19 ERA / 1.42 WHIP / 5.79 K9, 18 GS).** Build A's NRFI 52% was written blind; with BOTH starters at WHIP ≥1.42 the raw lean is YRFI ~57%, and the pre-registered **−5pp YRFI correction** takes it to **52%**. ⚠ **The market is AHEAD of the model here** (YRFI no-vig 54.3%), so this is **model-only / NO BET** — the mirror NRFI side prices at 45.7% no-vig and `pitcher_park_under` (Petco) halved to +1.5 lands TrueP 47.2%, **+1.5pp, short of the +2pp gate.** First 8/9 read where a real 1st-inning line was pulled (1 credit). |
| 8/9 | ATL @ NYY (Holmes 1.34 / Schlittler 0.95) | NRFI | 51% | _model-only_ | **W** (1st 0-0 → NRFI) | ⚠ A FLIPPED READ, and the ratchet flag from 8/8 is exactly why it is being called out. |
| 8/8 | TOR @ PHI (Scherzer/Nola) | YRFI | 63% | _model-only_ | **W** (1st 1-0 → YRFI) | Two worst WHIPs on the board (1.63/1.44) at CBP; Scherzer averaging 3.8 IP over 8 GS. Strongest read either way. [−5pp applied] |
| 8/8 | HOU @ SD (Lambert/King) | NRFI | 61% | _model-only_ | **L** (1st 0-1 → YRFI) | Petco + best matched WHIP pair (1.13/1.20). Same shape as 8/7's winning TB@SEA read. |
| 8/8 | COL @ STL (Freeland/Liberatore) | YRFI | 61% | _model-only_ | **W** (1st 1-2 → YRFI) | Identical 1.49 WHIPs, joint-worst pair. ⚠ Freeland coming off a 9.0 IP CG (1 ER). [−5pp applied] |
| 8/8 | LAA @ MIA (Ureña/Alcantara) | NRFI | 59% | _model-only_ | **W** (1st 0-0 → NRFI) | Two quality arms (2.54/3.68) in a roofed park vs two of the weakest tops in MLB. |
| 8/8 | TB @ SEA (Jax/Kirby) | NRFI | 58% | _model-only_ | **W** (1st 0-0 → NRFI) | T-Mobile, most run-suppressing park in MLB. Softer than 8/7's version — Kirby 1.28 is the weak half. |
| 8/8 | ATL @ NYY (Sale/Cole) | NRFI | 57% | _model-only_ | **W** (1st 0-0 → NRFI) | Best WHIP pair on the board (1.02/1.10), discounted hard for two loaded tops (+120 and +82 run diff). |
| 8/8 | ATH @ BOS (Jump/Bennett) | YRFI | 57% | _model-only_ | **W** (1st 0-2 → YRFI) | Asymmetric — Jump 1.47 faces a BOS top on a 9-1 L10 / 9-game win streak at Fenway. [−5pp applied] |
| 8/8 | LAD @ AZ (Yamamoto/Pfaadt) | NRFI | 57% | _model-only_ | **W** (1st 0-0 → NRFI) | Yamamoto's 0.88 is the best WHIP on the slate; closed dome. LAD's 7-game skid helps the under. |
| 8/8 | BAL @ TEX (Bradish/deGrom) | NRFI | 55% | _model-only_ | **L** (1st 1-0 → YRFI) | deGrom 1.14 / 10.69 K9 in a closed dome; Bradish's 1.36 is why this isn't 60%. |
| 8/8 | NYM @ PIT (Stock/Chandler) | NRFI | 54% | _model-only_ | **L** (1st 0-3 → YRFI) | PNC pitcher park, two poor tops. ⚠ Stock's 0.60 is a 5.0 IP / 1 GS sample — effectively unpriced. |
| 8/8 | CIN @ WSH (Burns/Alvarez) | NRFI | 54% | _model-only_ | **W** (1st 0-0 → NRFI) | Burns 2.35 / 10.39 K9 is the class of it; Alvarez 1.45 over 8 GS is the soft half. Thin. |
| 8/8 | MIN @ MIL (Bradley/Gasser) | NRFI | 54% | _model-only_ | **L** (1st 0-1 → YRFI) | Retractable roof, two ordinary arms, two ordinary tops. Coin flip nudged under by the dome. |
| 8/8 | CHC @ KC (Holmes/Lugo) | YRFI | 53% | _model-only_ | **W** (1st 0-1 → YRFI) | CHC's top is the hottest on the board (L10 7-3, W5) vs Lugo 1.39 at Kauffman. [−5pp applied] |
| 8/8 | CLE @ CWS (Williams/Kay) | NRFI | 53% | _model-only_ | **W** (1st 0-0 → NRFI) | Williams 1.04 / 11.53 K9 is a real NRFI arm, but Rate Field is a hitter park and Kay 1.35 is exposed. |
| 8/8 | DET @ SF (Jobe/Roupp) | NRFI | 52% | _model-only_ | **W** (1st 0-0 → NRFI) | ⚠ Lowest conviction: Jobe has ZERO 2026 MLB data (StatsAPI `stats: []`). The read is Oracle Park alone. |


| 8/15 | CWS @ DET (Kay/Melton) | NRFI | 60% | _model-only_ | **L** (1st 1-1 → YRFI) | Melton 1.46/0.90; Comerica + 7mph wind IN. |
| 8/15 | MIL @ LAD (Misiorowski/Wrobleski) | NRFI | 61% | **U0.5 −136 BetRivers → no-vig 52.9%** | TBD | 0.74 WHIP — lowest on the board; baserunners are the input. ⚠ **16:00: PRICED. Raw gap +8.1pp — DECLINED**, not promoted: model number is unanchored to market, `market_disagrees` fires, 8.9% hold. See the 16:00 block above. |
| 8/15 | AZ @ ATL (E-Rodriguez/Holmes) | NRFI | 57% | _model-only_ | TBD | Two sub-3.50 ERA arms, no park/air help. |
| 8/15 | SEA @ HOU (Hancock/Wesneski) | NRFI | 56% | _model-only_ | TBD | Dome, neutral air, two 1.1x WHIPs. |
| 8/15 | STL @ CHC (McGreevy/Boyd) | NRFI | 56% | _model-only_ | TBD | Matched 1.22 WHIPs; Wrigley wind PENDING at 14:20 first pitch. |
| 8/15 | BAL @ TB (Bradish/Seymour) | NRFI | 54% | _model-only_ | TBD | Seymour 10.56 K/9 in a dome; Bradish 1.34 the drag. |
| 8/15 | NYY @ TOR (Schlittler/Fisher-OPENER) | NRFI | 54% | _model-only_ | TBD | Schlittler 0.93 WHIP; fresh 1-inning opener is not a soft first frame. |
| 8/15 | KC @ LAA (Dobnak/Detmers) | NRFI | 54% | _model-only_ | TBD | Detmers 10.40 K/9 vs a KC offence at −113 run diff. |
| 8/15 | PHI @ MIN (Luzardo/Prielipp) | NRFI | 53% | _model-only_ | TBD | Luzardo 11.03 K/9 carries it; Prielipp vs the PHI top is the risk. |
| 8/15 | BOS @ PIT (Gray/Jones) | NRFI | 53% | _model-only_ | TBD | PNC suppresses; Jones gave 8 ER in 3.0 IP last out — the live YRFI half. |
| 8/15 | COL @ SF (Lorenzen/Webb) | YRFI | 53% | _model-only_ | TBD | Lorenzen 1.88 WHIP is a 1st-inning traffic magnet; Oracle is the counter. |
| 8/15 | SD @ CLE (TBA/Cantillo) | YRFI | 54% | _model-only_ | TBD | Cantillo 1.48 WHIP; E4 LOW CONFIDENCE — half the input missing. |
| 8/15 | TEX @ ATH (Gore/Ginn) | YRFI | 54% | _model-only_ | TBD | Sutter Health hot small-park; both arms mid. |
| 8/15 | WSH @ NYM (Lord-BULLPEN/Manaea) | YRFI | 55% | _model-only_ | TBD | Manaea 1.32 is the real input; Lord's 1-2 innings are fresh, not soft. |
| 8/15 | MIA @ CIN (Gusto/Singer) | YRFI | 58% | _model-only_ | TBD | Weakest pair on the board in the NL's best hitter's park. |

## Running totals (update on every settle)
- **Record:** **207-174 (54%)** (tracker opened 6/10/26). **NRFI:** **107-87 (55%)** · **YRFI:** **100-87 (53%)**. _(**Updated 8/15 11:00 Build A** — **8/14 is now FULLY SETTLED**; 13 rows auto-stamped off `linescore.innings[0]` by `nrfi_settle.py --apply` at session start. The 14-game slate went **5W-8L**, the tracker's weakest full slate since 8/9 — and it lands on the same board where the main build's two gate-clearing legs also lost, i.e. the day was broadly hostile to modelled reads rather than to one method. ⚠ Recorded plainly rather than averaged away: the overall win rate has now slipped from 55% to **54%** and the YRFI side has given back its edge to **53%**.)_ _(superseded 8/14 line: 202-165 (55%), NRFI 104-84 · YRFI 98-81)_ _(**Updated 8/14 11:00 Build A** — 8/13 FULLY SETTLED at 6W-3L (67%).)_ **NRFI:** **104-84 (55%)** · **YRFI:** **98-81 (55%)**. _(**Updated 8/14 11:00 Build A** — **8/13 is now FULLY SETTLED at 6W-3L (67%)**, the tracker's best slate since 8/8. The three late rows were auto-stamped off `linescore.innings[0]` by `nrfi_settle.py --apply` at session start: TEX@LAA NRFI **W**, MIL@LAD YRFI **L**, PHI@MIN YRFI **W**. Full day: NRFI leans **4-1**, YRFI leans **2-2** — the third straight slate the NRFI side carried the board.)_ _(**Updated 8/13 18:00 Build C** — six of today's nine reads are decided and the day stands **4W-2L**: CLE@DET NRFI ✅, PIT@MIA NRFI ✅, SEA@NYY NRFI ✅, BOS@TOR NRFI ❌, CIN@CWS YRFI ✅, CHC@WSH YRFI ❌. NRFI leans **3-1**, YRFI leans **1-1**. The three west-coast/late rows stay TBD for tomorrow's 11:00 settle.)_ _(**8/9 is now FULLY SETTLED — 15 of 15 reads decided, and the day finished 10W-10L (50%)**; the five rows still open at the 18:30 Build C lock were auto-stamped off `linescore.innings[0]` at session start — DET@SF **W**, TB@SEA **L**, LAD@AZ **L**, CLE@CWS **L**, HOU@SD **L**. 8/8's 11-3 remains the tracker's best slate.)_
- **Staked:** $0 · **P/L:** $0.00 (model leans only — no priced bets yet; tracking calibration).
- **Open (updated 8/14 11:00 Build A):** **14 of 14 reads TBD** — today's full slate is logged model-only; **8/13 is closed at 6-3 and nothing earlier remains open.** ⚠ **The −5pp YRFI correction enters slate NINE of its ~10-slate pre-registration.** Eight graded: 8/6 neutral, 8/7 neutral, 8/8 strongly positive, 8/9 strongly negative, 8/10 mildly negative, 8/11 neutral, 8/12 positive, 8/13 negative-on-the-flip. **Today it reverses exactly one read — MIL @ LAD**, raw YRFI 53% → NRFI 52%, flagged in-row. **Not tapered, not extended; the review is due after slate ten.** ⚠ **Three rows are E4-gated (TBA starters — BAL, ATL, ATH) and one is a bullpen game (CWS@DET, Newcomb 1 GS in 64.1 IP), so four of fourteen are explicitly LOW CONFIDENCE** rather than modelled as if complete. ⚠ **STL @ CHC first-pitches at 14:20 ET, before the 16:00 run** — its Wrigley wind input will never be re-read, which is a structural hole in the 11:00/16:00/18:00 cadence for early games rather than a miss on the day. ⚠ **Tool note, unchanged and still unfixed: `nrfi_settle.py` only stamps a row once the GAME is Final**, though the first inning decides these reads within ~20 minutes of first pitch — so the 18:00 run will again leave rows open that are already decided.
- **8/12 CLOSED at 9-6 (60%).** NRFI leans **6-2**, YRFI leans **3-4** — the second straight slate carried by the NRFI side. Record moves **187-156 → 196-162** (NRFI 100-83 · YRFI 96-79). ✅ **The −5pp YRFI correction's seventh graded slate is its cleanest win:** it flipped exactly one read, **NYM @ ATL** (raw YRFI 56% → NRFI 51%), the first inning went **0-0**, and the 8/12 note had named that specific row as *"the row I most expect the correction to be wrong on tonight."* Seven graded slates: 8/6 neutral, 8/7 neutral, 8/8 strongly positive, 8/9 strongly negative, 8/10 mildly negative, 8/11 neutral, 8/12 positive. **Not tapered, not extended** — it runs to the ~10-slate review per the pre-registration. ⚠ **Both NRFI misses were reads on quality arms:** SEA @ NYY NRFI 53% (Bryce Miller's 0.95 WHIP) and CLE @ DET NRFI 55% (Foster Griffin's 1.11) both busted. **A very good season WHIP is not a first-inning guarantee**, and this tracker keeps paying for treating it as one — the same shape as the main build's thesis-conflict problem on the same slate.
- **8/11 CLOSED at 10-5 (67%) — the tracker's second-best slate on record**, behind 8/8's 11-3. NRFI leans **7-3**, YRFI leans **3-2**; the first slate in a week where both sides contributed. Record moves **177-151 → 187-156** (NRFI 94-81 · YRFI 93-75). **The −5pp YRFI correction's sixth graded slate flipped two reads and they went 1-1:** CLE @ DET (raw YRFI 58% → NRFI 53%) went 0-0 ✅, and BAL @ MIN (raw YRFI 57% → NRFI 52%) went 2-0 ❌ — the row the 8/11 note had explicitly flagged as the one it most expected to be wrong. Six graded slates: 8/6 neutral, 8/7 neutral, 8/8 strongly positive, 8/9 strongly negative, 8/10 mildly negative, 8/11 neutral on the flips and strongly positive on the slate. **Not tapered and not extended** — it runs to the ~10-slate review per the pre-registration. ⭐ **The one promoted bet, PIT @ MIA NRFI −155 (+3.7pp), settled W** on a 0-0 first inning — but it is recorded as **a correct read on an unbettable leg**: the game had reached Warmup before the 18:00 run reached it, so it was never actually available. The W is calibration, not money.
- **8/10 CLOSED at 4-6.** NRFI leans **3-5**, YRFI leans **1-1**. ✅ **The −5pp YRFI correction was right on the only row it flipped** (BOS @ TOR, raw YRFI 53% → NRFI 52%, first inning 0-0). Fifth graded slate; running total across the five is 8/6 neutral, 8/7 neutral, 8/8 strongly positive, 8/9 strongly negative, 8/10 mildly negative on the slate but positive on the flip. Not tapered — the pre-registration says it runs to ~10 slates, and the reason it survived 8/8's good day is the reason it survives this one.
- **Superseded:** **8/10 — 10 reads logged, all model-only, all TBD** (8 NRFI / 2 YRFI after the correction; the raw model split is 7/3, so the ratchet reversed exactly one read, BOS@TOR). **8/9 is CLOSED at 10-10.** ⚠ **The −5pp YRFI correction had its worst graded slate: the YRFI leans went 5-1 while the NRFI leans went 5-9**, and all five of the late settles were games the correction had pushed toward NRFI — four of which went YRFI. That is now four graded slates (8/6 neutral, 8/7 neutral, 8/8 strongly positive, 8/9 strongly negative) and the pre-registration says it runs to the ~10-slate review regardless. **It is not being tapered after a bad day for the same reason it was not extended after 8/8's good one.** ⚠ The one-way-ratchet concern first raised on 8/7 is now supported by two slates of evidence rather than one: the correction only ever moves reads toward NRFI, and the NRFI side is the side that has lost on both of the slates where the split was lopsided.
- **Open:** **8/7 FULLY SETTLED — 15 of 15 reads decided; the day finished 8W-7L (53%)** (auto-stamped by `nrfi_settle.py --apply` at session start off `linescore.innings[0]`). **The −5pp YRFI correction's first graded slate came back NEUTRAL**: YRFI leans **4-4**, NRFI leans **4-3**, and the two reads it flipped (TOR@PHI, CIN@WSH) went **1-1**. No evidence for it, none against — it keeps running per the pre-registration. ⚠ **New and worth watching: the correction is a one-way ratchet.** It subtracts 5pp from YRFI leans and nothing from NRFI leans, so each slate it pushes the split further under — raw 8-3 → 8-7 on 8/6, and today it pulls a **raw 8-7 down to 4 YRFI / 11 NRFI**. A calibration correction that moves the split monotonically in one direction is hard to distinguish from a standing directional bet on NRFI. Flagged for the graded-experiment review, **not acted on** — tapering a pre-registered adjustment after one neutral day is the result-reading the doctrine forbids. **8/8: 15 reads logged below, all model-only at 11:00** — the priced `totals_1st_1_innings` sweep is the 16:00 run's job. No game is E4-gated today (all 30 probables posted), but **DET@SF's Jackson Jobe has zero 2026 MLB data**, so that read is written at near-coin-flip.

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
