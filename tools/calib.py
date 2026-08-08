#!/usr/bin/env python3
"""calib.py — recompute calibration / ROI from results_log.md (READ-ONLY).

WHY THIS EXISTS
    results_log.md's whole job is to keep the process honest — but its rollup tables
    (calibration bands, units/ROI, by-type record) are hand-maintained, so they drift
    and accumulate arithmetic slips. This re-derives them from the raw leg rows so the
    numbers in front of you are correct. It PRINTS a report and never edits the ledger;
    if the printed numbers disagree with the file's tables, the file is stale — fix it.

METHODOLOGY (matches the ledger's stated rules)
    • Calibration uses PLAYED legs with an explicitly-logged TrueP. Rows whose TrueP is
      marked '*' (reconstructed after the fact) are excluded, same as the file.
    • Bands are fixed 5-wide (50-54, 55-59, …) — these may not line up exactly with the
      hand-drawn bands in the file; the script's bands are the consistent ones going fwd.
    • ROI is summed straight from the played-ticket rollup (stake / return / P-L columns).

USAGE
    tools/calib.py [path/to/results_log.md]
"""
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # for leg_key's settle import

LEDGER = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "results_log.md")


def cells(line):
    """Split a markdown table row into stripped cell strings (drops outer pipes)."""
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep_or_header(c):
    joined = "".join(c)
    if joined and set(joined) <= set("-: "):     # |----|----| separator
        return True
    return bool(c) and c[0].lower() == "date"      # header row


def table_rows(text, header_substr):
    """Yield cell-lists for the markdown table following a heading line that
    contains header_substr, stopping at the next markdown heading."""
    rows, in_sec = [], False
    for ln in text.splitlines():
        if not in_sec:
            if header_substr in ln:
                in_sec = True
            continue
        if ln.lstrip().startswith("#"):           # next heading ends the section
            break
        if re.match(r"^\s*\|", ln):
            c = cells(ln)
            if c and not is_sep_or_header(c):
                rows.append(c)
    return rows


def parse_result(s):
    """W / L / Push from a bold-wrapped result cell like '**W** (12 K)' or '**would-L** (...)'.

    Returns None for non-outcome cells (TBD / SUPERSEDED / pointer rows) so they don't leak
    into the record. (Bug 6/7/26: naive substring matched 'w' in 'would', 'l' in 'Build',
    counting would-L as W and SUPERSEDED rows as L — the §4 record was inverted/garbage.)

    The SUPERSEDED check runs on the WHOLE cell, not just the first bold span (bug fixed
    8/7/26: 'SUPERSEDED @ 16:00 — … **L** (7 K)' extracted the bold L and the same leg
    settled at multiple prices into the bands, Brier AND pulse's window — 9 rows were
    double-counted. A superseded row must never settle, wherever the marker sits). TBD and
    pointer checks stay scoped to the bold segment — 'TBD' occurs mid-prose in genuinely
    decided rows ('vs MIN TBD/bullpen game'), so a whole-cell veto would drop real results.
    """
    if "superseded" in s.lower():
        return None
    m = re.search(r"\*\*(.+?)\*\*", s)
    seg = (m.group(1) if m else s).strip()
    low = seg.lower()
    if any(t in low for t in ("tbd", "played →", "played ->", "n/a")):
        return None
    if "push" in low:
        return "Push"
    core = re.sub(r"^\s*would-?\s*", "", low)   # strip a leading 'would-' qualifier
    if re.match(r"w\b", core):                  # first token is W / W (fade) / would-W
        return "W"
    if re.match(r"l\b", core):                  # first token is L / would-L
        return "L"
    return None


def parse_pct(s):
    """'~72%*' -> (72.0, starred=True); '60%' -> (60.0, False); '—' -> (None, _).

    NOTE (bug fixed 8/6/26): the star test used to be a bare `"*" in s`, which also matched
    the markdown BOLD markers in a cell like '**54.5%**'. Every bold-wrapped TrueP was
    therefore misread as a reconstructed legacy row and silently dropped from the calibration
    bands AND from the §1b Brier scoreboard — a large, invisible measurement loss, since the
    build writes its headline legs in bold. Strip bold first, then look for a real '*'.

    NOTE (bug fixed 8/7/26, same class): '"*" in stripped' ALSO matched italics annotations
    like '51.4% *(pre-shade 56.4%)*' — 18 rows, disproportionately the governor-audit rows,
    silently starred out of bands/Brier/attribution/pulse. The legacy marker is always glued
    to the percent ('72%*'); italics never are. Star = literal '%*' after bold-stripping.
    """
    stripped = s.replace("**", "")
    starred = "%*" in stripped
    m = re.search(r"(\d+(?:\.\d+)?)", stripped)
    return (float(m.group(1)) if m else None), starred


def parse_num(s):
    """Parse a unit number, tolerating the unicode minus and em-dash placeholders."""
    s = s.replace("−", "-").replace("—", "").strip()
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None


def band(p):
    lo = int(p // 5 * 5)
    return f"{lo}-{lo + 4}"


ADJ_TAG = re.compile(r"\[adj:\s*([^\]]*)\]")


def parse_adj_tags(cell):
    """'… [adj: ace_edge+3, wind_in_under+3]' → ['ace_edge','wind_in_under'];
    '[adj: none]' (any 'none …' variant, incl. 'PULSE-SHADED to none') → [] (a tagged,
    market-anchored control row); '[adj: n/a]' or untagged → None.

    Names are EXTRACTED, not suffix-stripped (bug fixed 8/7/26: 'hot_dog+3 (fades.md B1)'
    and 'pitcher_park_under+3 → **band-blocked…**' each minted a garbage singleton
    dimension in §1c and pulse — prose after the magnitude defeated the old trailing-\\d
    strip). A part yields a name only via 'name+N'/'name-N' or a clean bare name; prose
    fragments are dropped."""
    m = ADJ_TAG.search(cell or "")
    if not m:
        return None
    content = m.group(1).strip()
    if content.lower() in ("n/a", "na", "-", "—"):
        return None
    names = []
    for part in content.split(","):
        part = part.strip()
        low = part.lower()
        if not part or low.startswith("none") or low.startswith("pulse-shaded"):
            continue
        g = re.match(r"([A-Za-z][A-Za-z0-9_]*)\s*[+\-−][\d.]", part)
        if g:
            names.append(g.group(1))
        elif re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", part):
            names.append(part)
    return names


def leg_key(datecell, leg, typ):
    """Canonical identity of the PHYSICAL bet a row describes — (date, market, side, line).

    The ledger logs the same leg 2-4× per day (11:00 scan → 16:00/18:00 REPRICE →
    'promoted'), and supersede markers are only half machine-readable. Counting ROWS
    where doctrine means LEGS double/triple-counted the same W/L and the same CLV
    verdict into the bands, §1b Brier, §1c attribution AND pulse's window — on 8/8
    the 131-row window held only 107 unique legs, and three governor MARKET-SHADEs
    existed only because of the copies (audit 8/7/26). Dedup by this key, keeping
    the LAST row (latest reprice = the current state of that leg)."""
    from settle import parse_kprop as _kp, parse_hprop as _hp, find_team as _ft
    l = (leg or "").replace("**", "").replace("⭐", "").replace("⛔", "")
    d = (datecell or "").strip()
    kp = _kp(l)
    if kp:
        return (d, "K", kp[0].lower(), kp[1], kp[2])
    hp = _hp(l)
    if hp:
        return (d, "H", hp[0].lower(), hp[1], hp[2], hp[3])
    t = (typ or "").lower()
    ft = _ft(l)
    ab = ft[0] if ft else None
    m = re.search(r"\b(over|under|o|u)\s*(\d+(?:\.\d+)?)", l, re.I)
    if ab is not None:   # team-market keys need a resolved team, else two different
        if "total" in t and m:   # unresolvable legs on one date would wrongly merge
            return (d, "T", ab, m.group(1).lower()[0], m.group(2))
        if "run line" in t or re.search(r"[+-]\d\.5\s*(alt\s*)?RL\b", l, re.I) or " RL" in l:
            return (d, "RL", ab)
        if "ml" in t:
            return (d, "ML", ab)
    return (d, "other", re.sub(r"\s+", " ", l).strip().lower()[:40])


def dedup_rows(rows, keys):
    """Keep the LAST row per leg_key (order-preserving otherwise). rows and keys are
    parallel lists; returns the deduped row list."""
    last = {}
    for i, k in enumerate(keys):
        last[k] = i
    keep = sorted(last.values())
    return [rows[i] for i in keep]


def main():
    with open(LEDGER, encoding="utf-8") as fh:
        text = fh.read()

    played = table_rows(text, "## Played legs")
    recs = table_rows(text, "## Recommended but NOT played")
    tickets = table_rows(text, "### Played-ticket record")

    # One row per PHYSICAL leg (audit 8/7/26): reprice/supersede copies of the same bet
    # collapse to the latest row, within each section and across the §1b/§1c pool
    # (played version preferred over its scan row). Raw counts kept for transparency.
    def _keys(rows):
        return [leg_key(c[0] if c else "", c[1] if len(c) > 1 else "",
                        c[2] if len(c) > 2 else "") for c in rows]

    raw_counts = (len(played), len(recs))
    played = dedup_rows(played, _keys(played))
    recs = dedup_rows(recs, _keys(recs))
    pool = dedup_rows(recs + played, _keys(recs + played))
    dup_note = (f"   ({raw_counts[0] - len(played)} played + {raw_counts[1] - len(recs)} "
                f"recommended duplicate reprice rows collapsed to latest)")

    print("=" * 60)
    print(f"  CALIBRATION / ROI RECOMPUTE  (read-only)")
    print(f"  source: {os.path.relpath(LEDGER)}")
    print("=" * 60)

    # ---- 1. Calibration bands (played, explicit TrueP, '*' excluded) ----------
    # played cols: date, leg, type, price, truep, implp, edge, result, played, clv
    buckets = defaultdict(lambda: [0, 0, 0])  # band -> [n, won, lost] (Push ignored in hit%)
    excluded_star = 0
    for c in played:
        if len(c) < 9:
            continue
        if c[8].strip().upper() != "Y":
            continue
        truep, starred = parse_pct(c[4])
        if truep is None:
            continue
        if starred:
            excluded_star += 1
            continue
        res = parse_result(c[7])
        if res not in ("W", "L"):
            continue  # TBD / pending legs aren't decided yet — exclude from n until settled
        b = band(truep)
        buckets[b][0] += 1
        if res == "W":
            buckets[b][1] += 1
        elif res == "L":
            buckets[b][2] += 1

    print("\n-- 1. Calibration bands  (played legs, explicit TrueP only) --")
    print(f"   ({excluded_star} reconstructed '*' rows excluded, per the ledger's rule)")
    print(dup_note)
    print(f"   {'band':<8} {'n':>2}  {'W':>2}-{'L':<2}  {'hit%':>5}   vs band midpoint")
    total_n = total_w = 0
    for b in sorted(buckets, key=lambda x: int(x.split("-")[0])):
        n, w, l = buckets[b]
        dec = w + l
        hit = (w / dec * 100) if dec else 0.0
        lo = int(b.split("-")[0])
        mid = lo + 2.5
        flag = ""
        if dec >= 3:   # don't draw conclusions from 1-2 coin-flips
            if hit + 0.001 < mid - 7:
                flag = "  ⚠ under (overconfident)"
            elif hit > mid + 7:
                flag = "  ▲ over (room to bet more)"
        print(f"   {b:<8} {n:>2}  {w:>2}-{l:<2}  {hit:>4.0f}%   mid {mid:.1f}{flag}")
        total_n += n
        total_w += w
    print(f"   {'TOTAL':<8} {total_n:>2}  {total_w:>2} won")

    # ---- 1b. Brier skill vs the market (does TrueP beat the logged price?) ----
    # Pools EVERY decided LEG row (played + not-played) with an explicit TrueP and a
    # parseable ImplP — forecasts were pre-registered either way, so all of them score.
    # Brier = mean((forecast − outcome)²), lower is better; the DELTA vs the market's
    # no-vig ImplP on the SAME rows is the honest "do the written adjustments add
    # anything?" number. This converges far faster than band tables (a proper scoring
    # rule uses every row, not 5-wide buckets) — it's the leg-selection scoreboard.
    def scorable(rows):
        out = []
        for c in rows:
            if len(c) < 8:
                continue
            if "×" in c[1] or "parlay" in c[2].lower():   # leg-level only (no ticket rows)
                continue
            truep, starred = parse_pct(c[4])
            implp, _ = parse_pct(c[5])
            res = parse_result(c[7])
            if truep is None or starred or implp is None or res not in ("W", "L"):
                continue
            if not (1 <= truep <= 99 and 1 <= implp <= 99):
                continue
            out.append((truep / 100.0, implp / 100.0, 1.0 if res == "W" else 0.0))
        return out

    pooled = scorable(pool)   # cross-section deduped: one row per physical leg
    print("\n-- 1b. Brier skill vs market  (TrueP vs logged no-vig ImplP, every decided leg) --")
    if len(pooled) >= 10:
        b_model = sum((p - y) ** 2 for p, _, y in pooled) / len(pooled)
        b_market = sum((q - y) ** 2 for _, q, y in pooled) / len(pooled)
        skill = b_market - b_model
        print(f"   n={len(pooled)} scored legs   Brier(TrueP) {b_model:.4f}   "
              f"Brier(market ImplP) {b_market:.4f}   (coin-flip ref 0.2500)")
        if skill > 0:
            print(f"   skill {skill:+.4f} → TrueP BEATS the logged price — the written "
                  f"adjustments are adding signal")
        else:
            print(f"   skill {skill:+.4f} → TrueP does NOT beat the logged price — shrink "
                  f"adjustments toward the no-vig baseline")
        if len(pooled) < 40:
            print("   ⚠ n<40 — directional only; don't resize adjustment magnitudes off this yet.")
    else:
        print(f"   (only {len(pooled)} scorable legs — need ≥10)")

    # ---- 1c. Per-adjustment attribution (accrues from [adj: …] ledger tags) ---
    # truep.py prints a paste-able tag naming the adjustments behind each TrueP; rows
    # carrying it can be scored PER ADJUSTMENT (does ace_edge earn its +3pp?), with
    # '[adj: none]' rows as the market-anchored control. This is the accrual path to
    # eventually auto-calibrating the registry magnitudes instead of trusting them.
    per = defaultdict(lambda: [0, 0, 0.0, 0.0])   # name -> [n, wins, Σbrier_model, Σbrier_mkt]
    for c in pool:
        if len(c) < 8:
            continue
        tags = parse_adj_tags(c[1])
        if tags is None:
            continue
        truep, starred = parse_pct(c[4])
        implp, _ = parse_pct(c[5])
        res = parse_result(c[7])
        if truep is None or starred or implp is None or res not in ("W", "L"):
            continue
        y = 1.0 if res == "W" else 0.0
        for t in (tags or ["(none — market-anchored)"]):
            e = per[t]
            e[0] += 1
            e[1] += int(res == "W")
            e[2] += (truep / 100.0 - y) ** 2
            e[3] += (implp / 100.0 - y) ** 2
    print("\n-- 1c. Per-adjustment attribution  (from [adj: …] tags in leg cells) --")
    if not per:
        print("   (no tagged decided rows yet — truep.py now prints a paste-able tag;")
        print("    paste it into each leg cell and this section fills itself.")
        print("    Judge nothing before n≥20 per adjustment.)")
    else:
        print(f"   {'adjustment':<26} {'n':>3}  {'W-L':>6}  {'hit%':>5}  {'skill/leg':>9}")
        for t in sorted(per, key=lambda x: -per[x][0]):
            n, w, bm, bk = per[t]
            skill = (bk - bm) / n if n else 0.0
            flag = "" if n >= 20 else "  (n<20 — directional)"
            print(f"   {t:<26} {n:>3}  {w:>2}-{n - w:<3}  {w / n * 100:>4.0f}%  {skill:>+9.4f}{flag}")
        print("   (skill/leg = per-row Brier edge vs the market on rows carrying the tag;")
        print("    positive = the adjustment is earning its pp.)")

    # ---- 2. Record by bet type (played) ---------------------------------------
    by_type = defaultdict(lambda: [0, 0, 0])  # type -> [W, L, Push]
    for c in played:
        if len(c) < 9 or c[8].strip().upper() != "Y":
            continue
        t = c[2].strip()
        res = parse_result(c[7])
        if res == "W":
            by_type[t][0] += 1
        elif res == "L":
            by_type[t][1] += 1
        elif res == "Push":
            by_type[t][2] += 1

    print("\n-- 2. Record by bet type  (played legs) --")
    for t in sorted(by_type, key=lambda x: -(by_type[x][0] + by_type[x][1] + by_type[x][2])):
        w, l, p = by_type[t]
        dec = w + l
        hit = (w / dec * 100) if dec else 0.0
        push = f" +{p}P" if p else ""
        print(f"   {t:<14} {w}-{l}{push}   {hit:.0f}%")

    # ---- 2b. STANDALONE vs PARLAY split (played legs, by Bucket col) -----------
    # Tests the doctrine's core claim that parlays run near -EV chalk+vig. Bucket
    # is the last column (index 10); rows predating the column count as '?'.
    by_bucket = defaultdict(lambda: [0, 0, 0])  # bucket -> [W, L, Push]
    for c in played:
        if len(c) < 9 or c[8].strip().upper() != "Y":
            continue
        bkt = c[10].strip().upper() if len(c) > 10 and c[10].strip() else "?"
        bkt = {"S": "STANDALONE", "P": "PARLAY"}.get(bkt, "untagged")
        res = parse_result(c[7])
        if res == "W":
            by_bucket[bkt][0] += 1
        elif res == "L":
            by_bucket[bkt][1] += 1
        elif res == "Push":
            by_bucket[bkt][2] += 1

    print("\n-- 2b. STANDALONE vs PARLAY  (played legs — the parlay-tax test) --")
    for bkt in ("STANDALONE", "PARLAY", "untagged"):
        if bkt not in by_bucket:
            continue
        w, l, p = by_bucket[bkt]
        dec = w + l
        hit = (w / dec * 100) if dec else 0.0
        push = f" +{p}P" if p else ""
        note = "  (small n — directional)" if dec < 10 else ""
        print(f"   {bkt:<11} {w}-{l}{push}   {hit:.0f}%{note}")
    print("   (leg-level hit%; ticket-level ROI is section 3 [parlays] + bankroll.md [standalone ladder])")

    # ---- 3. Played-ticket units / ROI -----------------------------------------
    # ticket cols: date, ticket, odds, stake, return, pl, result
    stake_sum = ret_sum = pl_sum = 0.0
    wins = losses = 0
    parsed = 0
    for c in tickets:
        if len(c) < 6:
            continue
        result = c[6] if len(c) > 6 else ""
        ticket_txt = c[1] if len(c) > 1 else ""
        # Skip undecided rows AND dollar-denominated USER tickets — the latter are tracked
        # separately in the prose, not in the unit-ROI. (Bug 6/7/26: parse_num strips '$', so
        # $10→$30.62 USER rows + TBD rows were summed into the unit ROI → +213% vs prose +30.7%.)
        if "tbd" in result.lower():
            continue
        if "$" in c[3] or "$" in (c[4] if len(c) > 4 else "") or "user" in ticket_txt.lower():
            continue
        # Skip prob-tracked correlated rows: these put naive%/true%/edge in the stake/return/PL
        # columns (e.g. "+194 | 33.5% | 40.7% | +6.7"), not real flat-1u stakes. A '%' in the
        # stake or return column flags such a row → exclude from the unit-ROI (matches the
        # dashboard parser, which already excludes them). (Bug 6/12/26: settling these correlated
        # 6/11 rows made calib read 33.5u stakes → 112u staked / +24.99u vs the true flat-1u +7.39u.)
        if "%" in c[3] or "%" in (c[4] if len(c) > 4 else ""):
            continue
        stake = parse_num(c[3])
        ret = parse_num(c[4])
        pl = parse_num(c[5])
        if stake is None:
            continue
        parsed += 1
        stake_sum += stake
        ret_sum += (ret or 0.0)
        # prefer explicit P-L; else derive
        pl_sum += pl if pl is not None else ((ret or 0.0) - stake)
        if (ret or 0.0) > stake - 1e-9 and (ret or 0.0) > 1e-9:
            wins += 1
        else:
            losses += 1

    print("\n-- 3. Played PARLAY-ticket units / ROI --  (standalone ladder ROI: bankroll.md)")
    if parsed:
        roi = (pl_sum / stake_sum * 100) if stake_sum else 0.0
        print(f"   tickets: {parsed}   record: {wins}-{losses}")
        print(f"   staked {stake_sum:.2f}u   returned {ret_sum:.2f}u   "
              f"P/L {pl_sum:+.2f}u   ROI {roi:+.1f}%")
        print("   ⚠ small-n + flat-stake assumption — read ROI as directional, CLV is the better signal.")
    else:
        print("   (no parsable ticket rows)")

    # ---- 4. Recommended-not-played (secondary calibration) --------------------
    rec_w = rec_l = 0
    for c in recs:
        if len(c) < 8:
            continue
        res = parse_result(c[7])
        if res == "W":
            rec_w += 1
        elif res == "L":
            rec_l += 1
    print("\n-- 4. Recommended-not-played (fade/decline calibration) --")
    dec = rec_w + rec_l
    if dec:
        print(f"   {rec_w}-{rec_l}  →  recommendations we DIDN'T play went {rec_w}-{rec_l} "
              f"({rec_w / dec * 100:.0f}% would-win)")
        print("   (high would-win on declined legs = we're leaving edge on the table)")
    else:
        print("   (none parsable)")

    print("\n" + "=" * 60)
    print("  Read-only recompute — if these differ from the tables in")
    print("  results_log.md, the file is stale; update it to match.")
    print("=" * 60)


if __name__ == "__main__":
    main()
