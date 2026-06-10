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

| Date | Matchup | Pick | TrueP | Price | Result | Note |
|------|---------|------|-------|-------|--------|------|
| 6/10 | ATL @ CWS (Sale/Martin) | NRFI | 60% | _pull at book_ | TBD | model lean — Sale ace shuts CWS top; Martin vs ATL top = YRFI risk |
| 6/10 | MIN @ DET (Paredes/Valdez) | NRFI | 61% | _pull at book_ | TBD | model lean — Valdez GB/sinker + MIN cold bats; cleanest NRFI tonight |
| 6/10 | LAD @ PIT (Ohtani/Jones) | YRFI | 56% | _pull at book_ | TBD | model lean — LAD elite top vs Jones carries the over |

---

## Running totals (update on every settle)
- **Record:** 0-0 (tracker opened 6/10/26). **NRFI:** 0-0 · **YRFI:** 0-0.
- **Staked:** $0 · **P/L:** $0.00 (no priced bets yet — tonight's three are model leans only).

> Tracked like `fades.md` / `bankroll.md`: any change → commit → push → PR → squash-merge.
> Settle each row off `mlb_api.sh` box scores (1st-inning line score) the next morning.
</content>
</invoke>
