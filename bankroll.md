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
| 2 | 6/6 | 2 | $15.32 | LAD ML −182 (FanDuel, 1.549) | 64.7% | **TBD** (LAA vs Yamamoto) | _pending_ | safest qualifying fav on the board again — Yamamoto 2.86 ERA vs LAA (24-39, Kochanowicz 5.23); +3.0pp, not A-list. Win → $15.32×1.549 = **$23.73**. |

---

## Running totals (update on every settle)

- **Current:** Attempt **2**, balance **$15.32** (1 win), **roll 2 LIVE** — bet **LAD ML −182** (Yamamoto vs
  LAA), the single safest qualifying fav on the 6/6 board (+3.0pp, not A-list). Win → ~$23.73 (then roll 3).
- **Attempts completed:** 1 · **Targets hit (4 wins):** 0 · **Busts:** 1 · **Best run:** **1 win (active, attempt 2)**
- **Total real risk (attempts × $10):** **$20.00** risked · **Total withdrawn:** $0.00
- **Net P/L (withdrawn − deposited):** **−$10.00** (attempt 1 lost $10; attempt 2 live at $15.32, not yet withdrawn)

> Tracked like `fades.md` / `results_log.md`: any change → commit → push → PR → squash-merge.
