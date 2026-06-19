# tail-hunt output template v3 (logic-led · dashboard mandatory · self-adversarial trace)

> English mirror of `OUTPUT_TEMPLATE.md`.

**Core: logic argument occupies the main real estate; numbers occupy the verification real estate.** Fragility/undigested are CAUSAL REASONING, not measurement. Never compress an argument into one sentence.
**Whether or not there's an idea, Section 1 (dashboard) and Section 2 (fragility leaderboard) MUST be produced** — this is the "see the whole picture" you want, not just one recommendation.

Order: 0 header → 1 global dashboard → 2 fragility leaderboard → 2.5 watchlist → 3 candidate deep-adversarial → 4 verdict → 5 honesty notes.

---

## 0. Run header
```
date/time | scanned N tickers | runtime | data = OpenBB (yfinance ~15-min delayed) | IBKR = Ke eyeballs last
OpenBB anchors: HY OAS x% (yth pct) | IG OAS x% (yth pct) | VIX (yth pct) | 10Y-2Y
```

## 1. Global situational dashboard (mandatory · every run · even with no idea)
**This is "today's fragility map" — for each of 8 domains give [one-line state judgment + one key number].** Goal: let the reader see at a glance which corner is accumulating fragility and which is calm.
```
domain        state{complacent/tense/already-detonated/normal}   one-line judgment (why)            key number (PROVEN+source)
credit        complacent                                          spreads at historic lows, no event priced   HY OAS 1.4th pct
rates/FX      ...                                                                                              10Y-2Y 0.29
macro/money   ...
AI/tech       ...
geopolitics   ...
commodities   ...
market-struct ...                                                                                             VIX 54th pct
crypto        ...
```
**Dashboard conclusion:** one paragraph — what state is the overall market in today? Which 1-2 domains most deserve watching (fragility accumulating), which are noise? Pure judgment, numbers corroborate.

## 2. Fragility leaderboard (mandatory)
**All tickers ranked by "fragility"** — not buy recommendations, but the entry list of "what's worth taking into deep logic argument." rank.py outputs Top-N, but each row adds a column [first read: why it might be fragile] (one line, pure logic intuition, numbers corroborate).
```
#  ticker  type      spot    IV/RV  skew  off-52w-high%  first read: why it might be fragile (one line)
1  TLT     rate-tail ...     1.41   ...   ...            long bond, non-linear victim of a rate reversal
2  HYG     credit    ...     1.86   ...   ...            junk-bond redemption spiral (see reference argument)
...
```
**Group summary by type:** bonds/credit cluster overall state, banks, defensives, commodities… one line each.

## 2.5 Watchlist (mandatory · "where to look" intelligence map)
**Does NOT pass the triple-intersection gate (that's for buy recommendations). This only answers "where to look," breaking the whole picture into per-category homework you can act on at IBKR. Even on "nothing today" this must be produced.**

**Three hard rules (prevent degeneration):**
- **① Non-consensus quota:** label each category [causally independent of today's #1 consensus cluster?]. **Independent ones first, and independent categories ≥ half.** Prevents the list from quietly becoming "N skins of the #1 consensus" (e.g., AI-infra/semis/crypto are all variants of the "AI capex" tail).
- **② Light-heavy boundary:** here each "why" can be one line (it's an entrance, not a conclusion). But once a ticker enters Section 3 deep-adversarial, it **must expand into ≥5-step causal chain + falsification + independent skeptic kill** — don't fob off the deep stage with the one-liner.
- **③ Forced convergence:** ~6 categories × 1-2 each = **8-10 to glance**; at the end **converge to "today's 3 to deep-dig"** (most non-consensus + cheapest + most independent catalyst). Converging to 3 beats spreading 20.
```
category | independent? {indep✓ / consensus-variant✗ / semi} | watch (1-2) | why (one line) | which expiry | what data
agriculture | indep✓ | WEAT/CORN | El Nino weather tail, market treats as non-factor | Sep-Dec | IV Rank/skew + USDA WASDE + ENSO
rates       | indep✓ | TLT       | hawkish Fed + inflation, long bond very calm → non-linear | ~90-180d | IV/RV + Fed dots + CPI/PCE
nat gas     | indep✓ | UNG       | AI power marginal fuel + heating season | winter Nov-Jan | IV skew + EIA storage + NOAA
metals      | indep✓ | CPER/PPLT | copper smelter cuts / Pt SA grid | ~90-180d | LME inv + Eskom + WPIC
AI/conc.    | variant✗ | SMH     | Mag7 ~34%, node cascade | ~90-180d | which AI name still has low IV rank
crypto      | semi   | MSTR/COIN | leverage; beaten down | ~90d | IV (likely already high) + skew
```
**Converge · today's 3 to deep-dig:** list 3 + why (most non-consensus + cheapest + most independent catalyst).

**Uniform data spec (every ticker, two layers):**
- **Options (eyeball IBKR):** 52W IV Rank/Pct · IV/RV · skew · target OTM strike's bid/ask · mid as % of spot · OI · delta (~10-15 delta = classic cheap tail)
- **Catalyst (non-market data):** per the table above
- **Expiry default:** ~90d main + ~150-180d runway; **never <30d**; align to the catalyst's trigger date (WASDE/FOMC/heating season/earnings)

## 3. Candidate deep-adversarial (the body · logic occupies the page · one block each)
> Rule 1 order-lock: write ①② pure logic first (**no numbers**) → only at ⑤ bring numbers.
> Only candidates that passed the Section-2 first screen and that finder thinks worth digging enter here for full adversarial.
```
### [candidate] ticker/basket — connection type {contradiction | shared tail}

① Fragility argument (main column · multi-paragraph · pure causal chain · ≥5 steps · stands without numbers)
   [finder] because A (verifiable fact) → so B → and because C → so D → so E (violent non-linear break)
   - reflexive/circular: <what, how it self-reinforces>
   - hidden leverage / must-roll debt: <...>
   - no margin of safety / concentration / cascade: <which node falls → how it spreads>
   - fragile assumption: <built on what "treated as certain" assumption, why it reverts>
   → Taleb hits which ones

② Undigested argument (main column · multi-paragraph · pure connection · state "where the market is wrong")
   - contradiction: text says X dangerous / numbers price it as fine / where exactly the gap is
   - or shared tail: seemingly unrelated {A,B,C} share one causal tail, chain = <...>
   - consensus or non-consensus? (evidence: what consensus says) → edge = where the gap is

③ Falsification condition (Rule 3 · mandatory before proposing)
   under what conditions is this judgment wrong? <can't write it = candidate killed>

④ Self-adversarial record (Rule 4 · must truly fight · this is where tokens burn)
   [finder] argument: [cite ①]
   [skeptic] kill-shot 1: [specific counter / falsification scenario, no vague doubt]
   [finder] response 1: [rebut point-by-point or withdraw on the spot]
   [skeptic] kill-shot 2: [new angle, no repeat of 1]
   [finder] response 2: ...
   ...(until skeptic gives no new kill-shot for 2 rounds = held, or finder withdraws = killed)
   conclusion: held (what it finally withstood) / killed (by which shot)

⑤ Numbers verify (Rule 1 · only now · verify ①② + judge cheapness)
   spot | RV%(pct) | ATM-IV | OTM-IV | skew | IV/RV (<1=cheap) | cost $/contract | OI
   hallucination check: is IV monotonic across strikes; flag dirty quotes ⚠️ and cut
   → cheap? (IV/RV relative ranking + skew + liquidity gate)

⑥ Triple-intersection verdict: ① fragile✓? ② undigested✓? ③ cheap✓? → how many gates passed
```

## 4. Today's verdict
```
≤1 idea: ticker / structure (no naked, only buy or defined-risk spread) / expiry / strike / cost $ / max loss (fixed) /
  three columns (fragility summary / undigested summary / cheap verification) / trigger / life-or-death line
  OR
"nothing today": which gate of the triple intersection failed (① / ② / ③) + why (honest)
  —— but Section 1 dashboard + Section 2 leaderboard already gave the whole picture, so "nothing today" ≠ "wasted run"
→ write to output/tail-hunt_YYYY-MM-DD_HHMM.md + the life-or-death ledger
```

## 5. Honesty notes
```
- PROVEN (actually fetched) vs EXPECTED (reasoned) — which is which
- which candidates got killed by self-adversarial (and by which shot) ← proves real adversarial, not laziness
- data weaknesses (yfinance far-dated dirty quotes? free data has no clean IV history percentile?)
- residual consensus contamination (which "fragilities" are already public house view)
- IBKR cross-check status (if no subscription, note OpenBB-only, pending Ke's eyeball)
```

---

## Auditor self-check (before output, check each; fail = rewrite)
```
□ Section 1 dashboard: all 8 domains given state + judgment + number? (mandatory; missing = rewrite)
□ Section 2 leaderboard: produced, each row has "why it might be fragile"? grouped by type?
□ Section 3 each candidate: ①② multi-paragraph, ≥5-step causal chain? (one sentence = bounce)
□ Order-lock: any number sneaked into ①②? (yes = violates Rule 1)
□ Falsification: written for every candidate? (no = candidate killed)
□ Self-adversarial: ≥ multiple rounds, new point each, real fight? skeptic gives specific kill-shots not vague doubt?
□ Anti-nonsense: survivors "withstood specific kill-shots," not "written long"?
□ Sources: every number has PROVEN/EXPECTED + source?
□ Speed check: did this run take long enough? Seconds out = no reasoning = failure, redo.
```
