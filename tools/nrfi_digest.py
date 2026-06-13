#!/usr/bin/env python3
"""nrfi_digest.py — emit one day's NRFI/YRFI reads as a table + daily win%.

WHY THIS EXISTS
    The user wants the NRFI/YRFI picks (and the day's win%) included in the push
    notification + email on EVERY cron run (Build A/B/C). This produces that block
    deterministically from nrfi_tracker.md so each run drops in the same shape — no
    hand-retyping the table, and the daily record/win% is always computed, not eyeballed.

WHAT IT DOES
    Reads the nrfi_tracker.md ledger, selects the rows whose Date == the target day
    (default today, M/D format), and prints:
      • a header line with that day's settled record + win% + open count,
      • the day's reads (Matchup | Pick | TrueP | Result).

FORMATS
    --format md       (default) GitHub-markdown table — for the email body.
    --format text     aligned plain-text table — for plaintext contexts.
    --compact         single line (record/win% + pick counts) — for the push notification.

USAGE
    tools/nrfi_digest.py                    # today, markdown
    tools/nrfi_digest.py 2026-06-13         # a specific date
    tools/nrfi_digest.py --compact          # one-liner for the push notification
    tools/nrfi_digest.py --format text      # plain-text table
"""
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TRACKER = os.path.join(HERE, "..", "nrfi_tracker.md")


def md_date(d):
    """YYYY-MM-DD -> M/D (no leading zeros), matching the ledger's Date format."""
    _, m, day = d.split("-")
    return f"{int(m)}/{int(day)}"


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def load_rows(tracker, target):
    """Return ledger rows (dicts) whose Date == target (M/D)."""
    with open(tracker, encoding="utf-8") as f:
        lines = f.readlines()
    rows = []
    for line in lines:
        if "|" not in line:
            continue
        c = cells(line)
        if len(c) < 6 or not re.match(r"^\d+/\d+$", c[0]):
            continue
        if c[0] != target:
            continue
        res = c[5]
        result = "W" if re.search(r"\bW\b", res) else ("L" if re.search(r"\bL\b", res) else "TBD")
        rows.append({
            "matchup": re.sub(r"\s*\([^)]*\)", "", c[1]).strip(),  # drop "(SP/SP)" tail
            "pick": c[2].strip().upper(),
            "truep": c[3].strip(),
            "result": result,
        })
    return rows


def tally(rows):
    w = sum(r["result"] == "W" for r in rows)
    l = sum(r["result"] == "L" for r in rows)
    tbd = sum(r["result"] == "TBD" for r in rows)
    settled = w + l
    pct = (100.0 * w / settled) if settled else None
    nrfi = sum(r["pick"] == "NRFI" for r in rows)
    yrfi = sum(r["pick"] == "YRFI" for r in rows)
    return {"w": w, "l": l, "tbd": tbd, "settled": settled, "pct": pct,
            "nrfi": nrfi, "yrfi": yrfi, "n": len(rows)}


def header_line(target, t):
    if t["settled"]:
        rec = f"{t['w']}-{t['l']} ({t['pct']:.0f}% W)"
    else:
        rec = "no games settled yet"
    open_txt = f", {t['tbd']} open" if t["tbd"] else ""
    return f"NRFI/YRFI {target} — daily {rec}{open_txt} · {t['nrfi']} NRFI / {t['yrfi']} YRFI"


def render(rows, target, fmt):
    t = tally(rows)
    if not rows:
        return f"NRFI/YRFI {target} — no reads logged."
    head = header_line(target, t)

    if fmt == "compact":
        return head

    if fmt == "md":
        out = [head, "", "| Matchup | Pick | TrueP | Result |", "|---|---|---|---|"]
        for r in rows:
            out.append(f"| {r['matchup']} | {r['pick']} | {r['truep']} | {r['result']} |")
        return "\n".join(out)

    # plain text — aligned
    mw = max(len(r["matchup"]) for r in rows)
    out = [head, ""]
    for r in rows:
        out.append(f"  {r['matchup']:<{mw}}  {r['pick']:<4}  {r['truep']:>5}  {r['result']}")
    return "\n".join(out)


def main():
    args = sys.argv[1:]
    fmt = "md"
    if "--compact" in args:
        fmt = "compact"; args.remove("--compact")
    if "--format" in args:
        i = args.index("--format"); fmt = args[i + 1]; del args[i:i + 2]
    tracker = next((a for a in args if a.endswith(".md")), DEFAULT_TRACKER)
    dpos = next((a for a in args if re.match(r"^\d{4}-\d{2}-\d{2}$", a)), None)
    target = md_date(dpos) if dpos else md_date(date.today().isoformat())
    rows = load_rows(tracker, target)
    print(render(rows, target, fmt))


if __name__ == "__main__":
    main()
