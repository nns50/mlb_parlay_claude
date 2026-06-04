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
#   tools/mlb_api.sh standings [SEASON]         # division standings: W-L, pct, GB, L10, streak, run diff
#   tools/mlb_api.sh teamform <id|abbr|name> [N]# last-N results: W-L + run differential (fade re-verify)
#   tools/mlb_api.sh findteam "<name|abbr>"     # resolve a team name/abbr -> teamId
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
# Returns 0 if the StatsAPI is reachable (HTTP 200), 2 otherwise. Distinguishes the
# THREE failure modes so the verdict is actionable, not a bare "403":
#   (a) host_not_allowed  -> the egress allowlist does NOT include *.mlb.com in THIS
#       session/run. This is the expected block until the environment policy is fixed.
#   (b) 000 / timeout     -> a real network error, not an allowlist denial.
#   (c) other non-200     -> host reachable but rate-limiting/erroring, or odd proxy state.
_check() {
  local hdrs code deny
  hdrs="$(mktemp)"
  code=$(curl -sS -m "$TIMEOUT" -o /dev/null -D "$hdrs" -w '%{http_code}' "$BASE/teams?sportId=1" 2>/dev/null || echo "000")
  deny=$(grep -i '^x-deny-reason:' "$hdrs" 2>/dev/null | awk '{print $2}' | tr -d '\r' || true)
  rm -f "$hdrs"
  if [[ "$code" == "200" ]]; then
    return 0
  fi
  if [[ "$deny" == "host_not_allowed" ]]; then
    cat >&2 <<EOF
BLOCKED: statsapi.mlb.com denied AT THE EGRESS PROXY (HTTP $code, x-deny-reason: host_not_allowed).
  The cloud environment's network allowlist does NOT include *.mlb.com in THIS session/run.
  (Trusted-default hosts like pypi.org / github still pass — only mlb.com is missing, so this
   is a missing custom-domain entry, not a blanket no-network policy.)
  FIX (per https://code.claude.com/docs/en/claude-code-on-the-web#network-access):
    Edit the environment used by BOTH your interactive sessions AND the parlay routine ->
    Network access = Custom -> Allowed domains: add  *.mlb.com  ->
    CHECK "Also include default list of common package managers" -> Save changes ->
    start a NEW session / next routine run (the policy applies at startup, never mid-session).
  If it is STILL blocked in a fresh session: you likely edited a different environment than the
  routine/session uses, or didn't click Save, or the session started before the save landed.
  Until OK, use the 2-source WebSearch game-status gate from CLAUDE.md.
EOF
  elif [[ "$code" == "000" ]]; then
    cat >&2 <<EOF
BLOCKED: could not reach statsapi.mlb.com (no HTTP response / timeout) — a network error,
  NOT an allowlist denial (no x-deny-reason header was returned). Check connectivity and retry.
  Until OK, use the 2-source WebSearch game-status gate from CLAUDE.md.
EOF
  else
    cat >&2 <<EOF
BLOCKED: statsapi.mlb.com returned HTTP $code with no 'host_not_allowed' deny header.
  Not the usual allowlist block — the host may be up but rate-limiting/erroring, or the proxy
  returned an unexpected status. Inspect the raw response with:
    tools/mlb_api.sh raw "teams?sportId=1"
  Until confirmed, use the 2-source WebSearch game-status gate from CLAUDE.md.
EOF
  fi
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
  if _check; then
    echo "OK: statsapi.mlb.com reachable — authoritative game-status / finals / SP data is LIVE."
    echo "    Prefer it for the game-status gate, prior-day settle, and SP-freshness this session."
  else
    return 2
  fi
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

# resolve a team name/abbreviation -> teamId (echoes the first match's id)
_resolve_team() {
  local q="${1:-}"
  [[ "$q" =~ ^[0-9]+$ ]] && { echo "$q"; return 0; }
  _fetch "teams?sportId=1" \
  | jq -r --arg q "$q" '
      ($q|ascii_upcase) as $Q
      | .teams[]
      | select((.abbreviation|ascii_upcase) == $Q
               or (.name|ascii_upcase|contains($Q))
               or (.teamName|ascii_upcase|contains($Q)))
      | .id' | head -1
}

cmd_findteam() {
  local q="${1:?usage: findteam \"<name|abbr>\"}"
  _fetch "teams?sportId=1" \
  | jq -r --arg q "$q" '
      ($q|ascii_upcase) as $Q
      | .teams[]
      | select((.abbreviation|ascii_upcase) == $Q
               or (.name|ascii_upcase|contains($Q))
               or (.teamName|ascii_upcase|contains($Q)))
      | "\(.id)\t\(.abbreviation)\t\(.name)"'
}

cmd_standings() {
  local season; season="$(_season_of "${1:-}")"
  _fetch "standings?leagueId=103,104&season=$season&standingsTypes=regularSeason" \
  | jq -r '
    ({"200":"AL West","201":"AL East","202":"AL Central",
      "203":"NL West","204":"NL East","205":"NL Central"}) as $div
    | .records[]
    | ("\n=== " + ($div[(.division.id|tostring)] // ("division "+(.division.id|tostring))) + " ==="),
      ( .teamRecords[]
        | . as $t
        | ([ $t.records.splitRecords[]? | select(.type=="lastTen") ] | first) as $l10
        | "  " + (($t.divisionRank // "?")|tostring) + ". "
          + ($t.team.name)
          + "  " + ($t.wins|tostring) + "-" + ($t.losses|tostring)
          + " (" + ($t.winningPercentage // "?") + ")"
          + "  GB " + ($t.gamesBack // "-")
          + "  L10 " + (($l10.wins // "?")|tostring) + "-" + (($l10.losses // "?")|tostring)
          + "  " + ($t.streak.streakCode // "-")
          + "  RDiff " + (if (($t.runDifferential // 0) >= 0) then "+" else "" end) + (($t.runDifferential // 0)|tostring)
      )'
}

cmd_teamform() {
  local arg="${1:?usage: teamform <teamId|abbr|name> [N]}"
  local n="${2:-10}"
  local id; id="$(_resolve_team "$arg")"
  [[ -n "$id" ]] || die "could not resolve team '$arg' (try a teamId or an abbreviation like DET)"
  local start end
  start="$(date -d '25 days ago' +%F)"; end="$(date +%F)"
  _fetch "schedule?sportId=1&teamId=$id&startDate=$start&endDate=$end&hydrate=team,linescore" \
  | jq -r --argjson n "$n" --arg id "$id" '
    [ .dates[]?.games[]?
      | select(.status.abstractGameState=="Final")
      | select(.teams.home.score != null and .teams.away.score != null) ]
    | sort_by(.officialDate) | reverse | .[0:$n] | reverse
    | map(
        . as $g
        | ($g.teams.home.team.id == ($id|tonumber)) as $home
        | (if $home then $g.teams.home.score else $g.teams.away.score end) as $ts
        | (if $home then $g.teams.away.score else $g.teams.home.score end) as $os
        | (if $home then $g.teams.away.team.abbreviation else $g.teams.home.team.abbreviation end) as $opp
        | { date: $g.officialDate, loc: (if $home then "vs" else " @" end),
            opp: $opp, ts: $ts, os: $os, win: ($ts > $os), diff: ($ts - $os) } )
    | (map(select(.win)) | length) as $w
    | (length - $w) as $l
    | (map(.diff) | add // 0) as $rd
    | "team " + $id + " last " + (length|tostring) + ": " + ($w|tostring) + "-" + ($l|tostring)
      + "   run diff " + (if $rd>=0 then "+" else "" end) + ($rd|tostring),
      ( .[] | "  " + .date + "  " + .loc + " " + .opp + "  "
              + (if .win then "W" else "L" end) + " " + (.ts|tostring) + "-" + (.os|tostring) )'
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
    standings)   cmd_standings "$@";;
    teamform)    cmd_teamform "$@";;
    findteam)    cmd_findteam "$@";;
    raw)         cmd_raw "$@";;
    ""|-h|--help|help)
      sed -n '2,40p' "$0";;
    *) die "unknown subcommand: $sub (try: check slate status finals pitcher gamelog findpitcher standings teamform findteam raw)";;
  esac
}
main "$@"
