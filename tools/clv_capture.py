#!/usr/bin/env python3
"""clv_capture.py — batch CLV capture for all open (TBD) legs in results_log.md.

WHY THIS EXISTS
    The CLV column is the primary scoreboard (converges far faster than ROI at this sample),
    but it requires a near-first-pitch price snapshot for every open leg. Originally this
    shelled out to `odds_api.sh clv` per ML leg (1 credit each) and flagged everything else
    MANUAL. Now it reads the CACHED slate (warmed by session_start.sh at the start of the
    16:00/18:00 runs — i.e. near first pitch) directly, which covers THREE markets at ZERO
    extra credits: ML (h2h), GAME TOTALS, and RUN LINES (spreads). K/hitter props and team
    totals are not in the cached feed and stay MANUAL.

    It also prints an ⚠ EDGE-GONE warning when the closing no-vig has moved past the row's
    pre-registered TrueP (or within the +2pp gate) — a leg whose edge evaporated at the
    close should NOT be (re)bet, which makes this a pre-lock decision aid, not just a
    ledger-measurement step.

USAGE
    tools/clv_capture.py                              # targets today's date (read-only proposals)
    tools/clv_capture.py 2026-06-06                   # target a specific date
    tools/clv_capture.py --apply                      # WRITE the verdict into the CLV column in-place
    tools/clv_capture.py --apply 2026-06-06 path/to/results_log.md

CLV FILL KEY
    +   closing no-vig ImplP > bet no-vig ImplP  (line moved TO our side — good)
    −   closing no-vig ImplP < bet no-vig ImplP  (line moved against us — bad)
    =   flat (±0.5pp dead-band)

--apply MODE
    Computes the verdict (closing no-vig vs the row's logged no-vig ImplP, ±0.5pp dead-band)
    and rewrites ONLY the CLV cell of each matched row, preserving every other cell exactly.
    Captures bet-OR-recommended legs (no Played=Y gate) per doctrine. Idempotent: rows whose
    CLV is already filled are skipped, so re-running spends no quota. Covered: ML + game
    totals + run lines (cached slate). MANUAL: K/hitter props, team totals, parlay tickets.
"""
import json
import os
import re
import subprocess
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ODDS_API = os.path.join(HERE, "odds_api.sh")
DEFAULT_LEDGER = os.path.join(HERE, "..", "results_log.md")
CACHE_DIR = os.path.join(os.environ.get("TMPDIR", "/tmp"), "odds_cache")

# Shared with settle.py — longer nicknames first so "white sox" matches before bare "sox".
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
NICK_ORDER = sorted(NICK, key=len, reverse=True)
ABBR2NICK = {}
for _n, _a in NICK.items():          # first nickname per abbr wins (dupes like AZ are aliases)
    ABBR2NICK.setdefault(_a, _n)

# Abbreviations that may appear literally in leg text (e.g. "TB ML", "LAD ML").
# Checked as whole-word matches (\bABBR\b) AFTER NICK fails, to avoid false substring hits.
ABBREV = {
    "lad": "LAD", "laa": "LAA", "nyy": "NYY", "nym": "NYM", "sea": "SEA",
    "tb":  "TB",  "det": "DET", "cle": "CLE", "hou": "HOU", "atl": "ATL",
    "phi": "PHI", "mil": "MIL", "sd":  "SD",  "sf":  "SF",  "col": "COL",
    "stl": "STL", "chc": "CHC", "cin": "CIN", "pit": "PIT", "tex": "TEX",
    "bal": "BAL", "bos": "BOS", "tor": "TOR", "kc":  "KC",  "min": "MIN",
    "mia": "MIA", "wsh": "WSH", "ath": "ATH", "cws": "CWS", "az": "AZ",
}


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep_or_header(c):
    joined = "".join(c)
    if joined and set(joined) <= set("-: "):
        return True
    return bool(c) and c[0].lower() == "date"


def table_rows_from_sections(text, *header_substrs):
    """Yield (section_label, cell_list, raw_line) for every data row in any named section."""
    rows = []
    in_sec = False
    cur_label = ""
    for ln in text.splitlines():
        matched = next((h for h in header_substrs if h in ln), None)
        if matched:
            in_sec = True
            cur_label = matched
            continue
        if in_sec and ln.lstrip().startswith("#") and not any(h in ln for h in header_substrs):
            in_sec = False
            cur_label = ""
            continue
        if in_sec and re.match(r"^\s*\|", ln):
            c = cells(ln)
            if c and not is_sep_or_header(c):
                rows.append((cur_label, c, ln))
    return rows


def _pct(s):
    """Parse a percentage like '61.7%' or '~64%*' → float 61.7, or None."""
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", s or "")
    return float(m.group(1)) if m else None


def imp(price):
    """American price → implied probability (with vig)."""
    p = float(price)
    return 100.0 / (p + 100.0) if p > 0 else (-p) / ((-p) + 100.0)


# ── leg classification (which closing market settles this leg's CLV) ──────────

def classify_leg(leg, typ):
    """→ (kind, info): kind ∈ h2h | totals | spreads | manual | skip.
    totals info = ('Over'|'Under', point); spreads info = signed point (e.g. -1.5)."""
    t = (typ or "").lower()
    l = (leg or "").lower().replace("−", "-")
    if "parlay" in t or "×" in (leg or ""):
        return "skip", "parlay ticket — no single closing line"
    if (re.search(r"k-over|k-under|hitter|prop", t)
            or re.search(r"\d+(?:\.\d+)?\s*k\b", l)
            or "hits" in l or "team total" in l or re.search(r"\btt\b", l)):
        return "manual", "K/hitter prop or team total — not in the cached slate feed"
    if "total" in t or re.search(r"\b(over|under)\s+\d", l):
        m = re.search(r"\b(over|under)\s+(\d+(?:\.\d+)?)", l)
        if m:
            return "totals", (m.group(1).capitalize(), float(m.group(2)))
        return "manual", "total leg without a parseable Over/Under <point>"
    if "run line" in t or re.fullmatch(r"rl", t) or re.search(r"[+-](?:1|2)\.5\b", l):
        m = re.search(r"([+-])((?:1|2)\.5)\b", l)
        if m:
            return "spreads", float(m.group(1) + m.group(2))
        return "manual", "run-line leg without a parseable ±point"
    if "ml" in t:
        return "h2h", None
    return "manual", f"unrecognized leg type {typ!r}"


def find_team(text):
    """The team the leg is ON — the EARLIEST team mention in the text (ledger convention
    writes the bet side first: 'BAL ML (@ DET)' is a BAL leg). Position-based, not
    dict-order — dict-order bound 'BAL … (@ DET)' to DET and would capture the WRONG
    side's closing line (side-flip bug, 7/30)."""
    low = text.lower()
    best = None  # (pos, abbr, nickname)
    for nick in NICK_ORDER:
        p = low.find(nick)
        if p >= 0 and (best is None or p < best[0]):
            best = (p, NICK[nick], nick)
    for abbr, full_abbr in ABBREV.items():
        m = re.search(rf"\b{re.escape(abbr)}\b", low)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), full_abbr, ABBR2NICK.get(full_abbr, abbr))
    return (best[1], best[2]) if best else (None, None)


# ── cached-slate closing computation (0 credits) ──────────────────────────────

def load_cached_slate(d, allow_warm=True):
    """The slate cache session_start warms at run start (= near first pitch for 16/18 runs).
    Missing + allow_warm → one `slate` call (3 credits) rebuilds it; else None."""
    p = os.path.join(CACHE_DIR, f"slate_{d}.json")
    if not os.path.exists(p) and allow_warm:
        try:
            subprocess.run(["bash", ODDS_API, "slate", d], capture_output=True,
                           text=True, timeout=45)
        except Exception:  # noqa: BLE001
            return None
    if not os.path.exists(p):
        return None
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:  # noqa: BLE001
        return None


def match_game(slate, nick):
    """The one game whose team names contain the nickname; None if 0 or >1 (doubleheader)."""
    hits = [g for g in (slate or [])
            if nick and nick in f"{g.get('away_team', '')} {g.get('home_team', '')}".lower()]
    return hits[0] if len(hits) == 1 else None


def close_novig(game, kind, info, nick):
    """Closing no-vig prob (0-1) for OUR side of the leg from one cached game, or
    (None, reason). Pure over the parsed JSON — selftest-able."""
    if not game:
        return None, "game not matched in the cached slate"
    # Collect (name, point, price) per market across books
    outs = []
    for bk in game.get("bookmakers", []):
        for mkt in bk.get("markets", []):
            if mkt.get("key") != kind:
                continue
            for o in mkt.get("outcomes", []):
                outs.append((o.get("name", ""), o.get("point"), o.get("price")))
    if not outs:
        return None, f"no {kind} prices in the cached feed for this game"

    if kind == "h2h":
        def side_of(name):
            return nick in name.lower()
        pool = [(n, p) for n, _, p in outs if p is not None]
    elif kind == "totals":
        side, point = info
        pool = [(n, p) for n, pt, p in outs
                if p is not None and pt is not None and abs(pt - point) < 1e-9]
        if not pool:
            pts = sorted({pt for _, pt, _ in outs if pt is not None})
            return None, (f"closing board no longer quotes total {point:g} "
                          f"(available: {', '.join(f'{x:g}' for x in pts)}) — the NUMBER moved; "
                          f"pull the {point:g} close by hand (a moved total is itself information)")

        def side_of(name):
            return name.lower() == side.lower()
    else:  # spreads
        point = info
        pool = [(n, p) for n, pt, p in outs
                if p is not None and pt is not None and abs(abs(pt) - abs(point)) < 1e-9]
        if not pool:
            return None, f"closing board no longer quotes the ±{abs(point):g} run line"
        my_names = [n for n, pt, p in outs
                    if pt is not None and abs(pt - point) < 1e-9 and nick in n.lower()]
        if not my_names:
            return None, f"our team @{point:+g} not on the closing run-line board"

        def side_of(name):
            return name in my_names

    best = {}
    for n, p in pool:
        if n not in best or p > best[n]:
            best[n] = p
    if len(best) < 2:
        return None, "only one side priced at the close — can't devig"
    if any(abs(p) > 2000 for p in best.values()):
        return None, "implausible closing price (>|2000|) — game likely started/settled; skip"
    my = [n for n in best if side_of(n)]
    if len(my) != 1:
        return None, "couldn't isolate our side on the closing board"
    overround = sum(imp(p) for p in best.values())
    novig = imp(best[my[0]]) / overround
    if novig >= 0.95 or novig <= 0.05:
        return None, "closing no-vig implausible (≥95%/≤5%) — stale/settled feed; skip"
    return (novig, f"close best {my[0]} {best[my[0]]:+.0f} → no-vig {novig*100:.1f}%"), None


def verdict_from_close(closing_pct, bet_implp_cell):
    """'+ 64%cl' / '− 55%cl' / '= 60%cl' from a closing no-vig % vs the row's logged
    no-vig ImplP (±0.5pp dead-band). None if the row has no usable ImplP."""
    bet_novig = _pct(bet_implp_cell)
    if bet_novig is None or closing_pct is None:
        return None
    diff = closing_pct - bet_novig
    ch = "+" if diff > 0.5 else "−" if diff < -0.5 else "="
    return f"{ch} {int(round(closing_pct))}%cl"


def edge_warning(closing_pct, truep_cell):
    """Pre-lock decision aid: does the CLOSE leave any edge? None = no warning."""
    tp = _pct(truep_cell)
    if tp is None or closing_pct is None:
        return None
    if closing_pct >= tp:
        return (f"⚠ EDGE GONE at the close — closing no-vig {closing_pct:.1f}% ≥ TrueP "
                f"{tp:.0f}%; do NOT (re)bet this leg at the current number")
    if closing_pct > tp - 2:
        return (f"⚠ edge at the close is under the +2pp gate "
                f"({tp - closing_pct:+.1f}pp) — action, not value, at the current number")
    return None


# ── legacy per-leg fallback (odds_api.sh clv — costs 1 credit; used only w/o cache) ──

def verdict_from_clv_output(out, bet_implp_cell):
    """Derive the CLV cell string from cmd_clv stdout + the row's logged no-vig ImplP."""
    if not out:
        return None
    pm = re.search(r"Close best.*?:\s*([+-]?\d+)\s", out)
    if pm and abs(int(pm.group(1))) > 2000:
        return None
    m = re.search(r"no-vig\s+(\d+(?:\.\d+)?)\s*%", out)
    closing = float(m.group(1)) if m else None
    if closing is not None and (closing >= 95 or closing <= 5):
        return None
    v = verdict_from_close(closing, bet_implp_cell)
    if v:
        return v
    if "moved TO your side" in out:
        return f"+ {int(round(closing))}%cl" if closing is not None else "+"
    if "moved against you" in out:
        return f"− {int(round(closing))}%cl" if closing is not None else "−"
    return None


def clean_price(raw):
    return re.sub(r"[~≈≈\s]", "", raw).strip()


def run_clv(price_str, team_nick, target_date):
    p = clean_price(price_str)
    if not re.match(r"^[+-]?\d+$", p):
        return None, f"price {price_str!r} is not a parseable American odds value"
    try:
        r = subprocess.run(["bash", ODDS_API, "clv", p, team_nick, target_date],
                           capture_output=True, text=True, timeout=30)
        return (r.stdout.strip() or None), (r.stderr.strip() or None)
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def apply_clv_to_cell(raw_line, new_clv):
    """Replace ONLY the CLV cell (pipe-index 10) of a ledger row, preserving all else."""
    parts = raw_line.split("|")
    # | Date | Leg | Type | Price | TrueP | ImplP | Edge | Result | Played | CLV | Bucket |
    #  0  1     2     3       4       5       6       7        8         9      10      11    12
    if len(parts) <= 11:
        return raw_line
    parts[10] = f" {new_clv} "
    return "|".join(parts)


def md_date(d_str):
    _, m, day = d_str.split("-")
    return f"{int(m)}/{int(day)}"


def main():
    argv = sys.argv[1:]
    apply_mode = "--apply" in argv
    argv = [a for a in argv if a != "--apply"]
    target_date = next((a for a in argv if re.match(r"\d{4}-\d{2}-\d{2}", a)),
                       date.today().isoformat())
    ledger = next((a for a in argv if a.endswith(".md")), DEFAULT_LEDGER)
    target_md = md_date(target_date)

    with open(ledger, encoding="utf-8") as fh:
        text = fh.read()

    all_rows = table_rows_from_sections(text, "## Played legs", "## Recommended but NOT played")

    # cols: 0=Date 1=Leg 2=Type 3=Price 4=TrueP 5=ImplP 6=Edge 7=Result 8=Played 9=CLV 10=Bucket
    open_legs = []
    for sec, c, raw in all_rows:
        if len(c) < 10:
            continue
        if not c[0].startswith(target_md):
            continue
        if "tbd" not in c[7].lower():
            continue
        clv = c[9].strip() if len(c) > 9 else "—"
        if clv not in ("—", "–", ""):
            continue
        open_legs.append((sec, c, raw))

    mode_lbl = "AUTO-WRITE (--apply)" if apply_mode else "read-only proposals"
    print("=" * 66)
    print(f"  CLV CAPTURE — {target_date}  ({mode_lbl})")
    print("=" * 66)

    if not open_legs:
        print(f"\n  No open TBD legs with missing CLV for {target_date}.")
        print("  Check: (a) date mismatch, (b) all legs settled, or (c) CLV already filled.")
        print("=" * 66)
        return

    slate = load_cached_slate(target_date)
    src = ("cached slate (0 credits — warmed by session_start near first pitch)"
           if slate else "NO cache — ML falls back to per-leg odds_api.sh clv (1 credit each)")
    print(f"\n  {len(open_legs)} open leg(s) to capture.  Closing source: {src}\n")

    # ── rich-tier PROP auto-close (paid 20K tier only; ~1 credit per event+market) ──
    # Covers K-props AND the hitter/pitcher counting props the 16:00 sweep surfaces
    # (hits / TB / HR / RBI / runs / H+R+RBI / hits-allowed). On the free tier this
    # never spends: gated on the API reporting ≥5000 remaining.
    import kprice
    from settle import HPROP as SETTLE_HPROP
    from settle import parse_hprop as settle_parse_hprop
    from settle import parse_kprop as settle_parse_kprop
    PROP_MARKET = {"hits": "batter_hits", "tb": "batter_total_bases",
                   "hr": "batter_home_runs", "rbi": "batter_rbis",
                   "runs": "batter_runs_scored", "hrr": "batter_hits_runs_rbis",
                   "hitsallowed": "pitcher_hits_allowed"}
    props_cache = {}
    quota_state = {"rich": None}

    def try_prop_close(leg_txt):
        """(closing_pct, desc) for a prop leg from the live props market, or (None, why)."""
        kp = settle_parse_kprop(leg_txt)
        if kp:
            surname, direction, point = kp
            market, unit = "pitcher_strikeouts", "K"
        else:
            hp = settle_parse_hprop(leg_txt)
            if not hp:
                return None, "prop / team total — not in the cached slate feed"
            surname, direction, point, statkey = hp
            market = PROP_MARKET.get(statkey)
            unit = statkey
            if not market:
                return None, f"no odds market mapped for {statkey!r} — pull by hand"
        if quota_state["rich"] is None:
            rem = kprice.quota_remaining()
            quota_state["rich"] = rem is not None and rem >= 5000
        if not quota_state["rich"]:
            return None, ("prop close needs the paid tier (API reports <5000 credits) — "
                          "pull the closing line by hand")
        # Team from the leg MINUS the prop phrase ("Over 1.5 TB" must not bind Tampa Bay)
        _, nick = find_team(SETTLE_HPROP.sub(" ", leg_txt))
        if not nick:
            return None, "no team in the leg text to resolve the odds event"
        try:
            eid = kprice.event_id_for_team(target_date, nick)
            ck = (eid, market)
            if ck not in props_cache:
                props_cache[ck] = kprice.fetch_event_props(eid, market)
            tbl = kprice.best_by_point(props_cache[ck], surname, market_prefix=market)
            entry = next((tbl[pt] for pt in tbl if abs(pt - point) < 1e-9), None)
            if not entry:
                return None, (f"closing {unit} board has no {point:g} line for {surname} "
                              f"(available: {', '.join(f'{p:g}' for p in sorted(tbl)) or 'none'})")
            nv = kprice.novig_at_point(entry)
            if nv is None:
                return None, f"one-sided {unit} close at {point:g} — can't devig"
            myp = nv[0] if direction == "Over" else nv[1]
            if myp >= 0.95 or myp <= 0.05:
                return None, f"implausible {unit} close (≥95%/≤5%) — stale/settled; skip"
            pr, book = entry[direction]
            return myp * 100, (f"close best {direction} {point:g} {unit} {pr:+.0f} @{book} "
                               f"→ no-vig {myp*100:.1f}%")
        except SystemExit as e:
            return None, str(e)
        except Exception as e:  # noqa: BLE001
            return None, f"prop close failed ({e})"

    edits = {}
    for sec, c, raw in open_legs:
        leg, typ, price, truep, implp = c[1], c[2], c[3], c[4], c[5] if len(c) > 5 else ""
        print(f"── {leg}  [{typ}]  price: {price}")

        kind, info = classify_leg(leg, typ)
        if kind == "skip":
            print(f"   ⚠ SKIP — {info}\n")
            continue
        if kind == "manual":
            closing_pct, desc = try_prop_close(leg)
            if closing_pct is None:
                print(f"   ⚠ MANUAL — {desc}")
                print("     CLV fill key: + (closed in your favor) | − (moved against) | = (flat)\n")
                continue
            print(f"   {desc}  [K-prop, live props feed]")
            verdict = verdict_from_close(closing_pct, implp)
            warn = edge_warning(closing_pct, truep)
            if warn:
                print(f"   {warn}")
            if verdict:
                print(f"   → CLV verdict: {verdict}")
                if apply_mode:
                    edits[raw] = verdict
            elif apply_mode:
                print("   (could not derive a verdict to write — left as —)")
            print()
            continue

        team_abbr, team_nick = find_team(leg)
        if not team_nick:
            print("   ⚠ MANUAL — couldn't extract a team from the leg text.\n")
            continue

        verdict = None
        if slate is not None:
            game = match_game(slate, team_nick)
            got, err = close_novig(game, kind, info, team_nick)
            if err:
                print(f"   ⚠ MANUAL — {err}\n")
                continue
            novig, desc = got
            closing_pct = novig * 100
            print(f"   {desc}  [{kind}, cached]")
            verdict = verdict_from_close(closing_pct, implp)
            warn = edge_warning(closing_pct, truep)
            if warn:
                print(f"   {warn}")
        elif kind == "h2h":
            out, err = run_clv(price, team_nick, target_date)
            if err and not out:
                print(f"   ERROR: {err}\n")
                continue
            if out:
                for ln in out.splitlines():
                    print(f"   {ln}")
            verdict = verdict_from_clv_output(out, implp)
        else:
            print("   ⚠ MANUAL — no cache and non-ML; pull the closing number from a book.\n")
            continue

        if verdict:
            print(f"   → CLV verdict: {verdict}")
            if apply_mode:
                edits[raw] = verdict
        elif apply_mode:
            print("   (could not derive a verdict to write — left as —)")
        print()

    if apply_mode and edits:
        new_lines = []
        for ln in text.split("\n"):
            new_lines.append(apply_clv_to_cell(ln, edits[ln]) if ln in edits else ln)
        with open(ledger, "w", encoding="utf-8") as fh:
            fh.write("\n".join(new_lines))
        print(f"  ✓ APPLIED {len(edits)} CLV verdict(s) into {os.path.basename(ledger)}.")
        print("  → Re-run tools/calib.py to reconcile the rollup tables.")
    elif apply_mode:
        print("  (nothing to write — no leg produced a verdict.)")
    else:
        print("  → Apply: update CLV column (+/−/=) in results_log.md for each leg above,")
        print("    or re-run with --apply to write them automatically.")
        print("  → Then: re-run tools/calib.py to reconcile the rollup tables.")
    print("=" * 66)


if __name__ == "__main__":
    main()
