# tools/

## `mlb_api.sh` — authoritative MLB data via the public StatsAPI

Deterministic source for the things WebSearch keeps hallucinating: **game status**
(Scheduled / Pre-Game / In Progress / Final), **probable pitchers**, **final scores**,
and **pitcher season lines + start-by-start game logs**. Use it to resolve the
game-status gate and the SP-freshness gate without inferring from search prose.

### Status: BLOCKED in this environment (re-confirmed 2026-06-04, 2nd attempt)
The environment's egress is an **allowlist** enforced by a proxy that denies non-listed hosts
with `HTTP 403` + header `x-deny-reason: host_not_allowed`. Re-tested 2026-06-04 after the user
added a `*.mlb.com` rule and started a new session: **still BLOCKED.** Diagnosis was made airtight:
- `statsapi.mlb.com`, `www.mlb.com`, `mlb.com` → `403 x-deny-reason: host_not_allowed` (proxy denies; no upstream headers).
- `pypi.org`, `registry.npmjs.org`, `docs.claude.com`, `crates.io`, `api.github.com` → **pass the proxy** (reach the host).

So the environment is on **Trusted** (the default allowlist is active) but the custom `*.mlb.com`
entry is **NOT in this session's active policy** — i.e. a missing/unsaved custom domain on the
*specific environment this session launched from*, not a wildcard-syntax problem and not a blanket
no-network policy. The script **preflights** and prints a `BLOCKED` verdict (now naming the exact
deny reason) so the routine falls back to the 2-source WebSearch gate automatically.

### To enable it
The allowlist lives on the **cloud environment**, and BOTH interactive web sessions AND the
scheduled parlay routine *inherit that same environment's* network policy (docs:
[network access](https://code.claude.com/docs/en/claude-code-on-the-web#network-access),
[routines · environments-and-network-access](https://code.claude.com/docs/en/routines#environments-and-network-access)).
Fix the environment the routine actually uses:

1. **Open the environment for editing.**
   - For the routine: `claude.ai/code/routines` → open the parlay routine → pencil (**Edit**) →
     click the **cloud icon** (environment name, e.g. **Default**) → hover the environment → **settings gear**.
   - For interactive sessions: the same environment via the cloud icon where you start a session.
2. In **Update cloud environment**, set **Network access → Custom**; under **Allowed domains** add
   (one per line): `*.mlb.com`  (covers `statsapi.mlb.com`; `*.` wildcard subdomain matching is supported).
3. **Check "Also include default list of common package managers"** — otherwise you LOSE the
   Trusted defaults (pypi/npm/github-adjacent/etc.) and keep ONLY mlb.com.
4. **Save changes.** The policy applies **from the next run / a brand-new session** — a running
   container does NOT hot-reload (a mid-session edit leaves the live proxy still denying `*.mlb.com`).

Then verify with `./tools/mlb_api.sh check`:
- `OK` → live; prefer the StatsAPI for the status gate, prior-day `finals`, and SP-freshness this session.
- `BLOCKED … host_not_allowed` → the custom domain still isn't in THIS environment's active policy.
  Most common causes: **edited a different environment** than the routine/session uses; **didn't click Save changes**;
  or the **session started before the save landed** (start one more fresh session).

(The script is written against well-documented stable StatsAPI endpoints but has **not been
validated against live data in this environment** because the API is blocked here — sanity-check
the first live run, especially the `gamelog`/`pitcher` jq paths, and use `raw` to inspect the JSON
if a field looks off.)

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
