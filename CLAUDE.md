# Personal preferences

## MLB parlay analysis routine

When the user asks for an MLB parlay pick (or any MLB betting analysis), ALWAYS run the
full in-depth checklist below BEFORE recommending any leg. Do not rely on
generic "team X is favored" reasoning — verify each leg against the data.

### Pitcher props — verify before recommending
- Starter vs. swingman/opener status (e.g. how many of their appearances this
  season are actual starts vs. relief). A "starter" with <50% of appearances as
  starts has a pitch-count ceiling that kills Over K props. VERIFY the role
  claim against a current source (player's MLB.com page, FanGraphs game log)
  before using it to accept or reject a leg — a false role call (e.g. labeling
  an established starter "recently called up reliever") invalidates the entire
  leg analysis. Burned on 5/25/26 with a wrong call on Nolan McLean.
- Recent IP per start (last 3-5 starts) — does their workload support the K line?
- Season K/9 AND recent-form K/9 — flag if they diverge
- Opposing lineup K-rate vs. that pitcher's handedness, not just overall team rate.
  AUTO-FADE K Overs against known contact-heavy lineups even when the pitcher is
  elite-K (Royals burned a Will Warren 10.6+ K/9 Over with 3 Ks on 5/25/26;
  verify current K% rank for Royals/Astros/Guardians/D-backs before any K-Over leg)
- Manager's recent hook tendency (quick hook = lower K ceiling)
- Park and weather (cold/wind-in helps Ks, hot/wind-out hurts)
- Last meeting vs. same opponent if recent

### Hitter props — verify before recommending
- Recent form (last 10-15 games), not just season slash line. CRITICAL: a hitter
  in a documented slump is NOT a safe "Over 0.5 hits" play regardless of season avg
- Check for active slump narratives (news coverage of cold streaks)
- Splits vs. opposing starter's handedness
- Batting order slot (PA volume matters)
- Park factors and weather
- Bullpen matchup if starter exits early

### Moneyline / spread — verify before recommending
- Starting pitcher matchup quality (ERA, xFIP, recent form — not just season ERA)
- Starting pitcher's HR rate and first-inning issues
- Bullpen rest/availability — major factor for spread covers
- Lineup health (key bats in/out)
- Travel, day-after-night, getaway day spots
- Line movement vs. opener (sharp money signal)
- Modeled win probability if available — flag if it's below ~60% for a heavy fav

### Parlay construction rules
- Target true combined win probability ≥ 33% for a +200 parlay
- For a 3-leg parlay each leg should average ~70% true win prob
- Check correlation between legs (don't blindly stack team ML + pitcher K prop)
- For pitcher K-Over legs in a parlay, check alt K lines (e.g. Over 7.5 instead
  of the standard 8.5). If the standard line sits near 50/50, the alt line is
  usually the safer parlay leg even at -150 to -200; reserve the +EV standard
  line for stand-alone bets
- Confirm each leg's odds at a real sportsbook — never estimate
- If the user asks for ~+200, calculate the actual decimal product and show it

### Transparency requirements
- ALWAYS show the per-leg reasoning, not just the picks
- ALWAYS list legs considered AND rejected, with the reason for rejection
- ALWAYS flag when data is uncertain (lines not yet posted, lineup not set, weather
  unknown) rather than guessing
- If a leg looks borderline, say so — don't oversell
- Show the actual decimal math for the combined payout, not just "approximately +200"

### Default routine for "daily MLB parlay" requests
1. Pull today's schedule with confirmed probable pitchers — CROSS-CHECK probables
   from at least 2 sources (MLB.com + a beat-writer/preview article). Headlines
   often name multiple pitchers in a series preview; don't assume the first name
   mentioned is starting today. Also verify the pitcher → team attribution
   explicitly: search-result summaries can list "Pitcher A vs Pitcher B" with the
   names attributed to the wrong sides. Cross-check each pitcher's actual team
   before building a leg
2. For each candidate pitcher leg, run the pitcher-prop checklist
3. For each candidate hitter leg, check recent form + slump news
4. For each candidate ML/spread, verify SP quality and lineup health
5. Construct parlay, show per-leg odds and combined payout math
6. List rejected candidates with reasons
7. Flag any uncertainty and recommend re-checking lines at game time

## Learning and retrospectives

### Per-parlay logging
- After building a parlay, save the analysis to `parlays/YYYY-MM-DD.md` in this
  repo and commit + push it. The file should include: each leg with odds, the
  per-leg reasoning, true win prob estimate, the combined payout math,
  rejected candidates with reasons, and a `Result` section starting as TBD.
- When the user reports outcomes (e.g. "the Brewers ML hit", "Misi only got
  6 Ks"), update that day's file with per-leg results and a short
  retrospective. If something surprising burned us or worked, capture a
  one-line lesson in the file.

### Session-start review
- At the start of any session where the user might ask for a parlay, scan the
  3 most recent `parlays/*.md` files for filled-in results and captured
  lessons. Apply lessons before building today's parlay. If a recent result
  is still TBD, ask the user whether the parlay cashed before building a new one.

### Promoting recurring lessons
- When the same lesson appears in 2–3 different `parlays/*.md` files, promote
  it into the core routine in `CLAUDE.md` (the relevant checklist or rule).
  Reference the dates in the commit message so the lesson's history is
  traceable.

## Notifications and email drafts
- After completing an MLB parlay analysis, send a push notification with the
  summary unless the user says otherwise
- When the user asks to "draft an email with Gmail" — this environment does not
  have a Gmail integration, so save the draft to a file in /home/user/ and
  display the contents inline. Tell the user once that Gmail MCP isn't configured;
  don't repeat the disclaimer every time.
