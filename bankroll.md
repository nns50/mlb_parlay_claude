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
| 3 | 6/9 | 1 | $10.00 | MIA ML −129 (book, 1.775) | 59% | **WIN** (MIA 10-6 AZ) | **$17.75** | **Attempt 3 roll 1 CASHED.** Meyer + MIA bats erupted 10-6. Gate discipline vindicated: MIA (+2.5pp, cleared) over ATL (−148, +1.7pp under gate) — ATL LOST 5-6 to a CWS bullpen game (D5), so picking MIA on the gate also dodged the trap. $10×1.775 = $17.75. Roll 2 next slate. |
| 3 | 6/10 | 2 | $17.75 | TB ML −141 (BetOnline.ag, 1.709) | 60% | **WIN** (TB 7-5 BOS) | **$30.33** | Roll 2 CASHED — Rasmussen dealt (13 K / 7 IP), TB won 7-5. $17.75×1.709 = $30.33. Roll 3 next. |
| 3 | 6/10 | 3 | $30.33 | LAD ML −195 (BetUS, 1.513) | 67% | **LOSS** (LAD 8-9 PIT) | **$0.00** | **Attempt 3 BUSTS at roll 3.** Ohtani-led LAD blew a lead, PIT walked it off 9-8 (B2 dog cashed). The full-rollover risk realized — 2 wins ($10→$30.33) wiped to $0. Restart attempt 4 at $10 next slate (6/11). |
| 4 | 6/11 | 1 | $10.00 | NYM ML −138 (BetUS, 1.725) | 59% | **WIN** (NYM 5-4 STL) | **$17.25** | Roll 1 CASHED — Christian Scott (10.25 K/9 ace edge, +2.4pp) held STL to 4, NYM won 5-4. $10×1.725 = $17.25. Roll 2 next. |
| 4 | 6/11 | 2 | $17.25 | — NO BET — | — | — | $17.25 (carries) | At the 16:00 run the only pre-game fav left is LAD −166, but its devigged edge is **+0.9pp — under the +2pp gate** (SEA coin-flip, ATL is an A/D fade). No qualifying favorite → NO BET, balance carries to next slate. |
| 4 | 6/12 | 2 | $17.25 | SEA ML −138 (BetOnline, 1.725) | 60% | **TBD** | _pending_ | Roll 2 — **CONFIRMED at 16:00** (lineups posted, SEA@WSH both sides; line 2¢ shorter −140→−138). Safest qualifying fav clearing the +2pp gate: Bryce Miller red-hot (1.33 ERA / 0.78 WHIP, 6IP/0ER/9K @ DET 6/6) vs WSH + soft Littell. No-vig 56.7% → TrueP 60% (**+3.3pp**). Not an A-list fade. $17.25×1.725 = **$29.74** on a win → roll 3. (TB −162 at 62% is the higher-floor band but +1.6pp = under the gate; SEA is the cleanly-gated pick.) |

---

## Running totals (update on every settle)

- **Current:** **Attempt 4 OPEN — 1-0; roll 2 CONFIRMED 6/12 16:00 (TBD):** SEA ML −138 (BetOnline, 1.725), balance $17.25 → $29.74 on a win. (Roll 1 WON 6/11: NYM ML −138, NYM 5-4 → $10→$17.25. The 6/11 16:00 roll-2 slot was NO BET — nothing cleared the gate; this is the carried roll 2.)
  (Attempt 3 BUSTED 6/10 at roll 3; Attempt 2 COMPLETE 6/8 — 🎯 4-WIN TARGET HIT, withdrew $65.48.)
- **Attempts:** 3 completed + **1 open (attempt 4, 1-0)** · **Targets hit (4 wins):** **1** ✅ · **Busts:** 2 (attempt 1 @ roll 1, attempt 3 @ roll 3) · **Best run:** **4 wins (attempt 2 — TARGET)**
- **Total real risk (attempts × $10):** **$40.00** risked (attempt 4's $10 now in play) · **Total withdrawn:** **$65.48**
- **Net P/L (withdrawn − deposited):** **+$25.48** realized (attempt 1 −$10; attempt 2 +$55.48; attempt 3 −$10; attempt 4 −$10 in-play, $17.25 live balance)

> Tracked like `fades.md` / `results_log.md`: any change → commit → push → PR → squash-merge.
