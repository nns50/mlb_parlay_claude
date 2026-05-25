# Personal preferences

## MLB parlay analysis routine

When the user asks for an MLB parlay pick (or any MLB betting analysis), ALWAYS run the
full in-depth checklist below BEFORE recommending any leg. Do not rely on
generic "team X is favored" reasoning — verify each leg against the data.

### Pitcher props — verify before recommending
- Starter vs. swingman/opener status (e.g. how many of their appearances this
  season are actual starts vs. relief). A "starter" with <50% of appearances as
  starts has a pitch-count ceiling that kills Over K props.
- Recent IP per start (last 3-5 starts) — does their workload support the K line?
- Season K/9 AND recent-form K/9 — flag if they diverge
- Opposing lineup K-rate vs. that pitcher's handedness, not just overall team rate
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
   mentioned is starting today
2. For each candidate pitcher leg, run the pitcher-prop checklist
3. For each candidate hitter leg, check recent form + slump news
4. For each candidate ML/spread, verify SP quality and lineup health
5. Construct parlay, show per-leg odds and combined payout math
6. List rejected candidates with reasons
7. Flag any uncertainty and recommend re-checking lines at game time

## Notifications and email drafts
- After completing an MLB parlay analysis, send a push notification with the
  summary unless the user says otherwise
- When the user asks to "draft an email with Gmail" — this environment does not
  have a Gmail integration, so save the draft to a file in /home/user/ and
  display the contents inline. Tell the user once that Gmail MCP isn't configured;
  don't repeat the disclaimer every time.
