# tools/

## `mlb_api.sh` — authoritative MLB data via the public StatsAPI

Deterministic source for the things WebSearch keeps hallucinating: **game status**
(Scheduled / Pre-Game / In Progress / Final), **probable pitchers**, **final scores**,
and **pitcher season lines + start-by-start game logs**. Use it to resolve the
game-status gate and the SP-freshness gate without inferring from search prose.

### Status: LIVE ✅ (confirmed reachable 2026-06-04, this session)
The user allowlisted `*.mlb.com` on the environment and a **new session** picked it up, so
`./tools/mlb_api.sh check` now returns `OK`. The `slate` / `status` / `finals` / `pitcher` / `gamelog` /
`lineups` / `ump` / `splits` / `standings` / `teamform` commands have all been **validated against live data**.
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
- **K% by handedness (K-Over gate):** `splits <team>` returns team K% vs LHP and vs RHP from StatsAPI
  batting splits — deterministic replacement for manual K% research before K-Over legs.
- **Fade re-verification (`fades.md`):** `standings` gives every team's W-L / L10 / streak / run diff in
  one call, and `teamform <team> [N]` gives a precise last-N record + run differential — deterministic
  input for the "re-verify last-15 form each session" requirement (replaces manual WebSearch).
- **Always preferred when reachable; WebSearch gate is the fallback when `check` returns BLOCKED.**
