#!/usr/bin/env python3
"""nrfi_settle.py — auto-settle NRFI/YRFI reads off the 1st-inning line score.

WHY THIS EXISTS
    The NRFI/YRFI tracker (nrfi_tracker.md) used to rely on the run prompt remembering
    to settle open reads by hand — so it silently went stale (caught 6/11/26). This makes
    the settle DETERMINISTIC: it pulls each game's 1st-inning runs from StatsAPI and stamps
    W/L, the same way settle.py settles ML legs and clv_capture.py writes the CLV column.

WHAT IT DOES
    1. Pulls the day's schedule WITH linescore via `mlb_api.sh raw schedule?...&hydrate=linescore,team`.
    2. For each game extracts the 1st-inning total runs (away[0]+home[0]):
         total == 0  -> NRFI occurred   |   total > 0  -> YRFI occurred.
    3. Scans nrfi_tracker.md ledger rows whose Date matches and whose Result is TBD,
       reads the matchup's two team abbreviations, and decides W/L:
         pick NRFI -> W if NRFI occurred else L
         pick YRFI -> W if YRFI occurred else L
    Only games in a Final state are settled; in-progress/scheduled games are left TBD.

MODES
    (default)   READ-ONLY — print proposals (like settle.py). Apply by hand if you prefer.
    --apply     WRITE the Result cell (TBD -> **W (1st a-b)**) in place, idempotent (filled
                rows are skipped), and refresh the running-totals Record/NRFI/YRFI line.

USAGE
    tools/nrfi_settle.py                 # propose for yesterday (read-only)
    tools/nrfi_settle.py 2026-06-11      # propose for a specific date
    tools/nrfi_settle.py --apply         # settle yesterday in place
    tools/nrfi_settle.py 2026-06-11 --apply
"""
import json
import os
import re
import subprocess
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
MLB_API = os.path.join(HERE, "mlb_api.sh")
DEFAULT_TRACKER = os.path.join(HERE, "..", "nrfi_tracker.md")

# StatsAPI abbreviation aliases -> the form used in the tracker matchups.
ALIAS = {"CHW": "CWS", "ARI": "AZ", "OAK": "ATH", "WSN": "WSH", "SDP": "SD", "SFG": "SF",
         "TBR": "TB", "KCR": "KC"}


def norm(abbr):
    a = abbr.strip().upper()
    return ALIAS.get(a, a)


def md_date(d):
    """YYYY-MM-DD -> M/D (no leading zeros), matching the ledger's Date format."""
    _, m, day = d.split("-")
    return f"{int(m)}/{int(day)}"


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def pull_games(d):
    """Return {frozenset({away,home}): dict} with the 1st-inning total + state."""
    try:
        out = subprocess.run(
            ["bash", MLB_API, "raw",
             f"schedule?sportId=1&date={d}&hydrate=linescore,team"],
            capture_output=True, text=True, timeout=30).stdout
        data = json.loads(out)
    except Exception as e:  # noqa: BLE001
        print(f"⚠ could not pull schedule for {d}: {e}", file=sys.stderr)
        return {}
    games = {}
    for dt in data.get("dates", []):
        for g in dt.get("games", []):
            try:
                away = norm(g["teams"]["away"]["team"]["abbreviation"])
                home = norm(g["teams"]["home"]["team"]["abbreviation"])
            except KeyError:
                continue
            state = g.get("status", {}).get("detailedState", "?")
            innings = g.get("linescore", {}).get("innings", [])
            first_total = None
            if innings:
                f = innings[0]
                ar = f.get("away", {}).get("runs")
                hr = f.get("home", {}).get("runs")
                if isinstance(ar, int) and isinstance(hr, int):
                    first_total = (ar, hr)
            games[frozenset({away, home})] = {
                "away": away, "home": home, "state": state, "first": first_total}
    return games


def matchup_teams(text):
    """'ATL @ CWS (Sale/Martin)' -> ('ATL','CWS'); None if not parseable."""
    m = re.match(r"\s*([A-Z]{2,3})\s*@\s*([A-Z]{2,3})", text)
    if not m:
        return None
    return norm(m.group(1)), norm(m.group(2))


def verdict_for(pick, first_total):
    """(pick, (away1st,home1st)) -> ('W'|'L', nrfi_occurred:bool, total:int)."""
    total = first_total[0] + first_total[1]
    nrfi = total == 0
    pick = pick.upper()
    if pick == "NRFI":
        return ("W" if nrfi else "L"), nrfi, total
    if pick == "YRFI":
        return ("W" if not nrfi else "L"), nrfi, total
    return ("?", nrfi, total)


def recompute_record(lines, target_label="record"):
    """Tally W/L over ALL ledger rows (settled). Returns dict of counts."""
    rec = {"W": 0, "L": 0, "NRFI_W": 0, "NRFI_L": 0, "YRFI_W": 0, "YRFI_L": 0}
    for ln in lines:
        if not ln.lstrip().startswith("|"):
            continue
        c = cells(ln)
        if len(c) < 6 or not re.match(r"\d+/\d+", c[0]):
            continue
        pick = c[2].upper()
        res = c[5].upper()
        if pick not in ("NRFI", "YRFI"):
            continue
        if re.search(r"\bW\b", res):
            rec["W"] += 1
            rec[f"{pick}_W"] += 1
        elif re.search(r"\bL\b", res):
            rec["L"] += 1
            rec[f"{pick}_L"] += 1
    return rec


def main():
    argv = sys.argv[1:]
    apply = "--apply" in argv
    pos = [a for a in argv if not a.startswith("--")]
    d = pos[0] if pos and re.match(r"\d{4}-\d{2}-\d{2}", pos[0]) else \
        (date.today() - timedelta(days=1)).isoformat()
    tracker = next((a for a in pos if a.endswith(".md")), DEFAULT_TRACKER)

    games = pull_games(d)
    if not games:
        print(f"No games/linescore parsed for {d}. Nothing to settle.")
        return

    target = md_date(d)
    with open(tracker, encoding="utf-8") as fh:
        lines = fh.readlines()

    print("=" * 64)
    mode = "AUTO-WRITE (--apply)" if apply else "READ-ONLY (proposals)"
    print(f"  NRFI SETTLE — {d}   [{mode}]")
    print("=" * 64)

    changed = 0
    proposals = []
    for i, ln in enumerate(lines):
        if not ln.lstrip().startswith("|"):
            continue
        c = cells(ln)
        if len(c) < 6 or not c[0].startswith(target):
            continue
        # header/separator rows
        if c[2].upper() not in ("NRFI", "YRFI"):
            continue
        matchup, pick, result = c[1], c[2], c[5]
        if "tbd" not in result.lower():
            continue  # idempotent: already settled
        teams = matchup_teams(matchup)
        if not teams:
            proposals.append((matchup, "??", "could not parse teams from matchup"))
            continue
        g = games.get(frozenset(teams))
        if not g:
            proposals.append((matchup, "??", f"no game found for {teams[0]}@{teams[1]}"))
            continue
        if not g["state"].lower().startswith(("final", "game over", "completed")):
            proposals.append((matchup, "—", f"game not final (state={g['state']})"))
            continue
        if g["first"] is None:
            proposals.append((matchup, "—", "1st-inning line score not available"))
            continue
        verdict, nrfi, total = verdict_for(pick, g["first"])
        ev = f"1st {g['first'][0]}-{g['first'][1]} → {'NRFI' if nrfi else 'YRFI'}"
        proposals.append((f"{matchup} [{pick}]", verdict, ev))
        if apply and verdict in ("W", "L"):
            c[5] = f"**{verdict}** ({ev})"
            lines[i] = "| " + " | ".join(c) + " |\n"
            changed += 1

    if not proposals:
        print(f"\n  (no TBD {target} NRFI/YRFI rows to settle)")
    else:
        for leg, verdict, why in proposals:
            tag = {"W": "✅ W", "L": "❌ L"}.get(verdict, f"⚠ {verdict}")
            print(f"   {tag:<6} {leg[:46]:<46}  {why}")

    if apply and changed:
        rec = recompute_record(lines)
        new_total = f"**{rec['W']}-{rec['L']}**"
        new_nrfi = f"**{rec['NRFI_W']}-{rec['NRFI_L']}**"
        new_yrfi = f"**{rec['YRFI_W']}-{rec['YRFI_L']}**"
        joined = "".join(lines)
        joined, n1 = re.subn(r"(\*\*Record:\*\*\s*)\*\*\d+-\d+\*\*", r"\g<1>" + new_total, joined, count=1)
        joined, n2 = re.subn(r"(\*\*NRFI:\*\*\s*)\*\*\d+-\d+\*\*", r"\g<1>" + new_nrfi, joined, count=1)
        joined, n3 = re.subn(r"(\*\*YRFI:\*\*\s*)\*\*\d+-\d+\*\*", r"\g<1>" + new_yrfi, joined, count=1)
        with open(tracker, "w", encoding="utf-8") as fh:
            fh.write(joined)
        print(f"\n  ✍ wrote {changed} result(s) to {os.path.relpath(tracker, HERE)}")
        print(f"  record now {rec['W']}-{rec['L']}  (NRFI {rec['NRFI_W']}-{rec['NRFI_L']} · "
              f"YRFI {rec['YRFI_W']}-{rec['YRFI_L']})")
        if not (n1 and n2 and n3):
            print("  ⚠ running-totals Record line not fully updated — check the format by hand.")
    elif apply:
        print("\n  (nothing to write — no final TBD rows matched)")
    else:
        print("\n  → re-run with --apply to stamp these into nrfi_tracker.md.")
    print("=" * 64)


if __name__ == "__main__":
    main()
