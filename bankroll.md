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
| 4 | 6/12 | 2 | $17.25 | SEA ML −138 (BetOnline, 1.725) | 60% | **WIN** (SEA 10-2 WSH) | **$29.74** | Roll 2 CASHED — Bryce Miller dealt (8 IP / 2 ER / 7 K), SEA cruised 10-2. $17.25×1.725 = $29.74. Attempt 4 now **2-0** → roll 3 next. |
| 4 | 6/13 | 3 | $29.74 | MIL ML −143/−160 (1.699) | 60% | **LOSS** (PHI 9-8 MIL) | **$0.00** | **Attempt 4 BUSTS at roll 3** (was 2-0). MIL's elite bullpen blew it vs Nola/PHI — full-rollover risk realized, $10→$29.74 wiped. (18:00 alt pick KC −123 ALSO lost 7-8 to HOU, so either form of roll 3 busts.) Restart attempt 5 at $10 on 6/14. |
| 5 | 6/14 | 1 | $10.00 | NYY ML −130 (BetOnline.ag, 1.769) | 58.5% | **WIN** (NYY 8-3 TOR) | **$17.69** | **Attempt 5 roll 1 CASHED.** NYY 42-27/+102 elite, Warren held TOR; NYY won 8-3. $10×1.769 = $17.69. Roll 2 next slate (6/15). |
| 5 | 6/15 | 2 | $17.69 | PHI ML −182 (LowVig.ag, 1.549) | 67.5% | **WIN** (PHI 7-0 MIA) | **$27.40** | **Attempt 5 roll 2 CASHED.** Wheeler dominant (PHI 7-0, MIA shut out). $17.69×1.549 = $27.40. Attempt 5 now **2-0** → roll 3. |
| 5 | 6/16 | 3 | $27.40 | SEA ML −145 (BetUS, 1.690) | 61% | **WIN** (SEA 3-1 BAL) | **$46.31** | **Attempt 5 roll 3 CASHED.** Gilbert dealt vs BAL, SEA won 3-1. $27.40×1.690 = $46.31. Attempt 5 now **3-0** → roll 4 today (6/17) = the 4-win target roll. |
| 5 | 6/17 | 4 | $46.31 | LAD ML −158 (BetOnline.ag, 1.633) | 63% | **WIN** (LAD 5-4 TB) | **$75.63** | **🎯 4-WIN TARGET HIT → STOP & WITHDRAW $75.63.** Ohtani-anchored LAD (1.06 ERA ace-edge, +2.7pp) held off TB 5-4. $46.31×1.633 = $75.63. **Attempt 5 = SUCCESS (4 straight wins: NYY, PHI, SEA, LAD).** Restart next slate at $10. |
| — | — | — | — | — WITHDRAWN $75.63 — | — | **TARGET** | **$0 → restart $10** | Attempt 5 complete: $10 → $75.63 over 4 rolls (NYY 6/14, PHI 6/15, SEA 6/16, LAD 6/17). Net realized profit on attempt 5 = **+$65.63**. Next slate starts fresh attempt 6 at $10. |
| 6 | 6/18 | 1 | $10.00 | NYY ML −149 (LowVig.ag, 1.671) | 60.5% | **LOSS** (CWS 5-1 NYY) | **$0.00** | **Attempt 6 BUSTS at roll 1.** NYY 45-27/+122 elite at home, but Burke outpitched Weathers and CWS completed the road series win 5-1. The team/opponent-driven 60.5% floor (no ace-edge — Weathers 4.36) was really a coin-flip; the 60-64 calib band's overconfidence flag realized. Full-rollover risk: fresh $10 wiped at roll 1. Restart attempt 7 at $10 on 6/19. |
| 7 | 6/19 | 1 | $10.00 | AZ ML −167 (BetUS, 1.599) | 63.5% | **WIN** (AZ 9-5 MIN) | **$15.99** | Soroka ace-edge (+2.4pp), AZ home vs MIN rookie Prielipp. $10×1.599=$15.99. Roll 2 today (6/20). |
| 7 | 6/20 | 2 | $15.99 | PIT ML −195 (BetUS, 1.513) | 68% | **TBD** | — | Skenes ace-edge (+4.6pp), TrueP 68%, no-vig 63.4% (62-66% sweet spot). COL 29-47/Sugano ERA 4.54. $15.99×1.513=$24.19 if W. |

---

## Running totals (update on every settle)

- **Current:** **ATTEMPT 7 ACTIVE — roll 2 of 6/20 (balance $15.99 after 6/19 roll 1 W).** Roll 1 CASHED (6/19 AZ ML −167 → $10→$15.99). Roll 2 today: PIT ML −195 ($15.99→$24.19 target). (Attempt 6 BUSTED 6/18 at roll 1 — NYY ML −149 lost 1-5 to CWS.) (Attempt 5 COMPLETE 6/17 — 🎯 4-WIN TARGET HIT, withdrew $75.63; 2nd target hit overall.)
  (Attempt 4 BUSTED 6/13 at roll 3; Attempt 3 BUSTED 6/10 at roll 3; Attempt 2 COMPLETE 6/8 — 🎯 4-WIN TARGET HIT, withdrew $65.48.)
- **Attempts:** 6 completed · **Targets hit (4 wins):** **2** ✅✅ (attempt 2 $65.48; attempt 5 $75.63) · **Busts:** 4 (attempt 1 @ roll 1, attempt 3 @ roll 3, attempt 4 @ roll 3, attempt 6 @ roll 1) · **Best run:** **4 wins ×2 (attempts 2 & 5 — both TARGET)**
- **Total real risk (attempts × $10):** **$60.00** risked (6 attempts) · **Total withdrawn:** **$141.11** ($65.48 + $75.63)
- **Net P/L (withdrawn − deposited):** **+$81.11** realized (attempt 1 −$10; attempt 2 +$55.48; attempt 3 −$10; attempt 4 −$10; attempt 5 +$65.63; attempt 6 −$10) — **2 successful 4-win ladders banked.**

> Tracked like `fades.md` / `results_log.md`: any change → commit → push → PR → squash-merge.
