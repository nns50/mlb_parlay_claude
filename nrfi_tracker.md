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

## Tonight's reads — 2026-06-10 (model leans, un-priced; pull `totals_1st_1_innings` at the book)

| # | Matchup | Starters | Lean | TrueP | Why (1st-inning read) |
|---|---------|----------|------|-------|------------------------|
| 1 | **ATL @ CWS** | Sale (ATL) vs Davis Martin (CWS) | **NRFI (Under 0.5)** | ~60% | Sale (2.23 ERA, 10.65 K/9) routinely sets down a contact-average CWS top 1-2-3; the only YRFI risk is ATL's strong top (Harris/Albies/Olson) vs back-end Martin. Lean NRFI but Martin is the swing factor — not a lock. |
| 2 | **MIN @ DET** | Paredes (MIN) vs Valdez (DET) | **NRFI (Under 0.5)** | ~61% | Valdez is an elite sinker/ground-ball arm (weak early contact, low 1st-inning run rate) and MIN's bats are cold (L10 3-7). Paredes weak, but DET's top must manufacture a run vs a GB arm's mirror. Cleanest NRFI of the three. |
| 3 | **LAD @ PIT** | Ohtani (LAD) vs Jared Jones (PIT) | **YRFI (Over 0.5)** | ~56% | LAD's top is the board's most dangerous (Ohtani leadoff, Betts, Freeman) vs Jones — a real 1st-inning run threat; it only takes that one half. Ohtani shuts PIT's weak top down, but the LAD side carries YRFI. Slight YRFI lean. |

> Pull the real 1st-inning total + devig at first pitch; promote any read clearing +2pp into the ledger
> below with a pre-registered TrueP and the book price. Re-check lineups (a rested leadoff bat flips a read).

---

## Ledger (every NRFI/YRFI bet OR tracked read, append-only)

| Date | Matchup | Pick | TrueP | Price | Result | Reasoning (why this pick) |
|------|---------|------|-------|-------|--------|----------------------------|
| 6/10 | ATL @ CWS (Sale/Martin) | NRFI | 60% | _model-only (no bet)_ | TBD | **Pitching:** Sale ace (2.23 ERA / 10.65 K9) routinely retires a contact-average CWS top 1-2-3 in order. **Bats:** CWS top is league-avg (23% K vs LHP), no early-power threat. **YRFI risk:** ATL's strong top (Harris/Albies/Olson) vs back-end Davis Martin — the one half that can break NRFI. **Net:** lean NRFI ~60%, but Martin is the swing factor (not a lock). |
| 6/10 | MIN @ DET (Paredes/Valdez) | NRFI | 61% | _model-only (no bet)_ | TBD | **Pitching:** Valdez is an elite sinker/ground-ball arm — weak early contact, low 1st-inning run rate; the cleanest NRFI starter on the board. **Bats:** MIN's offense is cold (L10 3-7), unlikely to manufacture vs a GB arm. **YRFI risk:** Paredes (weak) means DET's top could score, but they'd have to string it together in the 1st. **Net:** cleanest NRFI of the three ~61%. |
| 6/10 | LAD @ PIT (Ohtani/Jones) | YRFI | 56% | _model-only (no bet)_ | **L** | **Thesis (YRFI):** LAD's top is the board's most dangerous (Ohtani leadoff, Betts, Freeman) vs hittable Jared Jones — a real 1st-inning run threat, and it only takes that one half-inning. Ohtani shuts PIT's weak top down, so the over rode entirely on the LAD side. **Result:** 1st inning 0-0 (LAD 0, PIT 0) — NRFI occurred, **lean MISSED.** Both starters threw clean 1sts; LAD's elite top didn't cash early. Calibration: the pitching-first bias beat the bats-first read. |

---

## Running totals (update on every settle)
- **Record:** 0-1 (tracker opened 6/10/26). **NRFI:** 0-0 · **YRFI:** 0-1.
- **Staked:** $0 · **P/L:** $0.00 (model leans only — no priced bets yet; tracking calibration).
- **Open:** ATL @ CWS (NRFI) + MIN @ DET (NRFI) — both TBD (CWS warmup / DET rain-delayed at settle time);
  settle off the 1st-inning line score on the next run.
- **Settled 6/10:** LAD @ PIT YRFI **L** (1st 0-0). First calibration point: a YRFI lean on an elite top
  missed because both aces' mirror held — reinforces the doctrine's NRFI/pitching-first bias.

> Tracked like `fades.md` / `bankroll.md`: any change → commit → push → PR → squash-merge.
> Settle each row off `mlb_api.sh` box scores (1st-inning line score) the next morning.
</content>
</invoke>
