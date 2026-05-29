# Personal preferences

## MLB parlay analysis routine

When the user asks for an MLB parlay pick (or any MLB betting analysis), ALWAYS run the
full in-depth checklist below BEFORE recommending any leg. Do not rely on
generic "team X is favored" reasoning — verify each leg against the data.

### MANDATORY SP-data-freshness field (gates EVERY starting-pitcher leg)
This applies to ANY leg that leans on a starting pitcher — a K prop AND an
ML/spread/total read built on SP quality. A run may NOT recommend OR reject an
SP-based leg until this field is filled in and shown in the build. It is a hard
gate, not a guideline.

For each SP referenced in a build, the writeup MUST include a checked line in
this exact form:

  - [ ] **SP DATA FRESHNESS — <Pitcher>:** ERA <x.xx> / WHIP <x.xx> / season K/9
        <x.x>, pulled from <date-stamped source> dated <YYYY-MM-DD>; **CONFIRMED
        the line includes the pitcher's most recent start** (last start: <date>
        vs <opp> — <IP/ER/K>). Recent-form K/9 over last 3-5 starts: <x.x>.

Rules:
- The source MUST be date-stamped to today's slate (a game-day preview, a recent
  game story, or a start-by-start game log) — NOT a bare stat aggregate, which
  can be frozen at a prior start. Cross-check against a 2nd source when the
  numbers look off or sources disagree.
- If you cannot confirm the line is current (no date-stamped source found, or two
  sources conflict and can't be reconciled), mark the stat **UNVERIFIED** and
  treat the leg as **PENDING — do not lock**, rather than guessing.
- This field is REQUIRED even when the pitcher was NOT swapped and is correctly
  named — staleness hits established starters in hot/cold swings too.
- Reference burn: 5/29/26 Imanaga — the 09:00 run used a 2.32 ERA frozen at his
  May 13 start while his CURRENT ERA was 4.04 after two shellings (8 R vs MIL,
  then 6 IP/7 ER/3 HR vs HOU on 5/24). A filled freshness field catches this
  PRE-publish. (Note: K rate can stay intact even when ERA craters — he K'd 6
  in the 5/24 shelling — so verify, then separate the run-prevention axis from
  the per-pitch-K axis; see the Cole/Skenes refinement below.)

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
- **The FAVORITE's OWN starter ERA is a hard ceiling on ML safety.** A model can
  list a team at 60-62% purely because the OPPONENT's starter is worse, but if
  the favorite's own SP carries a bad ERA (~5.00+), the game is a high-variance
  shootout, not a safe anchor — the favorite can be blown out even as the
  "right" side. DISCOUNT the favorite ML by ~5pp and DO NOT use it as a parlay
  anchor when its own starter's ERA is ~5.00+. Especially when BOTH starters are
  bad ("two-bad-SP shootout"), treat the game as a coin-flip-plus, not a 60%
  leg. Reference burn: 5/28/26 Tigers ML -130 (Flaherty 5.94 ERA vs G-Rod 10.61)
  — I rated it ~61% and made it the ANCHOR; DET lost 7-1. I had even flagged
  "Flaherty leaky → live but uncomfortable" and still anchored on it. The flagged
  risk WAS the outcome — when you name a blow-out risk on the favorite's starter,
  let it move the number, don't just note it.
- Bullpen rest/availability — major factor for spread covers
- Lineup health (key bats in/out)
- Travel, day-after-night, getaway day spots
- Line movement vs. opener (sharp money signal)
- Modeled win probability if available — flag if it's below ~60% for a heavy fav
- **DECOMPOSE the favorite's model win-prob: "good team" vs "bad opponent."**
  A model can list a favorite at 60-62% purely because the OPPONENT's starter is
  awful — that is NOT the same as "this is a team you can trust to win." Before
  anchoring ANY favorite ML, display its OWN season record AND last-15 form
  RIGHT NEXT TO the model number, and explicitly ask: is this number driven by
  the favorite being good, or just by the opponent being bad? If it's
  opponent-driven AND the favorite is a sub-.500 / poorly-playing team, fade it
  as an anchor — trust the "this team has been bad" read over the inflated
  number. Reference burn: 5/28/26 Tigers ML -130 was 62% only because G-Rod
  (10.61 ERA) was awful; Detroit itself had been playing badly and got blown out
  7-1. The gut read ("they've been bad") was correct and the number was
  misleading. Make the favorite's own record/form a REQUIRED, visible field in
  every build so this check happens before locking, not after losing.
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
  - **Fade as favorites — "was hot, now cold" / just plain cold**: Cubs
    (5/25/26; 0-10 skid then WON 3 straight 5/27-5/28 incl. beating Skenes 7-2
    on 5/28 — recovering, but KEEP on fade-as-fav list until last-15 climbs
    back above .550), Rangers (5/25/26; fade RE-CONFIRMED 5/28 — lost 5-1 to
    HOU, dropped 6 of last 7, season-worst 6 games under .500), **Tigers
    (ADDED 5/28/26 — 22-35, 4-18 since May 4, lost 7 straight series; the
    5/28 Tigers ML -130 anchor got blown out 7-1. Do NOT lay a price on DET as
    a favorite; the market keeps overrating them off the season-opening record
    and a soft-schedule SP line)**
  - **Value as underdogs — "quietly hot"**: White Sox (ADDED 5/28/26 — 29-27,
    won 12 of last 18, beat MIN 6-2 behind Davis Martin (8-1) on 5/28, run diff
    back to even for the first time since Opening Day; a genuinely improving
    club the market still prices soft); Pirates (added 5/26/26 — "quietly hot"
    tag now COLD: lost 10-4 (5/27) and 7-2 (5/28) to the Cubs, run ended —
    treat as neutral, NOT underdog value, until it re-heats); Twins (added
    5/28/26 — quietly-hot tag now COOLING: just lost 3 of 4 to CWS incl. 6-2 on
    5/28. Bullpen-strength-since-5/9 read still holds, but the offense went
    quiet — keep only as soft-matchup value, and remember the 5/28 CAVEAT: the
    tag does NOT override a confirmed ace-at-home, MIN got beat 6-1 by Davis
    Martin (1.14 home ERA). A clear pitching edge beats a recent-form narrative.)
    Honorable-mention watch: Angels (surging — won 5 of 6 incl. 2 of 3 at DET
    through 5/28) and Astros (won 6 of last 7 through 5/28, but Astros stay an
    AUTO-FADE K-Over lineup — back them on ML/total only, never opposing K-Over).
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
- **Avoid -350-or-worse ML legs as parlay anchors for a +200 target.** A
  heavy-fav ML (e.g. -420) contributes almost nothing to the payout (decimal
  ~1.24) while still carrying ~20% bust risk, which forces the rest of the
  ticket to take on excessive risk to reach +200. Price efficiency matters as
  much as raw hit rate when building a payout-targeted parlay. When a steep fav
  is your instinct, first look for a better-priced anchor (~-150 to -200, ~60-65%
  true win prob) from another game that delivers comparable safety with far more
  payout contribution. Reference win: 5/27/26 — I anchored Builds E/F on LAD ML
  -420; the user correctly faded it as poor value and substituted Yankees ML
  -156, and the +210 ticket (NYY ML + Sanchez Over 6.5 K) cashed. I had even
  surfaced that exact NYY combo in Build D before talking myself back into the
  heavy LAD anchor on hit-rate grounds. Don't default to the heavy-fav ML three
  days running (5/25 -310, 5/26 -235, 5/27 -420) — lead with the value anchor.
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
- BUT — never estimate alt-K prices when computing parlay payouts. Pull the
  exact alt price from a real book before publishing the decimal math. Books
  routinely juice the one-K-lower alt to -300 to -500 on elite-K arms that
  have a 100%-recent-Over-rate at that threshold (5/26/26 burn: Burns alt 5.5
  was estimated at ~-185 but the user's book priced it ~-400; the parlay
  paid +103, not the published +221). If the alt comes back juicier than the
  estimate, EITHER move that leg back to the standard line (accepting lower
  hit rate for better payout) OR drop the leg entirely.
- **A surprisingly LONG price on a liquid prop is information, not a gift —
  defer to the market over your raw model.** When the posted price implies a
  probability far below your model's estimate on a mainstream, liquid market
  (e.g. a plus-money Over on a high-K/9 arm), the gap almost always means the
  market is pricing something your model can't see — usually start-length /
  short-leash risk the raw K/9 number hides (cf. the Strider structural rule
  below). Books do NOT leave 15-20pp on a liquid K prop. Treat the line as a
  hard prior: shade your estimate toward the market, do NOT bet it as "free
  value," and re-derive the leg's true prob from BOTH posted lines when you
  have them. Reference burn: 5/29/26 Imanaga — I rated Over 5.5 K ~68%, but the
  book had it +120 (~44%) with Over 4.5 K at -200 (~64%); the two prices pinned
  a coin-flip distribution (median ~5 K) and exposed my 68% as overconfident.
  The phantom edge had anchored the whole "best win chance" ticket. RELATEDLY,
  decompose EVERY favorite's model number even on non-headline mid-slate games
  (same date: Astros ML 55.4% was a 25-32 team propped up by a thin-sample hot
  SP vs the 33-20 Brewers — the decompose rule flagged it only once I ran it).
- For K-Over legs on pitchers with STRUCTURAL pitch-count uncertainty (Tommy
  John return, MLB debut, post-IL return, opener-conversion, manager's
  documented quick hook), drop ONE alt deeper than the "value" line even at
  heavy juice. The standard K/9-based "value" alt assumes a normal start-length
  distribution; these pitchers' start-length distribution has a left tail the
  raw K/9 number can't see. Reference burn: 5/26/26 Strider (TJ return, 4 starts
  back) — recommended Over 5.5 K at -132 as the "value leg" (+15pp edge per my
  model); user overrode to Over 4.5 K at ~-625; Strider finished with exactly
  5 Ks, so 4.5 cashed and 5.5 would have busted. The user's variance-respecting
  choice saved the parlay (+216 vs $0). My true-prob estimate of 72% on Over 5.5
  was overconfident; actual probability was closer to 50-55%.
  - REFINEMENT (5/27/26 Cole): the structural-uncertainty fade is about
    START-LENGTH variance, NOT a downgrade of the pitcher's per-pitch K ability.
    Do NOT let a single throttled ramp-up start collapse your estimate of an
    elite arm's stuff. Separate the two axes: (a) start length / pitch cap =
    genuinely uncertain on a TJ/debut/IL return → still fade the K-Over on a
    parlay or take the deeper alt; (b) per-pitch whiff rate = anchor it to the
    pitcher's established true talent, NOT to one small-sample outing. Reference:
    in Build D (5/27) I let Cole's 2-K first start back drag my estimate of his
    K ability down to "diminished arm," then dropped Yankees ML true win prob to
    ~60% partly on that. Two starts back he went 10 K in 79 pitches, 0 BB, FB
    96.3 mph avg / 98.4 top — velocity back to pre-TJ baseline, 10 K against a
    K-resistant KC lineup, his first 10-K game since before the surgery. The
    velocity + whiff-efficiency (10 K on 79 pitches can't be a called-strike
    grind) confirmed the stuff was back. The pitch cap was still real (pulled at
    79 pitches / 6.2 IP), so the start-length fade held — but I had over-corrected
    the NYY ML down; with stuff back it deserved ~68-70%, making the -156 real
    value (and it cashed). CHECK CONFIRMED-VELOCITY before assuming a returning
    arm's K rate is suppressed: if velo is back to baseline, model the K rate at
    true talent with a capped pitch count, not at the ramp-up start's counting line.
- Confirm each leg's odds at a real sportsbook — never estimate
- If the user asks for ~+200, calculate the actual decimal product and show it
- **Heavy-mismatch matchups blow up the alt-K + favorite-ML recipe.** When the
  model's true win prob on the favorite is ≥70% AND the pitcher matchup is a
  clear edge (e.g. ace vs bottom-tier offense), expect ALL the standard
  recipe legs to be priced much heavier than estimates: ML often -350 to -500,
  one-K-lower alt often -800 to -1300, two-K-lower alt -250 to -400. The
  "deeper alt for safety" rule then destroys parlay payout, because the
  market has already priced the safety into the line. Reference burn:
  5/27/26 LAD/COL — Ohtani vs Sugano. My estimates: LAD ML -230, Ohtani
  Over 4.5 K -275, Sanchez Over 5.5 K -180. Actual book: -420, -1250, -275.
  Build B as published would have paid -125 instead of +200. **In these
  heavy-mismatch matchups, use the STANDARD K line (the "value alt"),
  not the deeper alt — the deeper alt becomes a near-lock at zero
  payout — AND substitute the spread (-1.5 RL) for the ML to recover
  payout.** The spread is the only knob with enough range to keep a
  parlay near +200 when the matchup is this lopsided.
  **BUT — when the market has already moved the spread to -150 or
  worse**, the spread is also priced into "fairly safe" territory and
  the substitution rule above doesn't recover the payout. Reference
  burn: same 5/27/26 LAD/COL game, LAD -1.5 RL came in at -172
  (market 63.2% vs true ~60% — fair). At that point the +EV pivots
  to the UP-alt of the OPPOSING pitcher's K Over (Sanchez Over 7.5 K
  at +182, market 35.5% vs true ~58%). The market over-anchors on
  the favorite-team narrative and under-prices the opposing pitcher's
  standalone K dominance. In heavy-mismatch matchups, check the
  opposing pitcher's UP-alt K line BEFORE assuming the spread is the
  payout-recovery knob.

### Safety-vs-EV tiebreaker (for unattended runs)
When a leg has a real tradeoff between a safer "deeper alt" line and a more
+EV "value" line (e.g. Strider Over 4.5 K at -625 vs Over 5.5 K at -132),
**default to the safer line** in unattended/scheduled sessions. The user
isn't there to confirm a judgment call, and today's reference burn (5/26/26
Strider) showed that the model's edge estimate can be wrong in ways the K/9
number can't see.

**Override the safety default and take the EV play ONLY when ALL of these hold:**
1. The pitcher has NO structural pitch-count uncertainty (not TJ-return,
   not MLB debut, not post-IL, not opener-conversion, not quick-hook manager)
2. Recent sample is 10+ starts at normal length (≥5 IP avg)
3. Modeled edge on the value line is ≥ +8pp
4. Opposing lineup K% and HP umpire are not negative signals

If any of those fail, take the safer alt and accept the lower payout.
Document the choice in the parlay file under "Build-iteration notes" so
the user can override at game-time if they want.

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
   before building a leg.
   - ALSO: do NOT reuse yesterday's pitcher assumptions for the same series.
     Rotations rotate, mid-series acquisitions debut, and the same teams often
     start completely different SPs the next day. Re-verify probables fresh
     each session from the live source — never carry over from yesterday's
     parlay file, AND do NOT accept a search-result attribution that lists
     yesterday's matchup (article headlines often surface "Yankees vs Royals
     5/26" in a 5/27 search and the first-pass scan can latch onto it).
     Reference burns: 5/26/26 assumed Sheehan/Gordon (yesterday's pitchers);
     actual was Lauer/Freeland. 5/27/26 assumed Schlittler/Falter from a
     5/26 article; actual was Cole (TJ-return) vs Cameron — completely
     different pitching profile that collapsed the NYY ML edge from +11pp
     to ~0pp.
   - WHEN A PITCHER SWAP IS FLAGGED MID-ANALYSIS, immediately pull the new
     pitcher's CURRENT-SEASON ERA, WHIP, recent form, and K/9. Do NOT estimate
     from career numbers or from how the pitcher looked at their last team.
     Reference burn: 5/26/26 Lauer was correctly identified as the LAD starter
     but his current-season ERA (6.69) was estimated at ~4.30 from career.
     That mis-estimate cost ~5pp on the Dodgers true win-prob, and the parlay
     was framed as "roughly fair" when it was actually slightly -EV.
   - ALSO applies to NON-swapped, correctly-named pitchers: an aggregate
     season stat line can be FROZEN at a prior start. Always cross-check a
     pitcher's season ERA/WHIP against a DATE-STAMPED current source (today's
     game-day preview or the start-by-start game log), not just a stat
     aggregate, before using it — a 2-start-old line badly misreads an arm in
     a recent hot/cold swing. Reference burn: 5/29/26 Imanaga — the 09:00 run
     used his 2.32 ERA (his line frozen as of his May 13 start); he was then
     shelled twice (8 R vs MIL, then 6 IP/7 ER/3 HR vs HOU on 5/24), so his
     CURRENT ERA was 4.04. The stale number made the writeup call him "the
     cleanest K profile on the board." NOTE the K-Over leg still held — he
     struck out 6 even in the 5/24 shelling — so separate the axes: stale ERA
     killed the run-prevention read, but per-pitch K stuff was intact (cf. the
     Cole/Skenes refinement above).
2. **Slate-wide value scan (MANDATORY before narrowing to final legs).**
   Enumerate EVERY game on today's slate and identify at least one
   value candidate per game across all bet types: ML, spread, total,
   team total, pitcher K-Over AND K-Under, hitter props. Do NOT
   tunnel-vision on the headline matchups (e.g. an Ohtani / Burns /
   Skenes start) without first scanning the full slate. The best
   value often hides in mid-slate games — weak-SP team-total plays,
   K-Over arms vs slumping lineups, contrarian underdog MLs, K-Under
   on a pitcher with structural pitch-count uncertainty. Produce a
   game-by-game value scan TABLE (one row per game, value candidate
   identified or "no edge") BEFORE narrowing to the final 2-3 legs.
   Reference burn: 5/27/26 — initial Builds A/B/C only deep-dove on
   LAD/COL and PHI/SD; user had to explicitly ask "did you check all
   games?" to surface Logan Gilbert K-Over (SEA/ATH), Yankees/KC
   Cole/Cameron matchup (which then turned out to be a price-trap),
   COL/CLE/CHC team-total Unders, and several other angles. The
   tunnel-vision cost a full conversational round-trip the user
   shouldn't have had to drive.
3. For each candidate pitcher leg, fill in the MANDATORY SP-data-freshness field,
   then run the pitcher-prop checklist
4. For each candidate hitter leg, check recent form + slump news
5. For each candidate ML/spread, fill in the MANDATORY SP-data-freshness field for
   the relevant starter(s), then verify SP quality and lineup health
6. Construct parlay, show per-leg odds and combined payout math
7. List rejected candidates with reasons
8. Flag any uncertainty and recommend re-checking lines at game time

## Git workflow
- Always commit, push, AND merge updates — never just commit. After any
  change to `parlays/*.md` or `CLAUDE.md`, the full cycle is: commit →
  push to the feature branch → open PR → squash-merge to main. Don't stop
  at commit; the user expects main to reflect the latest state by the end
  of every turn. If a merge conflict appears (typically after a prior
  squash-merge made the branch diverge), resolve by saving the latest
  working-tree state, resetting the branch to origin/main, re-applying the
  state, and force-pushing — then merge.

## Learning and retrospectives

### Per-parlay logging
- After building a parlay, save the analysis to `parlays/YYYY-MM-DD.md` in this
  repo and commit + push + MERGE it. The file should include: each leg with
  odds, the per-leg reasoning, true win prob estimate, the combined payout
  math, rejected candidates with reasons, and a `Result` section starting as TBD.

### Multi-run-per-day logging (scheduled cron)
- The routine runs 3× daily via cron (09:00, 11:00, 17:00 ET as of 5/26/26).
  Each run produces its own build of the parlay using fresh slate data
  (lineups posted, line movement, late scratches all evolve through the day).
- **One file per day, append-only.** If `parlays/YYYY-MM-DD.md` already
  exists when a run starts, APPEND a new `## Run HH:MM ET — Build [A|B|C]`
  block below the existing content. Do NOT overwrite earlier runs — each
  run's build is a record of what the slate looked like at that time.
- File schema:
  ```
  # Parlay — YYYY-MM-DD (Day)
  ## Daily slate context           (shared once; updated by each run if needed)
  ---
  ## Run 09:00 ET — Build A        (first run appends)
  ## Run 11:00 ET — Build B        (second run appends)
  ## Run 17:00 ET — Build C        (third run appends)
  ---
  ## Played build                  (filled in by user at night)
  ## Result                        (filled in once games settle)
  ```
- Each run's block contains the standard per-parlay logging fields: legs,
  per-leg reasoning, true win prob, combined math, rejected candidates,
  pre-bet checklist, run-specific notes.
- Each subsequent run should briefly compare to the prior run's build —
  if Build B refines Build A's legs based on new info (lineup posted,
  line moved), note the diff in B's "Run-specific notes."

### Reporting outcomes for multi-run days
- When the user reports at night which build they played (e.g. "I went with
  Build B with Strider swapped to 4.5 K"), locate that build, mark it as
  `**[CHOSEN BY USER]**` in its header, fill in the `## Played build`
  section, and write the per-leg result + retrospective under `## Result`.
- Lessons from the played build feed the Promoting-recurring-lessons rule.
  Lessons from rejected builds STILL count if today's outcome shows my
  analysis was wrong on those legs (e.g. Build A's pick lost where I'd
  said it was 80%, that's a calibration lesson even though we didn't bet it).

### Session-start review
- At the start of any session where the user might ask for a parlay, scan the
  3 most recent `parlays/*.md` files for filled-in results and captured
  lessons. Apply lessons before building today's parlay. If a recent result
  is still TBD, **SELF-SETTLE it first by pulling the finals via WebSearch**
  (the prior-day full-slate review below already does this on the 09:00 run) —
  do NOT wait on the user. Mark the played ticket W/L with per-leg outcomes +
  retrospective. Only ask the user as a fallback if the finals genuinely can't
  be confirmed (game suspended/postponed, or search can't surface a result).
  User confirmed 5/29/26: the scheduled 09:00 run should check results itself.

### Prior-day full-slate review (MANDATORY on the morning / 09:00 ET run)
- The 09:00 ET run is the first of the day. Before building today's parlay, do
  a complete retrospective of EVERY game played the day before — not just the
  legs we bet or the headline matchups. This is a standing step, not an
  on-request one (added 5/28/26 at user request).
- Procedure:
  1. Pull every final score from the prior day. Use WebSearch, not WebFetch —
     ESPN/MLB/FOX/CBS all return HTTP 403 to WebFetch; targeted WebSearch
     queries ("Team A Team B <date> final score recap") reliably return the
     finals and pitcher lines. Watch for stale results: searches for a given
     series often surface the PRIOR day's game, so confirm the date on each.
  2. Build a one-row-per-game table (final, winning/losing pitcher, any notable
     K line) covering the whole slate.
  3. For each game, check it against the routine's active reads:
     - K-Over/Under outcomes for any notable arm (did the AUTO-FADE lineups
       — Royals/Astros/Guardians/D-backs — suppress an elite arm's Ks? did an
       ace-vs-soft-lineup K-Over hit?).
     - Fade-list teams (did they lose as expected?) and value/"quietly hot"
       teams (did the underdog angle pay?).
     - Any candidate legs I REJECTED — did the rejection validate or was it a
       miss? (calibration both ways.)
     - New "was hot, now cold" or "was cold, now quietly hot" candidates.
  4. Update the watch list in CLAUDE.md per the existing watch-list rule, and
     promote any lesson that now has 2–3 occurrences.
  5. Write the review into the PRIOR day's `parlays/YYYY-MM-DD.md` under a
     `## Full-slate review` section (table + findings), then commit → push →
     merge. If that day's parlay was still TBD, also settle its `## Result`
     using the finals you just pulled.
- Keep it findings-focused: the point is calibration (which rules held, which
  missed), not a box-score dump. Surface 3-6 genuine takeaways, like the
  5/27 review (three ace-vs-soft-lineup K-Overs hit; Astros AUTO-FADE held
  deGrom to 6 K; Elder's 1.97-ERA FIP-flag rejection validated).

### Promoting recurring lessons
- When the same lesson appears in 2–3 different `parlays/*.md` files, promote
  it into the core routine in `CLAUDE.md` (the relevant checklist or rule).
  Reference the dates in the commit message so the lesson's history is
  traceable.

## Notifications and email drafts
- After completing an MLB parlay analysis, send a push notification with the
  summary unless the user says otherwise
- When the user asks to "draft an email with Gmail" — the Gmail MCP connector
  IS configured in this environment (confirmed working 5/27/26). Use the
  `mcp__Gmail__create_draft` tool to create the draft directly in the user's
  Gmail account (to/subject/body). The tool may be deferred at session start —
  load it via ToolSearch ("select:mcp__Gmail__create_draft") before calling.
  Also show the draft contents inline so the user can see what was created.
  Only fall back to saving a file in /home/user/ if the Gmail MCP server is
  genuinely disconnected (ToolSearch returns no match) — and say so once.
