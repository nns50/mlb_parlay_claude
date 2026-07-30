#!/usr/bin/env python3
"""recheck.py — pre-lock slate re-verify: catch SP scratches / status flips MECHANICALLY.

WHY THIS EXISTS
    Two whole burn classes (fades.md E3 carried-over/mis-attributed probables, E4 TBA starters —
    plus the 5/26 Lauer/Freeland and 5/27 Cole/Cameron burns) are "the starter I built the leg on
    is not the starter anymore, and nothing noticed." A scratched or swapped SP silently
    invalidates every K-leg AND every ML/total premised on that arm. This makes the check
    deterministic: the 11:00 build SNAPSHOTS the slate's probables (committed with the build as an
    audit record), and the 16:00/18:00 lock runs DIFF live StatsAPI state against the snapshot —
    any change screams before a leg is locked, not after it loses.

USAGE
    tools/recheck.py snap [YYYY-MM-DD]   # snapshot probables+status → parlays/.probables/<date>.json
    tools/recheck.py [YYYY-MM-DD]        # diff live state vs snapshot; ⚠/⛔ on changes; exit 1 if any
    tools/recheck.py --selftest          # offline fixture test of the diff logic (no network)

WHAT THE DIFF FLAGS
    ⛔ game started / final           → status gate: the leg can no longer be locked
    ⚠ probable CHANGED               → E3/E4: every leg built on the old arm is INVALID — re-run
                                        SP-freshness for the new arm or drop the leg
    ⚠ game vanished from the feed    → PPD/suspended — void the leg
    ℹ probable now posted (was TBA)  → the leg can graduate from PENDING (run SP-freshness first)
"""
import json
import os
import re
import subprocess
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
MLB_API = os.path.join(HERE, "mlb_api.sh")
SNAP_DIR = os.path.join(HERE, "..", "parlays", ".probables")


def pull_games(d):
    """Live schedule w/ probables via mlb_api.sh raw (StatsAPI). Returns list of game dicts."""
    path = f"schedule?sportId=1&date={d}&hydrate=probablePitcher"
    out = subprocess.run(["bash", MLB_API, "raw", path], capture_output=True,
                         text=True, timeout=30).stdout
    data = json.loads(out)
    games = []
    for day in data.get("dates", []):
        for g in day.get("games", []):
            row = {"pk": g.get("gamePk"), "state": g.get("status", {}).get("abstractGameState", "?"),
                   "detail": g.get("status", {}).get("detailedState", "?")}
            for side in ("away", "home"):
                t = g.get("teams", {}).get(side, {})
                row[side] = t.get("team", {}).get("name", "?")
                pp = t.get("probablePitcher") or {}
                row[f"{side}_sp_id"] = pp.get("id")
                row[f"{side}_sp"] = pp.get("fullName")
            games.append(row)
    return games


def diff_games(old, new):
    """Pure diff: list of (severity, message). severity ∈ {'⛔','⚠','ℹ'}."""
    out = []
    new_by_pk = {g["pk"]: g for g in new}
    for o in old:
        n = new_by_pk.get(o["pk"])
        label = f"{o['away']} @ {o['home']}"
        if n is None:
            out.append(("⚠", f"{label}: game GONE from the feed — PPD/suspended? Void dependent legs."))
            continue
        if o["state"] in ("Preview",) and n["state"] not in ("Preview",):
            out.append(("⛔", f"{label}: {n['state']} ({n['detail']}) — started/finished; "
                             f"status gate CLOSED, cannot lock."))
        for side in ("away", "home"):
            osp, nsp = o.get(f"{side}_sp_id"), n.get(f"{side}_sp_id")
            oname = o.get(f"{side}_sp") or "TBA"
            nname = n.get(f"{side}_sp") or "TBA"
            if osp and nsp and osp != nsp:
                out.append(("⚠", f"{label}: {side.upper()} SP CHANGED {oname} → {nname} — "
                                 f"E3 gate: every leg built on {oname} is INVALID (K-legs AND "
                                 f"ML/total premised on that arm). Re-run SP-freshness or drop."))
            elif osp and not nsp:
                out.append(("⚠", f"{label}: {side.upper()} SP {oname} REMOVED (now TBA) — "
                                 f"scratch risk; legs on {oname} are PENDING at best."))
            elif not osp and nsp:
                out.append(("ℹ", f"{label}: {side.upper()} probable now posted: {nname} "
                                 f"(was TBA) — run SP-freshness before using."))
    return out


def snap_path(d):
    return os.path.join(SNAP_DIR, f"{d}.json")


def cmd_snap(d):
    games = pull_games(d)
    os.makedirs(SNAP_DIR, exist_ok=True)
    with open(snap_path(d), "w", encoding="utf-8") as fh:
        json.dump(games, fh, indent=1)
    print(f"snapshot: {len(games)} games → {os.path.relpath(snap_path(d))}")
    for g in games:
        print(f"  {g['away']} ({g.get('away_sp') or 'TBA'}) @ "
              f"{g['home']} ({g.get('home_sp') or 'TBA'})  [{g['detail']}]")
    print("→ commit this with the build; the 16:00/18:00 runs diff against it.")


def cmd_diff(d):
    p = snap_path(d)
    if not os.path.exists(p):
        print(f"no snapshot for {d} ({os.path.relpath(p)}) — run 'tools/recheck.py snap {d}' "
              f"at build time first. Current live state:")
        for g in pull_games(d):
            print(f"  {g['away']} ({g.get('away_sp') or 'TBA'}) @ "
                  f"{g['home']} ({g.get('home_sp') or 'TBA'})  [{g['detail']}]")
        return 0
    with open(p, encoding="utf-8") as fh:
        old = json.load(fh)
    new = pull_games(d)
    findings = diff_games(old, new)
    print(f"recheck {d}: snapshot {len(old)} games vs live {len(new)} games")
    if not findings:
        print("  ✓ no scratches, no SP changes, no status flips — locked legs stand.")
        return 0
    for sev, msg in findings:
        print(f"  {sev} {msg}")
    hard = [1 for sev, _ in findings if sev in ("⛔", "⚠")]
    return 1 if hard else 0


def selftest():
    """Offline: the diff logic on fixtures — scratch, TBA-fill, started, unchanged, vanished."""
    old = [
        {"pk": 1, "state": "Preview", "detail": "Scheduled", "away": "A", "home": "B",
         "away_sp_id": 10, "away_sp": "Old Ace", "home_sp_id": 20, "home_sp": "Steady Arm"},
        {"pk": 2, "state": "Preview", "detail": "Scheduled", "away": "C", "home": "D",
         "away_sp_id": None, "away_sp": None, "home_sp_id": 40, "home_sp": "Same Guy"},
        {"pk": 3, "state": "Preview", "detail": "Scheduled", "away": "E", "home": "F",
         "away_sp_id": 50, "away_sp": "Vanishing", "home_sp_id": 60, "home_sp": "X"},
    ]
    new = [
        {"pk": 1, "state": "Preview", "detail": "Scheduled", "away": "A", "home": "B",
         "away_sp_id": 11, "away_sp": "Sub Arm", "home_sp_id": 20, "home_sp": "Steady Arm"},
        {"pk": 2, "state": "Live", "detail": "In Progress", "away": "C", "home": "D",
         "away_sp_id": 30, "away_sp": "Now Posted", "home_sp_id": 40, "home_sp": "Same Guy"},
    ]
    f = diff_games(old, new)
    msgs = "\n".join(m for _, m in f)
    checks = [
        ("SP change flagged ⚠", any(s == "⚠" and "SP CHANGED Old Ace → Sub Arm" in m for s, m in f)),
        ("unchanged SP silent", "Steady Arm →" not in msgs and "Same Guy →" not in msgs),
        ("started game flagged ⛔", any(s == "⛔" and "In Progress" in m for s, m in f)),
        ("TBA→posted flagged ℹ", any(s == "ℹ" and "Now Posted" in m for s, m in f)),
        ("vanished game flagged ⚠", any("GONE from the feed" in m for _, m in f)),
    ]
    bad = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"  {'✓' if ok else '✗'} {name}")
    print(f"── recheck self-test: {'ALL PASSED' if not bad else f'{len(bad)} FAILED'}")
    return 0 if not bad else 1


def main():
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        sys.exit(selftest())
    if args and args[0] == "snap":
        d = args[1] if len(args) > 1 else date.today().isoformat()
        if not re.match(r"\d{4}-\d{2}-\d{2}$", d):
            sys.exit(f"bad date {d!r} (YYYY-MM-DD)")
        cmd_snap(d)
        return
    d = args[0] if args else date.today().isoformat()
    if not re.match(r"\d{4}-\d{2}-\d{2}$", d):
        sys.exit(f"bad date {d!r} (YYYY-MM-DD); usage: recheck.py [snap] [date] | --selftest")
    sys.exit(cmd_diff(d))


if __name__ == "__main__":
    main()
