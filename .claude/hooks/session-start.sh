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
# SINGLE SOURCE OF TRUTH: the actual build prompts live in tools/cron_build.sh. This hook
# only picks the build for the current ET hour and delegates to `cron_build.sh <b> --prompt-only`,
# so the hook and the cron entry point can never drift apart again. (Bug 6/7/26: this hook
# carried its OWN copy of the prompts and was left on the stale 09/15/18 + non---apply CLV
# cadence when cron_build.sh was retimed to 11/16/18.)
HOUR=$(TZ="America/New_York" date +%H 2>/dev/null || date +%H)
ET_TIME=$(TZ="America/New_York" date '+%H:%M %Z' 2>/dev/null || date '+%H:%M')

# Same window boundaries as cron_build.sh's auto-detect (11 / 16 / 18 ET).
if   (( 10#$HOUR >= 6  && 10#$HOUR < 14 )); then BUILD="11"
elif (( 10#$HOUR >= 14 && 10#$HOUR < 17 )); then BUILD="16"
else BUILD="18"
fi

DIRECTIVE="$(bash tools/cron_build.sh "$BUILD" --prompt-only 2>/dev/null)"

echo "════════════════════════════════════════════════════════"
echo "  BUILD DIRECTIVE — Build $BUILD  (ET now: $ET_TIME)"
echo "════════════════════════════════════════════════════════"
echo ""
echo "CLAUDE: execute the following build automatically per CLAUDE.md."
echo "The session_start.sh digest above is your live context. Begin now:"
echo ""
echo "$DIRECTIVE"
echo ""
