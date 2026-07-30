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
       team-side bets (ML / run line / spread).
    4. K-props ("X Over 6.5 K" / "X O6.5K" / "X U4.5K") are settled off the pitcher's
       GAMELOG for that date (findpitcher → gamelog K count vs the line) — deterministic,
       which kills the mid-game/team-result mis-settle class (6/9 Burns, 6/16 Cease).
       Ambiguous names / no start that date → MANUAL. Other props/totals → MANUAL
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
import unicodedata
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

# K-prop leg text: "Gilbert Over 6.5 K", "Sánchez O7.5K", "Peterson U4.5K -110", ...
# Name = the token right before the Over/Under marker; O/U single letters are only
# accepted when glued to digits (so "O6.5K" parses but a stray capital O doesn't).
KPROP = re.compile(r"([^\s|]+)\s+(Over|Under|O(?=\d)|U(?=\d))\s*(\d+(?:\.\d+)?)\s*K\b")


def parse_kprop(text):
    """-> (surname, 'Over'|'Under', line) or None. Pure (selftest-able)."""
    m = KPROP.search(text)
    if not m:
        return None
    direction = "Over" if m.group(2).startswith("O") else "Under"
    return m.group(1), direction, float(m.group(3))


def kprop_verdict(direction, line, k):
    """W/L for a K-prop given the final K count. .5 lines can't push. Pure."""
    if direction == "Over":
        return "W" if k > line else "L"
    return "W" if k < line else "L"


_PITCHER_CACHE = {}


def _sh(args, timeout=30):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout).stdout


def propose_kprop(leg, d):
    """Resolve the K-prop's pitcher and settle off the gamelog (deterministic — kills the
    mid-game / team-result mis-settle class: 6/9 Burns, 6/16 Cease). Returns
    (leg, verdict, why) or None to fall back to MANUAL."""
    parsed = parse_kprop(leg)
    if not parsed:
        return None
    surname, direction, line = parsed
    # StatsAPI name search is accent-sensitive; the ledger writes "Sánchez" — query ASCII.
    query = unicodedata.normalize("NFD", surname)
    query = "".join(ch for ch in query if not unicodedata.combining(ch))
    season = d.split("-")[0]
    # Team abbrs mentioned in the leg text ("(SEA @ TEX)" / "(vs NYY)") — used to cross-check
    # the gamelog row's opponent, so a same-surname arm on another team can never match.
    leg_abbrs = {a for pat, a in ABBREV.items()
                 if re.search(rf"\b{re.escape(pat)}\b", leg.lower())}
    try:
        if query not in _PITCHER_CACHE:
            hits = [ln.split("\t") for ln in
                    _sh(["bash", MLB_API, "findpitcher", query]).splitlines() if "\t" in ln]
            # keep pitchers only (findpitcher's broad name search returns hitters too)
            _PITCHER_CACHE[query] = [h for h in hits if len(h) >= 3 and h[2].strip() == "P"]
        hits = _PITCHER_CACHE[query]
        if not hits:
            return (leg, "MANUAL", f"K-prop: no pitcher matched {surname!r} — resolve by hand")

        def k_on_date(pid):
            """(K, opponent) from the pitcher's gamelog on the settle date, else None."""
            for ln in _sh(["bash", MLB_API, "gamelog", pid, season]).splitlines():
                if not ln.strip().startswith(d):
                    continue
                parts = re.split(r"\s{2,}", ln.strip())
                if len(parts) >= 5:          # date  opponent  IP  ER  K  BB
                    return int(float(parts[-2])), parts[1].lower()
            return None

        # Common surnames (Miller, Gilbert…) match several pitchers — the settle DATE
        # disambiguates (who actually pitched that day), and the leg's team abbrs veto
        # a same-surname arm whose opponent doesn't appear in the leg text.
        cands = []
        for h in hits[:8]:
            got = k_on_date(h[0])
            if got is None:
                continue
            k, opp_txt = got
            if leg_abbrs:
                opp_abbr = next((NICK[nk] for nk in NICK_ORDER if nk in opp_txt), None)
                if opp_abbr is not None and opp_abbr not in leg_abbrs:
                    continue
            cands.append((h[0], h[1], k))
        if len(cands) != 1:
            return (leg, "MANUAL", f"K-prop: {surname!r} → {len(hits)} pitcher(s), "
                                   f"{len(cands)} matching an appearance on {d} — resolve by hand")
        pid, pname, k = cands[0]
        verdict = kprop_verdict(direction, line, k)
        return (leg, verdict, f"{pname} {k} K vs {direction} {line} (gamelog {d})")
    except Exception as e:  # noqa: BLE001 — proposal tool: degrade to MANUAL, never crash the settle
        return (leg, "MANUAL", f"K-prop lookup failed ({e}) — settle by hand")


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
        # K-props FIRST — compact notation ("Sánchez O7.5K") slips past PROP_HINT's \b and
        # used to fall through to the TEAM matcher, silently settling a prop off the team
        # result (the 6/16 Cease mis-flag class). parse_kprop handles both notations.
        kp = propose_kprop(leg, d)
        if kp:
            proposals.append(kp)
            continue
        if PROP_HINT.search(leg):
            proposals.append((leg, "MANUAL", "prop / total — a score can't settle it"))
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
