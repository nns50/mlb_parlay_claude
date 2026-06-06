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

# 1b. Odds API check — line-shopping / devig / CLV source (optional; needs key + allowlist)
hdr "1b. Odds API check (line-shop / devig / CLV — optional)"
if [[ -x "./tools/odds_api.sh" ]]; then
  ./tools/odds_api.sh check 2>&1 | sed 's/^/  /' || true
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

echo
echo "════════════════════════════════════════════════════════"
echo "  NEXT (routine judgment — not automated):"
echo "   • Self-settle any TBD above; write W/L + retro into the dated file."
echo "   • Read fades.md + results_log.md in FULL; apply calibration before building."
echo "   • Run tools/calib.py for fresh bands/ROI."
echo "   • Slate-wide value scan (ALL games) BEFORE narrowing to legs."
echo "   • At ~15:30/18:30: tools/mlb_api.sh lineups|ump|weather for the live gates."
echo "════════════════════════════════════════════════════════"
