#!/usr/bin/env python3
"""clv_capture.py — batch CLV capture for all open (TBD) legs in results_log.md.

WHY THIS EXISTS
    The CLV column is the primary scoreboard (converges far faster than ROI at this sample),
    but it requires a near-first-pitch price snapshot for every open leg. Before odds_api.sh
    was live, this was a manual book-by-book pull — so the column stayed blank. Now it's
    automated: this reads every TBD + uncaptured-CLV row, calls `tools/odds_api.sh clv` for
    each ML leg, and prints copy-ready proposals so you can fill the CLV column in one pass.

    Run it on the 15:30 / 18:30 near-first-pitch run. Props / totals / K-legs are flagged
    MANUAL (need a hand price lookup — they're not in the h2h feed).

USAGE
    tools/clv_capture.py                              # targets today's date
    tools/clv_capture.py 2026-06-06                   # target a specific date
    tools/clv_capture.py 2026-06-06 path/to/results_log.md

CLV FILL KEY
    +   closing no-vig ImplP > bet no-vig ImplP  (line moved TO our side — good)
    −   closing no-vig ImplP < bet no-vig ImplP  (line moved against us — bad)
    =   flat (no meaningful move)
"""
import os
import re
import subprocess
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ODDS_API = os.path.join(HERE, "odds_api.sh")
DEFAULT_LEDGER = os.path.join(HERE, "..", "results_log.md")

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

PROP_HINT = re.compile(
    r"\b(over|under|\d+\.\d+\s*k|hits|total|team\s+total|tt|k-over|k-under|run\s+line|rl)\b", re.I
)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep_or_header(c):
    joined = "".join(c)
    if joined and set(joined) <= set("-: "):
        return True
    return bool(c) and c[0].lower() == "date"


def table_rows_from_sections(text, *header_substrs):
    """Yield (section_label, cell_list) for every data row in any named section."""
    rows = []
    in_sec = False
    cur_label = ""
    for ln in text.splitlines():
        # Entering a target section?
        matched = next((h for h in header_substrs if h in ln), None)
        if matched:
            in_sec = True
            cur_label = matched
            continue
        # Leaving (next heading that isn't a target section)?
        if in_sec and ln.lstrip().startswith("#") and not any(h in ln for h in header_substrs):
            in_sec = False
            cur_label = ""
            continue
        if in_sec and re.match(r"^\s*\|", ln):
            c = cells(ln)
            if c and not is_sep_or_header(c):
                rows.append((cur_label, c))
    return rows


def md_date(d_str):
    """YYYY-MM-DD → M/D (no leading zeros) matching the ledger's Date column."""
    _, m, day = d_str.split("-")
    return f"{int(m)}/{int(day)}"


def find_team(text):
    low = text.lower()
    for nick in NICK_ORDER:
        if nick in low:
            return NICK[nick], nick
    # Fall back to whole-word abbreviation match (e.g. "TB ML", "LAD ML")
    for abbr, full_abbr in ABBREV.items():
        if re.search(rf"\b{re.escape(abbr)}\b", low):
            return full_abbr, abbr.upper()
    return None, None


def clean_price(raw):
    """Strip tildes / approximation chars and return a bare American price string."""
    return re.sub(r"[~≈≈\s]", "", raw).strip()


def run_clv(price_str, team_nick, target_date):
    """Call odds_api.sh clv; return (stdout_text, error_string)."""
    p = clean_price(price_str)
    if not re.match(r"^[+-]?\d+$", p):
        return None, f"price {price_str!r} is not a parseable American odds value"
    try:
        r = subprocess.run(
            ["bash", ODDS_API, "clv", p, team_nick, target_date],
            capture_output=True, text=True, timeout=30,
        )
        return (r.stdout.strip() or None), (r.stderr.strip() or None)
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def main():
    argv = sys.argv[1:]
    target_date = next(
        (a for a in argv if re.match(r"\d{4}-\d{2}-\d{2}", a)),
        date.today().isoformat(),
    )
    ledger = next((a for a in argv if a.endswith(".md")), DEFAULT_LEDGER)
    target_md = md_date(target_date)

    with open(ledger, encoding="utf-8") as fh:
        text = fh.read()

    all_rows = table_rows_from_sections(
        text, "## Played legs", "## Recommended but NOT played"
    )

    # cols: 0=Date 1=Leg 2=Type 3=Price 4=TrueP 5=ImplP 6=Edge 7=Result 8=Played 9=CLV 10=Bucket
    open_legs = []
    for sec, c in all_rows:
        if len(c) < 10:
            continue
        if not c[0].startswith(target_md):
            continue
        result = c[7]
        clv = c[9].strip() if len(c) > 9 else "—"
        if "tbd" not in result.lower():
            continue
        if clv not in ("—", "–", ""):   # already captured — skip
            continue
        open_legs.append((sec, c))

    print("=" * 66)
    print(f"  CLV CAPTURE — {target_date}  (read-only: apply fills by hand)")
    print("=" * 66)

    if not open_legs:
        print(f"\n  No open TBD legs with missing CLV for {target_date}.")
        print("  Check: (a) date mismatch, (b) all legs settled, or (c) CLV already filled.")
        print("=" * 66)
        return

    print(f"\n  {len(open_legs)} open leg(s) to capture.  "
          f"Run closest to first pitch for the best closing-line read.\n")

    for sec, c in open_legs:
        leg   = c[1]
        typ   = c[2]
        price = c[3]
        label = f"[{typ}]" if typ else ""
        print(f"── {leg}  {label}  price: {price}")

        # Props / totals / non-ML legs: can't be automated with h2h feed
        if PROP_HINT.search(leg) or "ML" not in typ.upper():
            print("   ⚠ MANUAL — prop / total / run-line: pull closing price from a book.")
            print("     CLV fill key: + (closed in your favor) | − (moved against) | = (flat)")
            print()
            continue

        team_abbr, team_nick = find_team(leg)
        if not team_abbr:
            print("   ⚠ MANUAL — couldn't extract team name from leg text.")
            print(f"     Try: tools/odds_api.sh clv {clean_price(price)} \"<team>\" {target_date}")
            print()
            continue

        print(f"   team matched: {team_nick!r} ({team_abbr}) — calling odds_api.sh clv …")
        out, err = run_clv(price, team_nick, target_date)
        if err and not out:
            print(f"   ERROR: {err}")
            print(f"   Manual: tools/odds_api.sh clv {clean_price(price)} \"{team_nick}\" {target_date}")
        else:
            if err:
                print(f"   (stderr: {err})")
            if out:
                for ln in out.splitlines():
                    print(f"   {ln}")
        print()

    print("  → Apply: update CLV column (+/−/=) in results_log.md for each leg above.")
    print("  → Then: re-run tools/calib.py to reconcile the rollup tables.")
    print("=" * 66)


if __name__ == "__main__":
    main()
