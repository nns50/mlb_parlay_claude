#!/usr/bin/env bash
#
# mlb_api.sh — authoritative MLB data via the public MLB StatsAPI (statsapi.mlb.com).
#
# WHY THIS EXISTS
#   Almost every painful round-trip in the parlay routine has been a WebSearch
#   hallucination: re-stamped finals, stale SP lines, wrong probables, wrong opponent.
#   The StatsAPI is the authoritative source and DETERMINISTICALLY resolves the
#   game-status gate (Scheduled / Pre-Game / In Progress / Final) plus probables,
#   finals, and pitcher game logs — no inference from search prose.
#
# IMPORTANT — NETWORK POLICY
#   This environment's egress is an ALLOWLIST. As of 2026-06-04, statsapi.mlb.com is
#   BLOCKED (HTTP 403 at the proxy in ~30ms; sandbox on or off; WebFetch also 403).
#   This script therefore PREFLIGHTS reachability and prints "BLOCKED" with guidance
#   instead of returning garbage. To enable it, the environment's network policy must
#   allowlist `statsapi.mlb.com` (configured when the environment is created —
#   see https://code.claude.com/docs/en/claude-code-on-the-web). Until then, the
#   parlay routine falls back to the 2-source WebSearch game-status gate.
#
# USAGE
#   tools/mlb_api.sh check                      # reachability preflight (exit 0 = reachable)
#   tools/mlb_api.sh slate [YYYY-MM-DD]         # schedule: status + probables + score per game
#   tools/mlb_api.sh status [YYYY-MM-DD]        # compact one-line-per-game status (the gate)
#   tools/mlb_api.sh finals [YYYY-MM-DD]        # final scores only (for prior-day settle)
#   tools/mlb_api.sh pitcher <personId> [SEASON]# season pitching line (ERA/WHIP/K) + last start
#   tools/mlb_api.sh gamelog <personId> [SEASON]# start-by-start pitching game log
#   tools/mlb_api.sh findpitcher "<name>"       # resolve a pitcher name -> personId
#   tools/mlb_api.sh raw "<api-path-and-query>" # raw JSON passthrough (e.g. "schedule?sportId=1")
#
# Dates default to today (local). SEASON defaults to the year of the date arg / today.
set -euo pipefail

BASE="https://statsapi.mlb.com/api/v1"
TIMEOUT=20

die() { echo "ERROR: $*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }
have curl || die "curl not found"
have jq   || die "jq not found"

# --- reachability preflight ---------------------------------------------------
# Returns 0 if the StatsAPI is reachable, 2 if blocked by the egress policy.
_check() {
  local code
  code=$(curl -sS -m "$TIMEOUT" -o /dev/null -w '%{http_code}' "$BASE/teams?sportId=1" 2>/dev/null || echo "000")
  if [[ "$code" == "200" ]]; then
    return 0
  fi
  cat >&2 <<EOF
BLOCKED: statsapi.mlb.com returned HTTP $code (egress policy / unreachable).
  This environment's network allowlist does not currently include statsapi.mlb.com.
  To enable authoritative MLB data, allowlist statsapi.mlb.com in the environment's
  network policy (set at environment-creation time):
    https://code.claude.com/docs/en/claude-code-on-the-web
  Until then, use the 2-source WebSearch game-status gate from CLAUDE.md.
EOF
  return 2
}

# fetch <path-with-query>  -> stdout JSON (preflights first)
_fetch() {
  _check || exit 2
  curl -sS -m "$TIMEOUT" "$BASE/$1"
}

_default_date() { date +%F; }
_season_of()    { echo "${1:-$(date +%F)}" | cut -d- -f1; }

cmd_check() {
  if _check; then echo "OK: statsapi.mlb.com reachable."; else return 2; fi
}

cmd_slate() {
  local d="${1:-$(_default_date)}"
  _fetch "schedule?sportId=1&date=$d&hydrate=probablePitcher,linescore,team" \
  | jq -r --arg d "$d" '
    "=== MLB slate " + $d + " ===",
    (.dates[]?.games[]? |
      "[" + .status.abstractGameState + "/" + .status.detailedState + "] "
      + (.teams.away.team.name) + " @ " + (.teams.home.team.name)
      + "  (" + ((.gameDate // "") ) + ")"
      + "\n    away SP: " + (.teams.away.probablePitcher.fullName // "TBD")
      + " | home SP: " + (.teams.home.probablePitcher.fullName // "TBD")
      + (if .status.abstractGameState == "Final"
         then "\n    FINAL: " + (.teams.away.team.abbreviation // .teams.away.team.name) + " " + ((.teams.away.score|tostring)//"?")
              + " - " + (.teams.home.team.abbreviation // .teams.home.team.name) + " " + ((.teams.home.score|tostring)//"?")
         else "" end)
    )'
}

cmd_status() {
  local d="${1:-$(_default_date)}"
  _fetch "schedule?sportId=1&date=$d" \
  | jq -r --arg d "$d" '
    .dates[]?.games[]? |
    .status.abstractGameState + " | " + .status.detailedState + " | "
    + (.teams.away.team.abbreviation // .teams.away.team.name) + " @ "
    + (.teams.home.team.abbreviation // .teams.home.team.name)
    + " | " + (.gameDate // "")'
}

cmd_finals() {
  local d="${1:-$(_default_date)}"
  _fetch "schedule?sportId=1&date=$d&hydrate=linescore,team" \
  | jq -r '
    .dates[]?.games[]? | select(.status.abstractGameState == "Final") |
    (.teams.away.team.abbreviation // .teams.away.team.name) + " " + ((.teams.away.score|tostring)//"?")
    + " - "
    + (.teams.home.team.abbreviation // .teams.home.team.name) + " " + ((.teams.home.score|tostring)//"?")
    + "   [" + .status.detailedState + "]"'
}

cmd_findpitcher() {
  local name="${1:?usage: findpitcher \"<name>\"}"
  # URL-encode spaces
  local q="${name// /%20}"
  _fetch "people/search?names=$q" 2>/dev/null \
  | jq -r '.people[]? | "\(.id)\t\(.fullName)\t\(.primaryPosition.abbreviation // "")\t\(.currentTeam.name // "")"' \
  || die "name search endpoint unavailable; use 'raw' with a sports/people query"
}

cmd_pitcher() {
  local id="${1:?usage: pitcher <personId> [season]}"
  local season; season="$(_season_of "${2:-}")"
  _fetch "people/$id?hydrate=stats(group=pitching,type=season,season=$season)" \
  | jq -r --arg s "$season" '
    .people[0] as $p |
    "Pitcher: " + ($p.fullName // "?") + " (id " + (($p.id|tostring)) + ")  season " + $s,
    ( $p.stats[]?.splits[]?.stat |
      "  ERA " + ((.era|tostring)//"?") + " | WHIP " + ((.whip|tostring)//"?")
      + " | IP " + ((.inningsPitched|tostring)//"?") + " | K " + ((.strikeOuts|tostring)//"?")
      + " | K/9 " + ((.strikeoutsPer9Inn|tostring)//"?")
      + " | GS " + ((.gamesStarted|tostring)//"?") + " | W-L " + ((.wins|tostring)//"?") + "-" + ((.losses|tostring)//"?")
    )'
}

cmd_gamelog() {
  local id="${1:?usage: gamelog <personId> [season]}"
  local season; season="$(_season_of "${2:-}")"
  _fetch "people/$id/stats?stats=gameLog&group=pitching&season=$season" \
  | jq -r '
    "date        opp     IP   ER  K  BB  result",
    ( .stats[]?.splits[]? |
      (.date // "?") + "  "
      + (if .isHome then "vs " else "@ " end) + ((.opponent.abbreviation // .opponent.name // "?"))
      + "  " + ((.stat.inningsPitched|tostring)//"?")
      + "  " + ((.stat.earnedRuns|tostring)//"?")
      + "  " + ((.stat.strikeOuts|tostring)//"?")
      + "  " + ((.stat.baseOnBalls|tostring)//"?")
    )'
}

cmd_raw() {
  local path="${1:?usage: raw \"<api-path-and-query>\"}"
  _fetch "$path" | jq .
}

main() {
  local sub="${1:-}"; shift || true
  case "$sub" in
    check)       cmd_check "$@";;
    slate)       cmd_slate "$@";;
    status)      cmd_status "$@";;
    finals)      cmd_finals "$@";;
    pitcher)     cmd_pitcher "$@";;
    gamelog)     cmd_gamelog "$@";;
    findpitcher) cmd_findpitcher "$@";;
    raw)         cmd_raw "$@";;
    ""|-h|--help|help)
      sed -n '2,40p' "$0";;
    *) die "unknown subcommand: $sub (try: check slate status finals pitcher gamelog findpitcher raw)";;
  esac
}
main "$@"
