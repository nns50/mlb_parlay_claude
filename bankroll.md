# $10 Rollover Bankroll — full-compounding ladder

**The game.** Start at **$10**. Each roll bets the **entire current balance** on the day's single
highest-floor qualifying favorite. Roll the full return (stake + winnings) into the next bet.
**Target = 4 consecutive wins → STOP & withdraw all.** Any losing roll → balance $0 →
**restart the next attempt at $10.**

**Honest framing (read every time).** Full rollover is maximum variance — one loss zeroes the attempt,
so the **median attempt busts**; the value lives entirely in the rare 4-win run. Downside is capped at
the **$10 per attempt**. At fair odds this is ~break-even; it is only mildly +EV if *every* roll truly
clears the min-edge gate, and even then the expectation is carried by the tail, not the typical outcome.
This is a capped-risk fun ladder, **not** an income strategy — and it's separate from unit-staking the
regular slate plays in `results_log.md`.

---

## Rules

1. **Stake = the whole balance, every roll** (true full rollover).
2. **Per-roll pick = the single safest +EV favorite on the WHOLE board, chosen INDEPENDENTLY of the
   daily parlay** (~60%, the -150/-200 zone) — it's whichever qualifying favorite has the highest floor,
   even if it's not one of the parlay legs:
   - MUST clear the **min-edge gate** (devigged edge ≥ +2pp) and **all** pre-publish gates
     (game-status not started, SP-freshness, lineup posted if it's a hitter prop, real-book price).
   - MUST NOT be a team on the `fades.md` **A list** (fade-as-favorite) — never roll the bankroll on a
     fade-as-fav team.
   - Prefer the cleaner **62-66% ace-edge favorites** (3/3 in calibration) over the soft **56-61% band**
     (hitting ~40% — directional). Within the single-fav mandate, pick *quality of edge*, not raw price.
   - **Single leg only — no parlay.** (This is the disciplined anti-+200-chase version by design; the
     bankroll grows through compounding, not through stacking legs.)
   - **No qualifying play that day → NO BET; balance carries unchanged to the next day** (don't force a roll).
3. **Target = 4 wins.** On the **4th consecutive win** → STOP, withdraw all (~$74 at typical odds), log it,
   restart at $10. *(4 wins ≈ 13%/attempt. Change the target anytime — 3 wins ≈ 22%, 5 wins ≈ 8%.)*
4. **Loss → $0 → restart at $10** on the next attempt (a fresh $10 of real money risked — tracked below
   so the net is honest, not just "I hit the target once").
5. New balance = balance × **decimal** odds on a win, $0 on a loss. Settle with `mlb_api.sh finals`.

## Reference ladder (illustrative @ ~1.65×/win; actual growth depends on each day's real price)

| Win # | Balance |
|------|---------|
| start | $10.00 |
| 1 | ~$16.50 |
| 2 | ~$27.20 |
| 3 | ~$44.90 |
| 4 | **~$74.10** → STOP & withdraw |

P(4 straight wins in an attempt) ≈ 0.60⁴ ≈ **13%** → expect ~8 attempts (~$80 risked) per successful run.

---

## Ledger (every roll, append-only)

| Attempt | Date | Roll | Balance before | Bet (leg @ book, decimal) | True% | Result | Balance after | Note |
|---------|------|------|----------------|---------------------------|-------|--------|---------------|------|
| 1 | 6/4 | 1 | $10.00 | ATL ML −205 (FanDuel, 1.488) | 67% | **LOSS** (TOR 7-2) | **$0.00** | bumped to 69% on TOR-bullpen-game logic — backfired (fades D5); **attempt 1 BUSTS** |
| 2 | 6/5 | 1 | $10.00 | LAD ML −188 (FanDuel, 1.532) | 66% | **WIN** (LAD 1-0) | **$15.32** | safest qualifying fav (40-23/+133, home); LAA SP = Detmers; not A-list fade; +3.3pp. **Note: the SAME Dodgers leg LOST inside the user's SEA×LAD parlay — standalone cashed, parlay didn't (parlay tax, live).** |
| 2 | 6/6 | 2 | $15.32 | LAD ML −182 (FanDuel, 1.549) | 64.7% | **WIN** (LAD 9-2) | **$23.73** | LAD beat LAA 9-2 (Yamamoto cruised); $15.32×1.549 = $23.73. Roll 2 cashed. |
| 2 | 6/7 | 3 | $23.73 | deGrom (TEX) ML −140 (BetUS, 1.714) | 60.1% | **WIN** (TEX 10-0) | **$40.67** | safest qualifying fav on the board — deGrom 3.48/10.86 K9 ace edge (+3.0pp), TEX home vs CLE/Cantillo; not A-list fade. deGrom dealt, TEX 10-0. $23.73×1.714 = $40.67. **Roll 4 = the 4-win target.** |
| 2 | 6/7 | 4 | $40.67 | — NO BET — | — | — | $40.67 (carries) | Roll 4 (the target roll) needs a qualifying fav, but at the 18:00 run the only pre-game game left is SF@CHC — **CHC −123 is an A1 fade-as-fav (excluded)**, SF is a dog. No qualifying favorite → NO BET, balance carries to next slate. |
| 2 | 6/8 | 4 | $40.67 | PHI ML −164 (LowVig, 1.610) | 63.8% | **WIN** (PHI 5-2 TOR) | **$65.48** | **🎯 4-WIN TARGET HIT → STOP & WITHDRAW $65.48.** Sánchez dealt (7 IP / 10 K / 2 ER), PHI held on 5-2. $40.67×1.610 = $65.48. **Attempt 2 = SUCCESS (4 straight wins).** Restart next slate at $10. |
| — | — | — | — | — WITHDRAWN $65.48 — | — | **TARGET** | **$0 → restart $10** | Attempt 2 complete: $10 → $65.48 over 4 rolls (LAD, LAD, deGrom, PHI). Net realized profit on attempt 2 = **+$55.48**. Next slate starts fresh attempt 3 at $10. |

---

## Running totals (update on every settle)

- **Current:** Attempt **2 COMPLETE — 🎯 4-WIN TARGET HIT.** PHI ML −164 **CASHED** 6/8 (PHI 5-2 TOR, Sánchez 7 IP/10 K)
  → $40.67×1.610 = **$65.48 → WITHDREW $65.48.** Attempt 2 ran $10 → $65.48 over 4 straight wins (LAD, LAD, deGrom, PHI).
  **Next slate = fresh attempt 3 at $10.**
- **Attempts completed:** 2 · **Targets hit (4 wins):** **1** ✅ · **Busts:** 1 · **Best run:** **4 wins (attempt 2 — TARGET)**
- **Total real risk (attempts × $10):** **$20.00** risked · **Total withdrawn:** **$65.48**
- **Net P/L (withdrawn − deposited):** **+$45.48** (attempt 1 lost $10; attempt 2 turned $10 into $65.48 → +$55.48; net +$45.48 across both)

> Tracked like `fades.md` / `results_log.md`: any change → commit → push → PR → squash-merge.
