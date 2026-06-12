#!/usr/bin/env bash
#
# selftest.sh — fast invariant suite for the parlay tooling.
#
# WHY THIS EXISTS
#   Every silent bug we've hit (CLV captured nothing for weeks; teamform LAD analyzed the
#   Phillies; calib counted would-L as a W) was a tool quietly doing something other than
#   what doctrine claimed — and nothing caught it because nothing CHECKED. This asserts the
#   exact invariants those bugs violated, so a regression screams on the next run instead of
#   corrupting data for weeks. (Added 6/7/26 after the full-tooling audit.)
#
# CONTRACT
#   • FAST (~a few seconds) and QUOTA-FREE: offline logic tests + free StatsAPI checks only.
#     It NEVER calls the paid Odds API (no `odds_api.sh` live calls / no credit spend).
#   • Exit 0 = all green; exit 1 = at least one failure (details printed).
#
# USAGE
#   tools/selftest.sh            # full suite (offline + free StatsAPI resolver checks)
#   tools/selftest.sh --quick    # offline-only (no network) — used by session_start.sh
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

QUICK=0; [[ "${1:-}" == "--quick" ]] && QUICK=1
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); printf "  \033[32m✓\033[0m %s\n" "$1"; }
no()  { FAIL=$((FAIL+1)); printf "  \033[31m✗ %s\033[0m\n" "$1"; [[ -n "${2:-}" ]] && printf "%s\n" "$2" | sed 's/^/        /'; }
eq()        { [[ "$2" == "$3" ]] && ok "$1" || no "$1" "expected: $2"$'\n'"actual:   $3"; }
has()       { [[ "$3" == *"$2"* ]] && ok "$1" || no "$1" "missing substring: $2"; }
hasnt()     { [[ "$3" != *"$2"* ]] && ok "$1" || no "$1" "should NOT contain: $2"; }
# run a heredoc python/await block; pass iff exit 0
runblk()    { if "$@" >/tmp/_selftest_out 2>&1; then ok "$DESC"; else no "$DESC" "$(cat /tmp/_selftest_out)"; fi; }

echo "════════ selftest $([ $QUICK = 1 ] && echo '(--quick, offline)') ════════"

# ── 1. Syntax: every script parses ───────────────────────────────────────────
echo "1. syntax"
for f in tools/*.sh .claude/hooks/session-start.sh; do
  [[ -f "$f" ]] || continue
  if bash -n "$f" 2>/tmp/_selftest_out; then ok "bash -n $f"; else no "bash -n $f" "$(cat /tmp/_selftest_out)"; fi
done
for f in tools/*.py; do
  if python3 -c "import ast,sys; ast.parse(open('$f').read())" 2>/tmp/_selftest_out; then ok "py-parse $f"; else no "py-parse $f" "$(cat /tmp/_selftest_out)"; fi
done

# ── 2. calib.py parse_result — the would-L / SUPERSEDED / TBD bug ─────────────
echo "2. calib.parse_result (record integrity)"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u
s=u.spec_from_file_location("c","tools/calib.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
cases=[("**W** (won 8-6)","W"),("**L** (lost 5-3)","L"),("**would-L** (SF 12-9)","L"),
       ("**would-W** (x)","W"),("**W (fade)** (AZ 1-14)","W"),("**Push**","Push"),
       ("**SUPERSEDED → Build B**",None),("TBD — Build A bankroll roll",None),
       ("**PLAYED → settled above**",None)]
bad=[(t,e,m.parse_result(t)) for t,e in cases if m.parse_result(t)!=e]
assert not bad, f"mismatches: {bad}"
PY
then ok "parse_result: W/L/would-L/SUPERSEDED/TBD all correct"; else no "parse_result" "$(cat /tmp/_selftest_out)"; fi

# ── 3. calib.py output reconciles with the ledger prose ──────────────────────
# Expected record/ROI are DERIVED from results_log.md prose (not hardcoded) so the
# test self-maintains as tickets settle; the only fixed guard is the +213 corruption check.
echo "3. calib reconciliation (no \$-USER / TBD leakage into unit ROI)"
COUT="$(python3 tools/calib.py 2>/dev/null)"
PROSE="$(grep -m1 'Record: .* W – .* L (recommended builds)' results_log.md)"
EXP_REC="record: $(echo "$PROSE" | grep -oE '[0-9]+ W – [0-9]+ L' | grep -oE '[0-9]+' | paste -sd-)"
EXP_ROI="$(echo "$PROSE" | grep -oE 'ROI [+-][0-9.]+%')"
has  "calib ROI is a unit % matching prose (not the inflated dollar +213%)" "$EXP_ROI" "$COUT"
has  "calib parlay record matches prose ($EXP_REC)" "$EXP_REC" "$COUT"
hasnt "calib ROI not the corrupted +213.6%" "+213" "$COUT"

# ── 4. settle.py find_team — abbreviation fallback (agrees w/ clv_capture) ────
echo "4. settle.find_team"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u
s=u.spec_from_file_location("s","tools/settle.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
assert m.find_team("LAD ML (vs LAA)")[0]=="LAD", m.find_team("LAD ML (vs LAA)")
assert m.find_team("Dodgers ML")[0]=="LAD"
assert m.find_team("TB ML (@ MIA)")[0]=="TB"
PY
then ok "find_team: LAD/Dodgers/TB resolve (abbr + nick)"; else no "find_team" "$(cat /tmp/_selftest_out)"; fi

# ── 5. clv_capture.py verdict guard + cell-surgical write ─────────────────────
echo "5. clv_capture (--apply safety)"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u
s=u.spec_from_file_location("v","tools/clv_capture.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
garbage="Close best LAD: -10000  → no-vig 97%\n  proxy CLV: + (line moved TO your side ✓)"
assert m.verdict_from_clv_output(garbage,"61.7%") is None, "garbage -10000 line should be rejected"
legit="Close best LAD: -195  → no-vig 64%\n  proxy CLV: + (line moved TO your side ✓)"
assert m.verdict_from_clv_output(legit,"61.7%")=="+ 64%cl"
row="| 6/6 | Dodgers ML | ML-fav | -182 | 64.7% | 61.7% | +3.0 | TBD | N | — | S |"
new=m.apply_clv_to_cell(row,"+ 64%cl")
op=row.split("|"); npp=new.split("|")
changed=[i for i,(a,b) in enumerate(zip(op,npp)) if a!=b]
assert changed==[10], f"apply must touch ONLY the CLV cell (idx 10); touched {changed}"
PY
then ok "verdict rejects garbage line; apply edits ONLY the CLV cell"; else no "clv_capture" "$(cat /tmp/_selftest_out)"; fi

# ── 5b. nrfi_settle.py — verdict mapping + matchup parse ──────────────────────
echo "5b. nrfi_settle (NRFI/YRFI W/L logic)"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u
s=u.spec_from_file_location("n","tools/nrfi_settle.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
# NRFI wins iff the 1st inning is scoreless; YRFI is its mirror.
assert m.verdict_for("NRFI",(0,0))[0]=="W", "NRFI vs 0-0 must be W"
assert m.verdict_for("NRFI",(1,0))[0]=="L", "NRFI vs 1-0 must be L"
assert m.verdict_for("YRFI",(0,0))[0]=="L", "YRFI vs 0-0 must be L"
assert m.verdict_for("YRFI",(0,2))[0]=="W", "YRFI vs 0-2 must be W"
assert m.matchup_teams("ATL @ CWS (Sale/Martin)")==("ATL","CWS"), "matchup parse"
assert m.matchup_teams("LAD @ PIT (Wrobleski/Keller)")==("LAD","PIT")
# alias normalization (StatsAPI CHW -> tracker CWS)
assert m.norm("CHW")=="CWS" and m.norm("ARI")=="AZ"
PY
then ok "verdict_for NRFI/YRFI ↔ 1st-inning total; matchup+alias parse"; else no "nrfi_settle" "$(cat /tmp/_selftest_out)"; fi

# ── 6. parlay.py — fractional footgun rejected, normal math intact ───────────
echo "6. parlay.py"
if ./tools/parlay.py --leg 0.6:-150 --leg 0.55:+120 >/tmp/_selftest_out 2>&1; then
  no "parlay rejects fractional TrueP (0.6)" "exited 0 — guard did not fire"
else
  has "parlay rejects fractional TrueP (0.6)" "fraction" "$(cat /tmp/_selftest_out)"
fi
has "parlay normal math (60:-150 + 55:+120 → 33.0%)" "33.0%" "$(./tools/parlay.py --leg 60:-150 --leg 55:+120 2>&1)"

# ── 7. devig.sh — no-vig math ─────────────────────────────────────────────────
echo "7. devig.sh"
DV="$(./tools/devig.sh -150 +130 2>&1)"
has "devig -150/+130 → ~58% fav side"  "58" "$DV"
has "devig -150/+130 → ~42% dog side"  "42" "$DV"

# ── 8. truep.py — registry loads ─────────────────────────────────────────────
echo "8. truep.py"
has "truep --list shows the ace_edge adjustment" "ace_edge" "$(./tools/truep.py --list 2>&1)"

# ── 9. cron_build.sh — prompt-only (single source) ───────────────────────────
echo "9. cron_build.sh --prompt-only"
for b in 11 16 18; do
  out="$(bash tools/cron_build.sh $b --prompt-only 2>&1)"
  has "build $b emits a prompt" "ET" "$out"
  hasnt "build $b prompt has no '[cron_build.sh]' header line" "[cron_build.sh]" "$out"
done
# bare --prompt-only (no hour) must auto-detect, NOT crash
if bare="$(bash tools/cron_build.sh --prompt-only 2>&1)" && [[ -n "$bare" ]]; then
  ok "bare --prompt-only auto-detects (no crash)"
else no "bare --prompt-only auto-detects" "$bare"; fi
# unknown build errors
if bash tools/cron_build.sh 99 --prompt-only >/dev/null 2>&1; then
  no "unknown build type errors out" "exit 0 for build 99"
else ok "unknown build type errors out"; fi

# ── 10. hook delegation + no stale cadence ───────────────────────────────────
echo "10. session-start hook (single source, no drift)"
HOOK="$(cat .claude/hooks/session-start.sh)"
has   "hook delegates to cron_build --prompt-only" "cron_build.sh" "$HOOK"
has   "hook passes --prompt-only" "--prompt-only" "$HOOK"
hasnt "hook carries no stale 09:00 label" "09:00 ET" "$HOOK"
hasnt "hook carries no stale 15:30 label" "15:30 ET" "$HOOK"

# ── 11. session_start CLV window starts at 16 (not 15 — premature-close guard) ─
echo "11. CLV auto-apply window"
SS="$(cat tools/session_start.sh)"
has   "session_start CLV uses clv_capture.py --apply" "clv_capture.py\" --apply" "$SS"
has   "CLV window starts at ET hour 16" "ET_HOUR >= 16" "$SS"

# ── 12. git doctrine forbids the amend (merge-conflict cause) ─────────────────
echo "12. git doctrine"
CM="$(cat CLAUDE.md)"
has   "CLAUDE.md prohibits amend --reset-author of the reset tip" "Do NOT" "$CM"
has   "CLAUDE.md run-timing is 11/16/18 ET" "11:00, 16:00, 18:00 ET" "$CM"

# ── 13. odds_api.sh filter_date — late-west-game slate bucketing (offline) ────
echo "13. odds_api filter_date (offline, no quota)"
if eval "$(awk '/^filter_date\(\) \{/{p=1} p{print} p&&/^\}/{exit}' tools/odds_api.sh)" 2>/dev/null; then
  ET_OFFSET=-4
  late='[{"commence_time":"2026-06-08T05:05:00Z","home_team":"H","away_team":"A"}]'   # 1:05am ET → prior slate
  eve='[{"commence_time":"2026-06-07T23:10:00Z","home_team":"H","away_team":"A"}]'    # 7:10pm ET same day
  nxt='[{"commence_time":"2026-06-08T17:35:00Z","home_team":"H","away_team":"A"}]'    # 1:35pm ET next day
  eq "late west game (1am ET) buckets to prior slate 6/7" "1" "$(echo "$late" | filter_date 2026-06-07 | jq 'length')"
  eq "evening game (7pm ET) on its own slate 6/7"          "1" "$(echo "$eve"  | filter_date 2026-06-07 | jq 'length')"
  eq "next-day afternoon game excluded from 6/7"            "0" "$(echo "$nxt"  | filter_date 2026-06-07 | jq 'length')"
else no "extract filter_date from odds_api.sh"; fi

# ── 13b. odds_api quota command + cron reports credits each run (offline) ────
echo "13b. odds credits reporting"
OA="$(cat tools/odds_api.sh)"
has "odds_api.sh has a 'quota' subcommand" "quota)   cmd_quota" "$OA"
has "odds_api.sh quota uses the FREE /sports endpoint" "FREE: the /sports" "$OA"
CRED_N="$(grep -c 'Odds API credits remaining' tools/cron_build.sh)"
[[ "${CRED_N:-0}" -ge 3 ]] && ok "all 3 builds report Odds API credits ($CRED_N mentions)" \
  || no "all 3 builds report Odds API credits" "only $CRED_N mentions (expect >=3)"

# ── 13c. full prop universe expansion (offline) ──────────────────────────────
echo "13c. prop universe (all/core expansion)"
CB="$(cat tools/cron_build.sh)"
has "odds_api defines PROPS_ALL universe" "PROPS_ALL=" "$OA"
has "odds_api defines PROPS_CORE subset"  "PROPS_CORE=" "$OA"
has "cmd_props expands 'all' keyword"     "all)  markets=\"\$PROPS_ALL\"" "$OA"
has "cmd_props expands 'core' keyword"    "core) markets=\"\$PROPS_CORE\"" "$OA"
has "PROPS_ALL includes home runs"        "batter_home_runs" "$OA"
has "PROPS_ALL includes total bases"      "batter_total_bases" "$OA"
has "16:00 build runs the prop value sweep" "FULL PROP VALUE SWEEP" "$CB"

# ── 13d. dashboard parser invariants + calib.py reconciliation (offline) ─────
# The dashboard parses hand-edited markdown with regex; a table reformat can
# silently drop every row. Its --selftest asserts ≥N rows parse from each source
# AND that its units P/L + calibration N reconcile with calib.py (source of truth).
echo "13d. dashboard parser invariants"
DESC="generate_dashboard --selftest (parse counts + calib reconcile + empty-safe)"
runblk python3 tools/generate_dashboard.py --selftest

# ── 14. ONLINE (free StatsAPI only): resolver collision regression ───────────
if [[ $QUICK -eq 0 ]]; then
  echo "14. mlb_api resolver (live StatsAPI — free, no odds quota)"
  if ./tools/mlb_api.sh check >/dev/null 2>&1; then
    has "teamform LAD → Dodgers (team 119, NOT Phillies 143)" "team 119" "$(./tools/mlb_api.sh teamform LAD 1 2>/dev/null | head -1)"
    has "teamform PHI → Phillies (team 143)"                  "team 143" "$(./tools/mlb_api.sh teamform PHI 1 2>/dev/null | head -1)"
    has "teamform NYY → Yankees (team 147)"                   "team 147" "$(./tools/mlb_api.sh teamform NYY 1 2>/dev/null | head -1)"
  else
    echo "  ⊘ SKIP (StatsAPI blocked this session)"
  fi
else
  echo "14. (skipped — --quick)"
fi

# ── summary ──────────────────────────────────────────────────────────────────
echo "──────────────────────────────────────────"
if (( FAIL == 0 )); then
  printf "  \033[32mALL %d CHECKS PASSED\033[0m\n" "$PASS"; exit 0
else
  printf "  \033[31m%d FAILED\033[0m / %d passed — investigate before trusting the tooling.\n" "$FAIL" "$PASS"; exit 1
fi
