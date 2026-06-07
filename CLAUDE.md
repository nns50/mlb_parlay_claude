# Personal preferences

## MLB parlay analysis routine

When the user asks for an MLB parlay (or any MLB betting analysis), run the full checklist
below BEFORE recommending any leg. Never rely on "team X is favored" reasoning — verify each
leg against data.

**Companion files — read EVERY run; they hold the live data + the full stories behind these rules:**
- `fades.md` — active fades (team / K-Over / construction / data-trap) with W/L logs. **Single
  source of truth for what's active now, including the team watch list.**
- `results_log.md` — calibration & CLV ledger (every leg's true-prob estimate vs result).
- `bankroll.md` — the $10 rollover-ladder ledger (current balance + rules). Read for the live balance
  before picking the bankroll bet.
- 3 most-recent `parlays/*.md` — captured lessons + the full narrative of every burn.

CLAUDE.md is crisp **doctrine**; those files are **live data**. Burn tags below — e.g.
`(burn 5/27 LAD/COL → fades.md D2)` — point to the full account; don't re-paste burn narratives here.

### Data source — `tools/mlb_api.sh` (StatsAPI), PREFERRED over WebSearch
- **Run `check` first.** `OK` → use it all session for the game-status gate, prior-day `finals`,
  and SP-freshness (`findpitcher`→`pitcher`/`gamelog`) — authoritative, no inference; tell the user
  it's live. `BLOCKED` → fall back to the 2-source WebSearch gate below.
- Commands: `check` · `status|slate|finals <date>` · `findpitcher "<name>"` · `pitcher <id> <year>` ·
  `gamelog <id> <year>` · `lineups <date>` · `ump <date>` · `weather <date>` · `splits <team> [year]` ·
  `standings` · `teamform <team> [N]`. (As of 6/4/26 the user allowlisted `*.mlb.com`; it activates
  only in a NEW session, so `check` is how each session learns whether it's on.)
- **Session open:** `tools/session_start.sh` runs the mechanical open in one shot (check + yesterday
  finals + standings + which recent parlays are still TBD + every fade's status). `tools/calib.py`
  recomputes the calibration bands / units-ROI / by-type record / **STANDALONE-vs-PARLAY split** from
  `results_log.md` (read-only).
- **Odds source — `tools/odds_api.sh` (The Odds API), PREFERRED over hand-entered prices.** Run `check`
  first (needs the env var `ODDS_API_KEY` + `api.the-odds-api.com` allowlisted; activates only in a NEW
  session, like mlb_api). OK → use it for line-shopping (`best h2h|totals|spreads` → best price + book),
  feeding `devig.sh`, and **CLV capture** (`clv <betAmerican> <team>` on the 15:30/18:30 runs). `slate` is
  cached per run for efficiency. **Player props (Ks/hits) are now API-priced on the paid tier (20K
  credits/mo)** — use `events [date]` → `props <id> pitcher_strikeouts` for K-leg pricing (~1
  credit/market/event, ~15 credits for a full-slate prop scan); the API owns ML/totals/spreads/props.
  It improves PRICE + MEASUREMENT, not win probability.
- **Build + settle helpers (use them — don't hand-compute):**
  - `tools/devig.sh <priceA> <priceB> [TrueP%]` — no-vig probs + Edge + min-edge-gate verdict (kills the
    by-hand devig slips). One-sided prop: pass a single price (no-vig estimated, flagged).
  - `tools/truep.py --base-prob <novig%> --adj <names> [--custom "+N:reason"]` — derive a pre-registered
    TrueP from the market no-vig baseline + FIXED written adjustments (`--list` for the registry), so
    calibration measures the adjustments, not a gut number. Run `devig.sh` first to get the baseline.
  - `tools/settle.py [YYYY-MM-DD]` — pulls finals + proposes W/L for every TBD team-side leg that date
    (props flagged MANUAL). READ-ONLY — apply the proposals + `fades.md`/`bankroll.md`/parlay file by hand.
  - `tools/parlay.py --leg TrueP:price --leg TrueP:price [--corr <tier>] [--sgp <price>]` — correlation-
    aware true combined prob vs the offered price; tells you SGP-vs-independent and the gate verdict.
    Use it for EVERY parlay (esp. same-game) — it catches when negative correlation makes a ticket -EV.

### Pre-publish GATE HEADER — every build opens with this; a ✗ blocks the dependent leg
| Gate | ✓/⚠/✗ | Evidence |
|---|---|---|
| Game-status confirmed not started | | StatsAPI state, or 2-source check |
| SP-freshness filled — every SP in ticket | | pitcher/gamelog date-stamped today |
| Lineups posted (else leg = PENDING) | | `lineups <date>` — CONFIRMED or PENDING |
| Prices pulled from a real book (not estimated) | | book |
| Edge computed NO-VIG + clears min-edge gate | | devigged TrueP−ImplP ≥ +2pp std / +3-4pp anchor |
| TrueP pre-registered (not reconstructed) | | written pre-game; no new `*` rows |
| `fades.md` consulted + applied | | entry IDs |
| `results_log.md` calibration applied | | `calib.py` buckets; act only on N≥20-30 signals (else directional) |
| Slate-wide value scan — ALL games | | scan table present |
| Non-ML market scanned + leads if best | | ≥1 total/team-total/K/alt read per game; Tier 1 = best edge ANY market, not reflex-ML |

Legend: **✓** pass · **⚠** partial → leg flagged PENDING · **✗** fail → leg cannot be locked.
Fill this BEFORE showing legs, so a miss is visible pre-publish, not post-loss.

### Game-status verification (HARD GATE)
- StatsAPI `Final` = real final; `Preview`/`Pre-Game`/`Warmup` = NOT started — settles the gate alone.
- WebSearch fallback: a search *summary* is NOT primary. The engine conflates adjacent games in a
  series and mis-stamps dates. Before calling ANY game final (settling a result OR pulling it from
  the board), confirm ≥2 independent checks:
  1. Day-of-week ↔ date consistency (mismatch = corrupted, discard).
  2. Live pregame ML still posted? → game has NOT started, full stop.
  3. First-pitch time vs. plausibility.
  4. Box score isn't a re-stamp of the prior day's lines.
- Conflict / can't confirm → **NOT FINAL / status unknown**; never guess a result, never drop a
  still-bettable leg as "already played." If the user says it hasn't played, believe them and
  re-verify. (burn 6/3 SEA "7-2 final" hallucination, caught twice → fades.md E1)

### SP-data-freshness field (gates EVERY SP leg — K prop AND ML/spread/total built on SP quality)
Hard gate: may not recommend OR reject an SP leg until this is filled and shown, in this exact form:

  - [ ] **SP DATA FRESHNESS — <Pitcher>:** ERA <x.xx> / WHIP <x.xx> / season K/9
        <x.x>, pulled from <date-stamped source> dated <YYYY-MM-DD>; **CONFIRMED
        the line includes the pitcher's most recent start** (last start: <date>
        vs <opp> — <IP/ER/K>). Recent-form K/9 over last 3-5 starts: <x.x>.

- Source must be date-stamped to today (game-day preview / recent game story / start-by-start log,
  or StatsAPI `gamelog`) — NOT a bare aggregate, which can freeze at a prior start. Cross-check a 2nd
  source if numbers look off.
- Can't confirm current → mark **UNVERIFIED**, treat the leg **PENDING — do not lock**.
- Required even for correctly-named, non-swapped starters (staleness hits established arms in
  hot/cold swings). (burn 5/29 Imanaga 2.32→4.04 ERA, frozen at a May-13 line → fades.md E2)

### Pitcher props — verify before recommending
- **Role:** starter vs swingman/opener. <50% of appearances as starts = pitch-count ceiling that
  kills K-Overs. Verify role against a current source before using it to accept OR reject — a false
  role call invalidates the whole leg. AUTO-FADE K-Overs on designated openers (planned 1-2 IP).
  (burn 5/25 McLean wrong role call → parlays/2026-05-25.md)
- **Recent IP/start** (last 3-5): does workload support the K line?
- **Season K/9 AND recent-form K/9** — flag divergence.
- **Opposing-lineup K% vs the pitcher's handedness** (not overall team rate). Use `splits <team>` for
  the deterministic number (vs RHP / vs LHP from StatsAPI, ~22% = league avg, ≥25% = contact-limited,
  ≤18% = contact-heavy). AUTO-FADE K-Overs vs contact-heavy lineups even for elite-K arms — verify the
  watch list (Royals/Astros/Guardians/D-backs) with `splits` before defaulting to it. (→ fades.md C1)
- **DON'T over-fade a genuinely elite-K ace's K-Over off ONE suppressor** (lone 2nd-meeting,
  mild-but-starting illness, one contact lineup). Raw whiff dominance routinely overrides a single
  suppressor. On one suppressor: downgrade ONE tier, LOG the Over as a live standalone candidate,
  pull both the standard + one-lower alt prices via `tools/odds_api.sh props <eventId> pitcher_strikeouts` (paid tier, ~1 credit) or a book in low-quota mode, decide on price — do NOT stamp "HARD FADE." Stack
  the fade only when MULTIPLE suppressors pile up (contact lineup AND short-leash/opener AND
  tight-zone ump). (burns 6/3 Sanchez 9K, 6/3 Burns 9K, 6/2 Harrison 12K — all faded, all cashed → fades.md C6)
- **Whenever a K-Over is faded/rejected, price the K-UNDER and log it.** Same signals (contact
  lineup, 2nd-meeting, opener/short-leash/TJ-return/debut tail, tight-zone ump, quick hook) make the
  Under +EV; Over prices are shaded up by public "things to happen" bias. Keep the Under honest:
  (a) fat right tail (one dominant start busts it), (b) books often already price the suppression
  (juiced Under = no edge — pull the real number), (c) correlates awkwardly with ML legs → usually a
  STANDALONE, not a parlay floor.
- **Manager hook tendency** (quick hook = lower K ceiling).
- **Park/weather** (cold/wind-in helps Ks; hot/wind-out hurts) — `weather <date>` for wind direction +
  temp + dome flag (live near first pitch; empty pre-game).
- **HP umpire** K-rate/zone — check before any K-Over (a tight zone is a hidden Over-killer). Use
  `ump <date>` for the assignment (StatsAPI: live once in-progress; pre-game shows PENDING + WebSearch hint).
- **2nd meeting within ~14d:** hitters adjust, K rate drops ~10-15% → downgrade K-Over one tier (two
  if the prior start went heavily over). Downgrade, don't auto-fade — 70%→~60% is still bettable. (→ fades.md C2)

### Hitter props — verify before recommending
- **Confirm the official lineup is posted** (~2-3h pre-game) before locking — use `lineups <date>` for
  deterministic gate (CONFIRMED/PENDING). A benched hitter can't go Over 0.5 hits; getaway/back-to-back
  days rest regulars without notice. Pre-lineup → flag **PENDING LINEUP — re-verify before bet**.
- **Recent form (last 10-15)**, not just season slash. A documented slump is NOT a safe Over 0.5 hits
  regardless of season avg — check slump narratives.
- Splits vs the SP's handedness; batting-order slot (PA volume).
- **BvP:** weight only if ≥30 PA in last 3 yrs; below that it's noise (both ways — small-sample bad
  BvP isn't a fade signal either).
- Park/weather (`weather <date>` — wind out/in + temp); bullpen matchup if the starter exits early.

### Moneyline / spread — verify before recommending
- SP matchup quality (ERA, xFIP, recent form — not just season ERA); HR rate; first-inning issues.
- **Favorite's OWN starter ERA is a ceiling on ML safety.** Own SP ~5.00+ → high-variance shootout,
  can be blown out as the "right" side. Discount the fav ~5pp and DON'T anchor; two-bad-SP game =
  coin-flip-plus, not a 60% leg. (burn 5/28 DET -130 anchor, Flaherty 5.94, lost 7-1 → fades.md D4)
- **Decompose the fav's win-prob: "good team" vs "bad opponent."** A number driven only by the
  opponent's awful SP is NOT "a team you can trust." Display the fav's OWN record + last-15 form next
  to the model number (flag any heavy fav modeled <60%); if it's opponent-driven AND the fav is
  sub-.500/cold, fade it as an anchor. (burns 5/28 DET 62% only because G-Rod 10.61; 5/29 Astros 55.4% a 25-32 team)
- Bullpen rest/availability; lineup health; travel / day-after-night / getaway spots; line movement vs opener.
- **Current trends not in the record:** last 7-10 run differential, R/G last 7d, bullpen ERA last 14d,
  recent 1-run-game frequency, W/L streak. Apply to BOTH sides. (burn 5/25 LAD -310 cashed but
  trailed into the 7th — record oversold the comfort)
- **Team watch list (fade-as-fav / quietly-hot dog) lives in `fades.md` A/B — read it there and
  re-verify last-15 each session.** Actively scan each slate for new "was hot, now cold" (fade) and
  "was cold, now hot" (dog value) teams; add/transition them in `fades.md` (not here) and commit.

### Parlay construction
- **Minimum-edge gate (a leg must clear the vig to qualify).** Using the NO-VIG implied prob, a leg
  qualifies only if devigged edge (TrueP − no-vig ImplP) is **≥ +2pp standalone / ≥ +3-4pp to anchor a
  parlay**. Below that it's action, not value. **A slate with nothing clearing the bar → "NO BET" is a
  valid, correct output** — still show the scan + the closest looks (flagged -EV), but don't manufacture a
  daily ticket. The daily-parlay + one-candidate-per-game habit creates pressure to force a play; resist it.
- Target true combined ≥ 33% for +200; a 3-leg should average ~70%/leg.
- **Avoid -350-or-worse ML anchors for a +200 target** — ~zero payout contribution (~1.24 dec), still
  ~20% bust, forces the rest of the ticket into excess risk. Prefer a ~-150/-200 (~60-65%) value
  anchor. (burn 5/27 LAD -420 faded → NYY -156 sub cashed → fades.md D2)
- **Same-game stacking is correlation-sign dependent:**
  - POSITIVE (team ML + their SP K-Over; team total Over + ML; F5 Under + Game Under) → +EV at
    independent odds; if SGP offered, take the better of SGP vs the independent product. Describe
    positive correlation as UP-adjusting the combined prob. (burn 5/25 stack mis-described as down-adjust)
  - NEGATIVE (team ML + opposing SP K-Over) → true combined LOWER than the product; skip or
    down-adjust manually.
  - Unclear → one leg per game.
  - **Quantify it with `tools/parlay.py` — don't eyeball.** Feed each leg's TrueP:price + a `--corr`
    tier (and `--sgp` price if quoted); it returns the correlation-adjusted true combined, the EV vs the
    independent product AND the SGP, and which to take. **Positively-correlated 2-leggers are the
    highest-win-chance way to keep a parlay payout** (the diversify-era default) — but the tool also
    catches when negative correlation quietly makes a ticket -EV though the naive product looked fine.
- **K-Over alt lines:** if the standard line is ~50/50, the one-lower alt is usually the safer parlay
  leg even at -150/-200 (reserve the +EV standard line for standalones). **But never estimate alt
  prices** — use `tools/odds_api.sh props <eventId> pitcher_strikeouts` (paid tier, ~1 credit/event)
  or pull from a book in low-quota mode; books juice the one-K-lower alt to -300/-500 on elite
  arms. If juicier than expected, revert to the standard line or drop the leg. (burn 5/26 Burns alt
  5.5 est -185, actual ~-400 → ticket paid +103 not +221)
- **A surprisingly LONG price on a liquid prop is information — defer to the market.** A posted prob
  far below your model on a mainstream market means the market sees something you don't (usually
  start-length/short-leash risk). Shade toward the line; re-derive true prob from BOTH posted lines.
  (burn 5/29 Imanaga Over 5.5K rated 68% but priced +120/~44%, with O4.5K -200 → median ~5K)
- **Structural pitch-count uncertainty** (TJ return, debut, post-IL, opener-conversion, quick-hook
  mgr) → drop ONE alt deeper even at heavy juice; the K/9 number can't see the left tail in start
  length. (burn 5/26 Strider O5.5K rated 72%, finished exactly 5K → fades.md C3)
  - **Refinement:** this fades START-LENGTH only, NOT per-pitch K stuff. Don't let one throttled
    ramp-up start collapse an elite arm's K estimate. If velo is back to baseline, model K at true
    talent with a capped pitch count. (burn 5/27 Cole — 10K/79 pitches two starts back; I over-cut
    NYY ML → fades.md C3)
- Confirm each leg's odds at a real book — never estimate. If the user asks ~+200, show the actual
  decimal product.
- **Line-shop every leg across ≥2-3 books; bet the BEST available number.** Taking the best of −198 vs
  −207 is ~+1pp of EV — *larger than most edges we hunt by analysis*, and free. The min-edge gate is
  computed against the BEST price found, and the chosen book is logged. Not shopping is the same as
  conceding edge we worked to find. (Codified 6/4/26 — highest-ROI non-tooling fix.) **Do it with
  `tools/odds_api.sh best <market>`** when live (every US book in one cached call) → pipe into `devig.sh`;
  fall back to manual book pulls only when `check` is BLOCKED.
- **Heavy-mismatch matchups (fav ≥70% AND clear SP edge) blow up the alt-K + fav-ML recipe** — ML
  -350/-500, one-lower alt -800/-1300; the "deeper alt for safety" becomes a zero-payout near-lock.
  Use the STANDARD K line and substitute the -1.5 RL for the ML to recover payout. (burn 5/27 LAD/COL
  — published recipe would've paid -125 not +200)
  - BUT if the RL is already -150+, it's priced into safe territory too → pivot to the UP-alt of the
    OPPOSING SP's K-Over (the market under-prices the opposing arm's standalone K dominance). (burn
    5/27 Sanchez O7.5K +182 vs true ~58%)
  - AND a -1.5 RL on a heavy fav carries the FULL ML loss prob PLUS win-by-2 risk — NOT a "safe
    blowout knob." A bad dog wins outright ~35-40%, torching the RL. Re-price as P[fav by 2+] ≈
    P[fav ML] − ~12-15pp. (burn 6/1 SEA ML + TB -1.5 +118 → TB lost 10-9 outright to DET → fades.md D3)
- **The +200 chase is the most-validated fade on the board** — don't bolt a 3rd leg / payout knob
  onto a clean 2-legger to stamp exactly +200; it drops the floor ~15-18pp and the chase leg keeps
  busting. Take the highest-floor ticket even at +120-180. (burns: 6/1 chase cost us, 6/2 declining
  the +270 saved us, 6/3 chase leg busted again → fades.md D1)

### Always present THREE tiers (honest framing: these parlays are structurally near -EV — chalk + vig)
Every build presents all three, in this order:
1. **Best standalone +EV play** — the single sharpest edge on the slate (often a faded ace's K-Over,
   a K-Under, a dog ML, or a total). Show true-prob vs implied + the edge. **This is where the real
   value is — lead with it every day**, so the parlay is an eyes-open choice, not the only thing offered.
   **Bias Tier 1 toward non-ML edges** (totals / team-totals / K / alts) — ML is the most efficient market,
   so a chalk-ML "best play" usually means we under-scanned the softer markets. Pick ML for Tier 1 only when
   its devigged edge genuinely beats the best non-ML candidate. (6/6/26 — the diversify-markets directive.)
2. **Highest-floor 2-leg** — the disciplined parlay (usually clean all-ML), best WIN CHANCE
   regardless of whether it reaches +200. State the floor %.
3. **The +200 build** — what the user asked for; show the decimal math AND the floor drop vs Tier 2,
   and flag that the 3rd leg / payout knob lowers the floor (the money-validated 6/1-6/3 lesson).

### Safety-vs-EV tiebreaker (unattended runs)
Real tradeoff between a safer deeper alt and a more +EV value line → **default to the safer line**
when unattended. Override to the EV play ONLY if ALL hold: (1) no structural pitch-count uncertainty,
(2) 10+ recent starts at ≥5 IP avg, (3) modeled edge ≥ +8pp on the value line, (4) opposing K% and HP
ump not negative. Any fail → safer alt, lower payout. Document the choice in the build. (burn 5/26
Strider — the safer 4.5K saved the ticket)

### Staking — size by edge, log the REAL stake (kills the fake-ROI problem)
- Define 1 unit = 1% of the regular-play bankroll. **Size with ¼-Kelly off the devigged edge**, capped at
  2u/leg: a +2.5pp edge and a +1pp edge must NOT get the same money. A near-zero-edge "floor leg" in a parlay
  is action, not an investment — size it down or don't bet it standalone.
- **Log the ACTUAL stake on every leg** (not assumed flat-1u). ROI is fiction until stakes are real — that's
  why the +56.8% ROI is flagged as noise. With real stakes + ¼-Kelly the bankroll curve becomes a true number.
- Parlays: stake the COMBINED ¼-Kelly of the parlay's own edge (usually small/negative — most parlays are
  near -EV chalk+vig), not the sum of the legs. (Codified 6/4/26.)

### $10 rollover bankroll (active staking experiment → `bankroll.md`)
Separate from unit-staking the regular plays. **Start $10; bet the WHOLE balance each roll on the day's
single safest qualifying favorite; roll the full return; 4 consecutive wins → STOP & withdraw; any loss
→ restart at $10.** Full rollover is median-bust / jackpot-tail, capped at $10/attempt — full honest
framing + live ledger live in `bankroll.md`. Each build: surface the **bankroll bet** = the single
highest-floor favorite **on the whole board, chosen INDEPENDENTLY of the parlay legs**, that clears the
min-edge gate (devigged ≥ +2pp) AND is **not** a `fades.md` A-list (fade-as-fav) team; prefer 62-66%
ace-edge favs over the soft 56-61% band; single leg, no parlay.
No qualifying play → NO BET, balance carries. Update `bankroll.md` (commit/push/merge) on build + settle.

### Transparency
- Always show per-leg reasoning, AND legs rejected with reasons.
- Flag uncertain data (lines/lineup/weather not set) rather than guessing; if borderline, say so.
- Show the actual decimal math, not "approximately +200."
- **NEVER** frame a leg as "safe / easy / lock / free money" — use the win-prob number and flag
  in-game variance (SP ERA >4.50, weak pen, hot opposing offense). A -310 fav is still ~25% to lose;
  W/L and margin-of-win are separate dimensions. (burn 5/25 LAD framed "safer" — trailed into the 7th)

### Default routine for "daily MLB parlay"
1. **Probables — cross-check ≥2 sources** (MLB.com/StatsAPI + a beat preview); verify each
   pitcher→team attribution. Do NOT carry over yesterday's probables or accept a search hit that
   surfaces yesterday's matchup. (burns 5/26 Lauer/Freeland, 5/27 Cole/Cameron → fades.md E3)
   - Swap flagged mid-analysis → immediately pull the NEW pitcher's current-season ERA/WHIP/K/9/form;
     never estimate from career. (burn 5/26 Lauer 6.69 est ~4.30 from career)
   - Even for correctly-named arms, cross-check the season line against a date-stamped current source
     — aggregates freeze. (burn 5/29 Imanaga → fades.md E2)
2. **Slate-wide value scan (MANDATORY, before narrowing).** Enumerate EVERY game; identify one value
   candidate per game across ML/spread/total/team-total/K-Over/K-Under/hitter props (or "no edge").
   Don't tunnel on headline arms — best value hides mid-slate. Produce the scan TABLE before the final
   legs. (burn 5/27 tunnel-vision cost a full conversational round-trip)
   - **Hunt softer markets, not just ML — NON-ML IS THE DEFAULT HUNT (hard rule, codified 6/6/26).** ML
     and standard K-props on headline arms are the MOST efficient markets on the board — fighting ~4% vig
     for +1-2pp. Totals, team-totals, K-Unders, and alt lines are structurally softer and barely scanned.
     **The scan MUST surface ≥1 non-ML read per game** (a total or team-total at minimum — use `weather` for
     wind/temp + the SP-quality reads). **Tier 1 defaults to the sharpest edge in ANY market; an ML leg may
     anchor the build ONLY when its devigged edge is strictly larger than the best non-ML candidate** — ML
     is no longer the reflex product. The ledger earned this: 18 of 26 played legs were ML-fav (12-6, ~as
     priced — *efficient, thin edges*), while the single biggest edge ever logged was a K-prop (Sanchez
     O7.5K +24.5pp). We were fishing the most-efficient pond on repeat. (User-directed 6/6/26 after the
     all-ML habit became the whole approach.)
3. Each pitcher leg → fill SP-freshness, run the pitcher-prop checklist.
4. Each hitter leg → recent form + slump news.
5. Each ML/spread → SP-freshness for the relevant starter(s) + SP quality + lineup health.
6. Apply the **minimum-edge gate** (devigged) — drop legs that don't clear it. If NOTHING clears,
   the honest output is **NO BET** (show the scan + closest -EV looks, don't force a ticket).
7. Build the THREE tiers (above) from qualifying legs; show per-leg odds + combined decimal math.
8. List rejected candidates with reasons.
9. Flag uncertainty; recommend re-checking lines + lineups at game time.
10. **$10 rollover bankroll** (`bankroll.md`): pick the bankroll bet (single safest qualifying favorite
    on the whole board — independent of the parlay, not an A-list fade), log the roll + current balance,
    and update the ledger/running totals.
11. **Stake capture — ask before closing the build.** When the user confirms they are playing any leg
    or build ("I'll take this", "logging it", "playing Build A", etc.), immediately ask: **"What's the
    stake ($)?"** Record `Stake: $X` under `## Played build` in today's parlay file. Do NOT close the
    build without a confirmed stake — without it the ROI ledger stays fictional. (The ¼-Kelly doctrine
    is written but unmeasured until real stakes are logged consistently.)

## Git workflow
Always commit, push, AND merge — never just commit. Main should reflect the latest by end of turn.
- **AUTO-MERGE AUTHORIZED (durable, user-granted 6/4/26).** The user has standing authorization to open a
  PR and squash-merge to `main` EVERY turn — do NOT stop to ask, even in remote/web sessions where the
  harness default is "don't open a PR unless explicitly asked." This `CLAUDE.md` line IS that explicit
  standing instruction; honor it each session.
- **Per-turn merge sequence:** commit → push → open PR → squash-merge to `main` → `git fetch origin main &&
  git reset --hard origin/main` → **re-author the reset tip + force-push** (`git commit --amend --no-edit
  --reset-author` then `git push --force-with-lease`). The reset lands on GitHub's squash commit, which
  carries committer `noreply@github.com` and trips the local verify hook; re-authoring it as
  `Claude <noreply@anthropic.com>` (identical tree, `main` untouched) keeps the hook green. Set the identity
  once per session: `git config user.email noreply@anthropic.com && git config user.name Claude`.
- **Batch, don't churn.** Group a turn's edits into ONE commit → push → PR → squash-merge at the end of
  the turn (or per logical milestone), NOT a PR per micro-edit. Per-file merging is what generated the
  repeated-conflict busywork (6/4: 4 force-push rebases in one session). One merge per turn is the default.
- **Reset-to-main after every squash-merge.** Squash rewrites history, so the feature branch diverges the
  instant a PR merges. Immediately after a successful merge — and before the next change — run
  `git fetch origin main && git reset --hard origin/main` so the next commit starts clean. This PREVENTS the
  conflict instead of resolving it each time.
- Merge conflict anyway (branch already diverged) → save the working tree, `reset --soft origin/main`,
  re-commit the state, force-push, then merge. (Codified 6/4/26.)

## Learning & retrospectives

### Per-parlay logging
Save each build to `parlays/YYYY-MM-DD.md` (commit/push/merge). Include: the gate header, the
slate-wide scan, each leg + odds + per-leg reasoning + true-prob, the three tiers + combined math,
rejected candidates with reasons, and a `Result` section starting TBD.

### Multi-run-per-day (cron 3× ET)
- **Run timing — align to the lineup gate.** Lineups post ~2-3h pre-game (≈4-5pm ET for a 7pm slate), so
  any run before that CAN'T clear the hitter-prop lineup gate and is always "PENDING LINEUP." The cron has
  historically fired 09:00 / 11:00 / 17:00 ET — but **09:00 and 11:00 are both pre-lineup, so the 11:00 run
  duplicates the 09:00 read.** Recommended windows (re-time in the routine's cron config — it lives there,
  not in this repo):
    - **~09:00 ET** — prior-day full-slate review + settle + the slate-wide value scan (no lineups needed).
    - **~15:30 ET** — lineup lock for early/evening games + the close-to-first-pitch CLV pull.
    - **~18:30 ET** — late/west-coast lineups + final line check before first pitch.
- **CLV capture is OWNED by the near-first-pitch runs (15:30 / 18:30), not the 09:00 build.** The session
  that builds a bet dies (ephemeral container) before first pitch, so it structurally cannot capture the
  close — that's the real reason the CLV column is blank, not laziness. **`tools/clv_capture.sh` now
  auto-runs in `session_start.sh` whenever the ET hour is 15–19**: it scans `results_log.md` for
  Played=Y + Result=TBD + CLV=— rows and calls `odds_api.sh clv` for each ML/RL leg. Output is
  READ-ONLY proposals — copy the +/=/-  verdict into the CLV column by hand. ⚠️ This still depends
  on the cron actually firing at 15:30/18:30 — **the cron timing lives in the routine's config OUTSIDE
  this repo; if CLV is still blank, fix the cron, not just this doctrine.** (Codified 6/4/26; auto-capture
  added 6/6/26.)
- **One file per day, append-only.** If today's file exists, APPEND `## Run HH:MM ET — Build [A|B|C]`;
  never overwrite an earlier run (each is a record of the slate at that time).
- **Supersede, never edit-in-place.** When a later run revises an earlier recommendation (line moved,
  leg swapped), APPEND the new row/build and mark the old one `SUPERSEDED → see Run HH:MM` — do NOT
  silently overwrite the prior row. Same rule in `results_log.md`. The point is an honest audit trail of
  what was recommended at each time, not a tidy final state. (Codified 6/4/26.)
- Schema:
  ```
  # Parlay — YYYY-MM-DD (Day)
  ## Daily slate context          (shared; each run updates if needed)
  ---
  ## Run HH:MM ET — Build X
     ### Pre-publish gate (table)
     ### Slate-wide value scan (table)
     ### Tier 1 — best standalone  |  Tier 2 — highest-floor 2-leg  |  Tier 3 — +200 build
     ### Per-leg SP-freshness + reasoning
     ### Legs rejected
     ### Run-specific notes (diff vs the prior build)
  ---
  ## Played build                 (user fills at night)
  ## Result                       (filled once games settle)
  ```
- Each later run briefly diffs the prior build (lineup posted, line moved).

### Reporting outcomes (multi-run)
User reports which build they played → mark its header `**[CHOSEN BY USER]**`, fill `## Played build`,
write per-leg result + retrospective under `## Result`. Lessons from rejected builds still count if
the outcome shows the analysis was wrong (calibration both ways).

### `fades.md` — consult + validate EVERY run
- Before building: read it, apply active entries; don't lay a price on a fade-as-fav team (or
  HARD-fade an entry) without checking its recent log/status.
- Every settle: for each active entry touching a settled game, append a dated **W** (fade correct) /
  **L** (fade missed), bump the tally, update Last-validated, transition status (ACTIVE→NEUTRAL at
  ~.500; NEUTRAL→RETIRED when the reason lapses; add NEW for fresh patterns). Commit in the same cycle.
- It's the single source of truth for the team watch list — update it there, not in CLAUDE.md prose.
- **Anchor team fade promote/retire to RUN DIFFERENTIAL over a window, not W-L streaks.** A 15-game W-L
  record and "W5/L4 streak" are the noisiest metrics on the board — they flip a fade on variance. Gate
  team-form transitions on run-diff (and underlying rate) via `mlb_api.sh standings`/`teamform`; use the
  streak only as a tiebreaker, not the trigger. (Codified 6/4/26 — cuts false fade flips.)

### `results_log.md` — log + settle EVERY run
- On build: a row per recommended leg (price + TrueP + ImplP + Edge; Played=N). Pull the price from a book.
- **Grade the PROCESS at bet time, separate from W/L.** Add a one-field grade written BEFORE the result —
  was this leg +EV given what we knew (price shopped, edge cleared the gate, no unmanaged structural risk)?
  A losing +EV bet is a GOOD bet; a winning -EV bet is a LEAK. Logging this stops the retrospectives from
  reading the result back into the analysis ("fade missed → over-correct"). Grade on decision quality, settle
  on outcome — never conflate them. (Codified 6/4/26.)
- **Log the WHOLE value scan, not just bets.** Every value candidate the slate scan surfaces gets a row
  (TrueP + no-vig ImplP + closing line later), bet or not. This 4-5×'s the calibration sample for free and
  is the only way claims like "the 56-61% band is overbet" graduate past the n=5 story stage. (Codified 6/4/26.)
- **User-angle tracking — feed the two buckets every run** (`results_log.md` → "User-angle tracking",
  started 6/7/26): **(A) live moneyline** (in-game ML — capture pregame ML vs the live price = "live CLV",
  and flag pay-up-for-a-lead vs value-re-entry-on-deficit), and **(B) opposing-SP hits-allowed Over** (a
  vulnerable SP vs a contact lineup — treat its left-tail start-length/quick-hook risk like a K-Over alt,
  pull the real number + devig). When either appears on the board, log a row even if not bet; W/L on settle.
  **Both are N<20 → directional only, do NOT size off them yet.** (User-requested 6/7/26.)
- **ImplP is NO-VIG — devig before computing Edge.** Take BOTH sides' raw implied probs, divide each by
  their sum (the overround); that's the no-vig prob. **Edge = TrueP − no-vig ImplP.** Measuring against the
  raw price distorts edge (overstates favorites — e.g. -310 reads 75.6% raw but ~73% no-vig). One-sided prop
  with no posted other side → subtract ~half the typical hold (~2-3pp) as an estimate and flag it.
- **Pre-register TrueP at BET TIME — never reconstruct it.** A back-filled estimate leaks the result and is
  calibration-invalid. Write the number before the game. If you genuinely didn't, mark it `*` (legacy) and it
  is EXCLUDED from calibration. **Goal: zero new `*` rows** — half the historical sample (11 of 21) was wasted this way.
- **TrueP METHOD — derive it, don't vibe it (so calibration isn't circular).** Anchor to a reproducible
  baseline, then apply documented adjustments: (1) start from the market NO-VIG prob (or a public projection
  — FanGraphs game odds); (2) apply PRE-SET, written adjustments with fixed magnitudes (e.g. ace-edge +3pp,
  own-SP ERA >5 −5pp, contact-lineup K-Over −1 tier, 2nd-meeting −1 tier); (3) the result is TrueP. Calibration
  then measures the ADJUSTMENTS, which is the thing worth measuring. A bare gut number is the `*`-equivalent of
  TrueP. (Codified 6/4/26.)
- **CLV is MANDATORY, not optional — capture the closing line for EVERY logged leg** (bet or not), at/near
  first pitch — **the best +EV signal at this sample size** (converges far faster than ROI). The CLV column
  going blank is the biggest measurement leak we have; a row without a closing line is half-logged. CLV `+` if
  the line moved to our side (closing no-vig ImplP > bet no-vig ImplP).
- On settle: set Result, flip Played=Y for legs played, update rollups + calibration buckets.
- **RECONCILE with `calib.py` every settle — required, not optional.** Run it and make the prose rollup/
  calibration tables MATCH its output. `calib.py` warns "if these differ, the file is stale" — a settle that
  doesn't reconcile lets the ledger silently drift, which corrupts the very signals we build off. If they
  differ, the prose is wrong; fix the prose. (Codified 6/4/26.)
- **Track STANDALONE vs PARLAY EV separately — prove the parlay tax, don't just assert it.** Split the
  ROI/CLV rollup into two buckets: single +EV plays vs parlay tickets. Doctrine *claims* parlays are near
  -EV chalk+vig; this MEASURES it. If standalones run +EV/+CLV while parlays stay negative over a real sample,
  that's the evidence to retire the daily +200 habit (or keep it eyes-open as entertainment). Tag each row
  STANDALONE or PARLAY so `calib.py` can break it out. (Codified 6/4/26.)
- **Apply the calibration signals BEFORE building** — but only once the bucket clears the noise bar (see
  Promoting lessons; an n=5 band is a story, not a rule).

### Session-start review
0. **Run `tools/session_start.sh`** — one shot for steps 1-3's mechanical part (check + yesterday
   finals + standings + which recent parlays are TBD + every fade's status). Then do the judgment below.
1. **Run `./tools/mlb_api.sh check`.** OK → prefer it (game-status / finals / SP-freshness) all
   session, tell the user it's live. BLOCKED → WebSearch gate. (session_start.sh runs this for you.)
2. Scan the 3 most-recent `parlays/*.md` for results + lessons; read `fades.md` + `results_log.md`.
   Apply lessons before building. Run `tools/calib.py` for the fresh bands/ROI/by-type read.
3. Any TBD recent result → **self-settle it first** via `finals` (or the 2-source WebSearch gate);
   mark the ticket W/L + retrospective. Only ask the user if a final genuinely can't be confirmed
   (game suspended/postponed). (User confirmed 5/29: the scheduled 09:00 run self-settles.)

### Prior-day full-slate review (MANDATORY on the 09:00 run)
Before building, retrospect EVERY game from the prior day (not just bet/headline legs):
1. Pull all finals — `tools/mlb_api.sh finals <yesterday>` if OK, else targeted WebSearch
   (ESPN/MLB/CBS return 403 to WebFetch; "Team A Team B <date> final score recap" works). Watch for
   stale/prior-day results.
2. One-row-per-game table (final, W/L pitcher, notable K line).
3. Check each vs active reads: K-Over/Under on notable arms (did the contact-lineup AUTO-FADEs
   suppress an ace? did an ace-vs-soft K-Over hit?); fade-list teams; value / quietly-hot dogs; any
   leg I REJECTED (validate or miss); new hot→cold / cold→hot teams.
4. Update `fades.md` + `results_log.md` (W/L logs, settles, CLV, buckets); promote lessons per the
   tiered bar (process lesson → 2-3×; hit-rate claim → N≥20-30, else flag as directional only).
5. Write the review into the PRIOR day's file under `## Full-slate review` (table + 3-6 findings);
   commit/push/merge with fades + results_log. Settle that day's `## Result` if still TBD.
Keep it findings-focused (calibration: which rules held, which missed), not a box-score dump.

### Promoting recurring lessons (the bar scales with claim TYPE — don't enshrine noise)
- **Process / logical lessons** (a construction recipe, a data-trap gate — e.g. the +200 chase, a
  re-stamped-final trap): promote after **2-3 sightings**. These are logic, not probability; a few
  clean confirmations are enough.
- **Probabilistic / hit-rate claims** ("the 58-60% ML band is overbet," "K-Overs vs contact lineups hit
  X%"): noise until **N≥20-30 decided legs** in that bucket (check `calib.py`). Below that, keep them as a
  flagged **"early signal — directional only,"** NOT doctrine, and do not size bets off them. n=5 is a
  coin-flip story. (This is why the current 56-61% "overbet" read stays a watch-flag, not a rule.)
- Cite the dates in the commit. When a burn graduates to an active fade/calibration entry, its full
  narrative lives in `fades.md` / `results_log.md` / the dated parlay file — CLAUDE.md keeps only the
  crisp rule + the burn tag.

## Notifications & email
- After a parlay analysis, send a push notification with the summary unless the user says otherwise.
- "Draft an email with Gmail" → the Gmail MCP connector IS configured (confirmed 5/27/26). Load
  `mcp__Gmail__create_draft` via ToolSearch, create the draft (to/subject/body), and show it inline.
  Fall back to a file in /home/user/ only if the server is genuinely disconnected (say so once).
