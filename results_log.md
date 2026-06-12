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
| 6/7 | deGrom (TEX) ML (vs CLE) | ML-fav | -140 | 60.1% | 57.1% | +3.0 | **W** (TEX 10-0, deGrom dealt) — Build A Tier 1 standalone + bankroll roll 3; ace edge (3.48/10.86 K9). Grade: **+EV (clears gate)** | N | + (live, line ran to −10000) | S |
| 6/7 | Braves ML (Elder, vs PIT) | ML-fav | -145 | 60% | 57.9% | +2.1 | **W** (ATL 3-2 PIT) — Build A Tier 2/3 partner; elite team + Elder 2.63, D5 caution applied. Grade: **+EV (thin)** | N | + 85%cl | P |
| 6/7 | LAD ML (Sheehan, vs LAA) | ML-fav | -210 | 63% | 66.3% | −3.3 | **would-L** (LAD 5-13 LAA — correct reject confirmed; offense-driven heavy price busted vs ace Soriano 2.72). Grade: **correct reject (−EV)** | N | + 85%cl | P |
| 6/7 | PHI ML (Nola, vs CWS) | ML-fav | -161 | 53% | 61.5% | −8.5 | **W** (PHI 9-5 — would-W; D4 trap fav won this time, fades.md D4 → 3-1) — scan REJECT; Nola 5.55 own-SP trap (D4) + CWS B1 dog. Grade: **correct reject (−EV process); outcome won** | N | + 85%cl | S |
| 6/8 | Sánchez Over 6.5 K (vs TOR) | K-Over | +100 | 58% | 46.9% | +11.1 | **SUPERSEDED → Build B** (price improved +100 → +116; lineups now posted, leg LIVE). Grade: was +EV | N | — | S |
| 6/8 | Sánchez Over 6.5 K (vs TOR) — Build B | K-Over | +116 | 58% | 43.7% | +14.3 | **W** (10 K in 7 IP vs TOR — sailed over 6.5) — Build B Tier 1 standalone (DraftKings). Devig O+116/U-148; market leaned harder Under (no-vig 56.3%) and was WRONG. Grade: **+EV (clears gate), WON** | Y | − (U juiced to -148) | S |
| 6/8 | PHI ML + Sánchez O6.5K SGP (vs TOR) — Build B **[CHOSEN BY USER]** | Parlay (+corr) | +248 ind / SGP TBD | 44.1% | 28.8% | +15.4 (ind) | **W** (PHI 5-2 TOR + Sánchez 10 K — BOTH legs cashed) — Build B Tier 3 best +200; same-game pos-corr (ρ≈+0.30), true comb 44.1% (the high-floor +200 answer hit). Grade: **+EV, WON** | Y | — | P |
| 6/8 | PHI ML (Sánchez, vs TOR) | ML-fav | -165 | 63.8% | 60.8% | +3.0 | **W** (PHI 5-2 TOR) — Build A Tier 2 anchor + bankroll roll 4 (4-WIN TARGET HIT); ace edge (1.46/10.74), PHI L15 7-3. Grade: **+EV (clears gate), WON** | Y | − 60%cl | P |
| 6/8 | MIL ML (Harrison, vs ATH) | ML-fav | -141 | 60.4% | 57.4% | +3.0 | **W** (MIL 15-14 ATH — wild slugfest, MIL held on) — Build A Tier 2/3 anchor; ace edge (1.57/11.46) + hot team 40-23/+105. Grade: **+EV (clears gate), WON** | N | − 56%cl | P |
| 6/8 | HOU ML (Arrighetti, vs LAA) | ML-fav | -126 | 56% | 54.5% | +1.5 | **W** (HOU 5-4 LAA — thin opponent-driven fav held on) — Build A Tier 3 +200 leg; Arrighetti 1.94 vs G-Rod 9.50; HOU 30-37 but the SP-edge carried. Grade: **thin +EV, WON.** ⚠️ settle.py mis-flagged this L (team-side parser confused HOU-away by "vs LAA"); StatsAPI final HOU 5-4 confirms W | N | | P |
| 6/9 | MIA ML (Meyer, vs AZ) | ML-fav | -129 | 59% | 56.5% | +2.5 | **W (MIA 10-6 AZ)** — Tier 1 standalone + bankroll roll 1 cashed; Meyer solid, MIA bats erupted. Grade: **+EV (clears gate) — correct, won** | Y | − 55%cl | S |
| 6/9 | ATL ML (Holmes, vs CWS) | ML-fav | -148 | 60% | 58.9% | +1.1 | **L (ATL 5-6 CWS)** — D5 validated 2nd time: CWS bullpen game (Eisert opener) beat the best team in baseball. ATL held 60% (not boosted) = correct, but +1.1pp = action not value. Grade: **near-fair (thin) — correct grade, lost** | Y | = 58%cl | P |
| 6/9 | Meyer O5.5 K (vs AZ) | K-Over | -113 | 50% | 49.5% | +0.5 | **(not bet)** AZ C1 contact suppressor → correctly dropped. Result: Meyer settle for reference. Grade: **no edge, correctly not bet** | N | — | S |
| 6/9 | Burns O6.5 K (@ SD) | K-Over | -148 | 70% | 56.1% | +13.9 | **W (7 K in 5.1 IP — OVER 6.5)** — surfaced as a Tier-1 standalone candidate (not bet); SD 23% K vs RHP = neutral (no C1), C6 elite-arm. Big edge HIT. **NOTE: I twice mis-settled this mid-game (called it "pulled at 4.2/6 K, under") — corrected; a K count only rises, settle at Final.** Grade: **+EV (big edge) — correct, won** | N | — | S |
| 6/9 | ATL ML + MIA ML (+200 build) | Parlay (indep) | +195 | 35.4% | 33.9% | +1.5 | **❌ LOST (−$30): MIA W, ATL L (D5 trap).** PLAYED, $30 @ +195. MIA leg cashed; ATL killed it. K-Over reality (vs the codified swap-the-weak-leg lesson): MIA+**Cease** O6.5K (11K), +**Skenes** O6.5K (7K), OR +**Burns** O6.5K (**7 K** — my standalone rec, HIT) all WOULD'VE cashed; only **Wheeler 5K** under. **3 of 4 candidate ace K-Overs hit** — swapping the thin ATL leg for ANY of the three turns the −$30 loss into a win. Lesson = process (price + pick by edge), strongly validated this slate. Grade: **+EV thin (action not value) — lost on the thin ATL leg, as flagged** | Y | | P |
| 6/10 | Rasmussen Over 4.5 K (vs BOS) | K-Over | -155 | 64% | 56.7% | +7.3 | **W (13 K in 7.0 IP vs BOS)** — Build A Tier 1 standalone (sharpest edge on board) CASHED HUGE. 9 K last out 6/5; 8/12 starts 5+ K; BOS neutral K%. The +7.3pp edge hit emphatically. Grade: **+EV (clears gate) — correct, won** | N | — | S |
| 6/10 | TB ML (Rasmussen, vs BOS) | ML-fav | -141 | 60% | 57.2% | +2.8 | **W (TB 7-5 BOS)** — Build A Tier 2 leg + bankroll attempt-3 roll 2 cashed; Rasmussen dealt (13 K). Grade: **+EV (clears gate) — correct, won** | Y | — | P |
| 6/10 | LAD ML (Ohtani, @ PIT) | ML-fav | -195 | 67% | 65.3% | +1.7 | **L (LAD 8-9 PIT)** — Build B Tier 2/3 anchor + **bankroll attempt-3 roll 3 (BUSTS)**; Ohtani-led LAD coughed up a lead to PIT (B2 dog cashed). Thin +EV leg, lost. Grade: **thin +EV (ace-edge floor leg), LOST** | N | − 54%cl | P |
| 6/10 | PHI ML (Luzardo, @ TOR) | ML-fav | -132 | 57% | 55.6% | +1.4 | **W (PHI 7-4 TOR)** — Tier 3 +200 second leg; Luzardo held, PHI won. Grade: **~fair/thin, WON** | N | − 54%cl | P |
| 6/10 | SD ML (King, vs CIN) | ML-fav | -156 | 58% | 59.7% | −1.7 | **W (SD 5-4 CIN)** — scan REJECT (didn't play); SD won despite cold form. Grade: **-EV reject — won anyway (variance)** | N | — | S |
| 6/10 | DET ML (Valdez, vs MIN) — Build B | ML-fav | -163 | 61.5% | 60.8% | +0.7 | **L (DET 4-6 MIN)** — Build B leg; under-gate (+0.7pp), DET lost to cold MIN. Grade: **~fair/thin (under gate), LOST** | N | = 61%cl | P |
| 6/10 | ATL ML (Sale, vs CWS) — Build B | ML-fav | -142 | 59.4% | 57.4% | +2.0 | **L (ATL 1-2 CWS)** — Build B Tier 1 standalone; Sale dealt but ATL bats silent vs B1 CWS home dog (D5 trap again — CWS 2-1). Grade: **+EV (cleared gate) — correct decision, LOST** | N | + 58%cl | P |
| 6/11 | NYM ML (Scott, vs STL) | ML-fav | -138 | 56.6% | 59% | +2.4 | **W** (NYM 5-4 STL) — Build A Tier 1 standalone + **bankroll attempt-4 roll 1 CASHED ($10→$17.25)**; Scott 2.50/10.25 K9 ace edge held STL. Grade: **+EV (cleared +2pp gate) — good bet, won** | Y | — | S |
| 6/11 | LAD ML (Wrobleski, @ PIT) | ML-fav | -163 | 60.8% | 62% | +1.2 | **W** (LAD 8-6 PIT) — Build A Tier 2 + Tier 3 anchor; LAD elite outlasted re-heating PIT (B2). Grade: **thin +EV (high-floor leg) — won** | N | — | P |
| 6/11 | MIA ML (Phillips, vs AZ) | ML-fav | -115 | 52.4% | 54% | +1.6 | **W** (MIA 2-0 AZ) — Build A Tier 3 leg + **USER PARLAY (NYM×MIA $10→$32.24)**; Phillips + MIA shut out cold AZ again. Grade: **thin +EV — won** | Y | — | P |
| 6/11 | DET ML (vs MIN) | ML-fav (A3 fade) | -122 | — | — | — | **L for the fade** (DET won 11-0 as fav) — A3 fade-as-fav MISSED; logged for fade calibration, not bet | N | — | S |
| 6/11 | LAD ML (Wrobleski, @ PIT) — Build B anchor | ML-fav | -166 | 61.1% | 62% | +0.9 | **W** (LAD 8-6 PIT) — Build B Tier-1 single + correlated-parlay anchor. Grade: **thin (under +2pp gate) standalone — won** | N | — | P |
| 6/11 | Shohei Ohtani Over 1.5 TB (vs Keller) | hitter-prop | -120 | 52.8% | 54% | +1.2 | **W** (Ohtani 2-4, HR, 5 TB) — Build B correlated complement; cleared easily. Grade: **thin standalone — won** | N | — | P |
| 6/11 | Shohei Ohtani Over 1.5 TB (vs Keller) — Build C | hitter-prop | -125 | 54% | 52.0% | +2.0 | **W** (Ohtani 2-4, HR, 5 TB) — Build C Tier-1 standalone, cleared +2pp gate and cashed. Grade: **+EV standalone — won** | N | — | P |
| 6/11 | Freddie Freeman Over 1.5 TB (vs Keller) — Build C | hitter-prop | -115 | 50% | 49.9% | +0.1 | **L** (Freeman 1-4, 1 TB) — Build C Tier-3 +200 complement; needed 2+ bases, got a single. Grade: **~fair standalone (under gate) — lost (variance, correct read it was a coin-flip)** | N | — | P |
| 6/12 | SEA ML (B. Miller, @ WSH) | ML-fav | -140 | 57.2% | 60% | +2.8 | **TBD** — Build A Tier 1 standalone + Tier 2/3 anchor + **bankroll attempt-4 roll 2**. Miller 1.33/0.78, 9K last out (6/6) vs WSH/Littell. Grade: **+EV (clears +2pp gate)** | N | — | S |
| 6/12 | TB ML (McClanahan, vs LAA) | ML-fav | -160 | 60.1% | 62% | +1.9 | **TBD** — Build A Tier 2 leg. McClanahan 2.85/8.85 vs LAA 27-42; 2nd-mtg + last-2 4ER shave it. Grade: **thin +EV (under gate, high-floor)** | N | — | P |
| 6/12 | MIN ML (J. Ryan, vs STL) | ML-fav | -131 | 55.5% | 57% | +1.5 | **TBD** — Build A Tier 3 (+200) leg. Joe Ryan 3.07/9.90 vs Leahy; live risk STL hot (L10 7-3). Grade: **thin +EV (under gate)** | N | — | P |
| 6/12 | BAL ML (Baz, vs SD) | ML-fav | -124 | 54.3% | 56% | +1.7 | **TBD** — Build A alt-Tier 3 leg. Baz K-stuff vs slumping SD (L10 3-7). Grade: **thin +EV (under gate)** | N | — | P |
| 6/6 | Dodgers ML (Yamamoto, vs LAA) | ML-fav | -182 | 64.7% | 61.7% | +3.0 | **W** (LAD 9-2) — Build A Tier 1 + bankroll roll 2 (logged @ −182). Grade: **+EV (clears gate)** | N | — | S |
| 6/6 | Braves ML (Strider, vs PIT) | ML-fav | -146 | 58.1% | 57.1% | +1.0 | **SUPERSEDED → Build B** (line moved −146 → −112 pick'em; ATL no longer a floor leg). Grade: ~fair/thin | N | — | P |
| 6/6 | Cardinals ML (Liberatore, vs CIN) | ML-fav | -126 | 54% | 53.7% | +0.3 | **SUPERSEDED → Build B** (Build A +200-chase 3rd leg dropped, D1). Grade: -EV chase | N | — | P |
| 6/6 | Dodgers ML (Yamamoto, vs LAA) — Build B | ML-fav | -350 | 77.7% | 74.7% | +3.0 | **W** (LAD 9-2) — Build B anchor. Grade: **+EV (clears gate)** | N | — | P |
| 6/6 | Yamamoto Over 7.0 K (vs LAA) | K-Over | +142 | 44.8% | 38.8% | +6.0 | **SUPERSEDED → Build C** (line moved O7.0 → O7.5; +142 no longer exists). Grade: was +EV | N | — | S |
| 6/6 | TB ML (McClanahan, @ MIA) | ML-fav | -144 | 58% | 56.7% | +1.3 | **SUPERSEDED → Build C** (game started — status gate fails). Grade: ~fair/thin | N | — | P |
| 6/6 | Dodgers ML (Yamamoto, vs LAA) — Build C | ML-fav | -340 | 78% | 75.7% | +2.3 | **W** (LAD 9-2) — Build C anchor. Grade: **+EV (clears gate)** | N | — | P |
| 6/6 | Yamamoto Over 7.5 K (vs LAA) — Build C | K-Over | +115 | 48% | 45.4% | +2.6 | **L** (4 K in 8 IP — cruised to contact in a win) — Build C Tier 1. Grade: **+EV (high-variance, lost; right-tail didn't show)** | N | — | S |
| 6/6 | Yamamoto Over 6.5 K alt (vs LAA) — Build C | K-Over alt | -186 | 63% | 60.8% | +2.2 | **L** (4 K, needed 7) — Build C Tier-2 safer K expr. Grade: **+EV thin (lost)** | N | — | P |
| 6/6 | Dodgers ML (Yamamoto, vs LAA) — Build D | ML-fav | -345 | 78% | 75.7% | +2.3 | **W** (LAD 9-2) — Build D final anchor. Grade: **+EV (clears gate)** | N | — | P |
| 6/6 | Yamamoto Over 7.5 K (vs LAA) — Build D | K-Over | +110 | 48% | 44.4% | +3.6 | **L** (4 K in 8 IP) — Build D Tier 1 + the +171 +200-build leg. Grade: **+EV (high-variance, lost)** | N | — | S |
| 6/6 | TOR Blue Jays live ML (vs BAL) — USER PLAYED | ML | -191 | * | — | — | **W** (TOR 6-4) — user Ticket 1 leg; live-ML, not in any build | Y | — | P |
| 6/6 | CLE Guardians ML (vs TEX) — USER PLAYED | ML | +101 | * | — | — | **W** (CLE 6-0) — user Ticket 1 leg; pick'em value side | Y | — | P |
| 6/6 | CLE Guardians -5.5 RL (vs TEX) — USER PLAYED | RL | -130 | * | — | — | **W** (CLE 6-0, by 6) — user Ticket 2 leg | Y | — | P |
| 6/6 | LA Dodgers -1.5 RL (vs LAA) — USER PLAYED | RL | (SGP) | * | — | — | **W** (LAD 9-2, won by 7) — user Ticket 2 SGP leg | Y | — | P |
| 6/6 | Kochanowicz Over 5.5 hits allowed (LAA, vs LAD) — USER PLAYED | Hit-prop | (SGP) | * | — | — | **W** (pulled 0.1 IP / 6 ER, cleared early) — user Ticket 2 SGP leg | Y | — | P |

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
| 6/6 | LAD ML −340 + Yamamoto O7.5K +115 (indep/+corr) | +178 | — | — | **L** (Yamamoto 4 K — K leg busted; LAD won) — Build C/D Tier 3 +200 build |
| 6/6 | **USER** TOR live ML −191 + CLE ML +101 | +206 | $10 | $30.62 | **+$20.62** | ✅ WON (both ML hit; user's own ticket, not a build) |
| 6/6 | **USER** CLE −5.5 RL + (LAD −1.5 RL + Kochanowicz O5.5 hits SGP) | +289 | $30 | $116.76 | **+$86.76** | ✅ WON all 3 (CLE −5.5, Kocha O5.5 hits, LAD −1.5 final 9-2 by 7). RIDE call correct. |
| 6/7 | deGrom TEX −140 + ATL −145 (indep, 2 games) | +190 | 1.00 | 2.90 | +1.90 | ✅ WON (Build A Tier 2/3; TEX 10-0 + ATL 3-2 — both legs cashed; true comb 36.1%, EV +4.4% — the high-chance +200-area answer hit) |
| 6/8 | **USER** PHI ML + Sánchez O6.5K SGP (pos-corr) | **+167 (FanDuel SGP)** | $10 | $26.70 | **+$16.70** | ✅ WON (PHI 5-2 + Sánchez 10 K; true comb 44.1% vs breakeven 37.5% → **edge +6.6pp, EV +17.7%**). Pos same-game corr, high-floor +200 build cashed at a +EV booked price. |
| 6/9 | **USER** MIA ML + ATL ML (Build C) | +195 | $30 | $0.00 | **−$30.00** | ❌ LOST (MIA W 10-6 ✅ + **ATL L 5-6 to CWS bullpen game — D5 trap, 2nd validation**). Thin +1.5pp ticket (action not value, as flagged); the won leg was the Tier-1 standalone MIA. Sharper same-payout MIA+Cease/Skenes O6.5K would've cashed (Wheeler 5K would've lost; Burns still live — TBD). |
| 6/10 | TB ML −141 + Rasmussen O4.5K −155 (SGP, +corr) | +181 indep | 1.00 | 2.81 | +1.81 | **✅ WON** (Build A Tier 2; TB 7-5 + Rasmussen 13 K — both legs cashed; true comb 45.5%, EV +27.8% — the highest-floor ticket hit, the diversify-era pos-corr template) |
| 6/10 | TB ML −141 × PHI ML −132 | +201 | — | — | — | **✅ WON** (Build A Tier 3 — TB 7-5 + PHI 7-4 both cashed; the +200 stamp hit despite the ~11pp floor drop vs Tier 2) |
| 6/10 | LAD ML −195 + ATL ML −142 (Build B Tier 2) | +158 | — | — | — | **❌ LOST** (highest-floor 2-leg; both legs LOST — LAD 8-9 PIT, ATL 1-2 CWS; true comb was 39.5% — the recommended "highest-chance" ticket bricked, both favs fell) |
| 6/10 | LAD ML −195 × DET ML −163 × ATL ML −142 (Build B Tier 3) | +316 | — | — | — | **❌ LOST** (all 3 favs lost — LAD, DET, ATL; the +200-zone 3-legger; D1 floor-drop trade-off — moot, every leg fell) |
| 6/10 | ATL ML −147 × PHI ML −129 (Build C Tier 3 — the +200) | +198 | — | — | — | **❌ LOST** (ATL 1-2 CWS killed it; PHI leg won. Genuine +200 build, one leg busted) |
| 6/10 | LAD ML −198 × ATL ML −147 (Build C Tier 2) | +153 | — | — | — | **❌ LOST** (both legs LOST — LAD + ATL; the drift-fair 2-leg) |
| 6/11 | NYM ML −138 × LAD ML −163 (Build A Tier 2) | +178 | — | — | — | **W** (both legs cashed: NYM 5-4 + LAD 8-6; highest-floor 2-leg, true comb **36.6%**) |
| 6/11 | LAD ML −163 × MIA ML −115 (Build A Tier 3 — the +200) | +202 | — | — | — | **W** (both legs cashed: LAD 8-6 + MIA 2-0; genuine +200, true comb **33.5%**) |
| 6/11 | LAD ML −166 × Ohtani O1.5 TB −120 (Build B — correlated +200) | +194 | 33.5% | 40.7% | +6.7 | **W** (LAD 8-6 + Ohtani 5 TB) — correlated +200 build cashed; the diversify-era template. |
| 6/11 | LAD ML −171 × Ohtani O1.5 TB −125 (Build C Tier 2 — highest floor) | +185 | 33.5% | 40.7% | +5.7 | **W** (LAD 8-6 + Ohtani 5 TB) — best-win-chance correlated 2-leg cashed (+185). |
| 6/11 | LAD ML −171 × Freeman O1.5 TB −110 (Build C Tier 3 — genuine +200) | +203 | 31.0% | 38.3% | +5.2 | **L** (LAD W but Freeman only 1 TB) — the +200-reach swap busted on the weaker complement; the Ohtani version (Tier 2) would have cashed. Lesson: the highest-floor leg (Ohtani) beat the +200-stamp swap (Freeman) — Tier-2-over-Tier-3 validated. |
| 6/11 | **USER** NYM ML −138 × MIA ML −115 | +222 | $10 | $32.24 | **+$22.24** | ✅ WON (NYM 5-4 + MIA 2-0 both cashed; user combined the two non-LAD legs — both early-game favs, clean win, dodged the LAD/PIT variance). |
| 6/12 | SEA ML −140 × TB ML −160 (Build A Tier 2 — highest floor) | +179 | 37.2% | 37.2% | +1.3 | **TBD** — two ace-form favs (Miller 1.33 + McClanahan 2.85); best win chance ~37%, lands +179. EV +3.6%. |
| 6/12 | SEA ML −140 × MIN ML −131 (Build A Tier 3 — the +200) | +202 | 34.2% | 34.2% | +1.1 | **TBD** — genuine +200, true comb 34.2%, EV +3.4%. Floor ~3pp under Tier 2 for the +200 stamp. Alt: SEA×BAL +210 (33.6%). |

**Units-tracked tickets (flat-1u rows): 14 tickets, record 7-7, staked 14.00u, returned 21.39u → P/L +7.39u, ROI +52.8%** (added 6/10 TB+Rasmussen SGP **WON** +1.81u — a pos-corr highest-floor ticket, the diversify-era template cashing again). Real-dollar USER builds: **6/8 PHI+Sánchez SGP WON** $10→$26.70 (**+$16.70**); **6/9 MIA+ATL LOST** $30→$0 (**−$30.00**); **6/10 TB+Rasmussen SGP WON** $10→$28.10 (**+$18.10**, +181, stake confirmed); **6/11 NYM+MIA WON** $10→$32.24 (**+$22.24**, both early favs cashed). Real-$ build P/L to date = **+$27.04** (3-1). Calib leg-level: **ML-fav 12-6**, STANDALONE 0-1 vs PARLAY 17-8, recommended-not-played **29-13** (6/10 declined legs settled 2-3: PHI W, SD W, LAD L, DET L, ATL L).
**User's own 6/6 tickets (logged separately, not from a build): Ticket 1 ✅ +$20.62; Ticket 2 2/3 locked, LAD −1.5 live (eff. W).**

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

---

## User-angle tracking (started 6/7/26 — user request)
Two angles the user gravitates to that aren't surfaced by the standard build. **Tracking dimension only**
— these rows ALSO live in the main "Played legs" table (tagged `*` until pre-registered); this section is
the per-angle scoreboard. Each run: when one of these appears on the board, note it here even if not bet,
and log W/L on settle. **Both are noise until N≥20-30 — directional only, do NOT size off them yet.**

### Angle A — LIVE moneyline (in-game ML, taken after first pitch)
The 6/6 TOR leg was a live-ML (−191, taken once TOR led). Thesis to test: does taking a fav's ML LIVE
(better price after an early lead, or a value re-entry on an early deficit) beat the pregame number?
Capture: pregame ML vs the live price taken (the "live CLV"), the game state at entry, result.
| Date | Game | Live price | Entry state | Pregame ML (ref) | Result | Live-CLV |
|------|------|-----------|-------------|------------------|--------|----------|
| 6/6 | TOR ML (vs BAL) | -191 | led early | ~-132 (open) | **W** (TOR 6-4) | took worse # for safety — live tax, but cashed |
| 6/7 | LAD (vs LAA, Sheehan/Soriano) | WATCH | re-entry IF trails early | pull at game time | **no-trigger** (LAD lost 5-13 — a deficit re-entry would have LOST; correct to pass) | candidate #1 — strong team, moderate fav; trail early → overshoot |
| 6/7 | NYY (vs BOS, Suarez LHP) | WATCH | re-entry IF trails early | -160 (open) | **no-trigger** (NYY won 6-1 wire-to-wire — no early deficit, no re-entry spot) | candidate #2 — Suarez tough; early NYY deficit = live value |
| 6/7 | ATL (vs PIT, Bryce Elder) | WATCH | re-entry IF trails early | -145 (open) | **no-trigger** (ATL won 3-2 close — pregame ML cashed; settled in main table) | candidate #3 — **probable is Elder (2.63), not Chandler** (pre-seed corrected); ATL also Build A Tier 2/3 anchor |

**Angle A record: 1-0** (6/7 = 3 pre-game WATCH candidates, value-re-entry type — execute in-game only). Watch: live-ML usually means PAYING UP for a lead already in (the −132→−191
move is the "live tax"). The edge case worth proving is the OPPOSITE — a value re-entry when a good team
falls behind early and the live price overshoots. Flag which type each entry is.

### Angle B — opposing-SP hits-allowed OVER (fade-the-bad-matchup hits prop)
The 6/6 Kochanowicz O5.5 hits cleared when he was shelled (0.1 IP / 6 ER). Thesis: a hits-allowed Over on
a vulnerable SP vs a strong contact offense is a softer market than the K-props/ML. Capture: SP, line,
opposing lineup contact quality, result (hits allowed).
| Date | SP (vs team) | Line | Opp contact read | Result | Hits |
|------|-------------|------|------------------|--------|------|
| 6/6 | Kochanowicz O5.5 (vs LAD) | (SGP) | LAD elite offense, K had 6.94 ERA into start | **W** | 6+ (pulled 0.1 IP/6 ER) |
| 6/7 | Freeland (COL LHP, vs MIL @ Coors) | WATCH — pull line | 8.06 ERA/1.71 WHIP, Coors; MIL 21% K but only .226 vs LHP | **no-trigger** (MIL won 12-4 @ Coors — Over hits would almost certainly have CASHED; line never pulled) | candidate #1 — park+profile cleanest; .226-vs-LHP caveat; low hook risk (eats IP) |
| 6/7 | ~~Chandler~~ Montgomery (PIT, @ ATL) | VOID | PIT probable = Mason Montgomery, not Chandler (pre-seed wrong) | — | candidate VOID — re-scan Montgomery if pulling the Angle-B line at 16:00 |
| 6/7 | Flaherty (DET RHP, vs SEA) | WATCH — pull line | 5.31 ERA/1.60 WHIP but 10.92 K/9; SEA .247/22% | **no-trigger** (SEA scored 4 in a 5-4 DET win — marginal; line never pulled) | candidate #3 — high K/9 converts hits→Ks, weakest |

**Angle B record: 1-0** (6/7 = 3 WATCH candidates; pull the real line + devig near first pitch — Gilbert/PHI passed: opener/start-length unknown). Watch: (a) hits-allowed correlates with IP — a quick hook (few outs) can CAP
hits even in a blowup, so it has the same left-tail start-length risk as K-Overs; (b) books shade these
up on public "blowup" narratives. Pull the real number, devig, and treat like a K-Over alt decision.
