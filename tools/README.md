# tools/

## `mlb_api.sh` — authoritative MLB data via the public StatsAPI

Deterministic source for the things WebSearch keeps hallucinating: **game status**
(Scheduled / Pre-Game / In Progress / Final), **probable pitchers**, **final scores**,
and **pitcher season lines + start-by-start game logs**. Use it to resolve the
game-status gate and the SP-freshness gate without inferring from search prose.

### Status: BLOCKED in this environment (as of 2026-06-04)
The environment's egress is an **allowlist** enforced by a proxy that denies non-listed hosts
with `HTTP 403` + header `x-deny-reason: host_not_allowed` (confirmed for `statsapi.mlb.com` and
`www.mlb.com`; `api.github.com` passes). The script **preflights reachability** and prints a
`BLOCKED` message with guidance instead of returning garbage — so the parlay routine falls back
to the 2-source WebSearch game-status gate automatically.

### To enable it
1. Allowlist `*.mlb.com` (or `statsapi.mlb.com`) in the environment's **network policy** —
   chosen when the environment is created. https://code.claude.com/docs/en/claude-code-on-the-web
2. **Start a NEW Claude Code web session.** The policy is applied at environment/session startup;
   a running container does NOT hot-reload an updated allowlist, so the edit only takes effect in a
   fresh session. (Confirmed 2026-06-04: editing the policy mid-session left the live proxy still
   returning `host_not_allowed` for `*.mlb.com`.)

In the new session, `./tools/mlb_api.sh check` returns `OK` and every subcommand works with no
code change. (The script is written against well-documented stable StatsAPI endpoints but has
**not been validated against live data in this environment** because the API is blocked here —
sanity-check the first live run, especially the `gamelog`/`pitcher` jq paths, and use `raw` to
inspect the JSON if a field looks off.)

### Commands
```
tools/mlb_api.sh check                       # reachability preflight (exit 0 reachable, 2 blocked)
tools/mlb_api.sh slate   [YYYY-MM-DD]        # per-game status + probables + score
tools/mlb_api.sh status  [YYYY-MM-DD]        # compact one-line-per-game status (the gate)
tools/mlb_api.sh finals  [YYYY-MM-DD]        # final scores only (prior-day settle)
tools/mlb_api.sh pitcher <personId> [SEASON] # season ERA/WHIP/IP/K/K9/GS/W-L
tools/mlb_api.sh gamelog <personId> [SEASON] # start-by-start log (date, opp, IP, ER, K, BB)
tools/mlb_api.sh findpitcher "<name>"        # resolve a name -> personId
tools/mlb_api.sh raw "schedule?sportId=1&date=2026-06-04"   # raw JSON passthrough
```

### How it slots into the routine
- **Game-status gate:** `status`/`slate` give `abstractGameState` (Preview/Live/Final) and
  `detailedState` — authoritative. A `Final` here is a real final; a `Preview`/`Pre-Game`/`Warmup`
  means NOT started. This replaces inferring status from a search summary (no more re-stamp burns).
- **Prior-day settle:** `finals <yesterday>` returns every final score in one call.
- **SP-freshness gate:** `findpitcher` → `pitcher`/`gamelog` give the current season line AND the
  most-recent start (date/opp/IP/ER/K), exactly what the freshness field requires.
- **Always preferred when reachable; WebSearch gate is the fallback when `check` returns BLOCKED.**
