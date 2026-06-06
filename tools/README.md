# tools/

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
  Run at ~15:30 ET; if PENDING, hitter-prop legs cannot be locked.
- **HP umpire gate:** `ump <date>` returns the HP ump name per game once games are in-progress. Pre-game
  (09:00 run): outputs PENDING with a WebSearch fallback hint for early assignment lookup.
- **Park/weather (totals + K signal):** `weather <date>` gives condition/temp/wind-with-direction + venue,
  and flags retractable/domed parks. "Out" wind boosts totals/HR (hurts K-Over); "In" + cold suppresses.
  Like `ump`, it populates near first pitch — empty pre-game (09:00), live at the 15:30/18:30 runs.
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

**Budget (free tier = 500 req/mo).** Cost = (#markets × #regions)/call. `slate` (h2h,totals,spreads × us)
= 3 credits and returns the WHOLE board, so it's **cached per run** — every leg reads the cache, not the
API. `events` is free. `props` is per-event and quota-spending — opt-in, it warns before spending.

```
tools/odds_api.sh check                    # key + reachability + remaining quota
tools/odds_api.sh slate [date]             # pull+cache h2h/totals/spreads; best-ML table
tools/odds_api.sh best h2h|totals|spreads [date]   # best line per game per side, with the book
tools/odds_api.sh game "<team>" [date]     # full book-by-book board for one game
tools/odds_api.sh events [date]            # event IDs (free; needed for props)
tools/odds_api.sh props <eventId> pitcher_strikeouts[,batter_hits]   # PER-EVENT props (spends quota!)
tools/odds_api.sh clv <betAmerican> "<team>" [date]   # closing no-vig vs your bet (ML)
```

**How it slots in:** at **build** → `best` feeds the best two-sided price into `devig.sh` (min-edge gate vs
the genuinely best number). At the **15:30 / 18:30 runs** → `clv` snapshots the close for every open leg and
you write CLV into `results_log.md`. Pairs with `parlay.py` (real prices → real combined EV). Player props
(Ks/hits) are limited/quota-heavy on the free tier → keep pricing them by hand; the API owns ML/totals/spreads.

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

## `settle.py` — match a day's finals to open legs and PROPOSE settle edits

Automates the error-prone settle lookup: pulls `mlb_api.sh finals <date>`, finds `results_log.md` rows
that are still TBD for that date, maps each leg's team (by nickname) to its final, and proposes W/L for
team-side bets (ML / run line / spread). Props / totals / K-legs → flagged **MANUAL**. **READ-ONLY** —
prints proposals; you apply them (and `fades.md` / `bankroll.md` / the parlay file) so the audit trail
stays deliberate.

```
tools/settle.py                 # settle yesterday
tools/settle.py 2026-06-05      # settle a specific date
tools/settle.py 2026-06-05 path/to/results_log.md
```
