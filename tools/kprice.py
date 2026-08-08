#!/usr/bin/env python3
"""kprice.py — one-shot K-prop pricing: a pitcher's strikeout lines, every book, devigged.

WHY THIS EXISTS
    Two standing doctrine rules need real prop prices: "never estimate alt prices — books
    juice the one-K-lower alt to -300/-500 on elite arms" (burn 5/26 Burns: est -185,
    actual ~-400, ticket paid +103 not +221), and "whenever a K-Over is faded, price the
    K-UNDER". Doing that by hand means: find the event, pull the props market, eyeball the
    best price per side per line, devig each. This does it in one command on the paid tier
    (~2 credits): resolve the pitcher → today's game (probables snapshot) → the odds event,
    fetch pitcher_strikeouts + pitcher_strikeouts_alternate, and print best-price-per-side
    PER LINE with the no-vig split — paste-ready for truep.py / ticket.py.

QUOTA
    Costs ~1 credit per market (2 with alternates). REFUSES to spend when the API reports
    <1000 credits remaining (free tier / tier not yet propagated) unless --force — the free
    500/mo is reserved for the slate cache + CLV. `events` and `quota` calls are free.

USAGE
    tools/kprice.py Gilbert                     # today's slate, both K markets
    tools/kprice.py "Sánchez" 2026-07-30        # accent-insensitive surname match
    tools/kprice.py Gilbert --standard-only     # 1 credit (skip the alternate market)
    tools/kprice.py Gilbert --event <eventId>   # explicit event (doubleheaders)
"""
import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import date, datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ODDS_API = os.path.join(HERE, "odds_api.sh")
SNAP_DIR = os.path.join(HERE, "..", "parlays", ".probables")

MIN_CREDITS = 1000   # refuse prop spends below this (free tier = 500/mo territory)


def _ascii(s):
    s = unicodedata.normalize("NFD", s or "")
    return "".join(ch for ch in s if not unicodedata.combining(ch)).lower()


def _sh(args, timeout=45):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout).stdout


def imp(price):
    p = float(price)
    return 100.0 / (p + 100.0) if p > 0 else (-p) / ((-p) + 100.0)


def quota_remaining():
    """Free call. None if unparseable (treat as not-enough)."""
    out = _sh(["bash", ODDS_API, "quota"])
    m = re.search(r"remaining:\s*([\d,]+)", out)
    return int(m.group(1).replace(",", "")) if m else None


def find_pitcher_game(d, surname):
    """(game_dict, side, full_name) from the probables snapshot (or live pull).
    Exactly one accent-insensitive surname match required."""
    snap = os.path.join(SNAP_DIR, f"{d}.json")
    games = None
    if os.path.exists(snap):
        with open(snap, encoding="utf-8") as fh:
            games = json.load(fh)
    if games is None:
        import recheck
        games = recheck.pull_games(d)
    want = _ascii(surname)
    hits = []
    for g in games:
        for side in ("away", "home"):
            nm = g.get(f"{side}_sp") or ""
            if want and want in _ascii(nm):
                hits.append((g, side, nm))
    if len(hits) != 1:
        names = ", ".join(f"{n} ({g[s]})" for g, s, n in hits) or "none"
        raise SystemExit(f"pitcher {surname!r} matched {len(hits)} probables on {d}: {names} "
                         f"— use a more specific name")
    return hits[0]


def event_id_for_team(d, team_name):
    """Odds event id whose matchup contains team_name. CACHE-FIRST: the slate cache's
    game objects carry the event id (0 credits, and it survives the /events feed's
    habit of dropping same-day games mid-slate); the free /events call is the fallback.
    Doubleheader (2 matches) → SystemExit listing the ids."""
    want = _ascii(team_name)
    ids = []
    cf = os.path.join(os.environ.get("TMPDIR", "/tmp"), "odds_cache", f"slate_{d}.json")
    try:
        with open(cf, encoding="utf-8") as fh:
            for g in json.load(fh):
                names = f"{g.get('away_team', '')} {g.get('home_team', '')}"
                if g.get("id") and want and want in _ascii(names):
                    ids.append((g["id"], f"{g.get('away_team')} @ {g.get('home_team')}"))
    except Exception:  # noqa: BLE001 — no/bad cache → fall through to /events
        pass
    if not ids:
        out = _sh(["bash", ODDS_API, "events", d])
        rows = [ln.split(None, 1) for ln in out.splitlines() if ln.strip()]
        ids = [(r[0], r[1]) for r in rows if len(r) == 2 and want and want in _ascii(r[1])]
    if len(ids) == 1:
        return ids[0][0]
    if not ids:
        raise SystemExit(f"no odds event found for {team_name!r} on {d} "
                         f"(game live/finished, or feed mismatch)")
    listing = "\n  ".join(f"{i}  {m}" for i, m in ids)
    raise SystemExit(f"{len(ids)} events match {team_name!r} (doubleheader?) — "
                     f"re-run with --event <id>:\n  {listing}")


def event_commence(d, eid):
    """commence_time ISO-Z for an event id, from the cached slate; None if unknown."""
    cf = os.path.join(os.environ.get("TMPDIR", "/tmp"), "odds_cache", f"slate_{d}.json")
    try:
        with open(cf, encoding="utf-8") as fh:
            for g in json.load(fh):
                if g.get("id") == eid:
                    return g.get("commence_time")
    except Exception:  # noqa: BLE001 — no cache → unknown, caller decides
        pass
    return None


def started(commence_iso, now_iso=None):
    """True when first pitch has passed — the props feed then serves IN-GAME prices,
    which are not pre-game lines (audit 8/7/26: the 16:00 sweep priced 13:35 games
    mid-start). ISO-Z strings compare lexically. Unknown commence → False (can't gate)."""
    if not commence_iso:
        return False
    now_iso = now_iso or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return commence_iso <= now_iso


def fetch_event_props(event_id, markets):
    """Raw event-odds JSON for the given prop market keys (~1 credit per market)."""
    path = (f"sports/baseball_mlb/events/{event_id}/odds"
            f"?regions=us&markets={markets}&oddsFormat=american&dateFormat=iso")
    raw = _sh(["bash", ODDS_API, "raw", path])
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise SystemExit(f"unparseable props response: {raw[:200]}")
    if isinstance(data, dict) and data.get("error_code") == "EVENT_NOT_FOUND":
        raise SystemExit("event id expired — the provider rolled its pre-match feed "
                         "(ids rotate; same-day games can drop temporarily). Re-warm the "
                         f"slate cache (rm the slate_*.json + odds_api.sh slate) and retry.")
    if isinstance(data, dict) and data.get("error_code"):
        raise SystemExit(f"props fetch error: {data.get('error_code')} — {data.get('message', '')[:120]}")
    return data


def best_by_point(event_json, surname, market_prefix="pitcher_strikeouts"):
    """{point: {'Over': (price, book), 'Under': (price, book)}} for the named player,
    best price per side per line across all books whose market key starts with
    market_prefix (default: both K markets; pass e.g. 'batter_total_bases' for hitter
    props). Pure — selftested."""
    want = _ascii(surname)
    table = {}
    names = set()
    for bk in (event_json or {}).get("bookmakers", []):
        book = bk.get("title", "?")
        for mkt in bk.get("markets", []):
            if not str(mkt.get("key", "")).startswith(market_prefix):
                continue
            for o in mkt.get("outcomes", []):
                desc = o.get("description", "")
                if want not in _ascii(desc):
                    continue
                names.add(desc)
                side, pt, pr = o.get("name"), o.get("point"), o.get("price")
                if side not in ("Over", "Under") or pt is None or pr is None:
                    continue
                cur = table.setdefault(pt, {})
                if side not in cur or pr > cur[side][0]:
                    cur[side] = (pr, book)
    # Same-surname ambiguity (both Contrerases in one game) would merge two players'
    # prices into one chimera table — refuse instead; caller passes a fuller name (audit 8/1).
    if len(names) > 1:
        return {}
    return table


def novig_at_point(entry):
    """entry = {'Over':(price,book), 'Under':(price,book)} → (over_novig, under_novig)
    or None if one-sided. Pure."""
    if "Over" not in entry or "Under" not in entry:
        return None
    io, iu = imp(entry["Over"][0]), imp(entry["Under"][0])
    s = io + iu
    return io / s, iu / s


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pitcher", help="pitcher surname (accent-insensitive)")
    ap.add_argument("date", nargs="?", default=date.today().isoformat(),
                    help="YYYY-MM-DD (default today)")
    ap.add_argument("--event", help="explicit odds event id (doubleheaders)")
    ap.add_argument("--standard-only", action="store_true",
                    help="fetch pitcher_strikeouts only (1 credit, no alternates)")
    ap.add_argument("--force", action="store_true",
                    help="spend credits even below the 1000-remaining guard")
    args = ap.parse_args()
    if not re.match(r"\d{4}-\d{2}-\d{2}$", args.date):
        ap.error(f"bad date {args.date!r}")

    rem = quota_remaining()
    markets = ("pitcher_strikeouts" if args.standard_only
               else "pitcher_strikeouts,pitcher_strikeouts_alternate")
    ncred = 1 if args.standard_only else 2
    if not args.force and (rem is None or rem < MIN_CREDITS):
        raise SystemExit(
            f"⛔ REFUSING to spend ~{ncred} credit(s): API reports {rem} remaining "
            f"(<{MIN_CREDITS} = free tier / paid tier not yet propagated).\n"
            f"   Props auto-unlock when the 20K tier shows up (session_start flips "
            f"ODDS_MODE=rich at ≥5000). Hand-price from a book meanwhile, or --force.")

    game, side, full_name = find_pitcher_game(args.date, args.pitcher)
    team = game[side]
    opp = game["home" if side == "away" else "away"]
    eid = args.event or event_id_for_team(args.date, team)
    if not args.force and started(event_commence(args.date, eid)):
        raise SystemExit(
            f"⛔ {team} @/vs {opp} has already started — the props feed now serves "
            f"IN-GAME prices, not pre-game lines. Refusing to spend {ncred} credit(s) "
            f"on numbers that can't be bet pre-game (--force to override for research).")
    print(f"{full_name} ({team}, {'@' if side == 'away' else 'vs'} {opp}) — "
          f"event {eid}, markets: {markets} (~{ncred} credits, {rem} remaining)")

    data = fetch_event_props(eid, markets)
    table = best_by_point(data, args.pitcher)
    if not table:
        raise SystemExit("no K-prop outcomes for this pitcher in the response "
                         "(market not posted yet, tier lacks props, or TWO players share "
                         "the surname — pass a fuller name, e.g. 'Willson Contreras')")

    # "standard" heuristic: the line with both sides + the most balanced juice
    def balance(pt):
        nv = novig_at_point(table[pt])
        return abs(nv[0] - 0.5) if nv else 9
    two_sided = [pt for pt in table if novig_at_point(table[pt])]
    std = min(two_sided, key=balance) if two_sided else None

    print("─" * 74)
    print(f"{'line':>6}  {'best Over':>16}  {'best Under':>16}  {'no-vig O%':>9}  {'no-vig U%':>9}")
    for pt in sorted(table):
        e = table[pt]
        o = f"{e['Over'][0]:+.0f} @{e['Over'][1]}" if "Over" in e else "—"
        u = f"{e['Under'][0]:+.0f} @{e['Under'][1]}" if "Under" in e else "—"
        nv = novig_at_point(e)
        no = f"{nv[0]*100:.1f}%" if nv else "one-sided"
        nu = f"{nv[1]*100:.1f}%" if nv else ""
        tag = ""
        if std is not None and pt == std:
            tag = "  ← STANDARD"
        elif std is not None and abs(pt - (std - 1)) < 1e-9:
            tag = "  ← one-lower alt (check the juice before 'safer')"
        print(f"{pt:>6g}  {o:>16}  {u:>16}  {no:>9}  {nu:>9}{tag}")
    print("─" * 74)
    print("Feed the chosen line into truep.py (baseline = its no-vig side) and ticket.py")
    print("(TrueP:price:game). Doctrine: a juiced one-lower alt can beat the 'safer' story —")
    print("price it, don't assume it (burn 5/26 Burns -185est/-400actual).")


if __name__ == "__main__":
    main()
