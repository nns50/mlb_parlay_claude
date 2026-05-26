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
  ALSO AUTO-FADE K Overs on designated openers (planned 1-2 IP, followed by
  bulk reliever). Verify the "starter" is going for length, not an opener day,
  via team beat reporter or recent rotation pattern.
- Recent IP per start (last 3-5 starts) — does their workload support the K line?
- Season K/9 AND recent-form K/9 — flag if they diverge
- Opposing lineup K-rate vs. that pitcher's handedness, not just overall team rate.
  AUTO-FADE K Overs against known contact-heavy lineups even when the pitcher is
  elite-K (Royals burned a Will Warren 10.6+ K/9 Over with 3 Ks on 5/25/26;
  verify current K% rank for Royals/Astros/Guardians/D-backs before any K-Over leg)
- Manager's recent hook tendency (quick hook = lower K ceiling)
- Park and weather (cold/wind-in helps Ks, hot/wind-out hurts)
- Home-plate umpire's K-rate / zone tendencies. K-friendly umps inflate
  K Overs; tight-zone umps suppress them. Check the scheduled HP ump
  before any K-Over leg (e.g. Umpire Scorecards, Baseball Savant umpire
  splits). A bad zone is a hidden killer of an otherwise sharp K-Over.
- Last meeting vs. same opponent within ~14 days. Hitters adjust on the
  second look in a short window — K rates typically drop 10-15% in the
  second meeting. If the SP faced the same lineup in the last 14 days,
  downgrade K-Over confidence by one tier (or two tiers if the prior
  start went heavily Over — the adjustment effect compounds). Do NOT
  auto-fade entirely; a 70% leg becoming ~60% is still bettable.

### Hitter props — verify before recommending
- CONFIRM the official lineup is posted (~2-3 hours pre-game) before
  locking any hitter prop. A hitter on the bench cannot go Over 0.5
  hits. Getaway-day games and back-to-backs often see regulars rested
  without notice. If recommending pre-lineup, flag the leg as "PENDING
  LINEUP — re-verify before bet" rather than locking it in.
- Recent form (last 10-15 games), not just season slash line. CRITICAL: a hitter
  in a documented slump is NOT a safe "Over 0.5 hits" play regardless of season avg
- Check for active slump narratives (news coverage of cold streaks)
- Splits vs. opposing starter's handedness
- Batting order slot (PA volume matters)
- Batter-vs-pitcher (BvP) career numbers: only weight if sample is
  ≥30 PAs in the last 3 years. Below that the sample is noise — do not
  justify a hitter Over with "4-for-9 lifetime" type lines. Small-sample
  BvP that LOOKS bad is also not a fade signal on its own.
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
- Current team trends NOT captured by season record: last 7-10 game run
  differential, runs-per-game over last 7 days, bullpen ERA over last 14
  days, frequency of close/1-run games recently, current win/loss streak.
  A team can be 33-20 by record but grinding out 1-run wins lately — same
  ML price, very different in-game comfort. Apply to BOTH sides of the
  matchup: a 20-34 underdog that's gone 6-4 over its last 10 with a hot
  bullpen is a different bet than its record suggests. Reference burn:
  5/25/26 Dodgers ML -310 cashed but trailed into the 7th; the record
  oversold the comfort level.
- SPECIFICALLY watch for "was hot, now cold" teams — clubs that built a
  strong record in the first 30-40 games but have gone cold in the last
  10-15. The market price still reflects the earlier hot streak, so
  betting them as favorites is overpriced. Always check the last-15-games
  record and run differential, not just the season line.
  Current watch list (RE-VERIFY each session before using):
  - **Fade as favorites — "was hot, now cold"**: Cubs (5/25/26, still
    fading — 9-game losing streak as of 5/26/26), Rangers (5/25/26)
  - **Value as underdogs — "quietly hot"**: Pirates (added 5/26/26 —
    won 9 straight vs Cubs, improved offense from Cruz/Reynolds/O'Hearn)
- ACTIVELY SCAN each day's slate for new candidates fitting this pattern,
  in BOTH directions:
    - "Was hot, now cold" — add to the fade watch list above
    - "Was cold, now quietly hot" — note as potential underdog value
      (good record-vs-form mismatch in the bettor's favor)
  When a new team is identified during analysis, update the watch list
  in this file and commit the change (one-line PR is fine) so the next
  session inherits it. When a watched team's form recovers (last-15
  back above .550 with positive run differential), remove it from the
  list with a commit explaining the reason and the date — keeping the
  list current is part of the routine, not an optional step.

### Parlay construction rules
- Target true combined win probability ≥ 33% for a +200 parlay
- For a 3-leg parlay each leg should average ~70% true win prob
- Same-game leg stacking is correlation-sign dependent. Don't default
  to "always stack" or "never stack" — identify the SIGN first:
    - POSITIVELY correlated (team ML + their SP's K Over; team total
      Over + team ML; F5 Under + Game Under): at independent-leg odds
      this is +EV for the bettor (true combined prob > the product
      of standalone probs). Books offer SGP pricing to reclaim this
      edge — when SGP is offered, compare the SGP price to the
      independent product and take whichever pays more. Today's
      Brewers ML + Misi K Over (5/25/26) was a positively-correlated
      stack that cashed at independent pricing.
    - NEGATIVELY correlated (team ML + opposing SP's K Over; team
      total Over + opposing team ML): at independent-leg odds the
      true combined prob is LOWER than the product implies — either
      skip the stack or downgrade the combined-prob estimate manually
      when building the parlay.
    - Unclear correlation: default to one leg per game.
  And when describing positively correlated stacks in the analysis,
  the correlation should UP-adjust the combined-prob estimate, not
  down-adjust it (the 5/25/26 parlay file mis-described this).
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
- NEVER frame a leg as "safe", "easy", "lock", or "free money" regardless of
  price. Use the actual win-probability number, and explicitly flag in-game
  variance factors (e.g. starter ERA > 4.50, weak bullpen, opponent on a hot
  run-scoring streak). A heavy-fav ML at -310 is still ~25% to lose and the
  margin of a win is a separate dimension from W/L. Burned trust on 5/25/26
  framing Dodgers ML as "the safer high-probability choice" — LAD trailed
  into the 7th before winning.

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
