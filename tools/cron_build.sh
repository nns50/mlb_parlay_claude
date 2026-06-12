#!/usr/bin/env bash
#
# cron_build.sh — time-aware cron entry point for the MLB parlay routine.
#
# HOW IT WORKS
#   1. Detects the current ET wall-clock time (or accepts a forced build type).
#   2. Selects the matching prompt (09 / 15 / 18 build).
#   3. Invokes `claude --print` (non-interactive) with that prompt.
#   4. The UserPromptSubmit hook fires → injects the session_start.sh digest
#      automatically → Claude runs the full routine and exits.
#
# CRONTAB EXAMPLE (ACTUAL schedule: 3 runs/day at 11:00, 16:00, 18:00 ET — user-confirmed 6/7/26)
#   # MLB parlay routine — 11:00, 16:00, 18:00 ET (adjust TZ as needed)
#   0  11  * * * bash /home/user/mlb_parlay_claude/tools/cron_build.sh 11 >> /tmp/mlb_cron.log 2>&1
#   0  16  * * * bash /home/user/mlb_parlay_claude/tools/cron_build.sh 16 >> /tmp/mlb_cron.log 2>&1
#   0  18  * * * bash /home/user/mlb_parlay_claude/tools/cron_build.sh 18 >> /tmp/mlb_cron.log 2>&1
#
# USAGE
#   tools/cron_build.sh           # auto-detect build from ET time (11→morning, 16→midday, 18→final)
#   tools/cron_build.sh 11        # force the 11:00 morning settle + build (alias: 09)
#   tools/cron_build.sh 16        # force the 16:00 CLV + lineup lock + user-angle build (alias: 15)
#   tools/cron_build.sh 18        # force the 18:00 final check + live-ML settle
#
# REQUIREMENTS
#   • `claude` CLI on PATH (Claude Code — https://claude.ai/code).
#   • ODDS_API_KEY set in the environment (for odds_api.sh calls).
#
set -uo pipefail
cd "$(dirname "$0")/.."

# ── Build type: forced arg OR auto-detect from ET hour ───────────────────────
# ACTUAL SCHEDULE (user-confirmed 6/7/26): the routine fires 3×/day at 11:00, 16:00, 18:00 ET.
#   11:00 ET → "morning"  (settle yesterday + full scan + initial 3-tier build; pre-lineup, props PENDING)
#   16:00 ET → "midday"   (lineup lock for the evening core + CLV + user-angle execution; revise build)
#   18:00 ET → "final"    (late/west-coast lineups + final CLV + live-ML trigger settle)
# Parse args order-independently so `--prompt-only` works WITH or WITHOUT an explicit hour
# (Bug 6/7/26: a bare `--prompt-only` was taken as the build type and hit the error case).
PROMPT_ONLY=0
BUILD=""
for a in "$@"; do
  case "$a" in
    --prompt-only) PROMPT_ONLY=1 ;;
    *) [[ -z "$BUILD" ]] && BUILD="$a" ;;
  esac
done
if [[ -z "$BUILD" ]]; then
  HOUR=$(TZ="America/New_York" date +%H 2>/dev/null || date +%H)
  if   (( 10#$HOUR >= 6  && 10#$HOUR < 14 )); then BUILD="11"
  elif (( 10#$HOUR >= 14 && 10#$HOUR < 17 )); then BUILD="16"
  else BUILD="18"
  fi
fi

# ── Prompts — each is a self-contained instruction for Claude ─────────────────
case "$BUILD" in

11|09|9)
  LABEL="11:00 ET — morning settle + full build (pre-lineup)"
  PROMPT="Run the 11:00 ET daily MLB parlay routine per CLAUDE.md (first of 3 runs: 11:00 / 16:00 / 18:00 ET). This is the morning build — lineups are NOT posted yet, so hitter/K/prop legs are PENDING LINEUP (the 16:00 run locks them). The session_start.sh digest is already in your context (injected by hook). Steps:
1. Self-settle all TBD results from yesterday: run tools/settle.py, apply W/L to results_log.md + fades.md + bankroll.md.
2. Run tools/calib.py and apply the fresh calibration bands before building.
3. Run tools/mlb_api.sh slate today for the full game list.
4. Do the mandatory slate-wide value scan (ALL games — non-ML markets first per CLAUDE.md).
4b. NRFI/YRFI TRACKER (nrfi_tracker.md — standalone daily tracker, NOT part of the 3-tier build; MANDATORY every run): (a) SETTLE every still-TBD prior-day read — pull the 1st-inning line score via tools/mlb_api.sh raw \"schedule?sportId=1&date=<yesterday>&hydrate=linescore,team\" (innings[0] away.runs+home.runs; total=0 -> NRFI occurred, total>0 -> YRFI), mark each ledger row W/L and update the running record; (b) REPLACE the 'Tonight's reads' section with TODAY's full slate — one NRFI (Under 0.5) / YRFI (Over 0.5) model-lean per game derived from both SPs' 1st-inning quality + both 1-2-3 trios (OBP/power) + park/weather, each with a pre-registered TrueP, and append one ledger row per game (model-only/no-bet unless you pull a real totals_1st_1_innings line that clears the +2pp gate). The dashboard step renders this file, so updating it daily is what keeps the dashboard's NRFI list fresh.
5. Fill SP-freshness blocks for every SP in the build.
6. Build all three tiers: Tier 1 best standalone, Tier 2 highest-floor 2-leg, Tier 3 +200 build.
7. Pick the bankroll bet (single safest qualifying fav, independent of parlay, not A-list fade).
8. Append this run to parlays/YYYY-MM-DD.md as '## Run 11:00 ET — Build A'.
9. Log all recommended legs in results_log.md with pre-registered TrueP + ImplP + Edge.
10. ODDS API CREDITS: run tools/odds_api.sh quota (FREE — 0 credits) and add a line 'Odds API credits remaining: <N> (used <M> this month)' to this run's section in today's parlay file BEFORE committing so it's captured in the repo record.
10b. DASHBOARD: run 'python3 tools/generate_dashboard.py' to refresh docs/index.html from the updated ledgers, and stage docs/index.html in the same commit (GitHub Pages auto-deploys it on merge to main).
11. Commit → push → open PR → squash-merge → git fetch+reset to main per CLAUDE.md git workflow.
12. Push notification: load PushNotification via ToolSearch (if needed), send title 'MLB Parlay Build A — <today>' summarizing Tier 1 standalone leg+edge, Tier 2 floor%, Tier 3 combined odds, bankroll bet, Odds API credits remaining; flag PENDING legs.
13. Email: load mcp__Gmail__create_draft via ToolSearch (if needed), draft to icecold67@live.com subject 'MLB Parlay — <today YYYY-MM-DD> Build A', body = the 3 tiers (legs+prices+edges/floor%) + bankroll bet + Odds API credits remaining + any PENDING flags, under 250 words."
  ;;

16|15)
  LABEL="16:00 ET — CLV capture + lineup lock + build update + user-angle execution"
  PROMPT="Run the 16:00 ET MLB parlay update per CLAUDE.md (2nd of 3 runs: 11:00 / 16:00 / 18:00 ET). This is the lineup-lock + CLV + user-angle run; it UPDATES the 11:00 Build A. Note: the early (~13:35 ET) games are already IN PROGRESS at 16:00 — mark them live-only (their Angle A live-ML is happening now). The session_start.sh digest is already in your context (injected by hook). Steps:
1. CLV is AUTO-APPLIED by session_start.sh (clv_capture.py --apply) when the ET hour is 15-19, so today's open ML legs should already have a CLV verdict written. VERIFY the CLV column filled; if any ML row is still blank, run 'python3 tools/clv_capture.py --apply' and confirm. Then re-run tools/calib.py to reconcile. Props/RL stay manual (h2h-only feed).
2. Run tools/mlb_api.sh lineups today — for any leg still flagged PENDING LINEUP, check if lineups are now posted and upgrade or flag accordingly.
3. Run tools/mlb_api.sh ump today and tools/mlb_api.sh weather today — update any K-Over/Under or total legs affected by ump or weather changes.
4. Run tools/odds_api.sh best h2h today — check for material line moves on active legs.
4b. USER-ANGLE EXECUTION (results_log.md -> 'User-angle tracking' — directional-only, N<20, do NOT size off them):
   - Angle B (opposing-SP hits-allowed Over): for each WATCH candidate run tools/odds_api.sh events today for the eventId, then tools/odds_api.sh props <eventId> pitcher_hits_allowed (fall back to a manual book pull if the market is unsupported on tier). Devig with tools/devig.sh. Also pull props <eventId> pitcher_outs to gauge the quick-hook / start-length left tail. Log the real line + devigged edge into the Angle B table; flag hook risk.
   - Angle A (live-ML re-entry): for each WATCH candidate confirm the pregame ref ML (tools/odds_api.sh best h2h) and record the in-game TRIGGER (strong team trails early -> live price overshoots). Live-ML is placed in-game ONLY, so note the trigger + ref price; do not 'lock' it pre-game.
4c. FULL PROP VALUE SWEEP (the 16:00 run owns this — lineups are locked; quota-gate: only if the digest shows ODDS_MODE=rich). For each pre-game (not yet started) game with a confirmed lineup: tools/odds_api.sh events today for the eventId, then tools/odds_api.sh props <eventId> core (HR/TB/HRR/RBI + K/hits-allowed/ER, ~7cr) — or 'all' (~14cr) on games already showing a signal. Devig EACH two-sided prop with tools/devig.sh, apply the min-edge gate (+2pp standalone / +3-4pp anchor), and run the prop-specific value reads in CLAUDE.md 'Full prop universe' (HR=park/wind/SP-HR9, TB/HRR=slot+matchup, RBI/runs=team-total correlated, SB=speed-vs-pop-time). Surface clearing props into the scan + log to results_log.md. Budget: prefer 'core' slate-wide or 'all' on ~3-5 signal games; do NOT sweep all-markets×all-games.
4d. NRFI/YRFI re-check (nrfi_tracker.md — MANDATORY every run): with lineups now locked, re-verify today's NRFI/YRFI leans (a scratched/rested leadoff bat flips a read) and adjust each TrueP; ALSO settle any of today's reads whose early games are already final (1st-inning line score via mlb_api.sh raw schedule&hydrate=linescore) and update the record. For any read worth betting, pull the real 1st-inning total (tools/odds_api.sh props <eventId> totals_1st_1_innings, or a book) + devig — promote only if it clears +2pp. Keep the tracker rows current so the dashboard refreshes.
5. If any leg or price changed materially since the 11:00 build, APPEND a new '## Run 16:00 ET — Build B' section to today's parlays/YYYY-MM-DD.md (do NOT overwrite Build A — mark old legs SUPERSEDED if replaced).
6. Update results_log.md with new or revised legs per the SUPERSEDE protocol.
7. Confirm or update the bankroll bet if lineup was PENDING at 11:00.
8. ODDS API CREDITS: run tools/odds_api.sh quota (FREE — 0 credits) and add 'Odds API credits remaining: <N> (used <M> this month)' to this run's section in today's parlay file BEFORE committing.
8b. DASHBOARD: run 'python3 tools/generate_dashboard.py' to refresh docs/index.html from the updated ledgers, and stage it in the same commit (GitHub Pages auto-deploys on merge).
9. Commit → push → open PR → squash-merge → reset per CLAUDE.md git workflow.
10. Push notification: load PushNotification via ToolSearch (if needed), send title 'MLB Parlay Build B update — <today>': CLV fills (count +/−), lineup upgrades, whether the build changed, Odds API credits remaining.
11. Email: load mcp__Gmail__create_draft via ToolSearch (if needed), draft to icecold67@live.com subject 'MLB Parlay — <today YYYY-MM-DD> Build B update', body = CLV fills per open leg, PENDING→CONFIRMED upgrades, superseded legs, current active build, Odds API credits remaining, under 200 words."
  ;;

18)
  LABEL="18:00 ET — final CLV + late lineups + line check + live-ML settle"
  PROMPT="Run the 18:00 ET final MLB parlay check per CLAUDE.md (3rd of 3 runs: 11:00 / 16:00 / 18:00 ET). This is the late/west-coast lock + final CLV + live-ML trigger settle. The session_start.sh digest is already in your context (injected by hook). Steps:
1. CLV auto-applied by session_start.sh (clv_capture.py --apply, ET hour 15-19). VERIFY today's open ML legs have a CLV verdict; run 'python3 tools/clv_capture.py --apply' for any still-blank late/west-coast legs now that their close is set. Re-run tools/calib.py to reconcile.
2. Run tools/mlb_api.sh lineups today — confirm late/west-coast game lineups; upgrade any remaining PENDING legs to CONFIRMED or flag them.
3. Run tools/odds_api.sh best h2h today — check for any late sharp line moves.
3b. USER-ANGLE EXECUTION (results_log.md -> 'User-angle tracking' — directional-only, N<20): finish any Angle B (opposing-SP hits-allowed Over) line pulls for late/west-coast games (props <eventId> pitcher_hits_allowed + pitcher_outs, devig); for live games already underway, settle any Angle A live-ML triggers that fired and record the live price taken vs the pregame ref (the 'live CLV'). Update both Angle tables.
3c. NRFI/YRFI settle (nrfi_tracker.md — MANDATORY every run): settle any of today's NRFI/YRFI reads whose games are now FINAL — pull the 1st-inning line score (mlb_api.sh raw \"schedule?sportId=1&date=<today>&hydrate=linescore,team\", innings[0] away+home runs) and mark each row W/L, update the running record; finalize any late/west-coast reads. This guarantees the tracker (and the dashboard NRFI list) is current at the end of every day.
4. If anything materially changed since the last build, APPEND '## Run 18:00 ET — Build C' to today's parlay file (mark prior build SUPERSEDED if replaced).
5. Flag any legs the user should manually re-check at first pitch.
6. ODDS API CREDITS: run tools/odds_api.sh quota (FREE — 0 credits) and add 'Odds API credits remaining: <N> (used <M> this month)' to this run's section in today's parlay file BEFORE committing.
6b. DASHBOARD: run 'python3 tools/generate_dashboard.py' to refresh docs/index.html from the updated ledgers, and stage it in the same commit (GitHub Pages auto-deploys on merge).
7. Commit → push → open PR → squash-merge → reset per CLAUDE.md git workflow.
8. Push notification: load PushNotification via ToolSearch (if needed), send title 'MLB Parlay Final check — <today>': final build legs confirmed, late lineup updates, first-pitch re-check flags, Odds API credits remaining.
9. Email: load mcp__Gmail__create_draft via ToolSearch (if needed), draft to icecold67@live.com subject 'MLB Parlay — <today YYYY-MM-DD> Final check', body = late lineup confirmations, remaining CLV fills, final active build legs+prices, first-pitch re-check flags, Odds API credits remaining, under 200 words."
  ;;

*)
  echo "ERROR: Unknown build type '$BUILD'. Use 11, 16, or 18 (aliases 09/15 accepted)." >&2
  exit 1
  ;;
esac

# ── Prompt-only mode (single source of truth for the hook + GitHub Actions) ───
# Pass --prompt-only to print JUST the prompt and exit (no header, no claude call).
# The session-start hook consumes this so the build prompts live in ONE place.
if [[ "$PROMPT_ONLY" == "1" ]]; then
  echo "$PROMPT"
  exit 0
fi

echo "[cron_build.sh] $(TZ=America/New_York date '+%Y-%m-%d %H:%M %Z') — $LABEL"

# ── Invoke Claude non-interactively ──────────────────────────────────────────
# NOTE: `claude -p` only works when called OUTSIDE a Claude Code session
# (from your cron/machine/GitHub Action). Calling it from inside an active
# session will fail — that's expected, not a bug.
if command -v claude >/dev/null 2>&1; then
  echo "[cron_build.sh] Invoking: claude -p ..."
  exec claude -p "$PROMPT"
else
  echo ""
  echo "ERROR: 'claude' CLI not found on PATH." >&2
  echo "  Option A — install Claude Code CLI: https://claude.ai/code" >&2
  echo "  Option B — GitHub Actions: use --prompt-only to get the prompt string:" >&2
  echo "    bash tools/cron_build.sh $BUILD --prompt-only" >&2
  echo ""
  echo "═══════════════════════════════════════════════════"
  echo "PROMPT FOR: $LABEL"
  echo "═══════════════════════════════════════════════════"
  echo "$PROMPT"
  echo "═══════════════════════════════════════════════════"
  exit 2
fi
