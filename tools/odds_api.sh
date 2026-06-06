#!/usr/bin/env bash
#
# odds_api.sh — sportsbook odds via The Odds API (api.the-odds-api.com).
#
# WHY THIS EXISTS
#   Every price in the routine has been hand-entered, so line-shopping, devig, and CLV
#   were manual and lossy — and CLV (the only real edge scoreboard) stayed empty because
#   the building session dies before first pitch. This pulls live book prices so the build
#   bets the BEST number (free EV) and a near-first-pitch run can snapshot the close to
#   fill CLV. It does NOT raise win probability — it improves PRICE and MEASUREMENT.
#
# IMPORTANT — NETWORK POLICY + KEY (both required)
#   • Egress is an allowlist: the environment must allowlist `api.the-odds-api.com`
#     (Network access → Custom; applies only in a NEW session). Until then `check` = BLOCKED.
#   • Set the API key as the env var ODDS_API_KEY (a secret — NEVER commit it). `check`
#     verifies the key and prints remaining monthly quota.
#
# BUDGET (paid tier = 20K req/mo; free tier = 500 req/mo)
#   Quota cost = (#markets × #regions) per call. `slate` (h2h,totals,spreads × us) = 3 credits
#   and returns the WHOLE board, so it is CACHED per run — every leg reads the cache, not the API.
#   `events` is free (0). `props` is PER-EVENT — 1 credit per market per event (pitcher_strikeouts
#   for a full 15-game slate ≈ 15 credits). Available on the paid tier; session_start.sh sets
#   ODDS_MODE=rich when ≥5000 credits remain, which gates whether props are used.
#
# USAGE
#   tools/odds_api.sh check                      # key + reachability + remaining quota
#   tools/odds_api.sh slate   [YYYY-MM-DD]       # pull+cache h2h/totals/spreads; best-price table
#   tools/odds_api.sh best    <h2h|totals|spreads> [date]   # best line per game per side (from cache)
#   tools/odds_api.sh game    "<team>" [date]    # full book-by-book board for one game
#   tools/odds_api.sh events  [date]             # list event IDs (free; needed for props)
#   tools/odds_api.sh props   <eventId> <market[,market]>   # PER-EVENT player props (spends quota!)
#   tools/odds_api.sh clv     <betAmerican> "<team>" [date] # closing no-vig vs your bet price (ML)
#   tools/odds_api.sh raw     "<path-and-query>"            # raw passthrough (apiKey auto-appended)
#
# Common prop market keys: pitcher_strikeouts, pitcher_outs, batter_hits, batter_total_bases.
# Dates default to today; game-day filtering uses ET (EDT, UTC-4) on commence_time.
set -uo pipefail

BASE="https://api.the-odds-api.com/v4"
SPORT="baseball_mlb"
REGIONS="us"
TIMEOUT=25
ET_OFFSET=-4   # EDT (June); flip to -5 for EST if used off-season
CACHE_DIR="${TMPDIR:-/tmp}/odds_cache"
mkdir -p "$CACHE_DIR"

die()  { echo "ERROR: $*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }
have curl || die "curl not found"
have jq   || die "jq not found"

# Key is required for live calls, but not for `check` (which reports the missing key) or bare help.
if [[ -z "${ODDS_API_KEY:-}" && -n "${1:-}" && "${1:-}" != "check" ]]; then
  die "ODDS_API_KEY is not set (export it as a secret env var; never commit it)."
fi

TODAY="$(date +%F)"

# GET with apiKey appended; captures headers to $HDRS_FILE for quota/deny inspection.
# IMPORTANT: HDRS_FILE is a fixed per-process path (not mktemp inside api_get) so that quota
# headers written by a subshell invocation of api_get (via raw="$(api_get ...)") are readable
# by quota_line() in the parent shell — a subshell can write to the same file path even though
# variable assignments inside $() don't propagate back to the parent.
HDRS_FILE="${TMPDIR:-/tmp}/odds_api_hdrs_$$"
api_get() {
  local path="$1" sep
  [[ "$path" == *\?* ]] && sep="&" || sep="?"
  curl -sS -m "$TIMEOUT" -D "$HDRS_FILE" "${BASE}/${path}${sep}apiKey=${ODDS_API_KEY}" 2>/dev/null
}
quota_line() {
  [[ -f "$HDRS_FILE" ]] || return 0
  local rem used
  rem=$(grep -i '^x-requests-remaining:'  "$HDRS_FILE" | awk '{print $2}' | tr -d '\r')
  used=$(grep -i '^x-requests-used:'       "$HDRS_FILE" | awk '{print $2}' | tr -d '\r')
  [[ -n "$rem" ]] && echo "  quota: ${rem} requests remaining this month (used ${used:-?})." >&2
}
deny_reason() { [[ -f "$HDRS_FILE" ]] && grep -i '^x-deny-reason:' "$HDRS_FILE" | awk '{print $2}' | tr -d '\r'; }

# Filter a /odds or /events JSON array to games whose ET date == $1.
filter_date() {
  jq --arg d "$1" --argjson off "$ET_OFFSET" \
     '[ .[] | select((.commence_time|fromdateiso8601 + ($off*3600) | strftime("%Y-%m-%d")) == $d) ]'
}

cmd_check() {
  [[ -n "${ODDS_API_KEY:-}" ]] || { echo "NO KEY: set ODDS_API_KEY (secret env var). Get one at the-odds-api.com." >&2; exit 3; }
  local body code
  body="$(api_get "sports?all=true")"; code=$?
  if [[ -n "$(deny_reason)" ]]; then
    echo "BLOCKED: api.the-odds-api.com denied at the egress proxy (x-deny-reason: $(deny_reason))." >&2
    echo "  Add 'api.the-odds-api.com' to the environment's Network allowlist, then start a NEW session." >&2
    rm -f "$HDRS_FILE"; exit 2
  fi
  if echo "$body" | jq -e 'type=="array"' >/dev/null 2>&1; then
    echo "OK: The Odds API reachable and key valid."
    quota_line
    rm -f "$HDRS_FILE"; return 0
  fi
  echo "BLOCKED/ERROR: unexpected response (bad key? quota? network):" >&2
  echo "$body" | head -c 300 >&2; echo >&2
  rm -f "$HDRS_FILE"; exit 2
}

cache_file() { echo "$CACHE_DIR/slate_${1}.json"; }

cmd_slate() {
  local date="${1:-$TODAY}" cf raw
  cf="$(cache_file "$date")"
  raw="$(api_get "sports/${SPORT}/odds?regions=${REGIONS}&markets=h2h,totals,spreads&oddsFormat=american&dateFormat=iso")"
  if ! echo "$raw" | jq -e 'type=="array"' >/dev/null 2>&1; then
    echo "ERROR pulling odds: $(echo "$raw" | head -c 300)" >&2; quota_line; rm -f "$HDRS_FILE"; exit 2
  fi
  echo "$raw" | filter_date "$date" > "$cf"
  quota_line; rm -f "$HDRS_FILE"
  local n; n=$(jq 'length' "$cf")
  echo "════ best ML lines — ${date} (${n} games, cached) ════"
  [[ "$n" -eq 0 ]] && { echo "(no games on this ET date in the feed)"; return 0; }
  jq -r "$(best_jq h2h)" "$cf"
  echo "  (totals/spreads also cached → 'tools/odds_api.sh best totals ${date}' / 'best spreads ${date}')"
}

# Shared jq: best price per outcome across books, with the winning book's name.
best_jq() {
  cat <<JQ
def sign(p): if p>0 then "+" else "" end;
.[] | . as \$g
| "── \(\$g.away_team) @ \(\$g.home_team)"
, ( [ \$g.bookmakers[] | {bk:.title, o:(.markets[]?|select(.key=="$1").outcomes[]?) } ]
    | group_by(.o.name)[]
    | max_by(.o.price) as \$b
    | "   \(\$b.o.name)\(if \$b.o.point != null then " "+(\$b.o.point|tostring) else "" end): \(sign(\$b.o.price))\(\$b.o.price)  @\(\$b.bk)" )
JQ
}

ensure_cache() {
  local date="$1" cf; cf="$(cache_file "$date")"
  [[ -f "$cf" ]] || cmd_slate "$date" >/dev/null
  echo "$cf"
}

cmd_best() {
  local mk="${1:?market: h2h|totals|spreads}" date="${2:-$TODAY}" cf
  case "$mk" in h2h|totals|spreads) ;; *) die "market must be h2h, totals, or spreads" ;; esac
  cf="$(ensure_cache "$date")"
  jq -r "$(best_jq "$mk")" "$cf"
}

cmd_game() {
  local team="${1:?team name or city}" date="${2:-$TODAY}" cf
  cf="$(ensure_cache "$date")"
  jq -r --arg t "$team" '
    .[] | select((.home_team+" "+.away_team)|ascii_downcase|contains($t|ascii_downcase))
    | "════ \(.away_team) @ \(.home_team)  (\(.commence_time)) ════",
      ( .bookmakers[] | "── \(.title)",
        ( .markets[] | "   [\(.key)] " + ([.outcomes[] | "\(.name)\(if .point then " "+(.point|tostring) else "" end) \(if .price>0 then "+" else "" end)\(.price)"]|join("  ")) ) )
  ' "$cf"
}

cmd_events() {
  local date="${1:-$TODAY}" raw
  raw="$(api_get "sports/${SPORT}/events?dateFormat=iso")"
  rm -f "$HDRS_FILE"
  echo "$raw" | filter_date "$date" | jq -r '.[] | "\(.id)  \(.away_team) @ \(.home_team)  \(.commence_time)"'
}

cmd_props() {
  local eid="${1:?eventId (from `events`)}" markets="${2:?market keys e.g. pitcher_strikeouts}"
  echo "ℹ PER-EVENT prop call — 1 credit/market (paid tier: negligible; free tier: use sparingly). Markets: $markets" >&2
  local raw; raw="$(api_get "sports/${SPORT}/events/${eid}/odds?regions=${REGIONS}&markets=${markets}&oddsFormat=american&dateFormat=iso")"
  quota_line
  echo "$raw" | jq -r '
    "════ \(.away_team) @ \(.home_team) ════",
    ( .bookmakers[] | "── \(.title)",
      ( .markets[] | "   [\(.key)]",
        ( .outcomes[] | "      \(.description // .name) \(.name) \(.point // "") \(if .price>0 then "+" else "" end)\(.price)" ) ) )
  ' 2>/dev/null || { echo "no prop data (event not found, market unsupported on tier, or quota):"; echo "$raw" | head -c 300; }
  rm -f "$HDRS_FILE"
}

# CLV for a moneyline bet: closing best price both sides → no-vig → vs your bet's raw implied.
cmd_clv() {
  local bet="${1:?your bet American price}" team="${2:?team}" date="${3:-$TODAY}" raw
  raw="$(api_get "sports/${SPORT}/odds?regions=${REGIONS}&markets=h2h&oddsFormat=american&dateFormat=iso")"
  quota_line; rm -f "$HDRS_FILE"
  echo "$raw" | filter_date "$date" | jq -r --arg t "$team" --argjson bet "$bet" '
    def imp(p): if p>0 then 100/(p+100) else (-p)/((-p)+100) end;
    def sign(p): if p>0 then "+" else "" end;
    .[] | select((.home_team+" "+.away_team)|ascii_downcase|contains($t|ascii_downcase))
    | [ .bookmakers[].markets[]? | select(.key=="h2h").outcomes[] ] as $o
    | ($o | group_by(.name) | map(max_by(.price))) as $bests
    | ($bests | map(imp(.price)) | add) as $overround
    | ($bests[] | select((.name|ascii_downcase)|contains($t|ascii_downcase))) as $my
    | (imp($my.price)/$overround) as $novig_close
    | "Game: \(.away_team) @ \(.home_team)",
      "Your bet:  \(sign($bet))\($bet)  → raw implied \((imp($bet)*100)|floor)%",
      "Close best \($my.name): \(sign($my.price))\($my.price)  → no-vig \(($novig_close*100)|floor)%",
      "→ EXACT CLV: compare the closing no-vig \(($novig_close*100)|floor)% to your LOGGED bet no-vig in",
      "  results_log.md (CLV + if closing no-vig > bet no-vig). The line below uses raw bet implied as a",
      "  quick proxy and slightly overstates your side:",
      "  proxy CLV: \(if $novig_close > imp($bet) then "+ (line moved TO your side ✓)" else "− (line moved against you)" end)"
  ' 2>/dev/null || echo "Could not compute CLV (team not matched / no h2h in feed)."
}

cmd_raw() { local p="${1:?path}"; api_get "$p"; rm -f "$HDRS_FILE"; echo; }

case "${1:-}" in
  check)   cmd_check ;;
  slate)   shift; cmd_slate "$@" ;;
  best)    shift; cmd_best "$@" ;;
  game)    shift; cmd_game "$@" ;;
  events)  shift; cmd_events "$@" ;;
  props)   shift; cmd_props "$@" ;;
  clv)     shift; cmd_clv "$@" ;;
  raw)     shift; cmd_raw "$@" ;;
  *) sed -n '2,40p' "$0"; exit 1 ;;
esac
