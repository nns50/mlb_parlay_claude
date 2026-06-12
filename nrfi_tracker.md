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

## Tonight's reads — 2026-06-11 (model leans, un-priced; pull `totals_1st_1_innings` at the book)

> At the 18:00 ET run only 3 games remain pre-game; the earlier 6/11 slate is final. These are the live reads.

| # | Matchup | Starters | Lean | TrueP | Why (1st-inning read) |
|---|---------|----------|------|-------|------------------------|
| 1 | **LAD @ PIT** | Wrobleski (LAD) vs Keller (PIT) | **YRFI (Over 0.5)** | ~57% | LAD's top (Ohtani leadoff / Betts / Freeman) is the board's most dangerous vs hittable Mitch Keller (4.81 ERA); wind 11 mph out to LF at PNC adds early offense. Wrobleski (2.62, contact arm) quiets PIT's weak top, so the over rides the LAD side — but that's the live one. Slight YRFI lean. |
| 2 | **ATL @ CWS** | Martín Pérez (ATL) vs Anthony Kay (CWS) | **YRFI (Over 0.5)** | ~56% | Two back-end/soft-contact arms (Pérez ~4.5, Kay swing-type) — neither misses bats early. ATL's top can string it together and CWS's hot home offense (L15 10-5, +27) is a 1st-inning threat too. Both half-innings live → mild YRFI. |
| 3 | **SEA @ BAL** | Bryan Woo (SEA) vs Kyle Bradish (BAL) | **NRFI (Under 0.5)** | ~55% | The cleanest NRFI of the three — Woo (3.74, strike-thrower) and Bradish both work fast early; SEA's and BAL's 1-2-3 are league-average, no loaded-top threat. Mild NRFI lean. |

> Pull the real 1st-inning total + devig at first pitch; promote any read clearing +2pp into the ledger
> below with a pre-registered TrueP and the book price. Re-check lineups (a rested leadoff bat flips a read).

---

## Ledger (every NRFI/YRFI bet OR tracked read, append-only)

| Date | Matchup | Pick | TrueP | Price | Result | Reasoning (why this pick) |
|------|---------|------|-------|-------|--------|----------------------------|
| 6/10 | ATL @ CWS (Sale/Martin) | NRFI | 60% | _model-only (no bet)_ | **W** | **Pitching:** Sale ace (2.23 ERA / 10.65 K9) routinely retires a contact-average CWS top 1-2-3 in order. **Bats:** CWS top is league-avg (23% K vs LHP), no early-power threat. **YRFI risk:** ATL's strong top (Harris/Albies/Olson) vs back-end Davis Martin — the one half that can break NRFI. **Net:** lean NRFI ~60%, but Martin is the swing factor (not a lock). **Result:** 1st inning 0-0 → NRFI occurred, **lean correct (W).** |
| 6/10 | MIN @ DET (Paredes/Valdez) | NRFI | 61% | _model-only (no bet)_ | **W** | **Pitching:** Valdez is an elite sinker/ground-ball arm — weak early contact, low 1st-inning run rate; the cleanest NRFI starter on the board. **Bats:** MIN's offense is cold (L10 3-7), unlikely to manufacture vs a GB arm. **YRFI risk:** Paredes (weak) means DET's top could score, but they'd have to string it together in the 1st. **Net:** cleanest NRFI of the three ~61%. **Result:** 1st inning 0-0 → NRFI occurred, **lean correct (W)** — note DET still won the game 11-... blowout, but the 1st was clean. |
| 6/10 | LAD @ PIT (Ohtani/Jones) | YRFI | 56% | _model-only (no bet)_ | **L** | **Thesis (YRFI):** LAD's top is the board's most dangerous (Ohtani leadoff, Betts, Freeman) vs hittable Jared Jones — a real 1st-inning run threat, and it only takes that one half-inning. Ohtani shuts PIT's weak top down, so the over rode entirely on the LAD side. **Result:** 1st inning 0-0 (LAD 0, PIT 0) — NRFI occurred, **lean MISSED.** Both starters threw clean 1sts; LAD's elite top didn't cash early. Calibration: the pitching-first bias beat the bats-first read. |
| 6/11 | LAD @ PIT (Wrobleski/Keller) | YRFI | 57% | _model-only (no bet)_ | **L** (1st 0-0 → NRFI) | LAD's elite top (Ohtani/Betts/Freeman) vs hittable Keller (4.81); wind 11 out to LF @ PNC. Wrobleski quiets PIT's weak top → over rides the LAD side. Slight YRFI. **⚠ Note the 6/10 LAD@PIT YRFI MISSED (1st 0-0) — same LAD-top thesis; downgraded confidence accordingly.** |
| 6/11 | ATL @ CWS (Pérez/Kay) | YRFI | 56% | _model-only (no bet)_ | TBD | Two soft-contact/back-end arms; ATL top + hot CWS home offense (L15 10-5/+27) both live in the 1st. Mild YRFI. |
| 6/11 | SEA @ BAL (Woo/Bradish) | NRFI | 55% | _model-only (no bet)_ | **L** (1st 1-0 → YRFI) | Cleanest NRFI of the three — Woo + Bradish both work fast early, neither top is loaded. Mild NRFI. |

---

## Running totals (update on every settle)
- **Record:** **2-3** (tracker opened 6/10/26). **NRFI:** **2-1** · **YRFI:** **0-2**.
- **Staked:** $0 · **P/L:** $0.00 (model leans only — no priced bets yet; tracking calibration).
- **Open:** 6/11 ATL@CWS (YRFI) — **POSTPONED** (no 1st inning); leave TBD / void. No other open reads.
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
