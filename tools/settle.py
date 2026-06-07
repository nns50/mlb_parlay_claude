#!/usr/bin/env python3
"""settle.py — match a day's finals to open (TBD) legs and PROPOSE settle edits.

WHY THIS EXISTS
    Settling is the most error-prone manual step: pull finals, eyeball which logged leg
    maps to which game, decide W/L, hand-edit results_log.md. This automates the lookup +
    matching and prints copy-ready proposals. It is READ-ONLY (like calib.py) — it never
    edits the ledger; you apply the proposals so the audit trail stays deliberate.

WHAT IT DOES
    1. Pulls finals via `mlb_api.sh finals <date>` (StatsAPI; needs the API reachable).
    2. Scans results_log.md for rows whose Date matches and whose Result is TBD.
    3. Maps each leg's team (by nickname) to the game's final and proposes W/L for
       team-side bets (ML / run line / spread). Props / totals / K-legs → flagged MANUAL
       (the score alone can't settle them).

USAGE
    tools/settle.py                 # settles yesterday (relative to today)
    tools/settle.py 2026-06-05      # settle a specific date
    tools/settle.py 2026-06-05 path/to/results_log.md
"""
import os
import re
import subprocess
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
MLB_API = os.path.join(HERE, "mlb_api.sh")
DEFAULT_LEDGER = os.path.join(HERE, "..", "results_log.md")

# Nickname (as it appears in leg text, lowercased) -> StatsAPI abbreviation.
NICK = {
    "diamondbacks": "AZ", "d-backs": "AZ", "dbacks": "AZ",
    "athletics": "ATH", "blue jays": "TOR", "red sox": "BOS", "white sox": "CWS",
    "dodgers": "LAD", "angels": "LAA", "padres": "SD", "giants": "SF", "rockies": "COL",
    "mariners": "SEA", "rangers": "TEX", "astros": "HOU",
    "yankees": "NYY", "orioles": "BAL", "rays": "TB", "mets": "NYM", "marlins": "MIA",
    "guardians": "CLE", "tigers": "DET", "royals": "KC", "twins": "MIN",
    "braves": "ATL", "phillies": "PHI", "nationals": "WSH", "pirates": "PIT",
    "brewers": "MIL", "cardinals": "STL", "cubs": "CHC", "reds": "CIN",
}
# Longer nicknames first so "white sox" matches before "sox"-style partials.
NICK_ORDER = sorted(NICK, key=len, reverse=True)

# Whole-word abbreviation fallback (e.g. a leg written "LAD ML" / "TB ML" with no nickname).
# Kept in sync with clv_capture.py so the two ledger tools agree on abbreviation-only legs.
# (Bug 6/7/26: settle.py lacked this, so it failed to match legs clv_capture.py matched fine.)
ABBREV = {
    "lad": "LAD", "laa": "LAA", "nyy": "NYY", "nym": "NYM", "sea": "SEA",
    "tb":  "TB",  "det": "DET", "cle": "CLE", "hou": "HOU", "atl": "ATL",
    "phi": "PHI", "mil": "MIL", "sd":  "SD",  "sf":  "SF",  "col": "COL",
    "stl": "STL", "chc": "CHC", "cin": "CIN", "pit": "PIT", "tex": "TEX",
    "bal": "BAL", "bos": "BOS", "tor": "TOR", "kc":  "KC",  "min": "MIN",
    "mia": "MIA", "wsh": "WSH", "ath": "ATH", "cws": "CWS", "az": "AZ",
}

PROP_HINT = re.compile(r"\b(over|under|\d+\.\d+\s*k|hits|total|team total|tt)\b", re.I)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def pull_finals(d):
    """Return {abbr: (own, opp, opp_abbr, state)} from `mlb_api.sh finals <date>`."""
    try:
        out = subprocess.run(["bash", MLB_API, "finals", d], capture_output=True,
                             text=True, timeout=30).stdout
    except Exception as e:  # noqa: BLE001
        print(f"⚠ could not run mlb_api.sh finals {d}: {e}", file=sys.stderr)
        return {}
    games = {}
    # lines like:  SF 18 - CHC 3   [Final]
    for ln in out.splitlines():
        m = re.match(r"\s*([A-Z]{2,3})\s+(\d+)\s*-\s*([A-Z]{2,3})\s+(\d+)\s*\[([^\]]+)\]", ln)
        if not m:
            continue
        a, as_, h, hs, state = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), m.group(5)
        games[a] = (as_, hs, h, state)
        games[h] = (hs, as_, a, state)
    return games, out


def md_date(d):
    """YYYY-MM-DD -> M/D (no leading zeros), matching the ledger's Date format."""
    y, m, day = d.split("-")
    return f"{int(m)}/{int(day)}"


def find_team(text):
    low = text.lower()
    for nick in NICK_ORDER:
        if nick in low:
            return NICK[nick], nick
    # Fall back to a whole-word abbreviation match (e.g. "LAD ML", "TB ML").
    for abbr, full_abbr in ABBREV.items():
        if re.search(rf"\b{re.escape(abbr)}\b", low):
            return full_abbr, abbr.upper()
    return None, None


def main():
    argv = [a for a in sys.argv[1:]]
    d = argv[0] if argv and re.match(r"\d{4}-\d{2}-\d{2}", argv[0]) else \
        (date.today() - timedelta(days=1)).isoformat()
    ledger = next((a for a in argv if a.endswith(".md")), DEFAULT_LEDGER)

    res = pull_finals(d)
    if not res:
        print(f"No finals parsed for {d} (API blocked, or no games). Nothing to propose.")
        return
    games, raw = res

    print("=" * 62)
    print(f"  SETTLE PROPOSALS for {d}  (read-only — apply these by hand)")
    print("=" * 62)
    print("\n-- finals (mlb_api.sh) --")
    print(raw.rstrip())

    target = md_date(d)
    with open(ledger, encoding="utf-8") as fh:
        lines = fh.readlines()

    proposals = []
    for ln in lines:
        if not ln.lstrip().startswith("|"):
            continue
        c = cells(ln)
        if len(c) < 8 or not c[0].startswith(target):
            continue
        leg, result = c[1], c[7]
        if "tbd" not in result.lower():
            continue
        if PROP_HINT.search(leg):
            proposals.append((leg, "MANUAL", "prop / total / K-leg — a score can't settle it"))
            continue
        abbr, nick = find_team(leg)
        if not abbr or abbr not in games:
            proposals.append((leg, "??", "team not matched to a final — check manually"))
            continue
        own, opp, opp_abbr, state = games[abbr]
        if not state.lower().startswith("final"):
            proposals.append((leg, "—", f"game not Final yet (state={state})"))
            continue
        verdict = "W" if own > opp else ("L" if own < opp else "Push")
        proposals.append((leg, verdict, f"{abbr} {own}-{opp} {opp_abbr} ({state})"))

    print(f"\n-- open (TBD) legs dated {target} --")
    if not proposals:
        print("   (none — nothing dated today is still TBD)")
    else:
        for leg, verdict, why in proposals:
            tag = {"W": "✅ W", "L": "❌ L", "Push": "➖ Push"}.get(verdict, f"⚠ {verdict}")
            print(f"   {tag:<8} {leg[:60]:<60}  {why}")
        print("\n   → apply: set Result, flip Played=Y where the user bet it, then re-run calib.py.")
        print("   → also settle fades.md / bankroll.md / the parlay file in the same cycle.")
    print("=" * 62)


if __name__ == "__main__":
    main()
