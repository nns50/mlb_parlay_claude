#!/usr/bin/env bash
#
# session_start.sh — one-shot session-open digest for the parlay routine.
#
# WHY THIS EXISTS
#   The CLAUDE.md "Session-start review" is a fixed checklist that otherwise takes
#   6-8 manual tool calls every run (check → finals yesterday → standings → scan
#   recent parlays for TBD → read active fades). Skipping a step is how a TBD result
#   goes un-settled or a stale fade gets applied. This composes the MECHANICAL part
#   into a single command so the open is consistent and nothing is silently dropped.
#
#   READ-ONLY. It surfaces the inputs the routine needs; it does not bet, settle, or
#   mutate any file. The judgment steps (self-settle, apply calibration, slate scan)
#   are still done by the routine after reading this digest.
#
# USAGE
#   tools/session_start.sh            # uses today / yesterday
#   tools/session_start.sh 2026-06-04 # pretend "today" is this date (yesterday derived)
#
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

API="./tools/mlb_api.sh"
TODAY="${1:-$(date +%F)}"
# yesterday relative to TODAY (GNU date)
YESTERDAY="$(date -d "$TODAY - 1 day" +%F 2>/dev/null || date -v-1d -j -f %F "$TODAY" +%F 2>/dev/null || echo "")"

rule() { printf '%s\n' "────────────────────────────────────────────────────────"; }
hdr()  { echo; rule; echo " $*"; rule; }

echo "════════════════════════════════════════════════════════"
echo "  SESSION-START DIGEST   today=$TODAY  yesterday=$YESTERDAY"
echo "════════════════════════════════════════════════════════"

# 1. StatsAPI reachability — sets whether the live gates are available this session
hdr "1. StatsAPI check (game-status / finals / SP / fades source)"
if $API check 2>/dev/null; then
  LIVE=1
else
  LIVE=0
  echo "  ⚠ BLOCKED — fall back to the 2-source WebSearch gate (see CLAUDE.md)."
fi

# 1b. Odds API check + slate cache warm (line-shop / devig / CLV — optional; needs key + allowlist)
#     Warming the cache at session open (3 credits) means all `best`/`game`/`clv_capture`
#     calls for the rest of the session read from cache instantly, at no additional quota cost.
#     After warming, quota mode is derived from the remaining count and echoed as ODDS_MODE=<mode>
#     so Claude can read it from this digest and decide whether to use props calls for K-leg pricing.
hdr "1b. Odds API check + slate cache warm (line-shop / devig / CLV)"
if [[ -x "./tools/odds_api.sh" ]]; then
  ODDS_STATUS="$(./tools/odds_api.sh check 2>&1)"
  echo "$ODDS_STATUS" | sed 's/^/  /'
  if echo "$ODDS_STATUS" | grep -q "^OK"; then
    echo "  Warming odds slate cache ($TODAY) — 3 credits, valid all session..."
    SLATE_OUT="$(./tools/odds_api.sh slate "$TODAY" 2>&1)" || true
    echo "$SLATE_OUT" | sed 's/^/  /'
    # Quota mode derived from remaining credits after the warm call
    QUOTA_REM=$(echo "$SLATE_OUT" | grep "requests remaining" | grep -oE '[0-9]+' | head -1)
    QUOTA_REM="${QUOTA_REM:-9999}"
    if   (( QUOTA_REM < 20 )); then
      echo "  ⚠ LOW QUOTA (${QUOTA_REM} remaining) — avoid additional API calls this session."
      echo "  Manual price entry recommended. Do NOT run best/clv without checking first."
      echo "  ODDS_MODE=low_quota"
    elif (( QUOTA_REM >= 5000 )); then
      echo "  Odds API: RICH tier (${QUOTA_REM} remaining) — player props available for K-leg pricing."
      echo "  K-prop: odds_api.sh events → odds_api.sh props <id> pitcher_strikeouts"
      echo "  ODDS_MODE=rich"
    else
      echo "  Standard (${QUOTA_REM} remaining, free 500/mo). Use: odds_api.sh best h2h|totals|spreads"
      echo "  Props (K-leg pricing) require the paid tier — hand-price K-props this session."
      echo "  ODDS_MODE=standard"
    fi
  fi
else
  echo "  (tools/odds_api.sh not present)"
fi

# 2. Yesterday's finals — input for self-settling any TBD result/fade
hdr "2. Yesterday's finals ($YESTERDAY) — self-settle TBD results + fades"
if [[ "$LIVE" == "1" && -n "$YESTERDAY" ]]; then
  $API finals "$YESTERDAY" 2>/dev/null || echo "  (no finals returned)"
else
  echo "  (StatsAPI blocked or date unknown — use the WebSearch settle gate)"
fi

# 3. Standings — deterministic fade re-verification (L10 / streak / run diff)
hdr "3. Standings — fade re-verify (cross-check A/B entries vs L10 + run diff)"
if [[ "$LIVE" == "1" ]]; then
  $API standings 2>/dev/null || echo "  (standings unavailable)"
else
  echo "  (StatsAPI blocked)"
fi

# 4. Recent parlay files — which still carry an unsettled Result: TBD
#    Sort by FILENAME (YYYY-MM-DD = date order), not mtime. Scope the TBD test to the
#    "## Result" section only — bare "TBD" also means an unannounced starter ("SP TBD")
#    elsewhere in the file and must not be mistaken for an unsettled result.
hdr "4. Recent parlays — unsettled results (settle these first)"
result_section_tbd() {
  awk '
    /^##[[:space:]]*Result/            { inres=1; buf=buf $0 "\n"; next }
    inres && /^##[[:space:]]/ && $0 !~ /Result/ { inres=0 }
    inres                              { buf=buf $0 "\n" }
    END                                { printf "%s", buf }
  ' "$1" | grep -qi 'TBD'
}
found=0
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  found=1
  if ! grep -qiE '^##[[:space:]]*Result' "$f" 2>/dev/null; then
    echo "  ⚠ $(basename "$f") — no ## Result section yet"
  elif result_section_tbd "$f"; then
    echo "  ⚠ $(basename "$f") — Result still TBD → self-settle"
  else
    echo "  ✓ $(basename "$f") — settled"
  fi
done < <(ls -1 parlays/*.md 2>/dev/null | sort -r | head -3)
[[ "$found" == "1" ]] || echo "  (no parlay files found)"

# 5. Active fades — every tracked entry + current status, in one glance
hdr "5. Fade registry — entries + status (apply ACTIVE; skip RETIRED)"
if [[ -f fades.md ]]; then
  awk -F'|' '
    /^\| *[A-E][0-9] *\|/ {
      id=$2; name=$3; status=$(NF-1);
      gsub(/\*\*/,"",name); gsub(/\*\*/,"",status);
      gsub(/^[[:space:]]+|[[:space:]]+$/,"",id);
      gsub(/^[[:space:]]+|[[:space:]]+$/,"",name);
      gsub(/^[[:space:]]+|[[:space:]]+$/,"",status);
      if (length(name) > 26) name=substr(name,1,25) "…";
      if (length(status) > 40) status=substr(status,1,39) "…";
      printf "  %-4s %-27s %s\n", id, name, status;
    }' fades.md
else
  echo "  (fades.md not found)"
fi

# 5b. A/B-list team recent form — verify active fade/dog status before building each session.
#     Only A (fade-as-fav) and B (quietly-hot dog) teams need live teamform; C/D/E are rule fades.
#     Skip entries with "/" — those are multi-team entries that can't map to a single abbreviation.
hdr "5b. A/B fade team recent form (last 15 — verify before applying or retiring)"
if [[ "$LIVE" == "1" && -f fades.md ]]; then
  declare -A TF_MAP=(
    ["cubs"]="CHC"        ["white sox"]="CWS"   ["tigers"]="DET"    ["guardians"]="CLE"
    ["royals"]="KC"       ["twins"]="MIN"        ["brewers"]="MIL"   ["cardinals"]="STL"
    ["reds"]="CIN"        ["pirates"]="PIT"      ["phillies"]="PHI"  ["nationals"]="WSH"
    ["braves"]="ATL"      ["mets"]="NYM"         ["marlins"]="MIA"   ["dodgers"]="LAD"
    ["padres"]="SD"       ["giants"]="SF"        ["rockies"]="COL"   ["mariners"]="SEA"
    ["rangers"]="TEX"     ["astros"]="HOU"       ["angels"]="LAA"    ["athletics"]="ATH"
    ["yankees"]="NYY"     ["orioles"]="BAL"      ["rays"]="TB"       ["red sox"]="BOS"
    ["blue jays"]="TOR"   ["diamondbacks"]="AZ"  ["d-backs"]="AZ"    ["dbacks"]="AZ"
  )
  AB_TEAMS=$(awk -F'|' '
    /^\| *[AB][0-9]+ *\|/ {
      name=$(NF-6); status=$(NF-1)
      gsub(/\*\*/, "", name); gsub(/\*\*/, "", status)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", name)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", status)
      if (name !~ /\// && status ~ /^ACTIVE/) print tolower(name)
    }
  ' fades.md 2>/dev/null)
  if [[ -z "$AB_TEAMS" ]]; then
    echo "  (no active A/B entries in fades.md)"
  else
    while IFS= read -r team_lc; do
      [[ -z "$team_lc" ]] && continue
      abbr="${TF_MAP[$team_lc]:-}"
      if [[ -z "$abbr" ]]; then
        echo "  ⚠ '${team_lc}' — no abbreviation mapping (add to TF_MAP in session_start.sh)"
        continue
      fi
      echo "  ── ${team_lc} (${abbr}):"
      $API teamform "$abbr" 15 2>/dev/null | sed 's/^/    /' || echo "    (teamform unavailable)"
    done <<< "$AB_TEAMS"
  fi
else
  [[ "$LIVE" != "1" ]] && echo "  (StatsAPI blocked)" || echo "  (fades.md not found)"
fi

echo
echo "════════════════════════════════════════════════════════"
echo "  NEXT (routine judgment — not automated):"
echo "   • Self-settle any TBD above; write W/L + retro into the dated file."
echo "   • Read fades.md + results_log.md in FULL; apply calibration before building."
echo "   • Run tools/calib.py for fresh bands/ROI."
echo "   • Slate-wide value scan (ALL games) BEFORE narrowing to legs."
echo "   • At ~15:30/18:30: tools/mlb_api.sh lineups|ump|weather for the live gates."
echo "════════════════════════════════════════════════════════"
