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
- **Bucket** = **S** (standalone single / bankroll roll) or **P** (rode on a parlay ticket). Lets `calib.py`
  break out calibration & record by bucket — the measurement that *proves or disproves the parlay tax*
  (doctrine claims parlays run near -EV chalk+vig; this is how we test it). Going forward the diversify-markets
  direction should grow the **S** sample (more Tier-1 standalones), so the split becomes real.
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
   *(`tools/odds_api.sh clv <price> "<team>"` automates this per ML leg — or run `tools/clv_capture.py` on the 15:30/18:30 run to batch-propose all open-leg CLV fills in one shot. Props / totals / K-legs remain a manual book pull.)*
3. **On settle:** set Result (W/L/Push), flip Played=Y for legs the user actually played, and for each
   **played ticket** record **stake + return** → update the units/ROI rollup. Self-settle via
   `mlb_api.sh finals` on the 09:00 review like the parlay files. **Verify the rollups with `tools/calib.py`.**
4. **Commit** this file in the same commit→push→PR→squash-merge cycle as the parlay/fade files.

---

## Played legs (the calibration core)

| Date | Leg (game) | Type | Price | TrueP | ImplP | Edge | Result | Played | CLV | Bucket |
|------|------------|------|-------|-------|-------|------|--------|--------|-----|--------|
| 5/25 | Dodgers ML (vs COL) | ML-fav | -310 | ~72%* | 75.6% | −3.6 | **W** | Y | — | P |
| 5/25 | Brewers ML (vs STL) | ML-fav | -220 | ~65%* | 68.8% | −3.8 | **W** | Y | — | P |
| 5/25 | Misiorowski Over 7.5 K (vs STL) | K-Over | ~-150 | ~62%* | 60.0% | +2.0 | **W** (12 K) | Y | — | P |
| 5/26 | Dodgers ML (vs COL) | ML-fav | -235 | 66% | 70.1% | −4.1 | **W** | Y | — | P |
| 5/26 | Burns Over 6.5 K (vs NYM) | K-Over | -110 | 55% | 52.4% | +2.6 | **W** | Y | — | P |
| 5/26 | Strider Over 4.5 K (vs BOS) | K-Over alt | ~-625 | 88% | 86.2% | +1.8 | **W** (exactly 5 K) | Y | — | P |
| 5/27 | Yankees ML (vs KC) | ML-fav | -156 | ~63%* | 60.9% | +2.1 | **W** | Y | — | P |
| 5/27 | Sanchez Over 6.5 K (vs SD) | K-Over alt | -112 | ~70%* | 52.8% | — | **W** (9 K) | Y | — | P |
| 5/28 | Tigers ML (vs LAA) | ML-fav | -130 | 61% | 56.5% | +4.5 | **L** (lost 7-1) | Y | — | P |
| 5/29 | Dodgers ML (vs PHI) | ML-fav | -118 | 57% | 54.1% | +2.9 | **W** | Y | — | P |
| 5/29 | Astros ML (vs MIL) | ML-dog | +100 | 50% | 50.0% | 0.0 | **L** (lost 5-4 in 10) | Y | — | P |
| 5/30 | Guardians ML (vs BOS) | ML-fav | -134 | ~58%* | 57.3% | +0.7 | **L** (lost 9-1) | Y | — | P |
| 5/30 | Padres ML (@ WSH) | ML-fav | -130 | ~57%* | 56.5% | +0.5 | **L** (lost 9-4) | Y | — | P |
| 5/31 | Brewers −1.5 RL (@ HOU) | Run line | ~+120 | ~48%* | 45.5% | +2.5 | **W** (won 2-0) | Y | — | P |
| 5/31 | Yankees ML (@ ATH) | ML-fav | -154 | ~60%* | 60.6% | −0.6 | **W** (13-3 rout) | Y | — | P |
| 6/1 | Mariners ML (vs NYM) | ML-fav | ~-150 | ~60% | 60.0% | 0.0 | **W** | Y | — | P |
| 6/1 | Rays −1.5 RL (vs DET) | Run line | +118 | ~47%* | 45.9% | +1.1 | **L** (lost 10-9 outright) | Y | — | P |
| 6/2 | Mariners ML (vs NYM) | ML-fav | ~-150 | 60% | 60.0% | 0.0 | **W** (3-2 in 10) | Y | — | P |
| 6/2 | Brewers ML (vs SF) | ML-fav | ~-145 | ~63%* | 59.2% | +3.8 | **W** (8-3, Harrison 12 K) | Y | — | P |
| 6/3 | Mariners ML (vs NYM) | ML-fav | -151 | 60% | 60.2% | −0.2 | **L** (lost 7-1) | Y | — | P |
| 6/3 | Phillies ML (vs SD) | ML-fav | -215 | 64% | 68.3% | −4.3 | **W** (3-0, Sanchez 9 K) | Y | — | P |
| 6/4 | Braves ML (Sale, vs TOR) | ML-fav | -205 | 67% | 64.6% | +2.4 | **L** (TOR 7-2 — bullpen game won outright) | Y | — (no odds API) | P |
| 6/4 | Phillies ML (Wheeler, vs SD) | ML-fav | -198 | 65% | 63.9% | +1.1 | **W** (6-4, Wheeler 7IP/2ER/8K) | Y | — (no odds API) | P |
| 6/4 | Sale Over 6.5 K (vs TOR) | K-Over | -179 | 64% | 61.5% | +2.5 | **L** (5.2 IP, 6 K — one-tier-deeper alt O5.5 would've cashed) | Y | — (no odds API) | S |
| 6/5 | Mariners ML (Woo, @ DET) | ML-fav | -120 | 59% | 52.2% | **+6.8** | **L** (lost 3-7) — slate's sharpest edge, +EV bet/variance loss. Grade: **+EV (good bet)** | Y | + | P |
| 6/5 | Dodgers ML (Sasaki, vs LAA) | ML-fav | -188 | 66% | 62.7% | +3.3 | **W** (won 1-0) — Tier 2 leg + bankroll. Grade: **+EV** | Y | + | P |

## Recommended but NOT played (calibration both ways)

| Date | Leg (game) | Type | Price | TrueP | ImplP | Edge | Result | Played | CLV | Bucket |
|------|------------|------|-------|-------|-------|------|--------|--------|-----|--------|
| 5/27 | Sanchez Over 7.5 K (vs SD) | K-Over | +182 | ~60% | 35.5% | +24.5 | **W** (9 K) — edge call validated | N | — | S |
| 6/2 | Yankees ML (Schlittler, vs CLE) | ML-fav | ~-220 | ~64%* | 68.8% | −4.8 | **L** (9-4) — declined 3rd leg, fade correct | N | — | P |
| 6/3 | Dodgers ML (vs ARI) | ML-fav | -200 | 66% | 66.7% | −0.7 | **W** — Build D rec leg | N | — | P |
| 6/3 | Rays ML (vs DET) | ML-fav | -144 | 57% | 59.0% | −2.0 | **L** (swept 7-2) — Build D weak leg, busted | N | — | P |
| 6/3 | Sanchez K-Over (faded on 2nd-mtg) | K-Over | — | — | — | — | **would-W** (9 K) — fade missed (C2) | N | — | S |
| 6/3 | Burns K-Over (faded illness+KC) | K-Over | — | — | — | — | **would-W** (9 K) — fade missed (C1) | N | — | S |
| 6/4 | Brewers ML (Crow, vs SF) | ML-fav | -153 | 60% | 58.2% | +1.8 | **would-L** (SF 12-9 — declining the rookie SP was correct) | N | — | P |
| 6/4 | Dodgers ML (Wrobleski LHP, @ AZ) | ML-fav | -134 | 55% | 55.1% | −0.1 | **L** (AZ 3-2) — Build C +200 3rd leg busted; ~fair price, fav-not-safe | N | — | P |
| 6/5 | Mariners ML / Dodgers ML | — | — | — | — | — | **PLAYED → settled in the played-legs table above (SEA L 3-7, LAD W 1-0)** | Y | + | P |
| 6/5 | Yankees ML (Weathers, vs BOS) | ML-fav | -144 | 56% | 56.7% | −0.7 | **L** (lost 5-3) — Tier 3 +200 leg flagged soft; the soft flag was right. Grade: **~fair/thin -EV (correct decline)** | N | = | P |
| 6/5 | Phillies ML (Luzardo, vs CWS) | ML-fav | -188 | 62% | 64.0% | −2.0 | **W** (won 8-6) — scan-only PASS; CWS B1 dog lost. Grade: **-EV pass (would-W)** | N | — | S |
| 6/5 | D-backs ML (Kelly, vs WSH) | ML-fav | -134 | 50% | 56.7% | −6.7 | **W (fade)** (AZ lost 1-14) — scan-only REJECT; Kelly 5.06 own-SP trap (D4) validated hard. Grade: **correct reject** | N | — | S |
| 6/6 | Dodgers ML (Yamamoto, vs LAA) | ML-fav | -182 | 64.7% | 61.7% | +3.0 | TBD — Build A Tier 1 + bankroll roll 2 (logged @ −182; line later moved to −350). Grade: **+EV (clears gate)** | N | — | S |
| 6/6 | Braves ML (Strider, vs PIT) | ML-fav | -146 | 58.1% | 57.1% | +1.0 | **SUPERSEDED → Build B** (line moved −146 → −112 pick'em; ATL no longer a floor leg). Grade: ~fair/thin | N | — | P |
| 6/6 | Cardinals ML (Liberatore, vs CIN) | ML-fav | -126 | 54% | 53.7% | +0.3 | **SUPERSEDED → Build B** (Build A +200-chase 3rd leg dropped, D1). Grade: -EV chase | N | — | P |
| 6/6 | Dodgers ML (Yamamoto, vs LAA) — Build B | ML-fav | -350 | 77.7% | 74.7% | +3.0 | TBD — Build B anchor (line re-pulled −350); ace-edge holds at the heavier number. Grade: **+EV (clears gate)** | N | — | P |
| 6/6 | Yamamoto Over 7.0 K (vs LAA) | K-Over | +142 | 44.8% | 38.8% | +6.0 | **SUPERSEDED → Build C** (line moved O7.0 → O7.5; +142 no longer exists). Grade: was +EV | N | — | S |
| 6/6 | TB ML (McClanahan, @ MIA) | ML-fav | -144 | 58% | 56.7% | +1.3 | **SUPERSEDED → Build C** (game started — status gate fails). Grade: ~fair/thin | N | — | P |
| 6/6 | Dodgers ML (Yamamoto, vs LAA) — Build C | ML-fav | -340 | 78% | 75.7% | +2.3 | TBD — Build C anchor (line −350 → −340); +2.3pp, borderline D2 heavy anchor (payout driven by the correlated K leg). Grade: **+EV (clears gate)** | N | — | P |
| 6/6 | Yamamoto Over 7.5 K (vs LAA) — Build C | K-Over | +115 | 48% | 45.4% | +2.6 | TBD — Build C Tier 1 standalone + +200 leg; recent 8/8/8/3/10 (4/5 cleared 8K), LAA 25% K vs RHP, first mtg. Needs 8 K (season 8+ = 4/11). Grade: **+EV (high-variance)** | N | — | S |
| 6/6 | Yamamoto Over 6.5 K alt (vs LAA) — Build C | K-Over alt | -186 | 63% | 60.8% | +2.2 | TBD — Build C Tier-2 safer K expression (needs 7 K). Grade: **+EV thin** | N | — | P |
| 6/6 | Dodgers ML (Yamamoto, vs LAA) — Build D | ML-fav | -345 | 78% | 75.7% | +2.3 | TBD — Build D final anchor (line −340 → −345); +2.3pp, borderline D2 heavy anchor (payout driven by the correlated K leg). Grade: **+EV (clears gate)** | N | — | P |
| 6/6 | Yamamoto Over 7.5 K (vs LAA) — Build D | K-Over | +110 | 48% | 44.4% | +3.6 | TBD — Build D Tier 1 standalone + the +171 +200-build leg; best Over +110 (BetRivers). Needs 8 K (season 8+ = 4/11; recent 4/5). Grade: **+EV (high-variance)** | N | — | S |

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
| 6/4 | PHI ML + ATL ML | +124 | 1.00 | 0.00 | −1.00 | ❌ LOST (PHI W 6-4, **ATL L 7-2** — ATL leg killed it) |
| 6/5 | SEA ML + LAD ML | +181 | 1.00 | 0.00 | −1.00 | ❌ LOST (**SEA L 3-7** — our sharpest edge; LAD W 1-0 — the won leg) |
| 6/6 | LAD ML −350 + Yamamoto O7.0K +142 (SGP, +corr) | +211 | — | — | — | **SUPERSEDED → Build C** (O7.0 line gone; recomputed at O7.5) |
| 6/6 | LAD ML −340 + Yamamoto O7.5K +115 (indep/+corr) | +178 | — | — | — | TBD (Build C Tier 3; true comb 40.5%, EV +12.8% — take indep product or SGP ≥ +147) |

**Record: 5 W – 7 L. Units @ flat 1u: staked 12.00, returned 15.68 → P/L +3.68u, ROI +30.7%.**

> **6/5 is the parlay tax, on the board:** the LAD leg cashed standalone (bankroll won) but the SEA×LAD
> *parlay* lost. Two individually-+EV favorites stacked = ~38% combined → the ticket dies the majority of
> nights regardless of leg quality. Standalone-vs-parlay EV split now reads: **standalone bankroll/Tier-1
> legs trending +, parlay tickets 5-7 / ROI bleeding toward breakeven** — the doctrine's "parlays are
> near-EV chalk+vig" claim is accumulating evidence.

> **6/4 standalone (separate from the parlay table):** Sale Over 6.5 K −179 — **LOST** (5.2 IP / 6 K).
> First K-Over loss in the log (played K-Overs now **5-for-6**). The lone suppressor (TOR 19% K / .213
> vs LHP) was real, and the **one-tier-deeper alt O5.5 would have cashed** — a live confirmation of the
> safety-vs-EV tiebreaker (the deeper alt on an unattended K leg).

> ⚠️ **Read this ROI as noise, not signal.** n=10 is variance-dominated and the +56.8% is carried by two
> ~+260 hits (5/31, 5/25); a single different bounce flips it. Stakes here are **assumed flat 1u** (not
> actually logged) — log the real stake each night so this becomes a true number. **This is exactly why
> CLV (above) matters more than ROI at this sample** — beat the close consistently and the ROI follows.

### Calibration buckets (reconciled to `calib.py` 2026-06-06 settle; `*` rows excluded)
| Band (calib.py) | n | W-L | Hit% | vs mid | Read |
|----------------|---|-----|------|--------|------|
| 50–54 | 1 | 0-1 | 0% | 52.5 | HOU +100 (L) — tiny n |
| 55–59 | 3 | 2-1 | 67% | 57.5 | +SEA 59 (L, 6/5 — sharpest edge, variance loss) |
| 60–64 | 6 | 3-3 | 50% | 62.5 | **⚠ under (overconfident)** — incl. Sale O6.5K 64 (L) |
| 65–69 | 4 | 3-1 | 75% | 67.5 | PHI 65 (W), LAD 66 (W ×2, incl 6/5), **ATL 67 (L, 6/4)** |
| 85–89 | 1 | 1-0 | 100% | 87.5 | Strider O4.5 (W) |
| **TOTAL** | **15** | **9-6** | | | |

> **Early signals (small samples — treat as directional, not conclusions):**
> 1. **The 60-64 band is now 3-3 (50%), under its ~62.5% midpoint** — the ML-favorite-overconfidence
>    flag persists, and the **65-69 band took its first loss (ATL 67, 6/4)**: a heavy ace-at-home fav
>    that I'd *bumped* to 69% on "TOR is a bullpen game" logic lost outright 7-2. **Bullpen-game ≠ ML
>    boost** (new fades.md D5) — do NOT shade a fav UP for a no-starter opponent; the pen can shut your
>    offense down AND the lineup can tee off on your ace.
> 2. **Played K-Overs took their first loss → 5-for-6** (Sale O6.5K 6/4, 6 K in 5.2 IP). The lone
>    suppressor (TOR 19% K / .213 vs LHP) was real and the **one-tier-deeper O5.5 alt would've cashed** —
>    the safety-vs-EV tiebreaker (deeper alt on an unattended K leg) is validated, not the standard line.
> 3. **Run-line legs are 1-1** (MIL −1.5 W; TB −1.5 L outright) — D3 (RL vs a live dog) consistent.

### Now capturing / still to capture
- **Stake + units/ROI** — now in the ticket rollup (flat-1u assumed pre-6/4; **log the real stake going
  forward** so ROI stops being an assumption).
- **CLV** — hard step at the run closest to first pitch; the single best +EV signal at this sample size.
  Still a manual book pull (no odds API).
- **Bet-type ROI** — once CLV + real stakes accrue, break ROI out by ML-fav / K-Over / RL / hitter-prop.
  Early hint from the data: **played K-Overs are 5-for-6** (first loss Sale 6/4, where the deeper alt
  would've cashed), while the **60-64 ML-fav band is 50%** (overbet). The 3-tier output exists to surface
  the K-Over standalone as the real product, not just the +200 parlay.
