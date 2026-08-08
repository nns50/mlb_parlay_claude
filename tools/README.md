# tools/

## Coverage matrix — audit against THIS, not against burns (added 8/1/26)

Every gap that survived multiple "sweeps" (RL settled by W/L not margin; DH G2 clobbering G1;
team totals left manual; hitter props unmeasured) shared one cause: audits were **burn-driven**
(fix what already bit) instead of **coverage-driven** (enumerate leg-type × pipeline-stage and
check every cell). This matrix is the enumeration. A sweep = re-verify every cell in code;
a new leg type or pipeline stage = add a row/column FIRST, then implement to fill it.

| Leg type ↓ / Stage → | Price | Gates | Construct | CLV | Settle | Measure |
|---|---|---|---|---|---|---|
| ML (fav/dog) | `best h2h` ✓ | status/SP/recheck ✓ | ticket.py ✓ | cached slate ✓ | score, DH-guarded ✓ | calib+Brier ✓ |
| Run line ±1.5 | `best spreads` ✓ | same ✓ | ticket.py ✓ | cached slate ✓ | **by MARGIN**, DH ✓ | ✓ |
| Game total | `best totals` ✓ | weather/ump ✓ | ticket.py ✓ | cached slate ✓ | away+home vs line ✓ | ✓ |
| Team total | ⚠ manual pull | weather/ump ✓ | ticket.py ✓ | ⚠ manual (market not wired) | own runs vs line ✓ | ✓ |
| K-prop (std+alt) | kprice.py ✓ | C1-C6 gates ✓ | corr tiers ✓ | props feed (rich) ✓ | gamelog ✓ | ✓ |
| Hitter counting (H/TB/HR/RBI/R/HRR/SB/BB/2B/1B) | `props core/all` (rich) ✓ | lineup gate ✓ | ticket.py ✓ | props feed (rich) ✓ | boxscore, DNP+DH-guarded ✓ | ✓ |
| Pitcher props (hits-allowed/outs/ER) | `props` (rich) ✓ | SP gates ✓ | ticket.py ✓ | props feed (rich) ✓ | boxscore/gamelog ✓ | ✓ |
| NRFI/YRFI | ⚠ model-only (line rarely pulled) | ⚠ judgment reads (linescore data via mlb_api; no deterministic tool) | standalone-only | n/a by doctrine | nrfi_settle ✓ | tracker+dashboard ✓ |
| Parlay/SGP ticket | parlay.py + min-SGP ✓ | leg gates ✓ | ticket.py search ✓ | n/a (no ticket close) | legs settle it ✓ | ticket rows ✓ |
| Live-ML (Angle A) | manual by design | — | — | "live CLV" manual | manual | N<20 directional |
| **Staking / stake-capture** | ¼-Kelly: ticket.py (tickets) + devig.sh (single legs) ✓ | — | — | — | user reports the real $ (doctrine step 11) | ⚠ ROI "fiction" until real stakes logged (calib flags it) |

**Open cells, held deliberately:** team-total pricing/CLV (thin, illiquid market — wire
`team_totals` event odds if the sweep starts surfacing them); NRFI real lines
(`totals_1st_1_innings` exists — model-only until doctrine promotes it); NRFI lean
derivation (judgment by design — the reads are pre-registered TruePs, not a model tool);
alt run lines / alt game totals (markets exist, unused by doctrine); F5 lines (not a
doctrine product); stake capture (only the user knows the real $ — the tools print
¼-Kelly, doctrine step 11 demands the number). **Selftest depth note:** mlb_api.sh output
parsers are fixture-tested only for the finals format (settle.py's backbone); lineups/
ump/weather/splits parse drift fails soft (visible garbage, not silent wrong verdicts).
An open cell must be HERE with a reason — an open cell not listed is a gap.

## `mlb_api.sh` — authoritative MLB data via the public StatsAPI

Deterministic source for the things WebSearch keeps hallucinating: **game status**
(Scheduled / Pre-Game / In Progress / Final), **probable pitchers**, **final scores**,
and **pitcher season lines + start-by-start game logs**. Use it to resolve the
game-status gate and the SP-freshness gate without inferring from search prose.

### Status: LIVE ✅ (confirmed reachable 2026-06-04, this session)
The user allowlisted `*.mlb.com` on the environment and a **new session** picked it up, so
`./tools/mlb_api.sh check` now returns `OK`. The `slate` / `status` / `finals` / `pitcher` / `gamelog` /
`lineups` / `ump` / `weather` / `splits` / `standings` / `teamform` commands have all been **validated against live data**.
**Always run `check` at session start** — it's the deterministic way a fresh session learns whether the policy is active this run.

**If `check` ever returns `BLOCKED` again** (e.g. the routine runs against a different environment whose
policy lacks the rule), the proxy denies non-allowlisted hosts with `HTTP 403` + `x-deny-reason:
host_not_allowed` and the script prints an actionable verdict. To re-enable: edit the environment the
routine/session uses → **Network access → Custom** → add `*.mlb.com` → **check "Also include default
package managers"** → **Save** → start a **new** session (the policy applies at startup, never
mid-session). Simpler alternative: **Network access → Full**. Until `check` is `OK`, the routine falls
back to the 2-source WebSearch game-status gate automatically.

### Commands
```
tools/mlb_api.sh check                       # reachability preflight (exit 0 reachable, 2 blocked)
tools/mlb_api.sh slate   [YYYY-MM-DD]        # per-game status + probables + score
tools/mlb_api.sh status  [YYYY-MM-DD]        # compact one-line-per-game status (the gate)
tools/mlb_api.sh finals  [YYYY-MM-DD]        # final scores only (prior-day settle)
tools/mlb_api.sh pitcher <personId> [SEASON] # season ERA/WHIP/IP/K/K9/GS/W-L
tools/mlb_api.sh gamelog <personId> [SEASON] # start-by-start log (date, opp, IP, ER, K, BB)
tools/mlb_api.sh findpitcher "<name>"        # resolve a name -> personId
tools/mlb_api.sh lineups [YYYY-MM-DD]        # batting orders per game (CONFIRMED or PENDING ~2-3h pre-game)
tools/mlb_api.sh ump     [YYYY-MM-DD]        # HP umpire per game (StatsAPI officials; pre-game = PENDING)
tools/mlb_api.sh weather [YYYY-MM-DD]        # condition/temp/wind + venue per game (totals/K signal; near first pitch)
tools/mlb_api.sh splits  <id|abbr|name> [Y]  # team K% vs LHP and vs RHP (K-Over handedness gate)
tools/mlb_api.sh standings [SEASON]          # division standings: W-L, pct, GB, L10, streak, run diff
tools/mlb_api.sh teamform <id|abbr|name> [N] # last-N results: W-L + run differential (fade re-verify)
tools/mlb_api.sh findteam "<name|abbr>"      # resolve a team name/abbr -> teamId
tools/mlb_api.sh raw "schedule?sportId=1&date=2026-06-04"   # raw JSON passthrough
```

### How it slots into the routine
- **Game-status gate:** `status`/`slate` give `abstractGameState` (Preview/Live/Final) and
  `detailedState` — authoritative. A `Final` here is a real final; a `Preview`/`Pre-Game`/`Warmup`
  means NOT started. This replaces inferring status from a search summary (no more re-stamp burns).
- **Prior-day settle:** `finals <yesterday>` returns every final score in one call.
- **SP-freshness gate:** `findpitcher` → `pitcher`/`gamelog` give the current season line AND the
  most-recent start (date/opp/IP/ER/K), exactly what the freshness field requires.
- **Lineup gate:** `lineups <date>` shows confirmed batting orders (or PENDING when not yet posted).
  Run at ~16:00 ET; if PENDING, hitter-prop legs cannot be locked.
- **HP umpire gate:** `ump <date>` returns the HP ump name per game once games are in-progress. Pre-game
  (11:00 run): outputs PENDING with a WebSearch fallback hint for early assignment lookup.
- **Park/weather (totals + K signal):** `weather <date>` gives condition/temp/wind-with-direction + venue,
  and flags retractable/domed parks. "Out" wind boosts totals/HR (hurts K-Over); "In" + cold suppresses.
  Like `ump`, it populates near first pitch — empty pre-game (11:00), live at the 16:00/18:00 runs.
- **K% by handedness (K-Over gate):** `splits <team>` returns team K% vs LHP and vs RHP from StatsAPI
  batting splits — deterministic replacement for manual K% research before K-Over legs.
- **Fade re-verification (`fades.md`):** `standings` gives every team's W-L / L10 / streak / run diff in
  one call, and `teamform <team> [N]` gives a precise last-N record + run differential — deterministic
  input for the "re-verify last-15 form each session" requirement (replaces manual WebSearch).
- **Always preferred when reachable; WebSearch gate is the fallback when `check` returns BLOCKED.**

## `odds_api.sh` — live book odds via The Odds API (line-shopping + CLV)

Ends hand-entered prices: pulls every US book's line so the build bets the **best number** (free EV) and
a near-first-pitch run can **snapshot the close to fill CLV** (the only real edge scoreboard). It does NOT
raise win probability — it improves PRICE and MEASUREMENT. Mirrors `mlb_api.sh`: a `check` subcommand
reports whether the policy is live and how much monthly quota remains.

**Requires two things (both on the user):** (1) the environment must allowlist `api.the-odds-api.com`
(Network access → Custom; applies only in a NEW session); (2) the API key in the env var **`ODDS_API_KEY`**
(a secret — NEVER commit it).

**Budget (paid tier = 20K credits/mo; free tier = 500).** Cost = (#markets × #regions)/call. `slate`
(h2h,totals,spreads × us) = 3 credits and returns the WHOLE board, so it's **cached per run** — every leg
reads the cache, not the API — and session_start reuses a fresh (<90 min, non-empty) cache at 0 credits.
`events`/`quota` are free. `props` is per-event and quota-spending — opt-in, it warns before spending;
props tooling (kprice, prop CLV close) self-gates on the API reporting a rich quota (≥5000).

```
tools/odds_api.sh check                    # key + reachability + remaining quota
tools/odds_api.sh slate [date]             # pull+cache h2h/totals/spreads; best-ML table
tools/odds_api.sh best h2h|totals|spreads [date]   # best line per game per side, with the book
                                           # (⛔ excludes games already started — a cached in-game
                                           #  price is not shoppable; banner shows the count)
tools/odds_api.sh game "<team>" [date]     # full book-by-book board for one game
tools/odds_api.sh events [date]            # event IDs (free; needed for props)
tools/odds_api.sh props <eventId> pitcher_strikeouts[,batter_hits]   # PER-EVENT props (spends quota!)
tools/odds_api.sh clv <betAmerican> "<team>" [date]   # closing no-vig vs your bet (ML)
```

**How it slots in:** at **build** → `best` feeds the best two-sided price into `devig.sh` (min-edge gate vs
the genuinely best number); K-legs price via `kprice.py`, the wider prop universe via `props core/all` on
the paid tier. At the **16:00 / 18:00 runs** → `clv_capture.py --apply` writes the close for every covered
leg automatically (cached slate for ML/totals/RL; live props feed for counting props). Pairs with
`parlay.py`/`ticket.py` (real prices → real combined EV).

## `clv_backfill.py` — retro-fill blank CLV cells from HISTORICAL snapshots (paid tier)

The live capture runs can only close games whose first pitch is still ahead of them — an early slate
(8/2: the whole board went live before capture armed → the day's five decided picks logged 0/5 closes)
or a dropped run leaves holes forever, and CLV is both the primary scoreboard and pulse's shade
trigger. This pulls The Odds API's **historical** board snapshot at each missed game's `commence − 2min`
(5-min grain) and writes the standard verdict with a ` bf` provenance marker.

```
tools/clv_backfill.py 2026-08-02              # PLAN: fillable rows, snapshots, exact cost — no spend
tools/clv_backfill.py 2026-08-02 --apply      # spend + write (gated: paid tier, --max-credits 150)
```

**Cost:** 30 credits per snapshot timestamp (10 × 3 markets × 1 region); rows group by first pitch so a
typical day is 3-8 snapshots. Scope v1 = ML / game totals / run lines; prop rows print MANUAL
(historical props are per-event — the v2 extension). DH teams skip MANUAL (no G-hint disambiguation).
Validated live 8/7: backfilled the 8/2 BOS@LAD Over 8.5 close (49.4% no-vig, `+ 49%cl bf`) for 30
credits. The 11:00 cron plans yesterday's backfill every morning and applies when cost ≤ 120 credits.

## `session_start.sh` — one-shot session-open digest

Composes the *mechanical* part of the CLAUDE.md "Session-start review" into a single command so the
open is consistent and no step is silently skipped: (1) `check`, (2) yesterday's `finals` for settling,
(3) `standings` for fade re-verify, (4) which of the 3 most-recent `parlays/*.md` still carry a
`## Result` of TBD, (5) every `fades.md` entry + its current status.

```
tools/session_start.sh            # today / yesterday
tools/session_start.sh 2026-06-04 # treat this as "today" (yesterday derived)
```

**READ-ONLY** — surfaces the inputs; it does not bet, settle, or edit files. The judgment steps
(self-settle TBDs, apply calibration, the slate-wide scan) are still the routine's, done after reading
the digest. Resilient to a BLOCKED `check`: the file-based sections (4, 5) still print.

**Date semantics (documented 8/7/26): `today` is the UTC date.** For the 11:00/16:00/18:00 ET cron
runs UTC and ET dates always agree, so every scheduled behavior is correct. An INTERACTIVE session
opened 20:00–23:59 ET sees `today` = tomorrow-ET: the slate warm targets tomorrow's board (correct —
it's pre-game) and "yesterday" = today-ET, whose in-progress games are protected by the Final-only
gates in `settle.py`/`nrfi_settle.py` (partial slates settle only their finished games). CLV auto-apply
is gated on the ET hour (16–19), so it never fires in that window. Known, benign — don't "fix" the date
math without re-checking every consumer.

## `calib.py` — recompute calibration / ROI from `results_log.md`

The ledger's rollup tables (calibration bands, units/ROI, by-type record) are hand-maintained and drift.
This re-derives them from the raw leg rows so the numbers stay correct. **READ-ONLY** — prints a report,
never edits the ledger; if the printed numbers disagree with the file's tables, the file is stale.

```
tools/calib.py [path/to/results_log.md]   # defaults to ../results_log.md
```

- Calibration uses **played** legs with an explicitly-logged TrueP; `*` (reconstructed) rows are excluded,
  matching the ledger's rule. Bands are fixed 5-wide and flagged only at n≥3 (no conclusions from coin-flips).
- ROI is summed straight from the played-ticket rollup (stake / return / P-L). Run it after each settle.
- **STANDALONE vs PARLAY split** (section 2b): reads the `Bucket` column (S/P) and breaks out leg-level
  record by bucket — the parlay-tax test. (Watch the gap: parlay *legs* can win ~68% individually while
  parlay *tickets* win far less — that gap IS the tax.) Standalone leg-level ROI lives in `bankroll.md`.
- **Brier skill vs market** (section 1b): scores EVERY decided leg (played + not-played) with an explicit
  TrueP against the outcome, and scores the logged no-vig ImplP on the same rows. The delta answers the
  single most important leg-selection question — *do the written adjustments beat the price?* — and,
  being a proper scoring rule over all rows, it converges far faster than 5-wide band tables. Positive
  skill = keep the adjustment registry; negative = shrink toward the no-vig baseline.

## `devig.sh` — no-vig implied prob + edge calculator

Removes the by-hand devig arithmetic from every build (the slips `calib.py` exists to catch). Two prices
in → no-vig probs + hold; add a TrueP% to get the Edge and the min-edge-gate verdict. One-sided props
estimate the no-vig at raw − 2.5pp and flag it.

```
tools/devig.sh <priceA> <priceB> [TrueP%_for_A]   # tools/devig.sh -120 +100 59  → +6.8pp, clears anchor bar
tools/devig.sh <priceA> [TrueP%_for_A]            # one-sided prop (estimated no-vig, flagged)
```

## `truep.py` — derive a pre-registered TrueP from baseline + fixed adjustments

Makes the CLAUDE.md TrueP method ("derive it, don't vibe it") mechanical: anchor on the market no-vig
prob (from `devig.sh`), apply PRE-SET written adjustments with fixed pp magnitudes, get a TrueP whose
audit trail is the adjustment list — so calibration measures the *adjustments*, not a gut number.

```
tools/truep.py --list                                          # the adjustment registry
tools/truep.py --base-prob 54.3 --adj ace_edge                 # named adjustments
tools/truep.py --base-prob 56.7 --custom "-2:Gray duel caps floor"   # ad-hoc, repeatable
```

Registry now includes **park / weather / umpire** factors (`wind_out_over`, `wind_in_under`,
`hitter_park_over`, `pitcher_park_under`, `cold_aids_kover`, `hot_hurts_kover`, `wide_zone_ump_kover`,
plus the existing `tight_zone_ump`) — softer-market signal from `mlb_api.sh weather`/`ump`. They're
direction-explicit ("aids <this side>"); they're NOISIER than SP/lineup edges, so keep magnitudes modest
and don't stack several.

K-prop "tiers" are NOT pp — those move the alt line, not this tool (which is for ML / spread / total / TT).

## `parlay.py` — correlation-aware true combined prob vs the offered price

Parlay legs win ~68% individually but tickets ~42% — the only thing that keeps a real win chance is
POSITIVE correlation (same-game legs that win together). This computes the naive product, the
**correlation-adjusted** true combined prob (2-leg pair), the fair odds, and the EV vs both the
independent-product price and an offered SGP price — then says which to take. It catches the trap where
NEGATIVE correlation makes a parlay -EV even though the naive product looks fine.

```
tools/parlay.py --leg 59:-120 --leg 66:-188                  # independent (different games)
tools/parlay.py --leg 59:-120 --leg 66:-188 --corr moderate  # same-game, positively correlated
tools/parlay.py --leg 60:-130 --leg 55:+110 --corr moderate --sgp +320   # compare SGP vs independent
```

Each `--leg` is `TrueP%[:americanPrice]`. `--corr` tiers (2-leg only): `strong/moderate/weak/none` and
`neg-weak/neg-moderate/neg-strong` (rough ρ; positive = legs win together, negative = legs fight → skip).

## `kprice.py` — one-shot K-prop pricing (paid tier; the anti-"estimated alt price" tool)

`tools/kprice.py <pitcher> [date]` resolves the pitcher to today's game (probables snapshot) and the
odds event, pulls `pitcher_strikeouts` + `pitcher_strikeouts_alternate` (~2 credits), and prints every
posted K line with the best price per side across all books and the no-vig split per line — flagging
the STANDARD line and the one-lower alt. This mechanizes two doctrine rules: "never estimate alt
prices" (burn 5/26 Burns: est −185, actual ~−400) and "whenever a K-Over is faded, price the K-Under."
**Refuses to spend when the API reports <1000 credits remaining** (free tier) unless `--force`;
`--standard-only` halves the cost; `--event <id>` disambiguates doubleheaders.

On the paid tier, `clv_capture.py --apply` uses the same machinery to **auto-close K-prop legs'
CLV** (~1 credit per event, cached per run) — gated on the API reporting ≥5000 remaining, so the free
tier never spends.

## `pulse.py` — recent-window exposure governor (strategy adapts to the flow)

User-directed 8/1/26 after the ace_edge decay and the Tier-1 K-prop monoculture sat visible in the
measurement output while nightly builds kept applying static doctrine. Principle: **recency governs
EXPOSURE every build; the n≥20-30 evidence bar governs BELIEF** — you stop leaning on a dimension the
moment it runs cold, without overfitting the doctrine to noise. Stateless: recomputed each run from
`results_log.md` (last 14 days, or last 25 decided **unique legs** — 8/7/26: reprice/supersede copies
of one physical bet collapse to the latest row via `calib.leg_key`; row-counting had inflated the window
131→107 and manufactured three MARKET-SHADEs from double-counted CLV. Row years anchor to the
`<!-- ledger-epoch: YYYY -->` marker in `results_log.md` — the season-anniversary trap where Aug-2026
rows would re-enter an Aug-2027 window as "3 days old" is closed, and the last-25 fallback ignores rows
older than 45 days so a quiet ledger idles the governor rather than governing off a prior season), per
dimension (bet type, K-line bucket, `[adj:]` tag, TrueP band), with fixed mechanical thresholds:

```
COOL          n≥5, hit ≤ claimed−15pp   halve its adjustments; barred from Tier 1 + parlay-anchor
SUSPEND       n≥6, hit ≤ claimed−25pp   no new legs in this dimension this build
MARKET-SHADE  CLV −'s ≥ +'s+2 (n≥4)     TrueP = market no-vig for this dimension until CLV recovers
GLOBAL SHRINK recent Brier loses to mkt halve every adjustment this build
RE-WARM       automatic                 ≥3 of the dimension's last 5 decided legs won
```

session_start prints it in every digest (§7); the cron builds must APPLY the actions and fill the
"Recent-window pulse applied" gate row. First live run flagged exactly the hand-found leaks — plus one
nobody had named: ML-favs at 2+/11− recent CLV.

## `recheck.py` — pre-lock SP-scratch / status detector (E3/E4 made mechanical)

A scratched or swapped starter silently invalidates every K-leg AND every ML/total premised on that
arm — two whole burn classes (E3 carried-over probables, E4 TBA starters). The 11:00 build runs
`recheck.py snap <date>` to snapshot the slate's probables + game states into
`parlays/.probables/<date>.json` (committed with the build as an audit record); the 16:00/18:00 lock
runs call `recheck.py <date>`, which re-pulls live StatsAPI and diffs:

```
⛔ game started/final       → status gate closed, cannot lock
⚠ probable CHANGED/REMOVED → every leg built on the old arm is INVALID — re-run SP-freshness or drop
⚠ game gone from the feed  → PPD/suspended, void dependent legs
ℹ probable posted (was TBA) → leg can graduate from PENDING after SP-freshness
```

Exit 1 when anything ⚠/⛔ fires so the cron output can't miss it. `--selftest` runs the diff logic on
offline fixtures (wired into selftest.sh §5a2).

## `ticket.py` — exhaustive +200-band ticket search (the construction optimizer)

`parlay.py` prices ONE ticket; this finds the BEST one. The ledger's construction leak (as of 7/29/26):
legs hit ~68-70% but hand-built tickets ran ~50%, D1 (the +200-chase 3rd leg) went 4-1 against, and the
same-game positive-correlation stack kept being the best route to ~+200. Feed it EVERY gate-cleared leg
from the slate scan; it enumerates every legal 1-3-leg construction (doctrine-aware: one leg per game
unless BOTH legs declare the same corr tier, max one pair per ticket, negative pairs auto-rejected),
prices pairs via `parlay.py`'s joint model, and prints:

1. the **payout/floor frontier** — what +200 truly costs vs +150 (the honest Tier-2-vs-Tier-3 view);
2. the **target band** (default +180..+260) ranked by TRUE combined prob — the recommended ticket is
   the max-floor route to the payout, with EV, ¼-Kelly stake, and (for corr pairs) the minimum SGP
   quote worth taking vs betting the legs separately;
3. **rejected constructions** with doctrine reasons.

```
tools/ticket.py --leg "63:-110:SEA-TEX:Gilbert O6.5K" --leg "63:-164:NYY-PHI:PHI ML" \
                --leg "57:-132:CIN-STL:STL ML"
tools/ticket.py --leg "63:-164:NYY-PHI:PHI ML:moderate" \
                --leg "58:-115:NYY-PHI:Sanchez O6.5K:moderate"      # deliberate same-game stack
tools/ticket.py --file legs.txt --min-price 180 --max-price 260 --top 5
```

Each `--leg` is `TrueP:price:game[:label[:tier]]` (TrueP whole-number percent, BEST shopped American
price, any shared game id; tier only for deliberate same-game pairs). Legs are assumed ALREADY
devig-gated upstream (`devig.sh` + the min-edge gate) — the tool's own `--min-edge` (default 0) only
drops legs that are -EV at the offered price. Run it on every build: Tier 2 = its best-floor pick,
Tier 3 = its band pick; never hand-pick a 3rd leg the search didn't rank first.

## `settle.py` — match a day's finals to open legs and PROPOSE settle edits

Automates the error-prone settle lookup: pulls `mlb_api.sh finals <date>`, finds `results_log.md` rows
that are still TBD for that date, and proposes a verdict for the FULL leg universe (7/30/26):

- **Team ML** by final score; **run lines by MARGIN** (a −1.5 fav that wins by 1 LOSES — previously a
  latent fall-through to the ML branch); **game totals** off away+home vs the line (integer lines Push).
- **K-props** ("Gilbert Over 6.5 K", compact "Sánchez O7.5K"/"Peterson U4.5K") off the pitcher's
  GAMELOG — findpitcher (accent-stripped) → pitchers only → settle date + leg team abbrs disambiguate.
- **Hitter/pitcher counting props** (hits / TB / HR / RBI / runs / H+R+RBI / hits-allowed) off the
  BOXSCORE — player accent-matched across both teams; TB = H+2B+2·3B+3·HR. A player with no
  boxscore line (DNP) → MANUAL, matching how books void those.
- The team is bound to the FIRST team mentioned in the leg text (the bet side by ledger convention) —
  dict-order matching silently bound "BAL … (@ DET)" to DET. **Team totals settle too** (own side's
  runs vs the line, 8/1/26). **Doubleheaders settle only with an explicit G1/G2 hint in the leg text**
  — G2 silently clobbered G1 before 8/1 (the 7/29 ATL-NYM G1 loss read as a W).

This kills the whole prop mis-settle class (mid-game K counts, team-result flips, side-flips).
**READ-ONLY** — prints proposals; you apply them (and `fades.md` / `bankroll.md` / the parlay file) so
the audit trail stays deliberate.

```
tools/settle.py                 # settle yesterday
tools/settle.py 2026-06-05      # settle a specific date
tools/settle.py 2026-06-05 path/to/results_log.md
```
