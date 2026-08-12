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
has   "calib Brier-skill section scores TrueP vs market" "Brier(TrueP)" "$COUT"

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

# ── 4b. settle.py K-prop parse + verdict (the 6/16 Cease mis-settle class) ────
echo "4b. settle K-prop (gamelog-based prop settle)"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u
s=u.spec_from_file_location("s","tools/settle.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
# both notations parse; team legs don't
assert m.parse_kprop("Gilbert Over 6.5 K (SEA @ TEX)")==("Gilbert","Over",6.5)
assert m.parse_kprop("Sánchez O7.5K (vs SD)")==("Sánchez","Over",7.5)
assert m.parse_kprop("Peterson U4.5K +102")==("Peterson","Under",4.5)
assert m.parse_kprop("PHI ML (vs NYY)") is None
assert m.parse_kprop("BOS @ COL Over 12.0 +107") is None, "team total must NOT parse as a K-prop"
# verdicts (.5 lines cannot push)
assert m.kprop_verdict("Over",6.5,7)=="W" and m.kprop_verdict("Over",6.5,4)=="L"
assert m.kprop_verdict("Under",4.5,1)=="W" and m.kprop_verdict("Under",4.5,5)=="L"
# ORDER guard: main() must try propose_kprop BEFORE the PROP_HINT/team fallthrough —
# compact "O7.5K" slips past PROP_HINT's \b and used to settle off the TEAM result.
src=open("tools/settle.py").read(); body=src[src.index("def main"):]
assert body.index("propose_kprop") < body.index("PROP_HINT.search"), "K-prop check must run first"
PY
then ok "parse_kprop both notations; verdicts; K-prop checked before team fallthrough"; else no "settle K-prop" "$(cat /tmp/_selftest_out)"; fi

# ── 4c. settle full-prop universe: hitter props / game totals / RL-by-margin ──
echo "4c. settle hitter props + totals + run-line margin (7/30 expansion)"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u
s=u.spec_from_file_location("s","tools/settle.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
# hitter/pitcher counting props parse (full + compact notation; stat-token priority)
assert m.parse_hprop("Ohtani Over 1.5 TB (LAD vs SEA)")==("Ohtani","Over",1.5,"tb")
assert m.parse_hprop("Judge O0.5 HR (NYY @ CWS)")==("Judge","Over",0.5,"hr")
assert m.parse_hprop("Kochanowicz Over 5.5 hits allowed (vs LAD)")==("Kochanowicz","Over",5.5,"hitsallowed")
assert m.parse_hprop("Ohtani U2.5 H+R+RBI")==("Ohtani","Under",2.5,"hrr")
assert m.parse_hprop("Kwan Over 0.5 hits (CLE @ CIN)")==("Kwan","Over",0.5,"hits")
assert m.parse_hprop("PHI @ MIA Over 8.5") is None          # game total ≠ player prop
assert m.parse_hprop("Gilbert Over 6.5 K") is None          # K-props stay with parse_kprop
# boxscore stat math (TB = H + 2B + 2·3B + 3·HR) + hits-allowed from pitching
assert m.stat_from_box({"hits":2,"doubles":1,"triples":0,"homeRuns":1},None,"tb")==6
assert m.stat_from_box({"hits":2,"runs":1,"rbi":3},None,"hrr")==6
assert m.stat_from_box(None,{"hits":7},"hitsallowed")==7
# verdicts: integer lines can push; run line settles by MARGIN not W/L
assert m.prop_verdict("Over",2.0,2)=="Push" and m.prop_verdict("Over",1.5,2)=="W"
assert m.spread_verdict(10,9,-1.5)=="L"    # won by 1 — the -1.5 fav LOSES the leg
assert m.spread_verdict(10,8,-1.5)=="W" and m.spread_verdict(3,4,1.5)=="W"
# game totals AND team totals settle off the final (finals are LISTS per team — DH-safe)
games={"PHI":[(6,8,"MIA","Final")],"MIA":[(8,6,"PHI","Final")]}
assert m.propose_total("PHI @ MIA Over 8.5",games)[1]=="W"    # game total 14
assert m.propose_total("PHI @ MIA Under 8.5",games)[1]=="L"
assert m.propose_total("PHI team total Over 6.5",games)[1]=="L"   # PHI scored 6 (own side)
assert m.propose_total("PHI team total Under 6.5",games)[1]=="W"
# doubleheader guard: one final resolves; two need an explicit G1/G2 hint (never guess)
e1,e2=(2,3,"NYM","Final"),(1,0,"NYM","Final")
assert m.resolve_game("ATL ML",[e1])==e1
assert m.resolve_game("ATL ML",[e1,e2]) is None
assert m.resolve_game("ATL ML G1",[e1,e2])==e1 and m.resolve_game("ATL ML Game 2",[e1,e2])==e2
# 8/1 stat expansion: ER / SB / walks / doubles / singles / pitcher outs
assert m.parse_hprop("Skubal Under 2.5 earned runs")==("Skubal","Under",2.5,"er")
assert m.parse_hprop("Ohtani O0.5 SB")==("Ohtani","Over",0.5,"sb")
assert m.parse_hprop("Soto Over 0.5 walks")==("Soto","Over",0.5,"bb")
assert m.parse_hprop("Sánchez Under 18.5 outs")==("Sánchez","Under",18.5,"outs")
assert m.parse_hprop("Betts Over 0.5 doubles")==("Betts","Over",0.5,"doubles")
assert m.stat_from_box({"hits":3,"doubles":1,"triples":0,"homeRuns":1},None,"singles")==1
assert m.stat_from_box(None,{"outs":18},"outs")==18
assert m.stat_from_box(None,{"earnedRuns":2},"er")==2
# find_team binds the FIRST team in the text (the bet side), not dict order
assert m.find_team("BAL -1.5 RL (@ DET)")[0]=="BAL"
assert m.find_team("TB ML (@ MIA)")[0]=="TB"
# ── adversarial-audit (8/1) regression pins ──
assert m.kprop_verdict("Over",7.0,7)=="Push" and m.kprop_verdict("Under",7.0,7)=="Push"
assert m.parse_kprop("**Rasmussen O5.5K -151 (KC @ TB)**")==("Rasmussen","Over",5.5)  # bold strip
assert m.parse_hprop("STL team total Over 4.5 runs") is None   # team totals are TOTALS
assert m.parse_hprop("NYY TT Over 4.5 runs") is None
assert m.resolve_game("TB ML G2",[e1]) is None    # hinted leg + lone final = ambiguous
assert m.find_team("ARI ML (Nelson, vs LAA)")[0]=="AZ"          # ARI alias (6/15 mis-settle root)
assert m.find_team("Grayson Rodriguez (@ NYY)")[0]=="NYY"       # no 'rays'-in-'Grayson' bind
# 2B/1B literals parse (matrix promised them; they only had word forms before 8/1 audit)
assert m.parse_hprop("Betts Over 0.5 2B")==("Betts","Over",0.5,"doubles")
assert m.parse_hprop("Arraez O1.5 1B")==("Arraez","Over",1.5,"singles")
# parse_finals fixture pins the mlb_api finals line format (settle's backbone) + DH lists
fx="ATL 2 - NYM 3   [Final]\nATL 1 - NYM 0   [Final]\nSEA 6 - TEX 4   [Final]\njunk line"
g=m.parse_finals(fx)
assert g["SEA"]==[(6,4,"TEX","Final")] and g["TEX"]==[(4,6,"SEA","Final")]
assert len(g["ATL"])==2 and g["ATL"][0]==(2,3,"NYM","Final") and g["ATL"][1]==(1,0,"NYM","Final")
PY
# RL margin branch must NOT be gated on an "RL" token — "BAL -1.5 (@ DET)" (no token)
# used to fall through and settle as ML by W/L (audit 8/1)
hasnt "settle margin branch not gated on an RL token" 'sp and re.search(r"\b(rl' "$(cat tools/settle.py)"
then ok "parse_hprop priorities; TB/HRR math; push; RL margin; totals; side binding"; else no "settle props v2" "$(cat /tmp/_selftest_out)"; fi
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u
s=u.spec_from_file_location("v","tools/clv_capture.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
assert m.find_team("BAL ML (@ DET)")[0]=="BAL", "clv side-binding must prefer first mention"
assert m.find_team("Rays ML (vs CLE)")==("TB","rays")
# adversarial-audit (8/1) pins: ARI alias; canonical feed nickname for aliases
# (d-backs is not a substring of 'Arizona Diamondbacks'); no nickname-inside-name binds
assert m.find_team("ARI ML (vs LAA)")[0]=="AZ"
assert m.find_team("D-backs ML (Kelly, vs WSH)")==("AZ","diamondbacks")
assert m.find_team("Grayson Rodriguez (@ NYY)")[0]=="NYY"
k=u.spec_from_file_location("k","tools/kprice.py"); km=u.module_from_spec(k); k.loader.exec_module(km)
ev={"bookmakers":[{"title":"DK","markets":[{"key":"batter_total_bases","outcomes":[
  {"description":"Shohei Ohtani","name":"Over","point":1.5,"price":-125},
  {"description":"Shohei Ohtani","name":"Under","point":1.5,"price":-105}]}]}]}
t=km.best_by_point(ev,"ohtani",market_prefix="batter_total_bases")
assert t[1.5]["Over"]==(-125,"DK"), t
assert km.best_by_point(ev,"ohtani") == {}   # default K prefix ignores batter markets
# same-surname chimera refusal: two Contrerases must yield NO table, not merged prices
ev2={"bookmakers":[{"title":"DK","markets":[{"key":"batter_hits","outcomes":[
  {"description":"Willson Contreras","name":"Over","point":0.5,"price":-200},
  {"description":"William Contreras","name":"Under","point":0.5,"price":250}]}]}]}
assert km.best_by_point(ev2,"contreras",market_prefix="batter_hits")=={}
PY
then ok "clv side-binding + aliases; kprice market_prefix + same-surname refusal"; else no "clv/kprice v2" "$(cat /tmp/_selftest_out)"; fi
# date matching must be EXACT (startswith let 6/22 rows settle off a 6/2 run) and
# parlay ticket rows must never settle off one leg
hasnt "settle date match is exact (no prefix collision)" 'c[0].startswith(target)' "$(cat tools/settle.py)"
hasnt "clv date match is exact (no prefix collision)" 'c[0].startswith(target_md)' "$(cat tools/clv_capture.py)"
has   "settle guards parlay ticket rows (settle from legs)" "parlay ticket — settle from its component legs" "$(cat tools/settle.py)"

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

# ── 5a. clv_capture v2 — cached-slate markets (h2h/totals/RL) + edge-gone warn ─
echo "5a. clv_capture cached markets (classify / close_novig / edge-gone)"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u
s=u.spec_from_file_location("v","tools/clv_capture.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
# classification routes by type + notation; K-props and parlays never hit the feed
assert m.classify_leg("Rays ML (vs TEX)","ML-fav")[0]=="h2h"
assert m.classify_leg("TEX @ TB Over 8.0","Total-Over")==("totals",("Over",8.0))
assert m.classify_leg("Rays -1.5 RL (vs TEX)","Run line")==("spreads",-1.5)
assert m.classify_leg("Gilbert Over 6.5 K","K-Over")[0]=="manual"
assert m.classify_leg("Sánchez O7.5K","K-Over")[0]=="manual"
assert m.classify_leg("A × B (Tier 2)","Parlay (+corr)")[0]=="skip"
# LEG-TEXT beats a loose Type: a player prop typed just "HR"/"BB" must never
# route to the game-totals branch off its "Over 0.5" (8/1 routing fix)
assert m.classify_leg("Judge Over 0.5 HR (NYY @ CWS)","HR")[0]=="manual"
assert m.classify_leg("Soto Over 0.5 walks (vs PHI)","BB")[0]=="manual"
assert m.classify_leg("LAD -2.5 alt RL (vs SEA)","Run line")==("spreads",-2.5)
# closing no-vig from a synthetic cached game (best-across-books, same-point pairing)
game={"away_team":"Texas Rangers","home_team":"Tampa Bay Rays","bookmakers":[
 {"title":"A","markets":[
   {"key":"totals","outcomes":[{"name":"Over","price":-104,"point":8.0},{"name":"Under","price":-118,"point":8.0}]},
   {"key":"h2h","outcomes":[{"name":"Tampa Bay Rays","price":-139},{"name":"Texas Rangers","price":126}]},
   {"key":"spreads","outcomes":[{"name":"Tampa Bay Rays","price":160,"point":-1.5},{"name":"Texas Rangers","price":-194,"point":1.5}]}]},
 {"title":"B","markets":[
   {"key":"totals","outcomes":[{"name":"Over","price":-101,"point":8.0},{"name":"Under","price":-121,"point":8.0}]}]}]}
got,err=m.close_novig(game,"totals",("Over",8.0),"rays"); assert err is None
assert abs(got[0]-0.4814)<0.002, got   # best O -101 vs best U -118 → no-vig 48.1%
got,err=m.close_novig(game,"totals",("Over",9.5),"rays")
assert got is None and "NUMBER moved" in err, err   # moved total = info, not silence
assert "nearest 8" in err and "no-vig" in err, err  # 8/7: hand-fill gets the nearest close
got,err=m.close_novig(game,"h2h",None,"rays"); assert err is None and abs(got[0]-0.568)<0.005
got,err=m.close_novig(game,"spreads",-1.5,"rays"); assert err is None
# verdict dead-band + the pre-lock edge-gone warning
assert m.verdict_from_close(56.8,"52.0%").startswith("+")
assert m.verdict_from_close(52.3,"52.0%").startswith("=")
assert m.verdict_from_close(48.0,"52.0%").startswith("−")
assert "EDGE GONE" in m.edge_warning(56.8,"54%")
assert "under the +2pp gate" in m.edge_warning(53.0,"54%")
assert m.edge_warning(48.0,"54%") is None
# in-game "close" guard (8/7): cache warmed AFTER first pitch = live line, NOT a close
assert m.close_is_stale("2026-08-08T00:33:34Z","2026-08-07T22:42:14Z") is True
assert m.close_is_stale("2026-08-07T20:00:00Z","2026-08-07T22:42:14Z") is False
assert m.close_is_stale(None,"2026-08-07T22:42:14Z") is False  # unknown mtime → don't block
assert m.close_is_stale("2026-08-07T20:00:00Z",None) is False
PY
then ok "classify + close_novig (3 markets) + verdict dead-band + edge-gone + stale-cache gate correct"; else no "clv_capture v2" "$(cat /tmp/_selftest_out)"; fi
has "session_start reuses a fresh slate cache (free-tier quota guard)" "Slate cache FRESH" "$(cat tools/session_start.sh)"

# ── 5a3. kprice.py — K-prop line table (pure parse; no credits) ──────────────
echo "5a3. kprice (best-by-point, accent match, no-vig, quota guard)"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u
s=u.spec_from_file_location("k","tools/kprice.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
ev={"bookmakers":[
 {"title":"DK","markets":[{"key":"pitcher_strikeouts","outcomes":[
   {"description":"Logan Gilbert","name":"Over","point":6.5,"price":-110},
   {"description":"Logan Gilbert","name":"Under","point":6.5,"price":-120},
   {"description":"Other Guy","name":"Over","point":4.5,"price":-200}]}]},
 {"title":"FD","markets":[{"key":"pitcher_strikeouts_alternate","outcomes":[
   {"description":"Logan Gilbert","name":"Over","point":6.5,"price":-105},
   {"description":"Logan Gilbert","name":"Over","point":5.5,"price":-210},
   {"description":"Logan Gilbert","name":"Under","point":5.5,"price":170}]}]}]}
t=m.best_by_point(ev,"gilbert")
assert t[6.5]["Over"]==(-105,"FD") and t[6.5]["Under"]==(-120,"DK"), t  # best across books+markets
assert t[5.5]["Over"]==(-210,"FD") and 4.5 not in t                     # other pitcher excluded
nv=m.novig_at_point(t[6.5]); assert abs(nv[0]-0.4843)<0.002, nv         # -105/-120 → O 48.4%
assert m.novig_at_point({"Over":(-210,"FD")}) is None                   # one-sided → no devig
ev2={"bookmakers":[{"title":"B","markets":[{"key":"pitcher_strikeouts","outcomes":[
   {"description":"Cristopher Sánchez","name":"Over","point":7.5,"price":120}]}]}]}
assert 7.5 in m.best_by_point(ev2,"Sanchez")                            # accent-insensitive
assert m.MIN_CREDITS>=1000                                              # free-tier spend guard
PY
then ok "best_by_point across books/markets; accent match; novig; one-sided; spend guard"; else no "kprice" "$(cat /tmp/_selftest_out)"; fi

# ── 5a2. recheck.py — SP-scratch / status-flip diff (offline fixtures) ────────
echo "5a2. recheck (pre-lock SP-scratch detector)"
if ./tools/recheck.py --selftest >/tmp/_selftest_out 2>&1; then
  ok "recheck diff: scratch ⚠ / started ⛔ / TBA-posted ℹ / vanished ⚠ / unchanged silent"
else no "recheck --selftest" "$(cat /tmp/_selftest_out)"; fi

# ── 5a4. pulse.py — recent-window exposure governor (fixtures) ────────────────
echo "5a4. pulse (recent-window exposure governor)"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u, datetime as dt
s=u.spec_from_file_location("p","tools/pulse.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
T=dt.date(2026,8,1)
hdr="## Played legs\n\n| Date | Leg | Type | Price | TrueP | ImplP | Edge | Result | Played | CLV | Bucket |\n|-|-|-|-|-|-|-|-|-|-|-|\n"
def row(d,leg,typ,tp,res,clv="—"):
    return f"| {d} | {leg} | {typ} | -120 | {tp}% | 55% | +2 | **{res}** | Y | {clv} | P |\n"
# COLD dimension: ace-tagged ML-favs 1-6 in the window → COOL or SUSPEND + CLV shade
txt=hdr
for i,(res,clv) in enumerate([("L","−"),("L","−"),("W","+"),("L","−"),("L","−"),("L","−"),("L","−")]):
    txt+=row(f"7/{22+i}",f"T{i} ML (vs X) [adj: ace_edge+3]","ML-fav",62,res,clv)
recent=m.window_rows(m.parse_rows(txt,T),T); assert len(recent)==7
dims,acts=m.actions_for(recent)
assert any(d=="adj:ace_edge" and ("COOL" in sev or "SUSPEND" in sev) for sev,d,_ in acts), acts
assert any(d=="type:ML-fav" and "MARKET-SHADE" in sev for sev,d,_ in acts), acts   # 1+/6−
# RE-WARM: 3 wins in the last 5 suppresses the freeze even if the window hit% is cold
txt2=hdr
for i,(res,clv) in enumerate([("L","—"),("L","—"),("L","—"),("W","—"),("W","—"),("L","—"),("W","—")]):
    txt2+=row(f"7/{22+i}",f"U{i} ML (vs X) [adj: hot_tag+3]","ML-fav",62,res,clv)
_,a2=m.actions_for(m.window_rows(m.parse_rows(txt2,T),T))
assert not any(d=="adj:hot_tag" and ("COOL" in sev or "SUSPEND" in sev) for sev,d,_ in a2), a2
# CLV shade needs a ≥2 margin — a 3−/2+ coin-flip split must NOT shade
txt3=hdr
for i,clv in enumerate(["+","+","−","−","−"]):
    txt3+=row(f"7/{22+i}",f"V{i} game total Over 8.5 (A @ B)","Total",56,"W",clv)
_,a3=m.actions_for(m.window_rows(m.parse_rows(txt3,T),T))
assert not any("MARKET-SHADE" in sev and d=="type:total" for sev,d,_ in a3), a3
# K-line bucketing feeds the dimension name
r=m.parse_rows(hdr+row("7/30","Cease Over 7.5 K (STL @ TOR)","K-Over",58,"L"),T)
assert any("type:K-Over ≥7.5" in x["dims"] for x in r), r
PY
then ok "COOL/SUSPEND on cold dims; ML-fav CLV shade; rewarm + margin guards; K-line buckets"; else no "pulse" "$(cat /tmp/_selftest_out)"; fi

# ── 5a5. 8/7 deep-dive audit pins: leg dedup / epoch years / bold CLV / started-game gates ──
echo "5a5. pulse dedup + epoch + live-price gates (8/7 audit)"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u, datetime as dt, tempfile, os, json
s=u.spec_from_file_location("p","tools/pulse.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
T=dt.date(2026,8,1)
hdr="## Played legs\n\n| Date | Leg | Type | Price | TrueP | ImplP | Edge | Result | Played | CLV | Bucket |\n|-|-|-|-|-|-|-|-|-|-|-|\n"
def row(d,leg,typ,tp,res,clv="—"):
    return f"| {d} | {leg} | {typ} | -120 | {tp}% | 55% | +2 | **{res}** | Y | {clv} | P |\n"
# DEDUP: the same physical leg logged 3x (scan + reprices) counts ONCE (131-rows-vs-107-legs bug)
txtd =hdr+row("7/30","Holmes U4.5K +100","K-Under",55,"L","−")
txtd+=row("7/30","**Holmes U4.5K** — 16:00 REPRICE +105","K-Under",55,"L","−")
txtd+=row("7/30","Holmes U4.5K (re-derived; supersedes the 11:00 row)","K-Under",55,"L","−")
txtd+=row("7/31","Gilbert O6.5K -110","K-Over",60,"W","+")
rd=m.parse_rows(txtd,T)
assert len(rd)==2, f"4 rows must dedup to 2 unique legs, got {len(rd)}"
# bold-wrapped CLV verdict parses (was silently dropped)
rb=m.parse_rows(hdr+row("7/30","Kirby U5.5K -113","K-Under",60,"W","**+**"),T)
assert rb[0]["clv"]=="+", rb
rb2=m.parse_rows(hdr+row("7/30","Sale U6.5K -120","K-Under",60,"W","**− (line moved, against)**"),T)
assert rb2[0]["clv"]=="−", rb2
# EPOCH anchor: a 2026 row must NOT re-enter an Aug-2027 window (season-anniversary trap)
ep="<!-- ledger-epoch: 2026 -->\n"+hdr+row("8/5","Kirby U5.5K -113","K-Under",60,"W","+")
T27=dt.date(2027,8,8)
r27=m.parse_rows(ep,T27)
assert r27 and r27[0]["date"].year==2026, r27
assert m.window_rows(r27,T27)==[], "stale season must idle the governor, not govern it"
# and the legacy (no-marker) inference DOES mis-date it — documents why the marker exists
rleg=m.parse_rows(hdr+row("8/5","Kirby U5.5K -113","K-Under",60,"W","+"),T27)
assert rleg[0]["date"].year==2027
# season wrap inside the epoch walk: 10/xx -> 3/xx rolls the year forward
wrap=("<!-- ledger-epoch: 2026 -->\n"+hdr
      +row("10/1","Kirby U5.5K -113","K-Under",60,"W","+")
      +row("3/28","Gilbert O6.5K -110","K-Over",60,"W","+"))
rw=m.parse_rows(wrap,dt.date(2027,4,2))
assert {x["date"].year for x in rw}=={2026,2027}, rw
# kprice started-game gate (in-game props are not pre-game lines)
ks=u.spec_from_file_location("k","tools/kprice.py"); km=u.module_from_spec(ks); ks.loader.exec_module(km)
assert km.started("2026-08-07T22:40:00Z","2026-08-08T00:30:00Z") is True
assert km.started("2026-08-08T01:40:00Z","2026-08-08T00:30:00Z") is False
assert km.started(None) is False
td=tempfile.mkdtemp(); os.environ["TMPDIR"]=td
os.makedirs(os.path.join(td,"odds_cache"),exist_ok=True)
json.dump([{"id":"ev1","commence_time":"2026-08-07T22:40:00Z"}],
          open(os.path.join(td,"odds_cache","slate_2026-08-07.json"),"w"))
assert km.event_commence("2026-08-07","ev1")=="2026-08-07T22:40:00Z"
assert km.event_commence("2026-08-07","nope") is None
PY
then ok "leg dedup; epoch year anchor + wrap + stale-idle; bold CLV; kprice started gate"; else no "pulse dedup/epoch" "$(cat /tmp/_selftest_out)"; fi
has "clv try_prop_close refuses a started game's live props feed" "game already started" "$(cat tools/clv_capture.py)"
has "odds_api cmd_clv refuses a started game's feed as a close" "already STARTED" "$(cat tools/odds_api.sh)"
has "odds_api cmd_game banners in-game cached boards" "GAME STARTED — cached prices" "$(cat tools/odds_api.sh)"
has "results_log carries the ledger-epoch season anchor" "ledger-epoch: 2026" "$(head -3 results_log.md)"

# ── 5a6. clv_backfill — historical-close retro-fill (pure helpers, no spend) ──
echo "5a6. clv_backfill (snapshot targeting / grouping / gates)"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u
s=u.spec_from_file_location("b","tools/clv_backfill.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
sched=m.parse_sched('{"dates":[{"games":['
 '{"gameDate":"2026-08-02T17:41:00Z","teams":{"away":{"team":{"name":"Pittsburgh Pirates"}},"home":{"team":{"name":"Cincinnati Reds"}}}},'
 '{"gameDate":"2026-08-02T20:11:00Z","teams":{"away":{"team":{"name":"Minnesota Twins"}},"home":{"team":{"name":"Seattle Mariners"}}}}]}]}')
assert sched["Cincinnati Reds"]==["2026-08-02T17:41:00Z"]
# snapshot = commence − 2min, floored to the API's 5-min grain (groups same-minute starts)
assert m.snap_ts("2026-08-02T17:41:00Z")=="2026-08-02T17:35:00Z"
assert m.snap_ts("2026-08-02T20:11:00Z")=="2026-08-02T20:05:00Z"
c,why=m.commence_for("reds",sched); assert c=="2026-08-02T17:41:00Z" and why is None
c,why=m.commence_for("cubs",sched); assert c is None and "no StatsAPI game" in why
dh=m.parse_sched('{"dates":[{"games":['
 '{"gameDate":"2026-08-02T17:00:00Z","teams":{"away":{"team":{"name":"A"}},"home":{"team":{"name":"Detroit Tigers"}}}},'
 '{"gameDate":"2026-08-02T23:00:00Z","teams":{"away":{"team":{"name":"A"}},"home":{"team":{"name":"Detroit Tigers"}}}}]}]}')
c,why=m.commence_for("tigers",dh); assert c is None and "doubleheader" in why
g,err=m.parse_snapshot('{"timestamp":"t","data":[{"id":"x"}]}'); assert err is None and g==[{"id":"x"}]
g,err=m.parse_snapshot('{"message":"INVALID_KEY"}'); assert g is None and "INVALID_KEY" in err
g,err=m.parse_snapshot('garbage'); assert "unparseable" in err
# row targeting: blank-CLV + exact date + backfillable kind only
hdr=("## Played legs\n\n| Date | Leg | Type | Price | TrueP | ImplP | Edge | Result | Played | CLV | Bucket |\n"
     "|-|-|-|-|-|-|-|-|-|-|-|\n")
txt=(hdr+"| 8/2 | Rays ML (vs TEX) | ML-fav | -139 | 58% | 56% | +2 | **W** | Y | — | P |\n"
         "| 8/2 | Rays -1.5 RL (vs TEX) | Run line | +160 | 40% | 38% | +2 | **L** | Y | + 40%cl | P |\n"
         "| 8/2 | Gilbert Over 6.5 K | K-Over | -110 | 60% | 55% | +5 | **W** | Y | — | P |\n"
         "| 8/3 | Rays ML (vs TEX) | ML-fav | -139 | 58% | 56% | +2 | **W** | Y | — | P |\n")
rows=m.target_rows(txt,"2026-08-02")
assert len(rows)==2, rows                       # filled row + wrong-date row excluded
kinds={r[3] for r in rows}
assert "h2h" in kinds                           # the ML row is fillable
assert any(r[6] and "hand-pull" in r[6] for r in rows), rows   # K-prop routed MANUAL
PY
then ok "backfill: sched parse, 5-min snap floor, DH refusal, snapshot shapes, row targeting"; else no "clv_backfill" "$(cat /tmp/_selftest_out)"; fi
has "clv_backfill gates spend on the paid tier" "RICH_FLOOR" "$(cat tools/clv_backfill.py)"
has "clv_backfill defaults to plan mode (no spend)" "PLAN (no spend)" "$(cat tools/clv_backfill.py)"

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

# ── 5c. nrfi_digest.py — per-day tally + win% (notification/email block) ──────
echo "5c. nrfi_digest (daily NRFI/YRFI win% + table)"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u
s=u.spec_from_file_location("d","tools/nrfi_digest.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
rows=[{"matchup":"A @ B","pick":"NRFI","truep":"55%","result":"W"},
      {"matchup":"C @ D","pick":"YRFI","truep":"54%","result":"L"},
      {"matchup":"E @ F","pick":"NRFI","truep":"53%","result":"TBD"}]
t=m.tally(rows)
assert (t["w"],t["l"],t["tbd"],t["settled"])==(1,1,1,2), t
assert abs(t["pct"]-50.0)<1e-9, t           # win% over SETTLED only (1 of 2)
assert (t["nrfi"],t["yrfi"])==(2,1), t
assert m.md_date("2026-06-13")=="6/13"
out=m.render(rows,"6/13","md")
assert "| Matchup | Pick | TrueP | Result |" in out and "50% W" in out, out
assert m.render([],"6/13","compact").endswith("no reads logged.")  # empty-day safe
PY
then ok "tally win% over settled-only; md table + empty-day guard"; else no "nrfi_digest" "$(cat /tmp/_selftest_out)"; fi

# ── 6. parlay.py — fractional footgun rejected, normal math intact ───────────
echo "6. parlay.py"
if ./tools/parlay.py --leg 0.6:-150 --leg 0.55:+120 >/tmp/_selftest_out 2>&1; then
  no "parlay rejects fractional TrueP (0.6)" "exited 0 — guard did not fire"
else
  has "parlay rejects fractional TrueP (0.6)" "fraction" "$(cat /tmp/_selftest_out)"
fi
has "parlay normal math (60:-150 + 55:+120 → 33.0%)" "33.0%" "$(./tools/parlay.py --leg 60:-150 --leg 55:+120 2>&1)"

# ── 6b. ticket.py — the +200-band construction optimizer ─────────────────────
echo "6b. ticket.py (band search, corr pairs, doctrine guards)"
TKT="$(./tools/ticket.py --leg '63:-110:SEA-TEX:Gilbert O6.5K' --leg '63:-164:NYY-PHI:PHI ML' --leg '57:-132:CIN-STL:STL ML' 2>&1)"
has "band pick = max-floor +207 @ 39.7% (7/26 reproduction)" "+207  floor  39.7%" "$TKT"
has "the +440 3-legger stays OUT of band (frontier only)" "+440  floor  22.6%" "$TKT"
TKC="$(./tools/ticket.py --leg '63:-164:NYY-PHI:PHI ML:moderate' --leg '58:-115:NYY-PHI:Sanchez O6.5K:moderate' 2>&1)"
has "same-game pos-corr pair up-adjusts (43.7% > naive 36.5%)" "floor  43.7%" "$TKC"
has "corr pair prints the min acceptable SGP quote" "worth taking only if the quote beats" "$TKC"
TKN="$(./tools/ticket.py --leg '60:-140:A-B:ML:neg-moderate' --leg '58:-115:A-B:OppK:neg-moderate' --leg '58:-125:C-D:C ML' --leg '56:-115:C-D:CK' 2>&1)"
has "negative pair rejected, never recommended" "negatively-correlated pair" "$TKN"
has "undeclared same-game pair rejected (one leg per game)" "without a declared corr tier" "$TKN"
if ./tools/ticket.py --leg "0.63:-110:X:frac" --leg "60:-120:Y:ok" >/tmp/_selftest_out 2>&1; then
  no "ticket.py rejects fractional TrueP (0.63)" "accepted a fraction — footgun regression"
else ok "ticket.py rejects fractional TrueP (0.63)"; fi

# ── 7. devig.sh — no-vig math ─────────────────────────────────────────────────
echo "7. devig.sh"
has "devig prints a ¼-Kelly stake line when TrueP given" "¼-Kelly" "$(./tools/devig.sh -130 +110 59 2>&1)"
DV="$(./tools/devig.sh -150 +130 2>&1)"
has "devig -150/+130 → ~58% fav side"  "58" "$DV"
has "devig -150/+130 → ~42% dog side"  "42" "$DV"

# ── 8. truep.py — registry loads ─────────────────────────────────────────────
echo "8. truep.py"
has "truep --list shows the ace_edge adjustment" "ace_edge" "$(./tools/truep.py --list 2>&1)"
has "truep emits the [adj: …] ledger tag (ace_edge stays +3 — on watch, n<20 unique)" "[adj: ace_edge+3, custom-2]" \
    "$(./tools/truep.py --base-prob 54.3 --adj ace_edge --custom=-2:test 2>&1)"
# registry review 8/7/26 pins: custom hard-cap ±3; ~name mirrors a registry adj (sign-flip)
has "truep rejects a custom beyond the ±3 cap" "exceeds the ±3 cap" \
    "$(./tools/truep.py --base-prob 50 --custom=+8:big 2>&1)"
has "truep ~name mirror flips the sign and tags the applied sign" "[adj: own_sp_hi+5]" \
    "$(./tools/truep.py --base-prob 43.4 --adj '~own_sp_hi' 2>&1)"
if python3 - <<'PY' 2>/tmp/_selftest_out
import importlib.util as u
s=u.spec_from_file_location("c","tools/calib.py"); m=u.module_from_spec(s); s.loader.exec_module(m)
assert m.parse_adj_tags("PHI ML [adj: ace_edge+3, wind_in_under+3]")==["ace_edge","wind_in_under"]
assert m.parse_adj_tags("LAD ML [adj: none]")==[]         # tagged control row
assert m.parse_adj_tags("LAD ML (no tag)") is None        # untagged rows are skipped
assert m.parse_adj_tags("X [adj: custom-2]")==["custom"]
PY
then ok "calib.parse_adj_tags: names / none-control / untagged all correct"; else no "parse_adj_tags" "$(cat /tmp/_selftest_out)"; fi

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

# best_jq excludes already-started games (8/7: a live BOS −10000 showed as a
# "best line"; in-game prices are not shoppable and poison devig/CLV)
if eval "$(awk '/^best_jq\(\) \{/{p=1} p{print} p&&/^\}/{exit}' tools/odds_api.sh)" 2>/dev/null; then
  mix='[{"commence_time":"2026-08-07T22:40:00Z","away_team":"Boston Red Sox","home_team":"Houston Astros",
         "bookmakers":[{"title":"DK","markets":[{"key":"h2h","outcomes":[
           {"name":"Boston Red Sox","price":-10000},{"name":"Houston Astros","price":2500}]}]}]},
        {"commence_time":"2026-08-08T01:40:00Z","away_team":"San Diego Padres","home_team":"Los Angeles Dodgers",
         "bookmakers":[{"title":"FD","markets":[{"key":"h2h","outcomes":[
           {"name":"San Diego Padres","price":140},{"name":"Los Angeles Dodgers","price":-165}]}]}]}]'
  BQ="$(echo "$mix" | jq -r --arg now "2026-08-08T00:30:00Z" "$(best_jq h2h)")"
  has "best_jq banners the started-game exclusion" "⛔ 1 game(s) already started" "$BQ"
  case "$BQ" in *"Boston Red Sox @"*) no "best_jq drops the started game's lines" "live BOS game still listed";;
                *) ok "best_jq drops the started game's lines";; esac
  has "best_jq keeps the not-yet-started game" "San Diego Padres @ Los Angeles Dodgers" "$BQ"
else no "extract best_jq from odds_api.sh"; fi

# ── 13b. odds_api quota command + cron reports credits each run (offline) ────
echo "13b. odds credits reporting"
OA="$(cat tools/odds_api.sh)"
has "odds_api.sh has a 'quota' subcommand" "quota)   cmd_quota" "$OA"
has "odds_api.sh quota uses the FREE /sports endpoint" "FREE: the /sports" "$OA"
CRED_N="$(grep -c 'Odds API credits remaining' tools/cron_build.sh)"
[[ "${CRED_N:-0}" -ge 3 ]] && ok "all 3 builds report Odds API credits ($CRED_N mentions)" \
  || no "all 3 builds report Odds API credits" "only $CRED_N mentions (expect >=3)"
# missed-run watchdog: 16:00 + 18:00 each self-heal a dropped earlier firing (8/7 gap)
WD_N="$(grep -c 'MISSED-RUN WATCHDOG' tools/cron_build.sh)"
[[ "${WD_N:-0}" -ge 2 ]] && ok "16:00 + 18:00 builds carry the missed-run watchdog ($WD_N)" \
  || no "missed-run watchdog in 16:00+18:00 builds" "only $WD_N mentions (expect >=2)"

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

# ── 13e. calib.py FIELD-LEVEL parse assertions (offline) ─────────────────────
# Three silent parse bugs in four days (8/3 placement, 8/4 verdict-token order,
# 8/6 bold-vs-star) each slipped past checks that assert row COUNTS and section
# PLACEMENT but never that an individual FIELD parses to the right value.
#   - 8/6: parse_pct used a bare `"*" in s`, which also matched the markdown bold
#     markers in `**54.5%**` — so every bold-wrapped TrueP was misread as a legacy
#     reconstructed row and silently dropped from the bands, from the Brier
#     scoreboard, and from pulse.py's window (172 -> 221 legs once fixed, and the
#     headline skill flipped sign). These assertions pin that class down.
echo "13e. calib.py field-level parse assertions"
DESC="parse_pct: bold TrueP '**54.5%**' parses as NOT starred"
runblk python3 -c "
import importlib.util,sys
spec=importlib.util.spec_from_file_location('c','tools/calib.py')
m=importlib.util.module_from_spec(spec); m.__dict__['__file__']='tools/calib.py'
exec(compile(open('tools/calib.py').read().split('def main')[0],'c','exec'), m.__dict__)
v,st=m.parse_pct('**54.5%**')
assert v==54.5, v
assert st is False, 'bold TrueP misread as a legacy starred row'
v,st=m.parse_pct('~72%*')
assert v==72.0 and st is True, 'real legacy star marker no longer detected'
v,st=m.parse_pct('60%')
assert v==60.0 and st is False
"

DESC="parse_result: '**W** ✅ WON' -> W, '**L** ❌ LOST' -> L, TBD/SUPERSEDED -> None"
runblk python3 -c "
import importlib.util
m=importlib.util.module_from_spec(importlib.util.spec_from_file_location('c','tools/calib.py'))
m.__dict__['__file__']='tools/calib.py'
exec(compile(open('tools/calib.py').read().split('def main')[0],'c','exec'), m.__dict__)
assert m.parse_result('**W** ✅ WON (12 K)')=='W'
assert m.parse_result('**L** ❌ LOST (5 runs)')=='L'
assert m.parse_result('**would-L** (...)')=='L'
assert m.parse_result('TBD — pending')is None
assert m.parse_result('**SUPERSEDED → see Run 16:00**')is None
assert m.parse_result('**n/a** — status row')is None
"

# 8/7 deep-dive pins — the fourth+fifth instances of the silent-parse class:
#   (a) italics annotation '% *(pre-shade …)*' starred out 18 governor-audit rows;
#   (b) 'SUPERSEDED @ 16:00 — … **L**' settled the same leg at multiple prices (9 dupes);
#   (c) prose suffixes in [adj: …] minted garbage singleton dimensions in §1c + pulse.
DESC="parse_pct: italics annotation NOT starred; star only when glued to % ('72%*')"
runblk python3 -c "
import importlib.util
m=importlib.util.module_from_spec(importlib.util.spec_from_file_location('c','tools/calib.py'))
m.__dict__['__file__']='tools/calib.py'
exec(compile(open('tools/calib.py').read().split('def main')[0],'c','exec'), m.__dict__)
assert m.parse_pct('51.4% *(pre-shade 56.4%)*')==(51.4,False), 'italics annotation must not star the row'
assert m.parse_pct('~72%*')==(72.0,True)
assert m.parse_pct('**54.5%**')==(54.5,False)
"
DESC="parse_result: SUPERSEDED anywhere vetoes a bold verdict; TBD mid-prose does NOT"
runblk python3 -c "
import importlib.util
m=importlib.util.module_from_spec(importlib.util.spec_from_file_location('c','tools/calib.py'))
m.__dict__['__file__']='tools/calib.py'
exec(compile(open('tools/calib.py').read().split('def main')[0],'c','exec'), m.__dict__)
assert m.parse_result('SUPERSEDED @ 16:00 — repriced; **L** (7 K, one short)') is None, 'superseded row must never settle'
assert m.parse_result('**L** (TEX 2-4 MIN) — home vs MIN TBD/bullpen game (D5)')=='L', 'TBD in prose must not drop a decided row'
"
DESC="parse_adj_tags: prose suffixes dropped; PULSE-SHADED→control; n/a→untagged"
runblk python3 -c "
import importlib.util
m=importlib.util.module_from_spec(importlib.util.spec_from_file_location('c','tools/calib.py'))
m.__dict__['__file__']='tools/calib.py'
exec(compile(open('tools/calib.py').read().split('def main')[0],'c','exec'), m.__dict__)
assert m.parse_adj_tags('[adj: hot_dog+3 (fades.md B1)]')==['hot_dog']
assert m.parse_adj_tags('[adj: pitcher_park_under+3 → **band-blocked**]')==['pitcher_park_under']
assert m.parse_adj_tags('[adj: market_disagrees-4, custom+8]')==['market_disagrees','custom']
assert m.parse_adj_tags('[adj: custom+3.2]')==['custom']
assert m.parse_adj_tags('[adj: PULSE-SHADED to none]')==[]
assert m.parse_adj_tags('[adj: none — pure line-shop]')==[]
assert m.parse_adj_tags('[adj: n/a]') is None
assert m.parse_adj_tags('untagged cell') is None
"

DESC="parse_adj_tags: BOLD/code-fenced tag names still resolve (8/12 silent-attribution bug)"
runblk python3 -c "
import importlib.util
m=importlib.util.module_from_spec(importlib.util.spec_from_file_location('c','tools/calib.py'))
m.__dict__['__file__']='tools/calib.py'
exec(compile(open('tools/calib.py').read().split('def main')[0],'c','exec'), m.__dict__)
# the ledger's house style bolds the magnitude; the leading '*' used to defeat the
# name regex and silently dump every tagged row into the '(none)' control bucket
assert m.parse_adj_tags('[adj: **hitter_park_over+3 (full magnitude)**]')==['hitter_park_over']
assert m.parse_adj_tags('[adj: **wind_out_over+4**, **custom+2**]')==['wind_out_over','custom']
assert m.parse_adj_tags('[adj: \`ace_edge+3\`]')==['ace_edge']
assert m.parse_adj_tags('[adj: **none — market-anchored**]')==[]
"

DESC="leg_key: multi-line aggregate rows never steal a real single leg's key"
runblk python3 -c "
import importlib.util,sys
sys.path.insert(0,'tools')
m=importlib.util.module_from_spec(importlib.util.spec_from_file_location('c','tools/calib.py'))
m.__dict__['__file__']='tools/calib.py'
exec(compile(open('tools/calib.py').read().split('def main')[0],'c','exec'), m.__dict__)
single=m.leg_key('8/11','TB @ ATH Total OVER 8.5 −205','Total')
agg=m.leg_key('8/11','STRUCK BY DOCTRINE — TB @ ATH Over 8.5/10.5 AND MIL @ SD Under 7.5','Total')
assert single!=agg, 'aggregate kill-list row must not collide with a real leg key'
assert agg[1]=='aggregate', agg
# a genuine single total still keys as a total
assert single[1]=='T' and single[4]=='8.5', single
"

DESC="no 8/6+ ledger row has a broken column count (13 fields)"
runblk python3 -c "
import sys
bad=[]
for i,ln in enumerate(open('results_log.md'),1):
    if ln.startswith('| 8/6 ') or ln.startswith('| 8/7 '):
        n=ln.count('|')+1
        if n!=13: bad.append((i,n))
assert not bad, 'rows with wrong column count (injected pipes): %r'%bad[:5]
"

# ── 14. ONLINE (free StatsAPI only): resolver collision regression ───────────
if [[ $QUICK -eq 0 ]]; then
  echo "14. mlb_api resolver (live StatsAPI — free, no odds quota)"
  if ./tools/mlb_api.sh check >/dev/null 2>&1; then
    has "teamform LAD → Dodgers (team 119, NOT Phillies 143)" "team 119" "$(./tools/mlb_api.sh teamform LAD 1 2>/dev/null | head -1)"
    # 8/12/26: teamform now carries the contact-surge fields. Run differential is blind to a
    # hits spike that has not yet converted to runs (MIN 8/12: L10 run diff -4 while hits/g ran
    # 8.8 with three 13+ games), so the header must keep printing them or the signal silently
    # disappears from every build that reads this line.
    has "teamform header carries hits/g + median + 13+ blowup count" "hits/g" "$(./tools/mlb_api.sh teamform LAD 5 2>/dev/null | head -1)"
    has "teamform per-game rows carry hits"                          "H"      "$(./tools/mlb_api.sh teamform LAD 5 2>/dev/null | sed -n 2p)"
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
