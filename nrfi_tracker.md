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

## Tonight's reads — 2026-06-20 (model leans, un-priced; pull `totals_1st_1_innings` at the book)

> 11:00 ET morning reads — 14-game slate. One model-lean per game, all model-only/no-bet (pull the real 1st-inning total at the book; promote only a read clearing +2pp).

| # | Matchup | Starters | Lean | TrueP | Why (1st-inning read) |
|---|---------|----------|------|-------|------------------------|
| 1 | CWS @ DET | Fedde / Melton | **NRFI** | ~53% | Melton young but works clean early; CWS top volatile vs ace Skubal yesterday. Mild. |
| 2 | CIN @ NYY | Abbott / Warren | **YRFI** | ~54% | NYY elite top vs Abbott; Warren gives up early contact (declining K). Lean YRFI. |
| 3 | TOR @ CHC | Corbin / Rea | **NRFI** | ~53% | Rea decent early-frame control; Corbin vet, slow but works. Neutral matchup. |
| 4 | SD @ TEX | Buehler / Eovaldi | **NRFI** | ~53% | Both capable early-frame control arms; no loaded tops. Mild NRFI. |
| 5 | WSH @ TB | Cavalli / Seymour | **YRFI** | ~53% | Seymour uncertain arm (dome); WSH top vs him is the live half. Mild YRFI. |
| 6 | SF @ MIA | McDonald / Meyer | **NRFI** | ~55% | **Meyer (ERA 2.75, K/9 10.06) mows the 1st clean — best NRFI arm on the evening core.** SF away top quiet. |
| 7 | MIL @ ATL | Harrison / Sale | **NRFI** | ~54% | Sale (ERA 2.30) elite early frames; Harrison also clean. Both aces working → NRFI. |
| 8 | CLE @ HOU | Cantillo / Arrighetti | **NRFI** | ~53% | Arrighetti (2.57) decent first-inning; dome suppresses extra run scoring. Mild NRFI. |
| 9 | NYM @ PHI | Peralta / Sánchez | **NRFI** | ~55% | **Sánchez (ERA 1.82) dominant early frames; CBP but Sánchez mows. Strong NRFI.** |
| 10 | PIT @ COL | Skenes / Sugano | **YRFI** | ~60% | **Coors Field + Sugano ERA 4.54** — PIT top can score early. Strongest YRFI on board. |
| 11 | LAA @ ATH | Ureña / Ginn | **YRFI** | ~54% | Ginn unverified SP-freshness; Ureña back-end. Both tops can score early. |
| 12 | MIN @ AZ | Bradley / Gallen | **YRFI** | ~55% | Gallen ERA 5.35 (struggling) — MIN top can jump on him early. |
| 13 | BAL @ LAD | Rogers / Yamamoto | **NRFI** | ~55% | Yamamoto (ERA 2.52) elite early frames; LAD top vs Rogers only risk. Strong NRFI. |
| 14 | BOS @ SEA | Early / Hancock | **YRFI** | ~53% | Both young arms; slight early-run lean. Mild YRFI. |

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
| 6/20 | CWS @ DET (Fedde/Melton) | NRFI | 53% | _model-only_ | TBD | Melton young but works clean; CWS top volatile. |
| 6/20 | CIN @ NYY (Abbott/Warren) | YRFI | 54% | _model-only_ | TBD | NYY elite top vs Abbott; Warren gives up early contact. |
| 6/20 | TOR @ CHC (Corbin/Rea) | NRFI | 53% | _model-only_ | TBD | Rea decent early; Corbin veteran. Neutral. |
| 6/20 | SD @ TEX (Buehler/Eovaldi) | NRFI | 53% | _model-only_ | TBD | Both capable early-frame control arms; no loaded tops. |
| 6/20 | WSH @ TB (Cavalli/Seymour) | YRFI | 53% | _model-only_ | TBD | Seymour uncertain; WSH top live. |
| 6/20 | SF @ MIA (McDonald/Meyer) | NRFI | 55% | _model-only_ | TBD | Meyer (2.75 ERA) mows early — best NRFI arm on core. |
| 6/20 | MIL @ ATL (Harrison/Sale) | NRFI | 54% | _model-only_ | TBD | Sale elite early; Harrison also clean. Both aces. |
| 6/20 | CLE @ HOU (Cantillo/Arrighetti) | NRFI | 53% | _model-only_ | TBD | Arrighetti decent; dome suppression. |
| 6/20 | NYM @ PHI (Peralta/Sánchez) | NRFI | 55% | _model-only_ | TBD | Sánchez (1.82 ERA) dominant early; strong NRFI. |
| 6/20 | PIT @ COL (Skenes/Sugano) | YRFI | 60% | _model-only_ | TBD | Coors + Sugano 4.54 ERA = strongest YRFI on board. |
| 6/20 | LAA @ ATH (Ureña/Ginn) | YRFI | 54% | _model-only_ | TBD | Ginn unverified; Ureña back-end. Both tops live. |
| 6/20 | MIN @ AZ (Bradley/Gallen) | YRFI | 55% | _model-only_ | TBD | Gallen struggling (5.35 ERA); MIN top can score early. |
| 6/20 | BAL @ LAD (Rogers/Yamamoto) | NRFI | 55% | _model-only_ | TBD | Yamamoto (2.52 ERA) elite early; LAD top vs Rogers only risk. |
| 6/20 | BOS @ SEA (Early/Hancock) | YRFI | 53% | _model-only_ | TBD | Both young arms; slight early-run lean. |

---

## Running totals (update on every settle)
- **Record:** **66-58** (tracker opened 6/10/26). **NRFI:** **33-36** · **YRFI:** **33-22**.
- **Staked:** $0 · **P/L:** $0.00 (model leans only — no priced bets yet; tracking calibration).
- **Open:** **6/20: 14 model-only reads open** (settle off the 1st-inning line score next run). 6/19's 14 reads settled 6W-8L (NRFI 3-4, YRFI 3-4) — bad day; notable miss: deGrom/TEX strong NRFI read (5-6 combined 1st) and PIT@COL YRFI (Coors + Freeland — clean 1st, NRFI). Record updated from 60-50 to 66-58.
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
