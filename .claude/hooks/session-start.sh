#!/bin/bash
set -euo pipefail

# Confirms the MLB parlay routine is loaded at session start.
# Extend this script later if you want to pre-fetch data, install tools, etc.

if [ -f "$CLAUDE_PROJECT_DIR/CLAUDE.md" ]; then
  echo "MLB parlay routine loaded from CLAUDE.md"
else
  echo "WARNING: CLAUDE.md not found at $CLAUDE_PROJECT_DIR/CLAUDE.md"
fi
