#!/bin/bash
#
# .claude/hooks/session-start.sh — UserPromptSubmit hook
#
# Fires on the FIRST message of each Claude Code session (registered in
# .claude/settings.json). Runs tools/session_start.sh once and injects its
# full digest into Claude's context so the routine has live data without
# being explicitly told to run it.
#
# Sentinel file prevents re-running on every message in the same session.
# Output goes to stdout → shown to Claude as pre-prompt context.
#
set -uo pipefail

SESSION_SENTINEL="/tmp/mlb_session_init_${CLAUDE_SESSION_ID:-$$}"

# Already ran this session — exit silently
if [[ -f "$SESSION_SENTINEL" ]]; then
  exit 0
fi
touch "$SESSION_SENTINEL"

# Move to project root (CLAUDE_PROJECT_DIR is set by the harness)
cd "${CLAUDE_PROJECT_DIR:-/home/user/mlb_parlay_claude}" || exit 0

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  AUTO SESSION-START — tools/session_start.sh injected by hook   ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
bash tools/session_start.sh 2>&1 || true
echo ""
echo "══ Hook complete. Claude should now proceed with the routine. ══"
echo ""
