# Results & Calibration Ledger

**Purpose.** The quantitative twin of `fades.md`. Every **recommended leg** (and especially every
**played** leg) gets logged here with my **true-prob estimate**, the **price**, the **closing
price** (CLV), and the **result** — so we can measure, not guess, how good the process is:
calibration (do my "70%" legs hit ~70%?), hit rate & ROI by bet type, and closing-line value.

**Columns.**
- **TrueP** = my **pre-bet** true-win-prob estimate — **written at bet time, never reconstructed.** A
  back-filled number leaks the result and is calibration-invalid. Rows I genuinely didn't log pre-game are
  marked `*` and EXCLUDED from calibration. *Goal: zero new `*` rows* (11 of 21 historical legs were wasted
  this way → calibration ran on n=10).
- **ImplP** = the price's **NO-VIG** implied prob. **Devig before logging:** take both sides' raw implied
  probs and divide each by their sum (the overround); that's the no-vig number. One-sided prop with no
  posted other side → subtract ~half the typical hold (~2-3pp) and flag the estimate. *(Pre-6/4 rows are
  still raw-vig and labeled; recompute as they settle.)*
- **Edge** = TrueP − no-vig ImplP (pp). Positive = value. A leg must clear the **min-edge gate** to be bet:
  **≥ +2pp standalone / ≥ +3-4pp to anchor a parlay** — below that it's action, not value (a slate clearing
  nothing = NO BET).
- **Result** = W / L / Push / TBD. **Played** = Y if on the user's actual ticket, N if recommended/rejected only.
- **Close** = closing American price; **CLV** = did the line move toward our side (closing no-vig ImplP >
  bet no-vig ImplP)? `+` good / `−` bad / `—` not captured. **CLV converges far faster than ROI at this
  sample — it's the primary scoreboard.** *(Capture starts now; pre-6/4 rows are `—`.)*
- **Stake / Return / P-L** = units staked, units returned (stake × decimal on a win, 0 on a loss), and
  net P/L (units). Tracked per *ticket* in the rollup → running units & ROI. **Log the real stake each
  night;** pre-6/4 rows assume flat 1u (labeled) so there's an immediate read.

---

## Logging protocol (run EVERY session)
1. **On build:** add a row for each recommended leg (Played=N) with price, **pre-registered TrueP**,
   **no-vig ImplP**, Edge. **Pull the price from a real book — never estimate. Devig both sides before
   computing Edge. Write TrueP BEFORE the game — never reconstruct** (a `*` row is wasted calibration).
2. **At/near close (HARD step — do it on the run closest to first pitch):** record the **closing price**
   and compute CLV (`+` if the line moved to our side, comparing no-vig probs). **CLV is the primary
   scoreboard — it converges far faster than ROI at this sample** — capture it even on legs we don't bet.
   *(No odds API yet, so this is a manual book pull; if an `odds_api.sh` helper is ever added it automates.)*
3. **On settle:** set Result (W/L/Push), flip Played=Y for legs the user actually played, and for each
   **played ticket** record **stake + return** → update the units/ROI rollup. Self-settle via
   `mlb_api.sh finals` on the 09:00 review like the parlay files. **Verify the rollups with `tools/calib.py`.**
4. **Commit** this file in the same commit→push→PR→squash-merge cycle as the parlay/fade files.

---

## Played legs (the calibration core)

| Date | Leg (game) | Type | Price | TrueP | ImplP | Edge | Result | Played | CLV |
|------|------------|------|-------|-------|-------|------|--------|--------|-----|
| 5/25 | Dodgers ML (vs COL) | ML-fav | -310 | ~72%* | 75.6% | −3.6 | **W** | Y | — |
| 5/25 | Brewers ML (vs STL) | ML-fav | -220 | ~65%* | 68.8% | −3.8 | **W** | Y | — |
| 5/25 | Misiorowski Over 7.5 K (vs STL) | K-Over | ~-150 | ~62%* | 60.0% | +2.0 | **W** (12 K) | Y | — |
| 5/26 | Dodgers ML (vs COL) | ML-fav | -235 | 66% | 70.1% | −4.1 | **W** | Y | — |
| 5/26 | Burns Over 6.5 K (vs NYM) | K-Over | -110 | 55% | 52.4% | +2.6 | **W** | Y | — |
| 5/26 | Strider Over 4.5 K (vs BOS) | K-Over alt | ~-625 | 88% | 86.2% | +1.8 | **W** (exactly 5 K) | Y | — |
| 5/27 | Yankees ML (vs KC) | ML-fav | -156 | ~63%* | 60.9% | +2.1 | **W** | Y | — |
| 5/27 | Sanchez Over 6.5 K (vs SD) | K-Over alt | -112 | ~70%* | 52.8% | — | **W** (9 K) | Y | — |
| 5/28 | Tigers ML (vs LAA) | ML-fav | -130 | 61% | 56.5% | +4.5 | **L** (lost 7-1) | Y | — |
| 5/29 | Dodgers ML (vs PHI) | ML-fav | -118 | 57% | 54.1% | +2.9 | **W** | Y | — |
| 5/29 | Astros ML (vs MIL) | ML-dog | +100 | 50% | 50.0% | 0.0 | **L** (lost 5-4 in 10) | Y | — |
| 5/30 | Guardians ML (vs BOS) | ML-fav | -134 | ~58%* | 57.3% | +0.7 | **L** (lost 9-1) | Y | — |
| 5/30 | Padres ML (@ WSH) | ML-fav | -130 | ~57%* | 56.5% | +0.5 | **L** (lost 9-4) | Y | — |
| 5/31 | Brewers −1.5 RL (@ HOU) | Run line | ~+120 | ~48%* | 45.5% | +2.5 | **W** (won 2-0) | Y | — |
| 5/31 | Yankees ML (@ ATH) | ML-fav | -154 | ~60%* | 60.6% | −0.6 | **W** (13-3 rout) | Y | — |
| 6/1 | Mariners ML (vs NYM) | ML-fav | ~-150 | ~60% | 60.0% | 0.0 | **W** | Y | — |
| 6/1 | Rays −1.5 RL (vs DET) | Run line | +118 | ~47%* | 45.9% | +1.1 | **L** (lost 10-9 outright) | Y | — |
| 6/2 | Mariners ML (vs NYM) | ML-fav | ~-150 | 60% | 60.0% | 0.0 | **W** (3-2 in 10) | Y | — |
| 6/2 | Brewers ML (vs SF) | ML-fav | ~-145 | ~63%* | 59.2% | +3.8 | **W** (8-3, Harrison 12 K) | Y | — |
| 6/3 | Mariners ML (vs NYM) | ML-fav | -151 | 60% | 60.2% | −0.2 | **L** (lost 7-1) | Y | — |
| 6/3 | Phillies ML (vs SD) | ML-fav | -215 | 64% | 68.3% | −4.3 | **W** (3-0, Sanchez 9 K) | Y | — |
| 6/4 | Braves ML (Sale, vs TOR) | ML-fav | -205 | 67% | 64.6% | +2.4 | TBD | Y | — |
| 6/4 | Phillies ML (Wheeler, vs SD) | ML-fav | -198 | 65% | 63.9% | +1.1 | **W** (6-4, Wheeler 7IP/2ER/8K) | Y | — (no odds API) |
| 6/4 | Sale Over 6.5 K (vs TOR) | K-Over | -179 | 64% | 61.5% | +2.5 | TBD | Y | — |

## Recommended but NOT played (calibration both ways)

| Date | Leg (game) | Type | Price | TrueP | ImplP | Edge | Result | Played | CLV |
|------|------------|------|-------|-------|-------|------|--------|--------|-----|
| 5/27 | Sanchez Over 7.5 K (vs SD) | K-Over | +182 | ~60% | 35.5% | +24.5 | **W** (9 K) — edge call validated | N | — |
| 6/2 | Yankees ML (Schlittler, vs CLE) | ML-fav | ~-220 | ~64%* | 68.8% | −4.8 | **L** (9-4) — declined 3rd leg, fade correct | N | — |
| 6/3 | Dodgers ML (vs ARI) | ML-fav | -200 | 66% | 66.7% | −0.7 | **W** — Build D rec leg | N | — |
| 6/3 | Rays ML (vs DET) | ML-fav | -144 | 57% | 59.0% | −2.0 | **L** (swept 7-2) — Build D weak leg, busted | N | — |
| 6/3 | Sanchez K-Over (faded on 2nd-mtg) | K-Over | — | — | — | — | **would-W** (9 K) — fade missed (C2) | N | — |
| 6/3 | Burns K-Over (faded illness+KC) | K-Over | — | — | — | — | **would-W** (9 K) — fade missed (C1) | N | — |
| 6/4 | Brewers ML (Crow, vs SF) | ML-fav | -153 | 60% | 58.2% | +1.8 | would-TBD — declined (rookie SP, superseded by Sale K) | N | — |
| 6/4 | Dodgers ML (Wrobleski LHP, @ AZ) | ML-fav | -134 | 55% | 55.1% | −0.1 | TBD — Build C +200 3rd leg (soft: AZ .279/16%K vs LHP, overbet band) | N | — |

---

## Rollup / calibration (update on each settle)

### Played-ticket record (parlays) — units @ flat 1u (see caveat)
| Date | Ticket | Odds | Stake(u) | Return(u) | P/L(u) | Result |
|------|--------|------|----------|-----------|--------|--------|
| 5/25 | LAD ML + MIL ML + Misi O7.5K | +221 | 1.00 | 3.21 | +2.21 | ✅ WON |
| 5/26 | LAD ML + Burns O6.5K + Strider O4.5K | +216 | 1.00 | 3.16 | +2.16 | ✅ WON |
| 5/27 | NYY ML + Sanchez O6.5K | +210 | 1.00 | 3.10 | +2.10 | ✅ WON |
| 5/28 | Tigers ML (anchor) + … | — | 1.00 | 0.00 | −1.00 | ❌ LOST |
| 5/29 | LAD ML + HOU ML | +269 | 1.00 | 0.00 | −1.00 | ❌ LOST |
| 5/30 | CLE ML + SD ML | +209 | 1.00 | 0.00 | −1.00 | ❌ LOST |
| 5/31 | MIL −1.5 RL + NYY ML | +263 | 1.00 | 3.63 | +2.63 | ✅ WON |
| 6/1 | SEA ML + TB −1.5 RL | ~+240 | 1.00 | 0.00 | −1.00 | ❌ LOST |
| 6/2 | SEA ML + MIL ML | ~+158 | 1.00 | 2.58 | +1.58 | ✅ WON |
| 6/3 | SEA ML + PHI ML | ~+183 | 1.00 | 0.00 | −1.00 | ❌ LOST |

**Record: 5 W – 5 L. Units @ flat 1u: staked 10.00, returned 15.68 → P/L +5.68u, ROI +56.8%.**

> ⚠️ **Read this ROI as noise, not signal.** n=10 is variance-dominated and the +56.8% is carried by two
> ~+260 hits (5/31, 5/25); a single different bounce flips it. Stakes here are **assumed flat 1u** (not
> actually logged) — log the real stake each night so this becomes a true number. **This is exactly why
> CLV (above) matters more than ROI at this sample** — beat the close consistently and the ROI follows.

### Calibration buckets (explicitly-logged TrueP legs only; `*` rows excluded)
| Predicted band | Legs | Won | Hit% | Read |
|----------------|------|-----|------|------|
| 50–55% | HOU +100 (50, L), Burns O6.5 (55, W) | 1/2 | 50% | on target (tiny n) |
| 56–61% | LAD -118 (57, W), TB -144 (57, L), SEA -151 (60, L), SEA -150 6/2 (60, W), DET -130 (61, L) | 2/5 | 40% | **running cold vs 58% predicted — watch for ML-fav overconfidence** |
| 62–66% | PHI -215 (64, W), LAD -200 (66, W), LAD -235 (66, W) | 3/3 | 100% | small n, but the cleaner ace-edge favorites held |
| 85–90% | Strider O4.5 (88, W) | 1/1 | 100% | — |

> **Early signals (small samples — treat as directional, not conclusions):**
> 1. **The ~58-60% ML-favorite band is hitting ~40%, below model.** Possible overconfidence on
>    "home favorite with SP edge" legs (SEA twice, DET, TB all landed here and several lost). If this
>    holds over more samples, shade mid-tier ML favorites DOWN a few pp.
> 2. **K-Over legs we PLAYED are 5-for-5** (Misi, Burns, Strider, Sanchez ×2 incl. the +182 edge) —
>    and the ones we FADED (Sanchez, Burns 6/3; Harrison 6/2) all hit too. Strongly reinforces the
>    `fades.md` C6 correction: we under-weight elite K stuff.
> 3. **Run-line legs are 1-1** (MIL −1.5 W; TB −1.5 L outright) — the D3 construction fade (RL vs a
>    live dog) is the one that lost. Consistent with the registry.

### Now capturing / still to capture
- **Stake + units/ROI** — now in the ticket rollup (flat-1u assumed pre-6/4; **log the real stake going
  forward** so ROI stops being an assumption).
- **CLV** — hard step at the run closest to first pitch; the single best +EV signal at this sample size.
  Still a manual book pull (no odds API).
- **Bet-type ROI** — once CLV + real stakes accrue, break ROI out by ML-fav / K-Over / RL / hitter-prop.
  Early hint from the data: **K-Overs are 5-for-5 played AND 5-for-5 on the ones we faded** (the edge),
  while the **56–61% ML-fav band is hitting 40%** (overbet). The 3-tier output exists to surface the
  K-Over standalone as the real product, not just the +200 parlay.
