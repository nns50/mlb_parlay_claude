#!/usr/bin/env python3
"""
Generate docs/index.html — read-only analytics dashboard.
Parses bankroll.md, results_log.md, parlays/*.md, fades.md.
Run after any build to refresh the Pages site.
"""
import re, json
from pathlib import Path
from datetime import datetime


def american_to_decimal(price_str: str):
    """Parse an American price string (e.g. '-310', '+100', '~-150') to decimal odds."""
    s = strip_md(price_str).replace('~', '').replace('−', '-').strip()
    m = re.search(r'([+-]\d+)', s)
    if not m:
        return None
    a = int(m.group(1))
    return 1 + (a / 100 if a > 0 else 100 / abs(a))

REPO = Path(__file__).parent.parent
DOCS = REPO / "docs"


# ─── Utility ──────────────────────────────────────────────────────────────────

def strip_md(s: str) -> str:
    s = s.strip()
    s = re.sub(r'\*+', '', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    return s.strip()

def parse_pct(s: str):
    m = re.search(r'([\d.]+)%', s)
    return float(m.group(1)) if m else None

def parse_dollar(s: str):
    s = strip_md(s).replace('$', '').replace(',', '')
    m = re.search(r'[\d.]+', s)
    return float(m.group()) if m else None

def parse_edge(s: str):
    s = strip_md(s).replace('−', '-').replace('–', '-')
    m = re.search(r'([+-]?[\d.]+)', s)
    return float(m.group(1)) if m else None

def parse_md_table(text: str, required: list) -> list[dict]:
    """Find the first markdown table whose header contains all required strings."""
    lines = text.split('\n')
    for i, line in enumerate(lines):
        s = line.strip()
        if not s.startswith('|'):
            continue
        if not all(r.lower() in s.lower() for r in required):
            continue
        if i + 1 >= len(lines) or not re.match(r'\|[-| :]+\|', lines[i + 1].strip()):
            continue
        headers = [strip_md(h) for h in s.split('|')[1:-1]]
        rows = []
        for j in range(i + 2, len(lines)):
            rl = lines[j].strip()
            if not rl.startswith('|'):
                break
            cells = rl.split('|')[1:-1]
            if len(cells) == len(headers):
                rows.append({headers[k]: cells[k].strip() for k in range(len(headers))})
        if rows:
            return rows
    return []


# ─── Bankroll ─────────────────────────────────────────────────────────────────

def parse_bankroll() -> list[dict]:
    path = REPO / "bankroll.md"
    if not path.exists():
        return []
    rows = parse_md_table(path.read_text(encoding='utf-8'),
                          ['Attempt', 'Balance before', 'Result'])
    out = []
    for row in rows:
        att = strip_md(row.get('Attempt', ''))
        if not att or att in ('—', '-'):
            continue
        roll = strip_md(row.get('Roll', ''))
        if not roll or roll in ('—', '-'):
            continue
        result_raw = strip_md(row.get('Result', '')).upper()
        if 'WIN' in result_raw:
            result = 'W'
        elif 'LOSS' in result_raw or 'BUST' in result_raw:
            result = 'L'
        elif '—' in result_raw or 'NO BET' in result_raw or not result_raw:
            result = None
        else:
            result = None
        out.append({
            'attempt': att,
            'date': strip_md(row.get('Date', '')),
            'roll': roll,
            'bal_before': parse_dollar(row.get('Balance before', '')),
            'bet': strip_md(row.get('Bet (leg @ book, decimal)', '') or row.get('Bet', ''))[:60],
            'truep': parse_pct(row.get('True%', '') or row.get('TrueP', '')),
            'result': result,
            'bal_after': parse_dollar(row.get('Balance after', '')),
            'note': strip_md(row.get('Note', ''))[:80],
        })
    return out


def bankroll_chart_data(rolls: list[dict]) -> dict:
    labels, values, pt_colors = [], [], []
    prev_att = None
    for roll in rolls:
        att = roll['attempt']
        if att != prev_att:
            if prev_att is not None:
                labels.append(''); values.append(None); pt_colors.append('#30363d')
            labels.append(f"A{att} ▸ Start")
            values.append(10.0)
            pt_colors.append('#8b949e')
            prev_att = att
        label = f"A{att} R{roll['roll']} ({roll['date']})"
        val = roll['bal_after'] if roll['bal_after'] is not None else 0.0
        if roll['result'] is None:
            color = '#eab308'
        elif roll['result'] == 'W':
            color = '#22c55e'
        else:
            color = '#ef4444'
            val = 0.0
        labels.append(label); values.append(val); pt_colors.append(color)

    # If the last attempt is finished (target hit or busted), show the next
    # attempt starting fresh at $10 as an in-progress marker.
    last_result = rolls[-1]['result'] if rolls else None
    if rolls and last_result in ('W', 'L'):
        try:
            next_att = int(rolls[-1]['attempt']) + 1
        except (ValueError, TypeError):
            next_att = '?'
        labels.append(''); values.append(None); pt_colors.append('#30363d')
        labels.append(f"A{next_att} ▸ Start ($10)")
        values.append(10.0); pt_colors.append('#8b949e')
    return {'labels': labels, 'values': values, 'colors': pt_colors}


# ─── Results log ──────────────────────────────────────────────────────────────

def _outcome(result_raw: str):
    if re.search(r'\bW\b', result_raw):
        return 'W'
    if re.search(r'\bL\b', result_raw):
        return 'L'
    return None

def _leg_rows(section_text: str) -> list[dict]:
    rows = parse_md_table(section_text, ['Date', 'Leg', 'TrueP'])
    out = []
    for row in rows:
        date_s = strip_md(row.get('Date', ''))
        if not date_s or re.match(r'^-+$', date_s):
            continue
        truep_raw = row.get('TrueP', '')
        result_raw = strip_md(row.get('Result', ''))
        clv_raw = strip_md(row.get('CLV', '')).replace('−', '-')
        out.append({
            'date': date_s,
            'leg': strip_md(row.get('Leg (game)', '') or row.get('Leg', ''))[:45],
            'type': strip_md(row.get('Type', '')),
            'price': strip_md(row.get('Price', '')),
            'truep': parse_pct(truep_raw),
            'implp': parse_pct(row.get('ImplP', '')),
            'edge': parse_edge(row.get('Edge', '')),
            'result': _outcome(result_raw),
            'played': strip_md(row.get('Played', '')).upper() == 'Y',
            'clv': clv_raw,
            'bucket': strip_md(row.get('Bucket', '')),
            'legacy': '*' in truep_raw,
        })
    return out


def parse_results_log() -> dict:
    path = REPO / "results_log.md"
    if not path.exists():
        return {'played': [], 'not_played': [], 'tickets': [], 'calib_buckets': []}
    text = path.read_text(encoding='utf-8')

    played_m = re.search(r'## Played legs.*?\n(.*?)(?=\n## |\Z)', text, re.DOTALL)
    played = _leg_rows(played_m.group(1)) if played_m else []

    np_m = re.search(r'## Recommended but NOT played.*?\n(.*?)(?=\n## |\Z)', text, re.DOTALL)
    not_played = _leg_rows(np_m.group(1)) if np_m else []

    # Ticket rollup
    ticket_m = re.search(r'### Played-ticket record.*?\n(.*?)(?=\n###|\n---|\Z)', text, re.DOTALL)
    tickets = []
    if ticket_m:
        for row in parse_md_table(ticket_m.group(1), ['Date', 'Ticket', 'Odds', 'Result']):
            date_s = strip_md(row.get('Date', ''))
            if not date_s:
                continue
            result_raw = strip_md(row.get('Result', ''))
            if re.search(r'WON|✅', result_raw):
                outcome = 'W'
            elif re.search(r'LOST|❌', result_raw):
                outcome = 'L'
            else:
                outcome = 'TBD'
            pl_raw = strip_md(row.get('P/L(u)', '') or row.get('P/L', ''))
            tickets.append({
                'date': date_s,
                'ticket': strip_md(row.get('Ticket', ''))[:55],
                'odds': strip_md(row.get('Odds', '')),
                'result': outcome,
                'pl': pl_raw,
            })

    # Calibration buckets (pre-computed by calib.py)
    calib_m = re.search(r'### Calibration buckets.*?\n(.*?)(?=\n###|\n>|\n---|\Z)', text, re.DOTALL)
    calib = []
    if calib_m:
        for row in parse_md_table(calib_m.group(1), ['Band', 'n', 'Hit%']):
            band = strip_md(row.get('Band (calib.py)', '') or row.get('Band', ''))
            if not band or 'TOTAL' in band.upper():
                continue
            n_m = re.search(r'\d+', strip_md(row.get('n', '')))
            if not n_m:
                continue
            n = int(n_m.group())
            hit = parse_pct(row.get('Hit%', ''))
            mid_s = strip_md(row.get('vs mid', ''))
            mid_m = re.search(r'[\d.]+', mid_s)
            if not mid_m or hit is None:
                continue
            mid = float(mid_m.group())
            wl_m = re.match(r'(\d+)-(\d+)', strip_md(row.get('W-L', '')))
            wins = int(wl_m.group(1)) if wl_m else 0
            losses = int(wl_m.group(2)) if wl_m else 0
            calib.append({'band': band, 'n': n, 'wins': wins, 'losses': losses,
                          'hit_pct': hit, 'midpoint': mid})

    return {'played': played, 'not_played': not_played,
            'tickets': tickets, 'calib_buckets': calib}


# ─── Parlays ──────────────────────────────────────────────────────────────────

def parse_parlays() -> list[dict]:
    d = REPO / "parlays"
    if not d.exists():
        return []
    items = []
    for f in sorted(d.glob("*.md")):
        text = f.read_text(encoding='utf-8')
        runs = re.findall(r'## Run (\d+:\d+) ET', text)

        # Capture "## Result" header line + body together
        result_m = re.search(r'## Result(.*?)(?=\n## |\Z)', text, re.DOTALL)
        result_full = result_m.group(1) if result_m else ''

        outcome = 'TBD'
        if result_full.strip():
            lines = result_full.split('\n')
            # 1. Header line (right after "## Result")
            header = lines[0]
            if re.search(r'\bLOST\b|\bLOSS\b|❌', header, re.IGNORECASE):
                outcome = 'L'
            elif re.search(r'\bWON\b|✅|CASHED', header, re.IGNORECASE):
                outcome = 'W'
            # 2. ### Outcome subsection (most reliable when present)
            if outcome == 'TBD':
                om = re.search(r'### Outcome\n(.*?)(?=\n###|\n##|\Z)', result_full, re.DOTALL)
                if om:
                    ot = om.group(1)
                    if re.search(r'\bLOST\b|\bLOSS\b', ot):
                        outcome = 'L'
                    elif re.search(r'\bWON\b|cashed|✅|🎉', ot, re.IGNORECASE):
                        outcome = 'W'
            # 3. First non-bullet/non-table body line containing a verdict
            if outcome == 'TBD':
                for ln in lines[1:]:
                    ln = ln.strip()
                    if not ln or ln.startswith(('- ', '| ', '> ', '#', '---')):
                        continue
                    if re.search(r'\bLOST\b|\bLOSS\b|❌', ln, re.IGNORECASE):
                        outcome = 'L'
                    elif re.search(r'\bWON\b|✅|🎉|CASHED', ln, re.IGNORECASE):
                        outcome = 'W'
                    break
            # 4. "Build X ... WON/LOST" anywhere in body
            if outcome == 'TBD':
                bm = re.search(r'Build [A-C][^.\n]*(WON|LOST|LOSS)', result_full, re.IGNORECASE)
                if bm:
                    outcome = 'W' if re.search(r'WON', bm.group(1), re.IGNORECASE) else 'L'

        summary = re.sub(r'\s+', ' ', result_full).strip()[:130] if result_full else '—'
        items.append({'date': f.stem, 'runs': runs, 'outcome': outcome, 'summary': summary})
    return items


# ─── Fades ────────────────────────────────────────────────────────────────────

def parse_fades() -> list[dict]:
    """Parse fades.md A–E tables → entries with W/L tally counted from the log column."""
    path = REPO / "fades.md"
    if not path.exists():
        return []
    text = path.read_text(encoding='utf-8')
    sections = {
        'A': 'Team fade (as favorite)', 'B': 'Underdog value',
        'C': 'K-Over fade', 'D': 'Parlay construction', 'E': 'Data/status trap',
    }
    out = []
    # Each category table header starts with "## X." — capture rows with an ID like A1, C3
    for block in re.split(r'\n## ', text):
        sec_m = re.match(r'([A-E])\.', block.strip())
        if not sec_m:
            continue
        sec = sec_m.group(1)
        for row in parse_md_table(block, ['ID', 'Reason', 'Status']):
            fid = strip_md(row.get('ID', ''))
            if not re.match(r'[A-E]\d', fid):
                continue
            # name col differs by table (Team / Fade / Trap)
            name = strip_md(row.get('Team') or row.get('Fade') or row.get('Trap') or '')
            log = row.get('Fade log (most-recent first)') or row.get('Value log') \
                  or row.get('Fade log') or row.get('Log') or ''
            # Count W / L tokens in the log column (word-boundary, bold or plain)
            wins = len(re.findall(r'(?<![A-Za-z])W\b', log))
            losses = len(re.findall(r'(?<![A-Za-z])L\b', log))
            status_raw = strip_md(row.get('Status', ''))
            status = status_raw.split('—')[0].split('(')[0].strip()[:22]
            out.append({
                'id': fid, 'section': sec, 'section_name': sections.get(sec, sec),
                'name': name[:38], 'wins': wins, 'losses': losses,
                'record': f"{wins}-{losses}", 'status': status,
                'reason': strip_md(row.get('Reason', ''))[:70],
            })
    return out


# ─── Summary stats ────────────────────────────────────────────────────────────

def _wl(legs):
    w = sum(1 for l in legs if l['result'] == 'W')
    return w, len(legs) - w

def compute_summary(results: dict, rolls: list[dict]) -> dict:
    played = [l for l in results['played'] if l['played'] and l['result'] in ('W', 'L')]
    wins, losses = _wl(played)

    t_decided = [t for t in results['tickets'] if t['result'] in ('W', 'L')]
    t_wins = sum(1 for t in t_decided if t['result'] == 'W')

    # ── Ticket win streak (chronological by date) ──
    t_chron = sorted(t_decided, key=lambda t: t['date'])
    cur_streak = 0
    for t in reversed(t_chron):          # current run from the most-recent ticket back
        if t['result'] == 'W':
            cur_streak += 1
        else:
            break
    best_streak = run = 0                 # longest W run anywhere in history
    for t in t_chron:
        run = run + 1 if t['result'] == 'W' else 0
        best_streak = max(best_streak, run)
    streak_active = bool(t_chron) and t_chron[-1]['result'] == 'W'

    all_legs = results['played'] + results['not_played']
    clv_list = [l['clv'] for l in all_legs
                if l.get('clv') and l['clv'] not in ('—', '-', '', 'TBD', 'MANUAL', 'PENDING')]
    clv_pos = sum(1 for c in clv_list if c.startswith('+'))

    # Current bankroll balance
    bal = None
    for r in reversed(rolls):
        if r['bal_after'] is not None:
            bal = r['bal_after']
            break

    # ── Standalone (S) vs Parlay (P) split — the parlay-tax measurement ──
    # Use ALL decided legs (played + recommended) — most standalone plays are
    # logged Played=N (bankroll rolls / Tier-1 recs), so played-only undercounts S.
    decided_all = [l for l in (results['played'] + results['not_played'])
                   if l['result'] in ('W', 'L')]
    s_legs = [l for l in decided_all if l['bucket'] == 'S']
    p_legs = [l for l in decided_all if l['bucket'] == 'P']
    sw, sl = _wl(s_legs)
    pw, pl = _wl(p_legs)

    return {
        'leg_record': f"{wins}-{losses}",
        'leg_win_pct': round(wins / max(wins + losses, 1) * 100, 1),
        'total_legs': wins + losses,
        'ticket_record': f"{t_wins}-{len(t_decided) - t_wins}",
        'ticket_total': len(t_decided),
        'cur_streak': cur_streak, 'best_streak': best_streak,
        'streak_active': streak_active,
        'clv_pos': clv_pos, 'clv_total': len(clv_list),
        'clv_pct': round(clv_pos / max(len(clv_list), 1) * 100, 1),
        'bankroll_bal': bal,
        's_record': f"{sw}-{sl}", 's_n': sw + sl,
        's_pct': round(sw / max(sw + sl, 1) * 100, 1),
        'p_record': f"{pw}-{pl}", 'p_n': pw + pl,
        'p_pct': round(pw / max(pw + pl, 1) * 100, 1),
    }


# ─── Leg-type breakdown ───────────────────────────────────────────────────────

def type_breakdown(results: dict) -> list[dict]:
    played = [l for l in (results['played'] + results['not_played'])
              if l['result'] in ('W', 'L')]
    groups = {}
    for l in played:
        # Normalise type into a coarse bucket
        t = l['type'].lower()
        if 'ml' in t and 'fav' in t:
            key = 'ML favorite'
        elif 'ml' in t and 'dog' in t:
            key = 'ML dog'
        elif 'ml' in t:
            key = 'Moneyline'
        elif 'k-over' in t or 'k over' in t:
            key = 'K-Over'
        elif 'k-under' in t:
            key = 'K-Under'
        elif 'run line' in t or 'rl' == t.strip():
            key = 'Run line'
        elif 'prop' in t or 'hit' in t:
            key = 'Hitter prop'
        elif not t or t in ('—', '-'):
            continue  # untyped (e.g. settled-elsewhere placeholder rows)
        else:
            key = l['type']
        groups.setdefault(key, []).append(l)
    out = []
    for key, legs in groups.items():
        w, ln = _wl(legs)
        edges = [l['edge'] for l in legs if l['edge'] is not None]
        # Hypothetical flat-1u standalone ROI from American price + W/L
        pl, staked = 0.0, 0
        for l in legs:
            dec = american_to_decimal(l['price'])
            if dec is None:
                continue
            staked += 1
            pl += (dec - 1) if l['result'] == 'W' else -1
        roi = round(pl / staked * 100, 1) if staked else None
        out.append({
            'type': key, 'n': len(legs), 'record': f"{w}-{ln}",
            'hit': round(w / max(len(legs), 1) * 100),
            'avg_edge': round(sum(edges) / len(edges), 1) if edges else None,
            'roi': roi, 'roi_n': staked,
        })
    out.sort(key=lambda x: -x['n'])
    return out


# ─── Edge-bucket distribution (is the edge gate predictive?) ──────────────────

def edge_buckets(results: dict) -> list[dict]:
    played = [l for l in (results['played'] + results['not_played'])
              if l['result'] in ('W', 'L') and l['edge'] is not None]
    bins = [('< 0', -99, 0), ('0–2', 0, 2), ('2–4', 2, 4),
            ('4–6', 4, 6), ('6+', 6, 99)]
    out = []
    for label, lo, hi in bins:
        legs = [l for l in played if lo <= l['edge'] < hi]
        if not legs:
            out.append({'label': label, 'n': 0, 'hit': None})
            continue
        w, _ = _wl(legs)
        out.append({'label': label, 'n': len(legs),
                    'hit': round(w / len(legs) * 100)})
    return out


# ─── CLV chart data ───────────────────────────────────────────────────────────

def clv_chart_data(results: dict) -> dict:
    legs = []
    seen = set()
    for l in results['played'] + results['not_played']:
        key = (l['date'], l['leg'][:20])
        if key in seen:
            continue
        seen.add(key)
        c = l.get('clv', '').strip()
        if not c or c in ('—', '-', '', 'TBD', 'MANUAL', 'PENDING'):
            continue
        # Try to parse a magnitude (e.g. "+3", "−2pp", "+ 85%cl"); else fall to ±1 sign
        mag = re.search(r'([+-−])\s*([\d.]+)', c)
        if mag:
            sign = -1 if mag.group(1) in '-−' else 1
            val = sign * min(float(mag.group(2)), 10)  # clamp outliers (e.g. %cl)
            color = '#22c55e' if sign > 0 else '#ef4444'
        elif c.startswith('+'):
            val, color = 1, '#22c55e'
        elif c.startswith(('-', '−')):
            val, color = -1, '#ef4444'
        elif c == '=':
            val, color = 0, '#8b949e'
        else:
            continue
        legs.append({
            'label': f"{l['date']} {l['leg'][:22]}",
            'raw': c, 'val': round(val, 1), 'color': color,
        })
    return {
        'labels': [x['label'] for x in legs],
        'values': [x['val'] for x in legs],
        'colors': [x['color'] for x in legs],
        'raw': [x['raw'] for x in legs],
    }


# ─── Cumulative win-rate trend (chronological) ────────────────────────────────

def _date_key(d: str):
    m = re.match(r'(\d{1,2})/(\d{1,2})', d)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return (99, 99)

def win_trend_data(results: dict) -> dict:
    played = [l for l in results['played'] if l['played'] and l['result'] in ('W', 'L')]
    played = sorted(played, key=lambda l: _date_key(l['date']))
    labels, cum, w = [], [], 0
    for i, l in enumerate(played, 1):
        if l['result'] == 'W':
            w += 1
        labels.append(f"{l['date']} {l['leg'][:18]}")
        cum.append(round(w / i * 100, 1))
    return {'labels': labels, 'values': cum}


# ─── Cumulative P/L (units) curve + real-dollar tally ─────────────────────────

def _parse_pl(pl_raw: str):
    """Return (value, is_dollar) from a P/L cell, or (None, _) if unparseable."""
    s = strip_md(pl_raw).replace('−', '-').replace(',', '').strip()
    if not s or s in ('—', '-', 'TBD'):
        return None, False
    is_dollar = '$' in s
    m = re.search(r'([+-]?[\d.]+)', s.replace('$', ''))
    if not m:
        return None, is_dollar
    return float(m.group(1)), is_dollar

def pl_curve_data(results: dict) -> dict:
    """Cumulative flat-1u UNITS P/L over decided tickets (chronological)."""
    tickets = [t for t in results['tickets'] if t['result'] in ('W', 'L')]
    tickets = sorted(tickets, key=lambda t: _date_key(t['date']))
    labels, cum_vals, running = [], [], 0.0
    dollar_pl, dollar_n = 0.0, 0
    for t in tickets:
        val, is_dollar = _parse_pl(t['pl'])
        if val is None:
            continue
        if is_dollar:
            dollar_pl += val
            dollar_n += 1
            continue  # real-$ tracked separately, not on the units curve
        running += val
        labels.append(f"{t['date']} {t['ticket'][:20]}")
        cum_vals.append(round(running, 2))
    return {'labels': labels, 'values': cum_vals,
            'final_units': round(running, 2),
            'dollar_pl': round(dollar_pl, 2), 'dollar_n': dollar_n}


# ─── CLV vs result (does CLV lead the scoreboard?) ────────────────────────────

def clv_vs_roi_data(results: dict) -> dict:
    """Per-leg chronological: cumulative win% vs cumulative CLV+ rate%."""
    legs = [l for l in (results['played'] + results['not_played'])
            if l['result'] in ('W', 'L')]
    legs = sorted(legs, key=lambda l: _date_key(l['date']))
    labels, winr, clvr = [], [], []
    w, n, cpos, cn = 0, 0, 0, 0
    for l in legs:
        n += 1
        if l['result'] == 'W':
            w += 1
        c = (l.get('clv') or '').strip()
        if c and c not in ('—', '-', '', 'TBD', 'MANUAL', 'PENDING'):
            cn += 1
            if c.startswith('+'):
                cpos += 1
        labels.append(f"{l['date']} {l['leg'][:16]}")
        winr.append(round(w / n * 100, 1))
        clvr.append(round(cpos / cn * 100, 1) if cn else None)
    return {'labels': labels, 'winrate': winr, 'clvrate': clvr}


# ─── HTML ─────────────────────────────────────────────────────────────────────

def render_html(rolls, results, parlays_list, summary, br_data, clv_data,
                trend_data, types, edges, fades, pl_data, clvroi_data) -> str:
    now = datetime.now()
    updated = now.strftime('%Y-%m-%d %H:%M ET')
    # Freshness: most recent parlay file date vs today
    stale = False
    if parlays_list:
        last = parlays_list[-1]['date']  # YYYY-MM-DD
        try:
            last_dt = datetime.strptime(last, '%Y-%m-%d')
            stale = (now - last_dt).days > 1
        except ValueError:
            pass
    fresh_cls = 'stale' if stale else 'fresh'
    fresh_txt = '⚠ data may be stale' if stale else '● live'
    calib = results['calib_buckets']

    # Bankroll chart JS
    if br_data['labels']:
        br_js = f"""
  new Chart(document.getElementById('brChart'), {{
    type: 'line',
    data: {{
      labels: {json.dumps(br_data['labels'])},
      datasets: [{{
        data: {json.dumps(br_data['values'])},
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59,130,246,0.08)',
        pointBackgroundColor: {json.dumps(br_data['colors'])},
        pointBorderColor: {json.dumps(br_data['colors'])},
        pointRadius: 6, pointHoverRadius: 8,
        tension: 0.25, fill: true, spanGaps: false,
      }}]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{
        legend: {{display: false}},
        tooltip: {{callbacks: {{label: ctx => ctx.parsed.y !== null ? '$' + ctx.parsed.y.toFixed(2) : 'break'}}}}
      }},
      scales: {{
        x: {{grid: {{color: '#21262d'}}, ticks: {{maxRotation: 50, font: {{size: 10}}}}}},
        y: {{grid: {{color: '#21262d'}}, ticks: {{callback: v => '$' + v}}, beginAtZero: false}}
      }}
    }}
  }});"""
        br_canvas = '<canvas id="brChart"></canvas>'
    else:
        br_js = ''
        br_canvas = '<p class="no-data">No bankroll rolls logged yet.</p>'

    # Calibration chart JS
    if calib:
        calib_labels = [b['band'] for b in calib]
        calib_actual = [b['hit_pct'] for b in calib]
        calib_mid = [b['midpoint'] for b in calib]
        calib_n = [f"n={b['n']} ({b['wins']}-{b['losses']})" for b in calib]
        cal_js = f"""
  new Chart(document.getElementById('calChart'), {{
    data: {{
      labels: {json.dumps(calib_labels)},
      datasets: [
        {{type: 'bar', label: 'Actual hit %', data: {json.dumps(calib_actual)},
         backgroundColor: 'rgba(59,130,246,0.75)', borderRadius: 3, order: 3}},
        {{type: 'bar', label: 'TrueP midpoint', data: {json.dumps(calib_mid)},
         backgroundColor: 'rgba(139,148,158,0.25)', borderRadius: 3, order: 2}},
        {{type: 'line', label: 'Perfect calibration', data: {json.dumps(calib_mid)},
         borderColor: '#f59e0b', borderWidth: 2, borderDash: [5,4],
         pointRadius: 3, pointBackgroundColor: '#f59e0b', fill: false, order: 1}}
      ]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{
        legend: {{position: 'top', labels: {{boxWidth: 10, font: {{size: 11}}}}}},
        tooltip: {{callbacks: {{afterBody: items => {json.dumps(calib_n)}[items[0].dataIndex]}}}}
      }},
      scales: {{
        x: {{grid: {{color: '#21262d'}}}},
        y: {{grid: {{color: '#21262d'}}, ticks: {{callback: v => v + '%'}}, min: 0, max: 100}}
      }}
    }}
  }});"""
        cal_canvas = '<canvas id="calChart"></canvas>'
    else:
        cal_js = ''
        cal_canvas = '<p class="no-data">Calibration data not yet available.</p>'

    # CLV chart JS
    if clv_data['labels']:
        clv_js = f"""
  new Chart(document.getElementById('clvChart'), {{
    type: 'bar',
    data: {{
      labels: {json.dumps(clv_data['labels'])},
      datasets: [{{
        data: {json.dumps(clv_data['values'])},
        backgroundColor: {json.dumps(clv_data['colors'])},
        borderRadius: 3,
      }}]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{
        legend: {{display: false}},
        tooltip: {{callbacks: {{label: ctx => 'CLV: ' + {json.dumps(clv_data['raw'])}[ctx.dataIndex]}}}}
      }},
      scales: {{
        x: {{grid: {{color: '#21262d'}}, ticks: {{maxRotation: 60, font: {{size: 9}}}}}},
        y: {{grid: {{color: '#21262d'}},
             ticks: {{callback: v => v > 0 ? '+' + v : v}}}}
      }}
    }}
  }});"""
        clv_canvas = '<canvas id="clvChart"></canvas>'
    else:
        clv_js = ''
        clv_canvas = '<p class="no-data">No CLV data captured yet.</p>'

    # Win-trend chart JS
    if trend_data['labels']:
        trend_js = f"""
  new Chart(document.getElementById('trendChart'), {{
    type: 'line',
    data: {{
      labels: {json.dumps(trend_data['labels'])},
      datasets: [{{
        data: {json.dumps(trend_data['values'])},
        borderColor: '#a78bfa', backgroundColor: 'rgba(167,139,250,0.08)',
        pointRadius: 2, pointHoverRadius: 5, borderWidth: 2,
        tension: 0.2, fill: true,
      }}]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{legend: {{display: false}},
        tooltip: {{callbacks: {{label: ctx => 'Cumulative: ' + ctx.parsed.y + '%'}}}}}},
      scales: {{
        x: {{grid: {{color: '#21262d'}}, ticks: {{maxRotation: 60, font: {{size: 9}}}}}},
        y: {{grid: {{color: '#21262d'}}, ticks: {{callback: v => v + '%'}}, min: 0, max: 100}}
      }}
    }}
  }});"""
        trend_canvas = '<canvas id="trendChart"></canvas>'
    else:
        trend_js = ''
        trend_canvas = '<p class="no-data">No decided legs yet.</p>'

    # Edge-bucket chart JS
    e_have = [e for e in edges if e['n'] > 0]
    if e_have:
        e_labels = [f"{e['label']}pp" for e in edges]
        e_hits = [e['hit'] for e in edges]
        e_ns = [f"n={e['n']}" if e['n'] else 'n=0' for e in edges]
        e_colors = ['rgba(34,197,94,0.7)' if (e['hit'] or 0) >= 50
                    else 'rgba(239,68,68,0.7)' for e in edges]
        edge_js = f"""
  new Chart(document.getElementById('edgeChart'), {{
    type: 'bar',
    data: {{
      labels: {json.dumps(e_labels)},
      datasets: [{{
        data: {json.dumps(e_hits)},
        backgroundColor: {json.dumps(e_colors)}, borderRadius: 3,
      }}]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{legend: {{display: false}},
        tooltip: {{callbacks: {{
          label: ctx => 'Hit ' + (ctx.parsed.y ?? 0) + '%',
          afterBody: items => {json.dumps(e_ns)}[items[0].dataIndex]}}}}}},
      scales: {{
        x: {{grid: {{color: '#21262d'}}}},
        y: {{grid: {{color: '#21262d'}}, ticks: {{callback: v => v + '%'}}, min: 0, max: 100}}
      }}
    }}
  }});"""
        edge_canvas = '<canvas id="edgeChart"></canvas>'
    else:
        edge_js = ''
        edge_canvas = '<p class="no-data">No edge data yet.</p>'

    # Cumulative P/L (units) chart JS
    if pl_data['labels']:
        pl_colors = '#22c55e' if pl_data['final_units'] >= 0 else '#ef4444'
        pl_js = f"""
  new Chart(document.getElementById('plChart'), {{
    type: 'line',
    data: {{
      labels: {json.dumps(pl_data['labels'])},
      datasets: [{{
        data: {json.dumps(pl_data['values'])},
        borderColor: '{pl_colors}', backgroundColor: 'rgba(34,197,94,0.06)',
        pointRadius: 3, pointHoverRadius: 6, borderWidth: 2, tension: 0.2, fill: true,
      }}]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{legend: {{display: false}},
        tooltip: {{callbacks: {{label: ctx => (ctx.parsed.y >= 0 ? '+' : '') + ctx.parsed.y + 'u'}}}}}},
      scales: {{
        x: {{grid: {{color: '#21262d'}}, ticks: {{maxRotation: 60, font: {{size: 9}}}}}},
        y: {{grid: {{color: '#21262d'}}, ticks: {{callback: v => (v >= 0 ? '+' : '') + v + 'u'}}}}
      }}
    }}
  }});"""
        pl_canvas = '<canvas id="plChart"></canvas>'
    else:
        pl_js = ''
        pl_canvas = '<p class="no-data">No decided tickets yet.</p>'

    # CLV-vs-ROI chart JS (two lines: cumulative win% vs cumulative CLV+ rate%)
    if clvroi_data['labels'] and any(v is not None for v in clvroi_data['clvrate']):
        clvroi_js = f"""
  new Chart(document.getElementById('clvroiChart'), {{
    type: 'line',
    data: {{
      labels: {json.dumps(clvroi_data['labels'])},
      datasets: [
        {{label: 'Cumulative win %', data: {json.dumps(clvroi_data['winrate'])},
         borderColor: '#3b82f6', backgroundColor: 'transparent',
         pointRadius: 1, borderWidth: 2, tension: 0.2}},
        {{label: 'Cumulative CLV+ rate %', data: {json.dumps(clvroi_data['clvrate'])},
         borderColor: '#f59e0b', backgroundColor: 'transparent', borderDash: [5,4],
         pointRadius: 1, borderWidth: 2, tension: 0.2, spanGaps: true}}
      ]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{legend: {{position: 'top', labels: {{boxWidth: 10, font: {{size: 11}}}}}}}},
      scales: {{
        x: {{grid: {{color: '#21262d'}}, ticks: {{maxRotation: 60, font: {{size: 9}}}}}},
        y: {{grid: {{color: '#21262d'}}, ticks: {{callback: v => v + '%'}}, min: 0, max: 100}}
      }}
    }}
  }});"""
        clvroi_canvas = '<canvas id="clvroiChart"></canvas>'
    else:
        clvroi_js = ''
        clvroi_canvas = '<p class="no-data">Not enough CLV data captured yet.</p>'

    # Fade tracking table
    fade_rows_html = ''
    for fd in fades:
        tested = fd['wins'] + fd['losses']
        if tested == 0:
            rec_cls, rec_txt = 'muted', 'untested'
        else:
            rate = fd['wins'] / tested
            rec_cls = 'pos' if rate >= 0.6 else ('neg' if rate < 0.4 else '')
            rec_txt = fd['record']
        st = fd['status'].upper()
        st_cls = ('pos' if 'ACTIVE' in st else 'neg' if 'RETIRED' in st
                  else 'muted')
        fade_rows_html += f"""
      <tr>
        <td class="mono">{fd['id']}</td>
        <td>{fd['name']}</td>
        <td class="muted small">{fd['reason']}</td>
        <td class="mono {rec_cls}">{rec_txt}</td>
        <td><span class="tag {st_cls}">{fd['status']}</span></td>
      </tr>"""

    # Recent played legs table
    decided = [l for l in results['played'] if l['played'] and l['result'] in ('W', 'L')]
    recent_legs = list(reversed(decided[-20:]))
    leg_rows_html = ''
    for l in recent_legs:
        rc = 'win' if l['result'] == 'W' else 'loss'
        edge_s = (f'+{l["edge"]:.1f}' if l['edge'] and l['edge'] >= 0
                  else f'{l["edge"]:.1f}' if l['edge'] else '—')
        edge_cls = 'pos' if l['edge'] and l['edge'] > 0 else ('neg' if l['edge'] and l['edge'] < 0 else '')
        clv_cls = 'pos' if l['clv'].startswith('+') else ('neg' if l['clv'].startswith('-') else '')
        star = ' <span class="star">*</span>' if l['legacy'] else ''
        leg_rows_html += f"""
      <tr>
        <td class="mono">{l['date']}</td>
        <td>{l['leg']}</td>
        <td><span class="tag">{l['type']}</span></td>
        <td class="mono">{l['price']}</td>
        <td class="mono">{f"{l['truep']:.0f}%" if l['truep'] else "—"}{star}</td>
        <td class="mono {edge_cls}">{edge_s}</td>
        <td class="mono {clv_cls}">{l['clv'] or '—'}</td>
        <td><span class="badge {rc}">{l['result']}</span></td>
      </tr>"""

    # Ticket rollup table
    ticket_rows_html = ''
    for t in reversed(results['tickets']):
        rc = 'win' if t['result'] == 'W' else ('loss' if t['result'] == 'L' else 'tbd')
        badge = '✅ WIN' if t['result'] == 'W' else ('❌ LOST' if t['result'] == 'L' else 'TBD')
        ticket_rows_html += f"""
      <tr>
        <td class="mono">{t['date']}</td>
        <td>{t['ticket']}</td>
        <td class="mono">{t['odds']}</td>
        <td class="mono">{t['pl']}</td>
        <td><span class="badge {rc}">{badge}</span></td>
      </tr>"""

    # Parlay history table
    parlay_rows_html = ''
    for p in reversed(parlays_list):
        rc = 'win' if p['outcome'] == 'W' else ('loss' if p['outcome'] == 'L' else 'tbd')
        badge_txt = '✅ W' if p['outcome'] == 'W' else ('❌ L' if p['outcome'] == 'L' else 'TBD')
        runs_str = ' / '.join(p['runs']) if p['runs'] else '—'
        parlay_rows_html += f"""
      <tr>
        <td class="mono">{p['date']}</td>
        <td class="mono muted">{runs_str}</td>
        <td><span class="badge {rc}">{badge_txt}</span></td>
        <td class="muted small">{p['summary']}</td>
      </tr>"""

    # Leg-type breakdown table
    type_rows_html = ''
    for t in types:
        edge_s = (f'+{t["avg_edge"]:.1f}' if t['avg_edge'] is not None and t['avg_edge'] >= 0
                  else f'{t["avg_edge"]:.1f}' if t['avg_edge'] is not None else '—')
        edge_cls = ('pos' if t['avg_edge'] and t['avg_edge'] > 0
                    else 'neg' if t['avg_edge'] and t['avg_edge'] < 0 else '')
        hit_cls = 'pos' if t['hit'] >= 50 else 'neg'
        roi_s = (f'+{t["roi"]:.1f}%' if t['roi'] is not None and t['roi'] >= 0
                 else f'{t["roi"]:.1f}%' if t['roi'] is not None else '—')
        roi_cls = ('pos' if t['roi'] and t['roi'] > 0
                   else 'neg' if t['roi'] and t['roi'] < 0 else '')
        type_rows_html += f"""
      <tr>
        <td>{t['type']}</td>
        <td class="mono">{t['n']}</td>
        <td class="mono">{t['record']}</td>
        <td class="mono {hit_cls}">{t['hit']}%</td>
        <td class="mono {edge_cls}">{edge_s}</td>
        <td class="mono {roi_cls}">{roi_s}</td>
      </tr>"""

    # Stat cards
    bal_txt = (f"${summary['bankroll_bal']:.2f}" if summary['bankroll_bal'] else "—")
    clv_pct_txt = f"{summary['clv_pct']}%" if summary['clv_total'] > 0 else "—"
    cs = summary['cur_streak']
    streak_big = (f"{'🔥 ' if cs >= 2 else ''}{cs}W" if cs > 0 else "0")
    streak_sub = (f"on a heater · best {summary['best_streak']}W" if summary['streak_active']
                  else f"last ticket lost · best {summary['best_streak']}W")

    # Ticket history pill timeline — last 15 decided tickets, oldest-left newest-right
    t_chron_all = sorted([t for t in results['tickets'] if t['result'] in ('W','L')],
                         key=lambda t: t['date'])
    t_recent = t_chron_all[-15:]
    pills_html = ''
    for t in t_recent:
        color = 'var(--green)' if t['result'] == 'W' else 'var(--red)'
        label = t['result']
        tip = f"{t['date']}: {t['ticket'][:50]}"
        pills_html += (
            f'<span class="tpill" style="background:{color}" title="{tip}">'
            f'{label}</span>'
        )
    if not pills_html:
        pills_html = '<span style="color:var(--muted);font-size:12px">No decided tickets yet</span>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#0d1117">
<title>MLB Parlay Dashboard</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230d1117'/%3E%3Ctext x='16' y='23' font-size='20' text-anchor='middle'%3E%E2%9A%BE%3C/text%3E%3C/svg%3E">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root {{
  --bg:#0d1117; --surf:#161b22; --surf2:#21262d; --border:#30363d;
  --text:#e6edf3; --muted:#8b949e; --green:#22c55e; --red:#ef4444;
  --yellow:#f59e0b; --blue:#3b82f6; --purple:#a78bfa;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:14px;line-height:1.5;font-feature-settings:'tnum' 1,'cv01' 1}}
a{{color:var(--blue);text-decoration:none}}
.num{{font-variant-numeric:tabular-nums}}

/* Header */
header{{background:linear-gradient(180deg,#161b22,#12161d);border-bottom:1px solid var(--border);padding:13px 24px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:30}}
header h1{{font-size:15px;font-weight:700;letter-spacing:-0.3px;display:flex;align-items:center;gap:7px}}
.updated{{font-size:11px;color:var(--muted)}}
.freshdot{{font-weight:600}}
.freshdot.fresh{{color:var(--green)}}
.freshdot.stale{{color:var(--red)}}

/* Sticky section nav */
nav.jump{{position:sticky;top:47px;z-index:20;background:rgba(13,17,23,.85);backdrop-filter:blur(8px);border-bottom:1px solid var(--border);padding:0 24px;display:flex;gap:2px;overflow-x:auto;-webkit-overflow-scrolling:touch}}
nav.jump a{{font-size:12px;color:var(--muted);padding:11px 13px;white-space:nowrap;border-bottom:2px solid transparent;font-weight:500;transition:color .15s,border-color .15s}}
nav.jump a:hover{{color:var(--text)}}
nav.jump a.active{{color:var(--text);border-bottom-color:var(--blue)}}

.wrap{{max-width:1320px;margin:0 auto;padding:18px 20px 48px}}
section{{scroll-margin-top:96px}}
.section-title{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--muted);margin:26px 0 11px;display:flex;align-items:center;gap:9px}}
.section-title::after{{content:'';flex:1;height:1px;background:linear-gradient(90deg,var(--border),transparent)}}

/* Hero scoreboard */
.hero{{background:linear-gradient(135deg,#171c24,#13171e);border:1px solid var(--border);border-radius:12px;padding:20px 22px;margin-bottom:6px;display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:14px;position:relative;overflow:hidden}}
.hero::before{{content:'';position:absolute;inset:0;background:radial-gradient(900px 120px at 0% 0%,rgba(59,130,246,.10),transparent)}}
.hero .h{{position:relative}}
.hero .h .lbl{{font-size:10px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);margin-bottom:6px}}
.hero .h .big{{font-size:32px;font-weight:800;letter-spacing:-1px;line-height:1}}
.hero .h .sub{{font-size:11px;color:var(--muted);margin-top:5px}}
.hero .divider{{position:absolute;left:0;top:14px;bottom:14px;width:1px;background:var(--border)}}

/* Stats */
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:11px}}
.stat{{background:var(--surf);border:1px solid var(--border);border-radius:9px;padding:14px 16px;transition:border-color .15s,transform .15s}}
.stat:hover{{border-color:#3d4654}}
.stat .lbl{{font-size:10px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin-bottom:6px}}
.stat .val{{font-size:23px;font-weight:700;letter-spacing:-.4px}}
.stat .sub{{font-size:11px;color:var(--muted);margin-top:3px}}

/* Legend */
.legend{{display:flex;flex-wrap:wrap;gap:14px;font-size:11px;color:var(--muted);margin:2px 0 4px;padding:9px 13px;background:var(--surf);border:1px solid var(--border);border-radius:8px}}
.legend span{{display:flex;align-items:center;gap:5px}}
.swatch{{width:11px;height:11px;border-radius:3px;display:inline-block}}
.tpill{{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:6px;font-size:11px;font-weight:700;color:#fff;cursor:default;transition:transform .1s}}
.tpill:hover{{transform:scale(1.2)}}
.tline{{display:flex;align-items:center;gap:5px;flex-wrap:wrap;padding:10px 13px;background:var(--surf);border:1px solid var(--border);border-radius:8px;margin:6px 0 4px}}
.tline .tlbl{{font-size:10px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);margin-right:4px}}

/* Cards */
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:6px}}
@media(max-width:820px){{.grid2{{grid-template-columns:1fr}}}}
.card{{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:18px;transition:border-color .15s}}
.card:hover{{border-color:#3d4654}}
.card h2{{font-size:13px;font-weight:600;margin-bottom:3px;letter-spacing:-.2px}}
.card .sub{{font-size:11px;color:var(--muted);margin-bottom:14px;line-height:1.4}}
.chart-wrap{{position:relative;height:224px}}
.chart-wrap-sm{{position:relative;height:150px}}

/* Tables */
.tcard{{background:var(--surf);border:1px solid var(--border);border-radius:10px;padding:18px;margin-bottom:6px;overflow-x:auto}}
.tcard h2{{font-size:13px;font-weight:600;margin-bottom:3px;letter-spacing:-.2px}}
.tcard .sub{{font-size:11px;color:var(--muted);margin-bottom:13px}}
table{{width:100%;border-collapse:collapse}}
thead th{{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.4px;text-align:left;padding:7px 10px;border-bottom:1px solid var(--border);position:sticky;user-select:none}}
thead th:hover{{color:var(--text)}}
tbody td{{padding:8px 10px;border-bottom:1px solid #1d232c;vertical-align:top}}
tbody tr:last-child td{{border-bottom:none}}
tbody tr:hover{{background:var(--surf2)}}
.mono{{font-family:'SF Mono',ui-monospace,SFMono-Regular,monospace;font-size:12px;font-variant-numeric:tabular-nums}}
.muted{{color:var(--muted)}}
.small{{font-size:12px}}
.pos{{color:var(--green)}}
.neg{{color:var(--red)}}
.star{{color:var(--yellow);font-size:10px}}

/* Badges & tags */
.badge{{display:inline-block;font-size:11px;font-weight:600;padding:2px 8px;border-radius:5px}}
.badge.win{{background:rgba(34,197,94,.15);color:var(--green)}}
.badge.loss{{background:rgba(239,68,68,.15);color:var(--red)}}
.badge.tbd{{background:rgba(139,148,158,.15);color:var(--muted)}}
.tag{{display:inline-block;font-size:10px;padding:1px 6px;border-radius:4px;background:var(--surf2);color:var(--muted)}}
.tag.pos{{background:rgba(34,197,94,.15);color:var(--green)}}
.tag.neg{{background:rgba(239,68,68,.15);color:var(--red)}}
.no-data{{text-align:center;padding:38px 20px;color:var(--muted);font-size:13px}}
.no-data::before{{content:'○';display:block;font-size:22px;opacity:.4;margin-bottom:8px}}
.note{{font-size:11px;color:var(--muted);margin:8px 0 6px;padding:9px 12px;background:var(--surf);border:1px solid var(--border);border-radius:7px;border-left:3px solid var(--blue);line-height:1.5}}

@media(max-width:560px){{
  header{{padding:11px 14px}}
  nav.jump{{top:43px;padding:0 12px}}
  .wrap{{padding:14px 12px 36px}}
  .card,.tcard{{padding:14px}}
  .hero{{padding:16px;gap:12px}}
  .hero .h .big{{font-size:26px}}
  .stat .val{{font-size:20px}}
  .chart-wrap{{height:200px}}
  thead th,tbody td{{padding:6px 7px;font-size:12px}}
}}
</style>
</head>
<body>
<header>
  <h1>⚾ MLB Parlay Dashboard</h1>
  <span class="updated"><span class="freshdot {fresh_cls}">{fresh_txt}</span> · Updated {updated}</span>
</header>
<nav class="jump">
  <a href="#overview">Overview</a>
  <a href="#bankroll">Bankroll</a>
  <a href="#trends">Trends</a>
  <a href="#pnl">P&amp;L</a>
  <a href="#fades">Fades</a>
  <a href="#tables">Tables</a>
</nav>
<div class="wrap">

  <section id="overview">
  <div class="hero">
    <div class="h">
      <div class="lbl">Ticket P/L (units)</div>
      <div class="big {'pos' if pl_data['final_units'] >= 0 else 'neg'}">{'+' if pl_data['final_units'] >= 0 else ''}{pl_data['final_units']}u</div>
      <div class="sub">flat-1u · +${pl_data['dollar_pl']:.0f} real / {pl_data['dollar_n']} $-staked</div>
    </div>
    <div class="h">
      <div class="lbl">Played leg record</div>
      <div class="big">{summary['leg_record']}</div>
      <div class="sub">{summary['leg_win_pct']}% · n={summary['total_legs']}</div>
    </div>
    <div class="h">
      <div class="lbl">Ticket win streak</div>
      <div class="big {'pos' if cs >= 2 else ''}">{streak_big}</div>
      <div class="sub">{streak_sub}</div>
    </div>
    <div class="h">
      <div class="lbl">CLV+ rate</div>
      <div class="big">{clv_pct_txt}</div>
      <div class="sub">beat the close · n={summary['clv_total']}</div>
    </div>
    <div class="h">
      <div class="lbl">Bankroll</div>
      <div class="big">{bal_txt}</div>
      <div class="sub">$10 rollover ladder</div>
    </div>
  </div>

  <div class="tline">
    <span class="tlbl">Last {len(t_recent)} tickets</span>
    {pills_html}
  </div>

  <div class="legend">
    <strong style="color:var(--text);font-weight:600">Colors:</strong>
    <span><i class="swatch" style="background:var(--green)"></i> win / +EV / beat close</span>
    <span><i class="swatch" style="background:var(--red)"></i> loss / −EV / missed close</span>
    <span><i class="swatch" style="background:var(--yellow)"></i> reference / legacy row</span>
    <span><i class="swatch" style="background:var(--muted)"></i> push / untested / no-bet</span>
  </div>

  <div class="section-title">Parlay tax — standalone vs parlay</div>
  <div class="stats">
    <div class="stat" style="border-left:3px solid var(--green)">
      <div class="lbl">Standalone legs (S)</div>
      <div class="val">{summary['s_record']} <span style="font-size:14px;color:var(--muted)">· {summary['s_pct']}%</span></div>
      <div class="sub">single +EV plays / bankroll rolls · n={summary['s_n']}</div>
    </div>
    <div class="stat" style="border-left:3px solid var(--red)">
      <div class="lbl">Parlay legs (P)</div>
      <div class="val">{summary['p_record']} <span style="font-size:14px;color:var(--muted)">· {summary['p_pct']}%</span></div>
      <div class="sub">legs ridden on a parlay ticket · n={summary['p_n']}</div>
    </div>
    <div class="stat">
      <div class="lbl">Ticket record</div>
      <div class="val">{summary['ticket_record']}</div>
      <div class="sub">parlay builds · n={summary['ticket_total']}</div>
    </div>
  </div>
  <p class="note">Doctrine claims parlays run near -EV chalk+vig. This split is the measurement: if standalones (S) outrun parlay legs (P) over a real sample, that's the evidence to keep the +200 chase eyes-open as entertainment, not strategy.</p>
  </section>

  <section id="bankroll">
  <div class="section-title">Bankroll &amp; calibration</div>
  <div class="grid2">
    <div class="card">
      <h2>Bankroll Curve</h2>
      <div class="sub">$10 rollover ladder — balance per roll (green = W, red = L)</div>
      <div class="chart-wrap">{br_canvas}</div>
    </div>
    <div class="card">
      <h2>Calibration</h2>
      <div class="sub">Bars = actual hit% · dashed amber line = perfect calibration (actual should meet the line)</div>
      <div class="chart-wrap">{cal_canvas}</div>
    </div>
  </div>

  </section>

  <section id="trends">
  <div class="section-title">Process trend &amp; edge predictiveness</div>
  <div class="grid2">
    <div class="card">
      <h2>Cumulative Win Rate</h2>
      <div class="sub">Running win% over all decided legs (chronological) — is the process improving?</div>
      <div class="chart-wrap">{trend_canvas}</div>
    </div>
    <div class="card">
      <h2>Hit Rate by Edge Bucket</h2>
      <div class="sub">Does a bigger devigged edge actually convert? (green ≥ 50%)</div>
      <div class="chart-wrap">{edge_canvas}</div>
    </div>
  </div>

  </section>

  <section id="pnl">
  <div class="section-title">Profit &amp; loss</div>
  <div class="grid2">
    <div class="card">
      <h2>Cumulative P/L (units)</h2>
      <div class="sub">Flat-1u running total over decided tickets — real money side: +${pl_data['dollar_pl']:.2f} over {pl_data['dollar_n']} $-staked tickets</div>
      <div class="chart-wrap">{pl_canvas}</div>
    </div>
    <div class="card">
      <h2>CLV vs Results</h2>
      <div class="sub">Cumulative win% (blue) vs CLV+ rate (amber) — doctrine: CLV leads ROI</div>
      <div class="chart-wrap">{clvroi_canvas}</div>
    </div>
  </div>

  <div class="card" style="margin-bottom:6px">
    <h2>CLV per Leg</h2>
    <div class="sub">Green = beat the close · red = missed · magnitude where logged, else ±1 by sign</div>
    <div class="chart-wrap-sm">{clv_canvas}</div>
  </div>
  <p class="note">CLV converges faster than ROI at small samples — it's the primary scoreboard. A sustained CLV+ rate is the clearest signal of process quality before ROI stabilises.</p>
  </section>

  <section id="fades">
  <div class="section-title">Record by leg type</div>
  <div class="tcard">
    <h2>Bet-type breakdown</h2>
    <div class="sub">All decided legs (played + recommended) · ROI = hypothetical flat-1u standalone from the American price</div>
    {'<table><thead><tr><th>Type</th><th>n</th><th>Record</th><th>Hit%</th><th>Avg edge</th><th>1u ROI</th></tr></thead><tbody>' + type_rows_html + '</tbody></table>' if types else '<p class="no-data">No typed legs yet.</p>'}
  </div>

  <div class="section-title">Fade registry tracking</div>
  <div class="tcard">
    <h2>Active fades &amp; their hit records</h2>
    <div class="sub">From fades.md · record = W (fade correct) − L (fade missed), counted from each entry's log · green ≥ 60%</div>
    {'<table><thead><tr><th>ID</th><th>Fade</th><th>Reason</th><th>Record</th><th>Status</th></tr></thead><tbody>' + fade_rows_html + '</tbody></table>' if fades else '<p class="no-data">No fades parsed.</p>'}
  </div>
  </section>

  <section id="tables">
  <div class="section-title">Recent played legs</div>
  <div class="tcard">
    <h2>Last 20 decided legs</h2>
    <div class="sub">Played=Y only · * = legacy/reconstructed TrueP (excluded from calibration)</div>
    {'<table><thead><tr><th>Date</th><th>Leg</th><th>Type</th><th>Price</th><th>TrueP</th><th>Edge</th><th>CLV</th><th>Result</th></tr></thead><tbody>' + leg_rows_html + '</tbody></table>' if decided else '<p class="no-data">No played legs logged yet.</p>'}
  </div>

  <div class="section-title">Ticket rollup</div>
  <div class="tcard">
    <h2>All parlay tickets</h2>
    <div class="sub">Flat 1u pre-6/4; real-dollar stakes from 6/5 onwards</div>
    {'<table><thead><tr><th>Date</th><th>Ticket</th><th>Odds</th><th>P/L</th><th>Result</th></tr></thead><tbody>' + ticket_rows_html + '</tbody></table>' if results['tickets'] else '<p class="no-data">No tickets logged yet.</p>'}
  </div>

  <div class="section-title">Parlay history</div>
  <div class="tcard">
    <h2>All daily builds</h2>
    <div class="sub">Most recent first</div>
    {'<table><thead><tr><th>Date</th><th>Runs</th><th>Result</th><th>Summary</th></tr></thead><tbody>' + parlay_rows_html + '</tbody></table>' if parlays_list else '<p class="no-data">No parlay files found.</p>'}
  </div>
  </section>

</div>
<script>
Chart.defaults.color = '#8b949e';
Chart.defaults.font.family = "-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif";
Chart.defaults.font.size = 11;
{br_js}
{cal_js}
{clv_js}
{trend_js}
{edge_js}
{pl_js}
{clvroi_js}

// ── Sortable tables (click a header to sort) ──
document.querySelectorAll('table').forEach(tbl => {{
  tbl.querySelectorAll('thead th').forEach((th, idx) => {{
    th.style.cursor = 'pointer';
    th.title = 'Click to sort';
    let asc = true;
    th.addEventListener('click', () => {{
      const tb = tbl.querySelector('tbody');
      const rows = Array.from(tb.querySelectorAll('tr'));
      rows.sort((a, b) => {{
        const x = a.children[idx].innerText.trim();
        const y = b.children[idx].innerText.trim();
        const nx = parseFloat(x.replace(/[^0-9.\\-]/g, ''));
        const ny = parseFloat(y.replace(/[^0-9.\\-]/g, ''));
        const bothNum = !isNaN(nx) && !isNaN(ny);
        if (bothNum) return asc ? nx - ny : ny - nx;
        return asc ? x.localeCompare(y) : y.localeCompare(x);
      }});
      asc = !asc;
      rows.forEach(r => tb.appendChild(r));
    }});
  }});
}});

// ── Scroll-spy: highlight the active nav link ──
const navLinks = Array.from(document.querySelectorAll('nav.jump a'));
const sections = navLinks.map(a => document.querySelector(a.getAttribute('href')));
const spy = () => {{
  const y = window.scrollY + 120;
  let active = 0;
  sections.forEach((s, i) => {{ if (s && s.offsetTop <= y) active = i; }});
  navLinks.forEach((a, i) => a.classList.toggle('active', i === active));
}};
window.addEventListener('scroll', spy, {{passive: true}});
spy();
</script>
</body>
</html>"""


# ─── Build pipeline ───────────────────────────────────────────────────────────

def build_all():
    """Parse every source + compute every derived dataset. Returns a dict."""
    rolls = parse_bankroll()
    results = parse_results_log()
    parlays_list = parse_parlays()
    fades = parse_fades()
    return {
        'rolls': rolls, 'results': results, 'parlays_list': parlays_list,
        'fades': fades,
        'summary': compute_summary(results, rolls),
        'br_data': bankroll_chart_data(rolls),
        'clv_data': clv_chart_data(results),
        'trend_data': win_trend_data(results),
        'types': type_breakdown(results),
        'edges': edge_buckets(results),
        'pl_data': pl_curve_data(results),
        'clvroi_data': clv_vs_roi_data(results),
    }


def render_from(d) -> str:
    return render_html(d['rolls'], d['results'], d['parlays_list'], d['summary'],
                       d['br_data'], d['clv_data'], d['trend_data'], d['types'],
                       d['edges'], d['fades'], d['pl_data'], d['clvroi_data'])


# ─── Self-test (parser invariants + calib.py reconciliation) ──────────────────

def _calib_units_pl():
    """Run calib.py and extract its derived units P/L (e.g. +5.58) for reconcile."""
    import subprocess
    out = subprocess.run(['python3', str(REPO / 'tools' / 'calib.py')],
                         capture_output=True, text=True, timeout=30).stdout
    m = re.search(r'P/L\s+([+-][\d.]+)u', out)
    tot = re.search(r'TOTAL\s+(\d+)\s', out)
    return (float(m.group(1)) if m else None,
            int(tot.group(1)) if tot else None)


def selftest() -> int:
    """Assert the dashboard parses real data & reconciles with calib.py. Exit 0/1."""
    fails = []
    def check(name, cond, detail=''):
        mark = '✓' if cond else '✗'
        print(f"  {mark} {name}" + (f"  ({detail})" if detail and not cond else ''))
        if not cond:
            fails.append(name)

    d = build_all()
    r = d['results']

    # 1. Parsers actually found rows — guards against a markdown reformat silently
    #    dropping every row (the real failure mode for regex-on-prose parsing).
    check("results_log: ≥20 played legs parsed", len(r['played']) >= 20,
          f"got {len(r['played'])}")
    check("results_log: ≥10 tickets parsed", len(r['tickets']) >= 10,
          f"got {len(r['tickets'])}")
    check("results_log: ≥3 calib buckets parsed", len(r['calib_buckets']) >= 3,
          f"got {len(r['calib_buckets'])}")
    check("fades.md: ≥15 entries parsed", len(d['fades']) >= 15,
          f"got {len(d['fades'])}")
    check("parlays/: ≥10 files parsed", len(d['parlays_list']) >= 10,
          f"got {len(d['parlays_list'])}")
    check("bankroll.md: ≥1 roll parsed", len(d['rolls']) >= 1,
          f"got {len(d['rolls'])}")

    # 2. Reconcile units P/L + calibration N against calib.py (the source of truth).
    calib_pl, calib_n = _calib_units_pl()
    dash_pl = d['pl_data']['final_units']
    check("P/L reconciles with calib.py",
          calib_pl is not None and abs(dash_pl - calib_pl) < 0.01,
          f"dashboard {dash_pl}u vs calib {calib_pl}u")
    dash_n = sum(b['n'] for b in r['calib_buckets'])
    check("calibration N reconciles with calib.py",
          calib_n is not None and dash_n == calib_n,
          f"dashboard {dash_n} vs calib {calib_n}")

    # 3. Records are internally consistent (W+L counts add up, no negatives).
    s = d['summary']
    check("S/P split non-negative & summed",
          s['s_n'] >= 0 and s['p_n'] >= 0 and (s['s_n'] + s['p_n']) > 0)

    # 4. Empty-season safety — the whole pipeline must not crash on no data.
    try:
        empty_results = {'played': [], 'not_played': [], 'tickets': [],
                         'calib_buckets': []}
        ed = {
            'rolls': [], 'results': empty_results, 'parlays_list': [], 'fades': [],
            'summary': compute_summary(empty_results, []),
            'br_data': bankroll_chart_data([]),
            'clv_data': clv_chart_data(empty_results),
            'trend_data': win_trend_data(empty_results),
            'types': type_breakdown(empty_results),
            'edges': edge_buckets(empty_results),
            'pl_data': pl_curve_data(empty_results),
            'clvroi_data': clv_vs_roi_data(empty_results),
        }
        html_empty = render_from(ed)
        check("empty-season renders without crashing", len(html_empty) > 1000)
    except Exception as e:
        check("empty-season renders without crashing", False, repr(e))

    # 5. The real render has no unrendered f-string artifacts.
    html = render_from(d)
    artifacts = re.findall(r"\{(?:summary|pl_data|json|fades|results)\b[^}]*\}", html)
    check("rendered HTML has no unrendered {python} artifacts", not artifacts,
          str(artifacts[:3]))
    check("rendered HTML wires all 7 charts", html.count('new Chart') == 7,
          f"got {html.count('new Chart')}")

    print(f"  ── dashboard self-test: {'ALL PASSED' if not fails else str(len(fails)) + ' FAILED'}")
    return 0 if not fails else 1


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    import sys
    if '--selftest' in sys.argv or '--check' in sys.argv:
        raise SystemExit(selftest())

    print("Parsing sources …")
    d = build_all()
    r = d['results']
    print(f"  {len(r['played'])} played · {len(r['not_played'])} not-played · "
          f"{len(r['tickets'])} tickets · {len(d['fades'])} fades · "
          f"{len(d['parlays_list'])} parlays · {len(d['rolls'])} rolls")

    print("Generating HTML …")
    html = render_from(d)

    DOCS.mkdir(exist_ok=True)
    (DOCS / ".nojekyll").write_text("")
    out = DOCS / "index.html"
    out.write_text(html, encoding='utf-8')
    print(f"  → {out}  ({len(html):,} bytes)")


if __name__ == '__main__':
    main()
