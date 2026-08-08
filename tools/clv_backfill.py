#!/usr/bin/env python3
"""clv_backfill.py — retro-fill blank CLV cells from The Odds API HISTORICAL snapshots.

WHY THIS EXISTS
  CLV is the doctrine's primary scoreboard AND the trigger for pulse's MARKET-SHADE,
  but the 16:00/18:00 capture runs can only close games whose first pitch is still
  ahead of them: an early slate (8/2: the whole board went live before capture armed
  → the day's five decided picks logged 0/5 closes) or a dropped run leaves holes
  forever. ~30% of decided rows were blank at the 8/7 audit — holes that bias the
  governor's own trigger. The paid tier's /historical endpoint serves full-board
  snapshots at 5-minute grain, so yesterday's close is retrievable at commence−2min
  for exactly the games the live runs missed.

COST (why plan mode is the default)
  A historical odds call bills 10 credits × markets × regions → h2h+totals+spreads
  @ us = 30 credits PER SNAPSHOT TIMESTAMP. Rows are grouped by first pitch, so one
  snapshot serves every game starting that minute; a typical backfill day is 3-8
  snapshots (90-240 credits). Gates: paid tier only (API must report ≥5000
  remaining), --max-credits ceiling (default 150), and plan mode spends nothing.

USAGE
  tools/clv_backfill.py 2026-08-02             # PLAN: rows, snapshots, exact cost
  tools/clv_backfill.py 2026-08-02 --apply     # spend + write verdicts into the ledger
  tools/clv_backfill.py 2026-08-02 --apply --max-credits 90

SCOPE v1: ML / game totals / run lines (the kinds close_novig prices from a board).
  Props are per-event on the historical API (10cr × event × market) — hand-pull those.
  Doubleheader teams are skipped MANUAL (no snapshot disambiguation without a G-hint).
  Verdicts are written in the standard clv_capture format plus a ' bf' provenance
  marker (pulse/calib read the leading sign, so the marker is invisible to them).
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clv_capture import (apply_clv_to_cell, classify_leg, close_novig, find_team,  # noqa: E402
                         match_game, md_date, table_rows_from_sections, verdict_from_close)

HERE = os.path.dirname(os.path.abspath(__file__))
ODDS_API = os.path.join(HERE, "odds_api.sh")
MLB_API = os.path.join(HERE, "mlb_api.sh")
LEDGER = os.path.join(HERE, "..", "results_log.md")
SNAP_COST = 30          # 10cr × 3 markets × 1 region, per the API's historical pricing
RICH_FLOOR = 5000       # only the paid tier may spend on backfills
BACKFILLABLE = ("h2h", "totals", "spreads")


def sh(args, timeout=90):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout).stdout


def quota_remaining():
    m = re.search(r"credits remaining:\s*(\d+)", sh(["bash", ODDS_API, "quota"], 30))
    return int(m.group(1)) if m else None


# ── pure helpers (selftest fixtures run these without the network) ────────────

def parse_sched(json_text):
    """StatsAPI schedule JSON → {full team name: [commence_iso, ...]} (DH = 2 entries)."""
    out = {}
    try:
        data = json.loads(json_text)
    except Exception:  # noqa: BLE001
        return out
    for day in data.get("dates", []):
        for g in day.get("games", []):
            iso = (g.get("gameDate") or "").replace(".000Z", "Z")
            if not iso:
                continue
            for side in ("away", "home"):
                nm = (((g.get("teams") or {}).get(side) or {}).get("team") or {}).get("name")
                if nm:
                    out.setdefault(nm, []).append(iso)
    return out


def snap_ts(commence_iso):
    """The snapshot to request for a game: commence − 2min, floored to the API's
    5-minute snapshot grain (flooring also groups same-minute starts onto one call)."""
    t = datetime.strptime(commence_iso, "%Y-%m-%dT%H:%M:%SZ") - timedelta(minutes=2)
    t -= timedelta(minutes=t.minute % 5, seconds=t.second)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def commence_for(nick, sched):
    """(commence_iso, why_not). Unique game only — a DH team is MANUAL by doctrine."""
    hits = [(nm, ts) for nm, tss in sched.items() if nick and nick in nm.lower() for ts in tss]
    if not hits:
        return None, f"no StatsAPI game for '{nick}' that date"
    if len({ts for _, ts in hits}) > 1:
        return None, "doubleheader — snapshot can't disambiguate without a G-hint; hand-pull"
    return hits[0][1], None


def target_rows(text, d):
    """Rows worth backfilling: exact date, blank CLV cell, a backfillable market kind.
    Returns [(sec, cells, raw, kind, info, nick, skip_reason)]."""
    tmd = md_date(d)
    out = []
    for sec, c, raw in table_rows_from_sections(text, "## Played legs",
                                                "## Recommended but NOT played"):
        if len(c) < 10 or c[0].strip() != tmd:
            continue
        clv = (c[9] if len(c) > 9 else "").strip()
        if clv not in ("—", "–", ""):
            continue                       # already has a verdict (or a manual note)
        kind, info = classify_leg(c[1], c[2])
        if kind not in BACKFILLABLE:
            out.append((sec, c, raw, kind, info, None,
                        "prop/ticket/status row — historical props are per-event; hand-pull"))
            continue
        _, nick = find_team(c[1])
        if not nick:
            out.append((sec, c, raw, kind, info, None, "no team resolved from the leg text"))
            continue
        out.append((sec, c, raw, kind, info, nick, None))
    return out


def parse_snapshot(json_text):
    """Historical response → (games_list, err). Shape: {timestamp, data:[games…]}."""
    try:
        js = json.loads(json_text)
    except Exception:  # noqa: BLE001
        return None, f"unparseable response: {json_text[:120]!r}"
    if isinstance(js, dict) and isinstance(js.get("data"), list):
        return js["data"], None
    if isinstance(js, dict) and js.get("message"):
        return None, f"API error: {js['message']}"
    return None, f"unexpected shape: {str(js)[:120]}"


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    argv = sys.argv[1:]
    apply_mode = "--apply" in argv
    max_credits = 150
    if "--max-credits" in argv:
        max_credits = int(argv[argv.index("--max-credits") + 1])
    pos = [a for a in argv if re.match(r"\d{4}-\d{2}-\d{2}$", a)]
    if not pos:
        raise SystemExit("usage: clv_backfill.py YYYY-MM-DD [--apply] [--max-credits N]")
    d = pos[0]

    with open(LEDGER, encoding="utf-8") as fh:
        text = fh.read()
    rows = target_rows(text, d)
    print("=" * 66)
    print(f"  CLV BACKFILL — {d}  ({'APPLY' if apply_mode else 'PLAN (no spend)'})")
    print("=" * 66)
    if not rows:
        print("  no blank-CLV rows for this date — nothing to backfill.")
        return

    sched = parse_sched(sh(["bash", MLB_API, "raw", f"schedule?sportId=1&date={d}"]))
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    groups, skips = {}, []
    for sec, c, raw, kind, info, nick, skip in rows:
        if skip:
            skips.append((c[1], skip))
            continue
        commence, why = commence_for(nick, sched)
        if why:
            skips.append((c[1], why))
            continue
        ts = snap_ts(commence)
        if ts >= now_iso:
            skips.append((c[1], "first pitch still ahead — tonight's live runs own this close"))
            continue
        groups.setdefault(ts, []).append((c, raw, kind, info, nick))

    cost = SNAP_COST * len(groups)
    print(f"  fillable rows: {sum(len(v) for v in groups.values())}  "
          f"across {len(groups)} snapshot(s) → cost {cost} credits "
          f"(cap {max_credits})")
    for leg, why in skips:
        print(f"   ⚠ MANUAL — {leg[:64]}: {why}")
    if not groups:
        return
    for ts, members in sorted(groups.items()):
        print(f"   snapshot {ts}: {', '.join(m[4] for m in members)}")

    if not apply_mode:
        print("  PLAN ONLY — rerun with --apply to spend and write.")
        return
    rem = quota_remaining()
    if rem is None or rem < RICH_FLOOR:
        raise SystemExit(f"⛔ refusing to spend: API reports {rem} remaining (<{RICH_FLOOR}).")
    if cost > max_credits:
        raise SystemExit(f"⛔ cost {cost} exceeds --max-credits {max_credits}; "
                         f"raise the cap explicitly or backfill fewer rows.")

    edits = {}
    for ts, members in sorted(groups.items()):
        path = (f"historical/sports/baseball_mlb/odds?regions=us"
                f"&markets=h2h,totals,spreads&oddsFormat=american&dateFormat=iso&date={ts}")
        games, err = parse_snapshot(sh(["bash", ODDS_API, "raw", path]))
        if err:
            print(f"   ⚠ snapshot {ts} failed — {err}")
            continue
        for c, raw, kind, info, nick in members:
            game = match_game(games, nick)
            got, cerr = close_novig(game, kind, info, nick)
            if cerr or got is None:
                print(f"   ⚠ MANUAL — {c[1][:56]}: {cerr or 'no close in snapshot'}")
                continue
            verdict = verdict_from_close(got[0] * 100, c[5] if len(c) > 5 else "")
            if verdict is None:
                print(f"   ⚠ MANUAL — {c[1][:56]}: logged ImplP unparseable")
                continue
            edits[raw] = f"{verdict} bf"
            print(f"   ✓ {c[1][:56]} → {verdict} bf   ({got[1]})")

    if edits:
        lines = text.splitlines(keepends=True)
        new_lines = [apply_clv_to_cell(ln, edits[ln]) if ln in edits else ln for ln in lines]
        with open(LEDGER, "w", encoding="utf-8") as fh:
            fh.writelines(new_lines)
        print(f"  WROTE {len(edits)} backfilled verdict(s) into results_log.md "
              f"(re-run calib.py + pulse.py to pick them up).")
    else:
        print("  nothing written — every fillable row failed to a MANUAL note.")


if __name__ == "__main__":
    main()
