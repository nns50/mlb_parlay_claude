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


# Hitter/pitcher counting props: "Ohtani Over 1.5 TB", "Judge O0.5 HR", "Soto U1.5 hits",
# "Kochanowicz Over 5.5 hits allowed", "Ohtani Over 2.5 H+R+RBI". Alternation order matters:
# 'hits allowed' before 'hits', 'hrr'/'h+r+rbi' before 'hr'.
HPROP = re.compile(
    r"([^\s|]+)\s+(Over|Under|O(?=\d)|U(?=\d))\s*(\d+(?:\.\d+)?)\s*"
    r"(hits\s+allowed|earned\s+runs?|stolen\s+bases?|total\s+bases|tb|"
    r"hits\+runs\+rbis?|h\+r\+rbi|hrr|home\s*runs?|hr|rbis?|runs(?:\s+scored)?|"
    r"walks?|doubles?|singles?|outs?|hits|sb|bb|er)\b", re.I)

_STAT_KEY = {"hits allowed": "hitsallowed", "total bases": "tb", "tb": "tb",
             "hits+runs+rbi": "hrr", "hits+runs+rbis": "hrr", "h+r+rbi": "hrr", "hrr": "hrr",
             "home run": "hr", "home runs": "hr", "hr": "hr",
             "rbi": "rbi", "rbis": "rbi", "runs": "runs", "run": "runs",
             "runs scored": "runs", "hits": "hits",
             "earned run": "er", "earned runs": "er", "er": "er",
             "stolen base": "sb", "stolen bases": "sb", "sb": "sb",
             "walk": "bb", "walks": "bb", "bb": "bb",
             "double": "doubles", "doubles": "doubles",
             "single": "singles", "singles": "singles",
             "out": "outs", "outs": "outs"}


def parse_hprop(text):
    """-> (surname, 'Over'|'Under', line, statkey) or None. Pure (selftest-able)."""
    m = HPROP.search(text or "")
    if not m:
        return None
    direction = "Over" if m.group(2).upper().startswith("O") else "Under"
    stat = re.sub(r"\s+", " ", m.group(4).lower().strip())
    key = _STAT_KEY.get(stat)
    if key is None:
        return None
    return m.group(1), direction, float(m.group(3)), key


def stat_from_box(batting, pitching, key):
    """Compute the prop stat from boxscore stat dicts (batting/pitching). Pure.
    TB = H + 2B + 2·3B + 3·HR; singles = H − 2B − 3B − HR; outs from pitching."""
    b = batting or {}
    p = pitching or {}
    if key in ("hitsallowed", "er", "outs"):
        return p.get({"hitsallowed": "hits", "er": "earnedRuns", "outs": "outs"}[key])
    if not b:
        return None
    if key == "tb":
        need = ("hits", "doubles", "triples", "homeRuns")
        if any(b.get(x) is None for x in need):
            return None
        return b["hits"] + b["doubles"] + 2 * b["triples"] + 3 * b["homeRuns"]
    if key == "singles":
        need = ("hits", "doubles", "triples", "homeRuns")
        if any(b.get(x) is None for x in need):
            return None
        return b["hits"] - b["doubles"] - b["triples"] - b["homeRuns"]
    if key == "hrr":
        if any(b.get(x) is None for x in ("hits", "runs", "rbi")):
            return None
        return b["hits"] + b["runs"] + b["rbi"]
    return b.get({"hits": "hits", "hr": "homeRuns", "rbi": "rbi", "runs": "runs",
                  "sb": "stolenBases", "bb": "baseOnBalls", "doubles": "doubles"}[key])


def prop_verdict(direction, line, val):
    """W/L/Push for a counting prop (integer lines can push). Pure."""
    if abs(val - line) < 1e-9:
        return "Push"
    return kprop_verdict(direction, line, val)


def spread_verdict(own, opp, point):
    """W/L/Push for a run line from OUR side's score + signed point (e.g. -1.5, +1.5).
    Pure. Fav -1.5 needs a 2+ margin; dog +1.5 survives a 1-run loss."""
    adj = own - opp + point
    if abs(adj) < 1e-9:
        return "Push"
    return "W" if adj > 0 else "L"


SPREAD_RX = re.compile(r"([+-])(\d+\.5)\b")
TOTAL_RX = re.compile(r"\b(Over|Under|O(?=\d)|U(?=\d))\s*(\d+(?:\.\d+)?)\b")


def propose_total(leg, games):
    """Settle a GAME total (away+home) OR a TEAM total (the named side's runs) off the
    final score. Both are fully deterministic — team totals were wrongly MANUAL before
    8/1/26. Returns (leg, verdict, why) or None if the leg isn't a total."""
    l = leg.lower()
    team_total = "team total" in l or bool(re.search(r"\btt\b", l))
    m = TOTAL_RX.search(leg)
    if not m:
        return None
    direction = "Over" if m.group(1).upper().startswith("O") else "Under"
    line = float(m.group(2))
    abbr, _ = find_team(leg)
    if not abbr or abbr not in games:
        return (leg, "MANUAL", "total: team not matched to a final — check manually")
    entry = resolve_game(leg, games[abbr])
    if entry is None:
        return (leg, "MANUAL", f"doubleheader — {len(games[abbr])} finals for {abbr}; "
                               f"add a G1/G2 hint to the leg or settle by hand")
    own, opp, opp_abbr, state = entry
    if not state.lower().startswith("final"):
        return (leg, "—", f"game not Final yet (state={state})")
    if team_total:
        return (leg, prop_verdict(direction, line, own),
                f"{abbr} TEAM total {own} vs {direction} {line:g} ({abbr} {own}-{opp} {opp_abbr})")
    total = own + opp
    return (leg, prop_verdict(direction, line, total),
            f"game total {total} vs {direction} {line:g} ({abbr} {own}-{opp} {opp_abbr})")


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


_SCHED_CACHE = {}
_BOX_CACHE = {}


def _schedule(d):
    """[{pk, names, state}] for the date (cached). names = 'away home' lowercase."""
    if d not in _SCHED_CACHE:
        import json
        out = _sh(["bash", MLB_API, "raw", f"schedule?sportId=1&date={d}"])
        games = []
        try:
            for day in json.loads(out).get("dates", []):
                for g in day.get("games", []):
                    games.append({
                        "pk": g.get("gamePk"),
                        "names": (g.get("teams", {}).get("away", {}).get("team", {}).get("name", "")
                                  + " "
                                  + g.get("teams", {}).get("home", {}).get("team", {}).get("name", "")).lower(),
                        "state": g.get("status", {}).get("abstractGameState", "?")})
        except Exception:  # noqa: BLE001
            pass
        _SCHED_CACHE[d] = games
    return _SCHED_CACHE[d]


def _boxscore(pk):
    if pk not in _BOX_CACHE:
        import json
        out = _sh(["bash", MLB_API, "raw", f"game/{pk}/boxscore"])
        try:
            _BOX_CACHE[pk] = json.loads(out)
        except Exception:  # noqa: BLE001
            _BOX_CACHE[pk] = {}
    return _BOX_CACHE[pk]


def propose_hprop(leg, d):
    """Settle a hitter/pitcher counting prop off the StatsAPI BOXSCORE (deterministic —
    extends the K-prop approach to the full prop universe: hits/TB/HR/RBI/runs/HRR/
    hits-allowed). Returns (leg, verdict, why) or None if the leg isn't such a prop."""
    parsed = parse_hprop(leg)
    if not parsed:
        return None
    surname, direction, line, key = parsed
    want = unicodedata.normalize("NFD", surname)
    want = "".join(ch for ch in want if not unicodedata.combining(ch)).lower()
    try:
        # Resolve the team from the leg MINUS the prop phrase — otherwise the stat token
        # collides with team abbrs ("Over 1.5 TB" would bind Tampa Bay).
        abbr, _tok = find_team(HPROP.sub(" ", leg))
        nickname = ABBR2NICK.get(abbr)          # full-name fragment for schedule matching
        cands = [g for g in _schedule(d)
                 if nickname and nickname in g["names"]] if nickname else list(_schedule(d))
        if not cands:
            return (leg, "MANUAL", f"prop: no {d} game matched the leg's team — settle by hand")
        if len(cands) > 1:                       # doubleheader — never guess which game
            m2 = GAME_HINT.search(leg)
            if m2 and int(m2.group(1)) - 1 < len(cands):
                cands = [cands[int(m2.group(1)) - 1]]
            else:
                return (leg, "MANUAL", f"prop: doubleheader ({len(cands)} games) — add a "
                                       f"G1/G2 hint to the leg or settle by hand")
        hits = []
        for g in cands:
            if not g["state"].lower().startswith("final"):
                return (leg, "—", f"game not Final yet (state={g['state']})")
            box = _boxscore(g["pk"])
            for side in ("away", "home"):
                for p in box.get("teams", {}).get(side, {}).get("players", {}).values():
                    nm = p.get("person", {}).get("fullName", "")
                    norm = unicodedata.normalize("NFD", nm)
                    norm = "".join(ch for ch in norm if not unicodedata.combining(ch)).lower()
                    if want and want in norm:
                        st = p.get("stats", {})
                        val = stat_from_box(st.get("batting"), st.get("pitching"), key)
                        if val is not None:
                            hits.append((nm, val))
        if len(hits) != 1:
            return (leg, "MANUAL", f"prop: {surname!r} matched {len(hits)} player-lines "
                                   f"in the boxscore — settle by hand")
        pname, val = hits[0]
        verdict = prop_verdict(direction, line, val)
        return (leg, verdict, f"{pname} {val} {key} vs {direction} {line:g} (boxscore {d})")
    except Exception as e:  # noqa: BLE001
        return (leg, "MANUAL", f"prop lookup failed ({e}) — settle by hand")


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
    # Each team maps to a LIST of finals (feed order = schedule order, G1 first) —
    # a doubleheader used to CLOBBER G1 with G2, silently settling a G1 leg off the
    # G2 score (7/29 ATL-NYM: the G1 loss read as a W). resolve_game() disambiguates.
    for ln in out.splitlines():
        m = re.match(r"\s*([A-Z]{2,3})\s+(\d+)\s*-\s*([A-Z]{2,3})\s+(\d+)\s*\[([^\]]+)\]", ln)
        if not m:
            continue
        a, as_, h, hs, state = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), m.group(5)
        games.setdefault(a, []).append((as_, hs, h, state))
        games.setdefault(h, []).append((hs, as_, a, state))
    return games, out


GAME_HINT = re.compile(r"\bG(?:ame)?\s*([12])\b", re.I)


def resolve_game(leg, entries):
    """Pick THE final for a leg from a team's finals that date. One game → it. Two
    (doubleheader) → only with an explicit G1/G2 hint in the leg text; else None
    (MANUAL — never guess which game of a DH a leg belongs to). Pure."""
    if not entries:
        return None
    if len(entries) == 1:
        return entries[0]
    m = GAME_HINT.search(leg or "")
    if m:
        idx = int(m.group(1)) - 1
        if idx < len(entries):
            return entries[idx]
    return None


def md_date(d):
    """YYYY-MM-DD -> M/D (no leading zeros), matching the ledger's Date format."""
    y, m, day = d.split("-")
    return f"{int(m)}/{int(day)}"


ABBR2NICK = {}
for _n, _a in NICK.items():          # first nickname per abbr wins (AZ aliases collapse)
    ABBR2NICK.setdefault(_a, _n)


def find_team(text):
    """The team the leg is ON — the EARLIEST team mention in the text (ledger convention
    writes the bet side first: 'BAL -1.5 RL (@ DET)' is a BAL leg). Position-based, not
    dict-order — dict-order silently bound 'BAL … (@ DET)' to DET (side-flip bug, 7/30)."""
    low = text.lower()
    best = None  # (pos, abbr, token)
    for nick in NICK_ORDER:
        p = low.find(nick)
        if p >= 0 and (best is None or p < best[0]):
            best = (p, NICK[nick], nick)
    for abbr, full_abbr in ABBREV.items():
        m = re.search(rf"\b{re.escape(abbr)}\b", low)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), full_abbr, abbr.upper())
    return (best[1], best[2]) if best else (None, None)


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
        # Hitter/pitcher counting props (hits/TB/HR/RBI/runs/HRR/hits-allowed) settle off
        # the boxscore; game totals stay MANUAL below (a team-total line needs the market).
        hp = propose_hprop(leg, d)
        if hp:
            proposals.append(hp)
            continue
        tot = propose_total(leg, games)
        if tot:
            proposals.append(tot)
            continue
        if PROP_HINT.search(leg):
            proposals.append((leg, "MANUAL", "prop / total — a score can't settle it"))
            continue
        abbr, nick = find_team(leg)
        if not abbr or abbr not in games:
            proposals.append((leg, "??", "team not matched to a final — check manually"))
            continue
        entry = resolve_game(leg, games[abbr])
        if entry is None:
            proposals.append((leg, "MANUAL", f"doubleheader — {len(games[abbr])} finals for "
                                             f"{abbr}; add a G1/G2 hint or settle by hand"))
            continue
        own, opp, opp_abbr, state = entry
        if not state.lower().startswith("final"):
            proposals.append((leg, "—", f"game not Final yet (state={state})"))
            continue
        # Run line / spread: settle by MARGIN, not W/L — a −1.5 fav that wins by 1 LOSES
        # the leg. (Latent mis-settle: these previously fell through to the ML branch.)
        sp = SPREAD_RX.search(leg.replace("−", "-"))
        if sp and re.search(r"\b(rl|run\s*line|spread)\b", leg, re.I):
            point = float(sp.group(1) + sp.group(2))
            verdict = spread_verdict(own, opp, point)
            proposals.append((leg, verdict,
                              f"{abbr} {own}-{opp} {opp_abbr} w/ {point:+g} → margin {own - opp:+d}"))
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
