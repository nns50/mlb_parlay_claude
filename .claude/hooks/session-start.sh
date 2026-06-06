#!/bin/bash
#
# .claude/hooks/session-start.sh — UserPromptSubmit hook
#
# Fires on the FIRST message of each Claude Code session. Runs
# tools/session_start.sh, then detects the current ET time and tells Claude
# exactly which build to run — so the full routine is self-directed with no
# additional prompt needed from the user or cron.
#
# Output goes to stdout → shown to Claude as pre-prompt context.
# Sentinel on CLAUDE_SESSION_ID prevents re-running on every message.
#
set -uo pipefail

SESSION_SENTINEL="/tmp/mlb_session_init_${CLAUDE_SESSION_ID:-$$}"
if [[ -f "$SESSION_SENTINEL" ]]; then
  exit 0
fi
touch "$SESSION_SENTINEL"

cd "${CLAUDE_PROJECT_DIR:-/home/user/mlb_parlay_claude}" || exit 0

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  AUTO SESSION-START — tools/session_start.sh injected by hook   ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
bash tools/session_start.sh 2>&1 || true
echo ""

# ── Detect ET time and select build type ─────────────────────────────────────
HOUR=$(TZ="America/New_York" date +%H 2>/dev/null || date +%H)
ET_TIME=$(TZ="America/New_York" date '+%H:%M %Z' 2>/dev/null || date '+%H:%M')

if   (( 10#$HOUR >= 6  && 10#$HOUR < 12 )); then
  # Morning window (fires 6–11:59 ET) — catches 09:00 and 11:00 cron slots
  BUILD="09"
  LABEL="09:00 ET — morning settle + full build"
  INSTRUCTIONS="Run the 11:00 ET daily MLB parlay routine per CLAUDE.md:
1. Self-settle all TBD results from yesterday: run tools/settle.py, apply W/L to results_log.md + fades.md + bankroll.md.
2. Run tools/calib.py and apply the fresh calibration bands before building.
3. Run tools/mlb_api.sh slate today for the full game list.
4. Run tools/mlb_api.sh lineups today — lineups for early/day games (12pm-2pm ET first pitch) are ALREADY POSTED at 11 ET (post ~2-3h pre-game). Confirm those now; mark evening games PENDING LINEUP (re-checked at 16:00 run).
5. Do the mandatory slate-wide value scan (ALL games — non-ML markets first per CLAUDE.md). If the session digest above shows ODDS_MODE=rich, also run odds_api.sh events to get event IDs, then odds_api.sh props <id> pitcher_strikeouts for K-prop leg pricing instead of hand-pricing.
6. Fill SP-freshness blocks for every SP in the build.
7. Build all three tiers: Tier 1 best standalone, Tier 2 highest-floor 2-leg, Tier 3 +200 build. Day-game hitter props with confirmed lineups can be fully locked; evening hitter props stay PENDING.
8. Pick the bankroll bet (single safest qualifying fav, independent of parlay, not A-list fade).
9. Append this run to parlays/YYYY-MM-DD.md as '## Run 11:00 ET — Build A'.
10. Log all recommended legs in results_log.md with pre-registered TrueP + ImplP + Edge.
11. Commit → push → open PR → squash-merge → git reset to main per CLAUDE.md git workflow.
12. Email the build summary: load mcp__Gmail__create_draft via ToolSearch (if not already loaded), then create a draft to icecold67@live.com, subject 'MLB Parlay — [today YYYY-MM-DD] Build A', body: Tier 1 standalone (leg + edge + best price), Tier 2 2-leg (legs + floor%), Tier 3 +200 (legs + combined odds), bankroll bet, any PENDING flags or key warnings. Keep body under 250 words."

elif (( 10#$HOUR >= 12 && 10#$HOUR < 17 )); then
  # Lineup-lock window (fires 12:00–16:59 ET) — catches 16:00 cron slot
  # Lineups typically post ~4-5pm ET for 7pm games; 16:00 catches most of them.
  BUILD="15"
  LABEL="15:30 ET — CLV capture + lineup lock + build update"
  INSTRUCTIONS="Run the 15:30 ET MLB parlay update per CLAUDE.md:
1. Run tools/clv_capture.py for today — fill the CLV column in results_log.md for all open ML legs.
2. Run tools/mlb_api.sh lineups today — upgrade any PENDING LINEUP legs to CONFIRMED or keep flagged.
3. Run tools/mlb_api.sh ump today and tools/mlb_api.sh weather today — update K-Over/Under or total legs affected.
4. Run tools/odds_api.sh best h2h today — check for material line moves on active legs.
5. If any leg or price changed materially, APPEND '## Run 15:30 ET — Build B' to today's parlay file (do NOT overwrite Build A; mark old rows SUPERSEDED).
6. Update results_log.md with any new or revised legs per the SUPERSEDE protocol.
7. Confirm or update the bankroll bet if lineup was PENDING at 09:00.
8. Commit → push → open PR → squash-merge → reset per CLAUDE.md git workflow.
9. Email the Build B update: load mcp__Gmail__create_draft via ToolSearch (if not loaded), create a draft to icecold67@live.com, subject 'MLB Parlay — [today YYYY-MM-DD] Build B update', body: CLV fills (+ or − for each open leg), lineup upgrades (PENDING→CONFIRMED or still flagged), any superseded legs, current active build. Under 200 words."

else
  BUILD="18"
  LABEL="18:30 ET — final CLV + late lineups + line check"
  INSTRUCTIONS="Run the 18:30 ET final MLB parlay check per CLAUDE.md:
1. Run tools/clv_capture.py for today — update CLV column for any remaining open legs.
2. Run tools/mlb_api.sh lineups today — confirm late/west-coast lineups; upgrade remaining PENDING legs.
3. Run tools/odds_api.sh best h2h today — check for late sharp line moves on active legs.
4. If anything changed materially, APPEND '## Run 18:30 ET — Build C' to today's parlay file (mark prior build SUPERSEDED if replaced).
5. Flag any legs to re-check at first pitch.
6. Commit → push → open PR → squash-merge → reset per CLAUDE.md git workflow.
7. Email the final check: load mcp__Gmail__create_draft via ToolSearch (if not loaded), create a draft to icecold67@live.com, subject 'MLB Parlay — [today YYYY-MM-DD] Final check', body: late lineup confirmations, remaining CLV fills, final active build legs with prices, any first-pitch re-check flags. Under 200 words."
fi

echo "════════════════════════════════════════════════════════"
echo "  BUILD DIRECTIVE  (ET now: $ET_TIME)"
echo "  $LABEL"
echo "════════════════════════════════════════════════════════"
echo ""
echo "CLAUDE: execute the following build automatically per CLAUDE.md."
echo "The session_start.sh digest above is your live context. Begin now:"
echo ""
echo "$INSTRUCTIONS"
echo ""
