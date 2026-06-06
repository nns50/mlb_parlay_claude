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
# CRONTAB EXAMPLE (3 runs/day at the recommended ET windows)
#   # MLB parlay routine — 09:00, 15:30, 18:30 ET (adjust TZ as needed)
#   0   9  * * * bash /home/user/mlb_parlay_claude/tools/cron_build.sh 09 >> /tmp/mlb_cron.log 2>&1
#   30 15  * * * bash /home/user/mlb_parlay_claude/tools/cron_build.sh 15 >> /tmp/mlb_cron.log 2>&1
#   30 18  * * * bash /home/user/mlb_parlay_claude/tools/cron_build.sh 18 >> /tmp/mlb_cron.log 2>&1
#
# USAGE
#   tools/cron_build.sh           # auto-detect build from ET time
#   tools/cron_build.sh 09        # force the 09:00 morning build
#   tools/cron_build.sh 15        # force the 15:30 CLV + lineup build
#   tools/cron_build.sh 18        # force the 18:30 final check
#
# REQUIREMENTS
#   • `claude` CLI on PATH (Claude Code — https://claude.ai/code).
#   • ODDS_API_KEY set in the environment (for odds_api.sh calls).
#
set -uo pipefail
cd "$(dirname "$0")/.."

# ── Build type: forced arg OR auto-detect from ET hour ───────────────────────
BUILD="${1:-}"
if [[ -z "$BUILD" ]]; then
  HOUR=$(TZ="America/New_York" date +%H 2>/dev/null || date +%H)
  if   (( 10#$HOUR >= 6  && 10#$HOUR < 13 )); then BUILD="09"
  elif (( 10#$HOUR >= 13 && 10#$HOUR < 17 )); then BUILD="15"
  else BUILD="18"
  fi
fi

# ── Prompts — each is a self-contained instruction for Claude ─────────────────
case "$BUILD" in

09|9)
  LABEL="09:00 ET — morning settle + full build"
  PROMPT="Run the 09:00 ET daily MLB parlay routine per CLAUDE.md. The session_start.sh digest is already in your context (injected by hook). Steps:
1. Self-settle all TBD results from yesterday: run tools/settle.py, apply W/L to results_log.md + fades.md + bankroll.md.
2. Run tools/calib.py and apply the fresh calibration bands before building.
3. Run tools/mlb_api.sh slate today for the full game list.
4. Do the mandatory slate-wide value scan (ALL games — non-ML markets first per CLAUDE.md).
5. Fill SP-freshness blocks for every SP in the build.
6. Build all three tiers: Tier 1 best standalone, Tier 2 highest-floor 2-leg, Tier 3 +200 build.
7. Pick the bankroll bet (single safest qualifying fav, independent of parlay, not A-list fade).
8. Append this run to parlays/YYYY-MM-DD.md as '## Run 09:00 ET — Build A'.
9. Log all recommended legs in results_log.md with pre-registered TrueP + ImplP + Edge.
10. Commit → push → open PR → squash-merge → git fetch+reset to main per CLAUDE.md git workflow."
  ;;

15)
  LABEL="15:30 ET — CLV capture + lineup lock + build update"
  PROMPT="Run the 15:30 ET MLB parlay update per CLAUDE.md. The session_start.sh digest is already in your context (injected by hook). Steps:
1. Run tools/clv_capture.py for today — fill the CLV column in results_log.md for all open ML legs.
2. Run tools/mlb_api.sh lineups today — for any leg still flagged PENDING LINEUP, check if lineups are now posted and upgrade or flag accordingly.
3. Run tools/mlb_api.sh ump today and tools/mlb_api.sh weather today — update any K-Over/Under or total legs affected by ump or weather changes.
4. Run tools/odds_api.sh best h2h today — check for material line moves on active legs.
5. If any leg or price changed materially since the 09:00 build, APPEND a new '## Run 15:30 ET — Build B' section to today's parlays/YYYY-MM-DD.md (do NOT overwrite Build A — mark old legs SUPERSEDED if replaced).
6. Update results_log.md with new or revised legs per the SUPERSEDE protocol.
7. Confirm or update the bankroll bet if lineup was PENDING at 09:00.
8. Commit → push → open PR → squash-merge → reset per CLAUDE.md git workflow."
  ;;

18)
  LABEL="18:30 ET — final CLV + late lineups + line check"
  PROMPT="Run the 18:30 ET final MLB parlay check per CLAUDE.md. The session_start.sh digest is already in your context (injected by hook). Steps:
1. Run tools/clv_capture.py for today — update CLV column for any remaining open legs.
2. Run tools/mlb_api.sh lineups today — confirm late/west-coast game lineups; upgrade any remaining PENDING legs to CONFIRMED or flag them.
3. Run tools/odds_api.sh best h2h today — check for any late sharp line moves.
4. If anything materially changed since the last build, APPEND '## Run 18:30 ET — Build C' to today's parlay file (mark prior build SUPERSEDED if replaced).
5. Flag any legs the user should manually re-check at first pitch.
6. Commit → push → open PR → squash-merge → reset per CLAUDE.md git workflow."
  ;;

*)
  echo "ERROR: Unknown build type '$BUILD'. Use 09, 15, or 18." >&2
  exit 1
  ;;
esac

echo "[cron_build.sh] $(TZ=America/New_York date '+%Y-%m-%d %H:%M %Z') — $LABEL"

# ── Prompt-only mode (for GitHub Actions / external triggers) ─────────────────
# Pass --prompt-only to print the prompt and exit without invoking Claude.
# Useful for wiring into a GitHub Action's `prompt:` field or any other runner.
if [[ "${2:-}" == "--prompt-only" || "${1:-}" == "--prompt-only" ]]; then
  echo "$PROMPT"
  exit 0
fi

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
