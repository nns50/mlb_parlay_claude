#!/usr/bin/env python3
"""
Generate docs/index.html — read-only analytics dashboard.
Parses bankroll.md, results_log.md, parlays/*.md.
Run after any build to refresh the Pages site.
"""
import re, json
from pathlib import Path
from datetime import datetime

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


# ─── Summary stats ────────────────────────────────────────────────────────────

def compute_summary(results: dict, rolls: list[dict]) -> dict:
    played = [l for l in results['played'] if l['played'] and l['result'] in ('W', 'L')]
    wins = sum(1 for l in played if l['result'] == 'W')
    losses = len(played) - wins

    t_decided = [t for t in results['tickets'] if t['result'] in ('W', 'L')]
    t_wins = sum(1 for t in t_decided if t['result'] == 'W')

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

    # ROI from ticket rollup (flat-1u)
    staked = len(t_decided)
    pl_legs = [l for l in results['played'] if l['played'] and l['result'] in ('W', 'L')]
    return {
        'leg_record': f"{wins}-{losses}",
        'leg_win_pct': round(wins / max(wins + losses, 1) * 100, 1),
        'total_legs': wins + losses,
        'ticket_record': f"{t_wins}-{len(t_decided) - t_wins}",
        'ticket_total': len(t_decided),
        'clv_pos': clv_pos, 'clv_total': len(clv_list),
        'clv_pct': round(clv_pos / max(len(clv_list), 1) * 100, 1),
        'bankroll_bal': bal,
    }


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
        if c.startswith('+'):
            val, color = 1, '#22c55e'
        elif c.startswith('-'):
            val, color = -1, '#ef4444'
        elif c == '=':
            val, color = 0, '#8b949e'
        else:
            continue
        legs.append({
            'label': f"{l['date']} {l['leg'][:22]}",
            'raw': c, 'val': val, 'color': color,
        })
    return {
        'labels': [x['label'] for x in legs],
        'values': [x['val'] for x in legs],
        'colors': [x['color'] for x in legs],
        'raw': [x['raw'] for x in legs],
    }


# ─── HTML ─────────────────────────────────────────────────────────────────────

def render_html(rolls, results, parlays_list, summary, br_data, clv_data) -> str:
    updated = datetime.now().strftime('%Y-%m-%d %H:%M ET')
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
    type: 'bar',
    data: {{
      labels: {json.dumps(calib_labels)},
      datasets: [
        {{label: 'Actual hit %', data: {json.dumps(calib_actual)},
         backgroundColor: 'rgba(59,130,246,0.75)', borderRadius: 3}},
        {{label: 'TrueP midpoint', data: {json.dumps(calib_mid)},
         backgroundColor: 'rgba(139,148,158,0.25)', borderRadius: 3}}
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
        y: {{grid: {{color: '#21262d'}}, min: -1.5, max: 1.5,
             ticks: {{callback: v => v > 0 ? '+ beat' : v < 0 ? '− missed' : 'even'}}}}
      }}
    }}
  }});"""
        clv_canvas = '<canvas id="clvChart"></canvas>'
    else:
        clv_js = ''
        clv_canvas = '<p class="no-data">No CLV data captured yet.</p>'

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

    # Stat cards
    bal_txt = (f"${summary['bankroll_bal']:.2f}" if summary['bankroll_bal'] else "—")
    clv_pct_txt = f"{summary['clv_pct']}%" if summary['clv_total'] > 0 else "—"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MLB Parlay Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root {{
  --bg:#0d1117; --surf:#161b22; --surf2:#21262d; --border:#30363d;
  --text:#e6edf3; --muted:#8b949e; --green:#22c55e; --red:#ef4444;
  --yellow:#f59e0b; --blue:#3b82f6; --purple:#a78bfa;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:14px;line-height:1.5}}
a{{color:var(--blue);text-decoration:none}}
header{{background:var(--surf);border-bottom:1px solid var(--border);padding:14px 24px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:10}}
header h1{{font-size:16px;font-weight:600;letter-spacing:-0.3px}}
.updated{{font-size:11px;color:var(--muted)}}
.wrap{{max-width:1380px;margin:0 auto;padding:20px 20px 40px}}
.section-title{{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);margin:24px 0 10px}}

/* Stats */
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:4px}}
.stat{{background:var(--surf);border:1px solid var(--border);border-radius:8px;padding:14px 16px}}
.stat .lbl{{font-size:10px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin-bottom:5px}}
.stat .val{{font-size:22px;font-weight:700}}
.stat .sub{{font-size:11px;color:var(--muted);margin-top:2px}}

/* Cards */
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}}
@media(max-width:800px){{.grid2{{grid-template-columns:1fr}}}}
.card{{background:var(--surf);border:1px solid var(--border);border-radius:8px;padding:18px}}
.card h2{{font-size:13px;font-weight:600;margin-bottom:2px}}
.card .sub{{font-size:11px;color:var(--muted);margin-bottom:14px}}
.chart-wrap{{position:relative;height:220px}}
.chart-wrap-sm{{position:relative;height:150px}}

/* Tables */
.tcard{{background:var(--surf);border:1px solid var(--border);border-radius:8px;padding:18px;margin-bottom:14px;overflow-x:auto}}
.tcard h2{{font-size:13px;font-weight:600;margin-bottom:2px}}
.tcard .sub{{font-size:11px;color:var(--muted);margin-bottom:12px}}
table{{width:100%;border-collapse:collapse}}
thead th{{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.4px;text-align:left;padding:6px 10px;border-bottom:1px solid var(--border)}}
tbody td{{padding:7px 10px;border-bottom:1px solid var(--border);vertical-align:top}}
tbody tr:last-child td{{border-bottom:none}}
tbody tr:hover{{background:var(--surf2)}}
.mono{{font-family:'SF Mono',ui-monospace,monospace;font-size:12px}}
.muted{{color:var(--muted)}}
.small{{font-size:12px}}
.pos{{color:var(--green)}}
.neg{{color:var(--red)}}
.star{{color:var(--yellow);font-size:10px}}

/* Badges & tags */
.badge{{display:inline-block;font-size:11px;font-weight:600;padding:2px 8px;border-radius:4px}}
.badge.win{{background:rgba(34,197,94,.15);color:var(--green)}}
.badge.loss{{background:rgba(239,68,68,.15);color:var(--red)}}
.badge.tbd{{background:rgba(139,148,158,.15);color:var(--muted)}}
.tag{{display:inline-block;font-size:10px;padding:1px 6px;border-radius:3px;background:var(--surf2);color:var(--muted)}}
.no-data{{text-align:center;padding:40px 20px;color:var(--muted);font-size:13px}}
.note{{font-size:11px;color:var(--muted);margin-top:8px;padding:8px 10px;background:var(--surf2);border-radius:4px;border-left:2px solid var(--border)}}
</style>
</head>
<body>
<header>
  <h1>⚾ MLB Parlay Dashboard</h1>
  <span class="updated">Updated {updated}</span>
</header>
<div class="wrap">

  <div class="section-title">Overview</div>
  <div class="stats">
    <div class="stat">
      <div class="lbl">Played leg record</div>
      <div class="val">{summary['leg_record']}</div>
      <div class="sub">{summary['leg_win_pct']}% · n={summary['total_legs']}</div>
    </div>
    <div class="stat">
      <div class="lbl">Ticket record</div>
      <div class="val">{summary['ticket_record']}</div>
      <div class="sub">parlay builds · n={summary['ticket_total']}</div>
    </div>
    <div class="stat">
      <div class="lbl">CLV+ rate</div>
      <div class="val">{clv_pct_txt}</div>
      <div class="sub">beat the close · n={summary['clv_total']}</div>
    </div>
    <div class="stat">
      <div class="lbl">Bankroll balance</div>
      <div class="val">{bal_txt}</div>
      <div class="sub">$10 rollover ladder</div>
    </div>
  </div>

  <div class="section-title">Bankroll &amp; Calibration</div>
  <div class="grid2">
    <div class="card">
      <h2>Bankroll Curve</h2>
      <div class="sub">$10 rollover ladder — balance per roll (green = W, red = L)</div>
      <div class="chart-wrap">{br_canvas}</div>
    </div>
    <div class="card">
      <h2>Calibration</h2>
      <div class="sub">Actual hit rate vs TrueP midpoint per bucket (non-legacy played legs)</div>
      <div class="chart-wrap">{cal_canvas}</div>
    </div>
  </div>

  <div class="section-title">Closing Line Value</div>
  <div class="card" style="margin-bottom:14px">
    <h2>CLV per Leg</h2>
    <div class="sub">Green = beat the close · Red = missed · h2h ML only; props/RL are manual</div>
    <div class="chart-wrap-sm">{clv_canvas}</div>
  </div>
  <p class="note">CLV converges faster than ROI at small samples — it's the primary scoreboard. A sustained CLV+ rate is the clearest signal of process quality before ROI stabilises.</p>

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

</div>
<script>
Chart.defaults.color = '#8b949e';
Chart.defaults.font.family = "-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif";
Chart.defaults.font.size = 11;
{br_js}
{cal_js}
{clv_js}
</script>
</body>
</html>"""


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("Parsing bankroll.md …")
    rolls = parse_bankroll()
    print(f"  {len(rolls)} rolls")

    print("Parsing results_log.md …")
    results = parse_results_log()
    print(f"  {len(results['played'])} played legs · "
          f"{len(results['not_played'])} not-played · "
          f"{len(results['tickets'])} tickets · "
          f"{len(results['calib_buckets'])} calib buckets")

    print("Parsing parlays/ …")
    parlays_list = parse_parlays()
    print(f"  {len(parlays_list)} files")

    summary = compute_summary(results, rolls)
    br_data = bankroll_chart_data(rolls)
    clv_data = clv_chart_data(results)

    print("Generating HTML …")
    html = render_html(rolls, results, parlays_list, summary, br_data, clv_data)

    DOCS.mkdir(exist_ok=True)
    (DOCS / ".nojekyll").write_text("")
    out = DOCS / "index.html"
    out.write_text(html, encoding='utf-8')
    print(f"  → {out}  ({len(html):,} bytes)")


if __name__ == '__main__':
    main()
