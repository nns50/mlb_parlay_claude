#!/usr/bin/env bash
# tools/clv_capture.sh — snapshot closing ML lines for open TBD legs in results_log.md.
#
# READ-ONLY — prints CLV proposals; apply the +/=/-  verdict to the CLV column by hand.
# Designed for 15:30 / 18:30 ET near-first-pitch runs.
# Auto-called from session_start.sh when the ET hour is 15–19.
#
# WHAT IT DOES
#   Scans results_log.md for rows matching ALL of:
#     • Date  = today (or the supplied date)
#     • Played = Y   (user has confirmed the bet)
#     • CLV   = —    (closing line not yet captured)
#     • Result contains TBD   (game not yet played)
#     • Type  contains ML or RL   (h2h CLV is meaningful; skip K/total props)
#   For each qualifying row: calls `odds_api.sh clv <price> <team>` and prints the output.
#
# REQUIRES
#   ODDS_API_KEY set + api.the-odds-api.com allowlisted (same env as odds_api.sh).
#
# USAGE
#   tools/clv_capture.sh [YYYY-MM-DD]   # defaults to today
#
# OUTPUT FORMAT
#   Each leg prints the closing no-vig, your bet implied, and a +/=/-  proxy CLV direction.
#   Copy the verdict (+/=/- or the exact no-vig %) into results_log.md's CLV column.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG="$REPO_ROOT/results_log.md"
ODDS="$SCRIPT_DIR/odds_api.sh"

[[ -f "$LOG" ]]   || { echo "SKIP: results_log.md not found."         >&2; exit 0; }
[[ -x "$ODDS" ]]  || { echo "SKIP: odds_api.sh not found/executable." >&2; exit 0; }
[[ -n "${ODDS_API_KEY:-}" ]] || { echo "SKIP: ODDS_API_KEY not set."  >&2; exit 0; }

TARGET_FULL="${1:-$(date +%F)}"
TARGET_SHORT="$(date -d "$TARGET_FULL" +%-m/%-d 2>/dev/null || \
  python3 -c "import datetime; d=datetime.date.fromisoformat('$TARGET_FULL'); print(f'{d.month}/{d.day}')")"

echo "════ CLV CAPTURE — ${TARGET_SHORT} ════"
echo "  Scanning for Played=Y + CLV=— + Result=TBD rows on ${TARGET_SHORT}..."

found=0
while IFS= read -r line; do
  # Only process table data rows
  [[ "$line" =~ ^\| ]] || continue

  # Parse via awk — tab-separated output for safe read
  IFS=$'\t' read -r rdate rleg rtype rprice rresult rplayed rclv < <(awk -F'|' '
  {
    for (i = 1; i <= NF; i++) { v = $i; gsub(/^[[:space:]]+|[[:space:]]+$/, "", v); col[i] = v }
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n",
      col[2], col[3], col[4], col[5], col[9], col[10], col[11]
  }' <<< "$line" 2>/dev/null) || continue

  # Skip header / separator rows (date must start with a digit)
  [[ -z "$rdate" || "$rdate" == "Date" ]] && continue
  [[ "$rdate" =~ ^[0-9] ]] || continue

  # Gate: today, Played=Y, CLV blank/dash/em-dash, Result contains TBD
  [[ "$rdate"   == "$TARGET_SHORT" ]]                          || continue
  [[ "$rplayed" == "Y" ]]                                      || continue
  [[ "$rclv"    == "—" || "$rclv" == "-" || -z "$rclv" ]]     || continue
  [[ "$rresult" =~ TBD ]]                                      || continue

  # Only ML / RL have meaningful h2h CLV
  if ! [[ "$rtype" =~ ML|RL|[Rr]un.?[Ll]ine ]]; then
    echo "  SKIP (${rtype} — h2h CLV N/A): $rleg" >&2
    continue
  fi

  # Clean price: strip ~ estimate prefix; must resolve to a bare integer
  price_clean="${rprice#\~}"
  if ! [[ "$price_clean" =~ ^[+-]?[0-9]+$ ]]; then
    echo "  SKIP (unparseable price '${rprice}'): $rleg" >&2
    continue
  fi

  # Extract team name: text before " ML", " RL", or " −" then drop any trailing parenthetical
  team="$(echo "$rleg" \
    | sed 's/[[:space:]]ML[[:space:]].*//' \
    | sed 's/[[:space:]]RL[[:space:]].*//' \
    | sed 's/[[:space:]]−.*//'             \
    | sed 's/[[:space:]]([^)]*)//'         \
    | sed 's/[[:space:]]*$//')"

  [[ -n "$team" ]] || { echo "  SKIP (can't extract team): $rleg" >&2; continue; }

  echo ""
  echo "  ── Leg: ${rleg}"
  echo "     Bet price: ${rprice}  |  Team lookup: \"${team}\""
  "$ODDS" clv "$price_clean" "$team" "$TARGET_FULL" 2>&1 \
    || echo "  (CLV lookup failed — team not matched in closing feed)"

  found=$((found + 1))
done < "$LOG"

echo ""
if (( found == 0 )); then
  echo "  No qualifying legs found (Played=Y + CLV=— + Result=TBD on ${TARGET_SHORT})."
  echo "  If a build was just confirmed, ensure results_log.md rows have Played=Y before re-running."
else
  echo "  → Copy each CLV verdict (+/=/-) into the CLV column in results_log.md."
fi
