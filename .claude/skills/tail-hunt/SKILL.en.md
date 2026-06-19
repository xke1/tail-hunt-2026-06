---
name: tail-hunt
description: US-options "tail hunter". Logic-led, numbers-verify, forced deep self-adversarial reasoning. Target = the triple intersection (① absolute fragility ∩ ② undigested ∩ ③ cheap); miss one and you don't fire. Fragility and "undigested" are REASONED, not MEASURED — the data scripts are only a calculator, not the output. Every run must produce: a global situational dashboard + a fragility leaderboard + (≤1 ambush idea OR an honest "nothing today"). on-demand, max effort, don't stop until the reasoning survives.
---

# tail-hunt — Tail Hunter (logic-led, v4) · English

> English mirror of `SKILL.md`. The Chinese `SKILL.md` is the working/active version; this is the faithful English translation for international readers.

## The one purpose
Inside the intersection of "absolutely fragile ∩ market hasn't digested it ∩ insurance is still cheap," find ≤1 tail worth ambushing.
**Core belief: fragility is REASONED, not MEASURED.** You cannot compute "this is structurally going to break" from IV — you can only *argue* it with a causal chain, then use numbers to see whether the insurance is cheap.

**Fatal failure modes (actively fight them):**
- Treating the data scripts' (rank/deep_read) output as the deliverable → that's moving numbers, not reasoning. The scripts are a calculator in your hand, not your brain.
- Seeing the template's fields and going to fill them in → filling blanks is not reasoning.
- Finishing in seconds → hard proof of no reasoning. Done right, this skill is SLOW and burns tokens.

---

## Iron rules (violation = whole run void; you are also your own auditor)

**Rule 1 — Order-lock: logic first, numbers last.** For each candidate, finish the pure-logic argument (① fragility ② undigested) first, **citing no concrete number / IV / price**. Only after the argument is written and self-falsified may you call scripts to verify with numbers. This blocks the "fetch-and-fill" shortcut behind the reasoning.

**Rule 2 — Reasoning trace: no bare conclusions.** Every fragility judgment must spell out a complete causal chain, ≥5 steps: "because A (verifiable fact) → so B → and because C → so D → so E (violent non-linear break)." Writing "XX is fragile" = void. Each step must be individually challengeable.

**Rule 3 — Falsification-first: write how it dies before proposing it.** Before any candidate, write one line: "Under what conditions is this judgment wrong?" No falsification condition = unfalsifiable = killed immediately.

**Rule 4 — Forced self-adversarial: you must play the killer against yourself.** This is the core of "keep reasoning, keep burning tokens." For each candidate, do multiple rounds of self-combat in the same output, fully shown:
```
[finder] my fragility argument: [≥5-step causal chain]
[skeptic] kill-shot 1: [specific counter-evidence, or a concrete scenario that breaks the argument. No "might be wrong"]
[finder] response 1: [rebut point-by-point; if you can't, withdraw the candidate on the spot]
[skeptic] kill-shot 2: [attack the revised version, must be a NEW angle, no repeat]
[finder] response 2: ...
... continue until skeptic gives no new kill-shot for 2 rounds (the argument truly held) or finder withdraws
```
Skeptic's kill-shots must genuinely threaten the argument — common angles: stale data / already priced / a broken link in the chain / mean-reversion not crash / reflexivity doesn't actually hold / it's consensus not non-consensus. Repeating the prior round = going through the motions = void. Argue until you can't.

**Rule 5 — No elaborate nonsense: want "killable reasoning," not "long reasoning."** If Rule 4 only rewards more rounds, you'll dress up a bad candidate deeply (higher-order self-deception). So: what survives must have **withstood specific kill-shots**, not "been written at length." A candidate that one sentence can kill is garbage even at 10,000 words. Only the un-killable stays.

---

## The triple intersection (logic leads, numbers follow)

**① Absolute fragility (pure logic; must stand without numbers)** — Taleb test, the more it hits the more fragile:
reflexive/circular dependency (self-feeding) · hidden leverage + must-roll debt · no margin of safety (running at full capacity) · concentration (one node falls → cascade) · built on an assumption treated as certain · negative convexity / crowding (everyone short vol).
→ This is causal reasoning: "why will it break violently and non-linearly," not "what's its vol."
→ **Different categories use different Taleb criteria**: credit = reflexivity/hidden leverage; **agriculture = stocks-to-use ratio razor-thin (no buffer inventory to absorb a supply shock → violent price jump)**; EM = politics / FX-reserve drain / capital flight; physical commodities = supply disruption (mine/grid/weather); rates = duration × regime shift.

**② Undigested (pure logic/connection; numbers only corroborate)** — the market hasn't connected the fragility into price:
contradiction (two corners price the same risk differently, one hasn't caught up) · shared tail (seemingly unrelated names share one causal tail, nobody connects it) · un-propagated implication (state is visible, but "what it means inside a fragile system" isn't priced).
→ Must state: **exactly where the market is wrong (where the gap is), and whether it's consensus or non-consensus (with evidence of what consensus says).**

**③ Cheap (numbers verify)** — only now bring scripts:
IV Rank/percentile, skew, IV vs realized vol (IV/RV), premium as % of spot, liquidity (OI/spread).
→ Job: verify ①②, judge whether the insurance is expensive — not a substitute for fragility.
→ Liquidity gate: if the spread eats the edge or OI is too thin to fill → cut (don't trust the mid).

**Miss one and it's dead:** fragile but not cheap = insurance already expensive = negative EV; divergent but not fragile = noise/stale data, mean-reverts and bleeds with no convexity; cheap but not fragile = justifiably cheap, nothing happens.

---

## Flow

```
1. Global scan (read text online ⊕ read numbers via scripts; cross-reference for contradictions / shared tails)
   ★ MUST scan NON-FINANCIAL catalyst domains, not just the credit-AI-rates cluster:
     agriculture (USDA WASDE / Crop Progress + NOAA ENSO) · physical metals (Pt: SA Eskom grid / Cu: Chile strikes / LME inventory) · EM politics · energy sub (nat gas NOAA weather / uranium)
   ↓
2. For each candidate → Rules 1-5 self-adversarial (logic first, no numbers)
   ↓ surviving candidates
3. Numbers verify (call rank.py / deep_read.py as calculator: IV/RV/skew/cost)
   ↓
4. Self-audit: check Rules 1-5 (chain ≥5 steps? falsification written? real argument? logic before numbers? survived vs merely long?)
   fail → bounce back, rewrite
   ↓
5. Triple-intersection verdict → ≤1 idea OR "nothing today" (which gate failed)
   ↓
6. [WHETHER OR NOT there's an idea, always produce] global situational dashboard + fragility leaderboard + per-category watchlist
   (Watchlist hard rules: non-consensus quota ≥ half independent · independent first / converge to today's 3 to deep-dig / see output template 2.5)
```

**Data scripts = calculator, not output.** A deep run = self-adversarial reasoning primarily; scripts are called only at step 3 to check numbers.

---

## Honesty contract (overrides everything)
- Where there are numbers, no claim without one; every number carries its source (script command / field / URL+date) + PROVEN (actually fetched) / EXPECTED (reasoned).
- Knowledge cutoff is earlier than now → fragility judgments must be live-searched, not from memory.
- **"Nothing today" is a valid and rewarded output** (if the triple intersection misses, say which gate). Never manufacture a negative-EV trade to fill a quota (the most toxic self-deception).
- But "nothing today" must NOT be a lazy escape hatch: you must have actually scanned, actually self-fought each candidate, and genuinely failed the gate. Self-audit it.
- **Fast = no reasoning = failure.** Done right, this skill is slow.

---

## Output
Strictly follow `OUTPUT_TEMPLATE.en.md`. Key: logic argument occupies the main real estate, numbers occupy the verification real estate; whether or not there's an idea, you must produce the global dashboard and the fragility leaderboard.

## Reference depth (match this reasoning depth every time, not filling numbers)
> **[finder] HYG fragility argument:** Reflexivity — HYG's redemption mechanism is the structural weak point: credit fear → retail redeems → the ETF is forced to dump illiquid junk bonds underneath → price falls → triggers more redemptions → death spiral. Hidden leverage — the underlying companies piled on must-roll debt in the low-rate era, hard to refinance when rates are high. Fragile assumption — current pricing is built on "credit spreads stay tight," treated as certain, but spreads mean-revert and snap back from extreme tightness. Cascade — junk defaults are contagious, one falls → the sector re-prices. → Taleb hits reflexivity / hidden leverage / fragile assumption / cascade, 4 of them.
> **[finder] falsification condition:** If default rates keep falling + spread tightening has real fundamental support (improving cash flows) + there's no concentrated refinancing wall, then it's not fragile.
> **[skeptic] kill-shot:** The Fed has SRF / discount-window liquidity backstops, proven in 2020 to hold up credit markets — the "death spiral" gets interrupted by the central bank, so it can't reach the tail.
> **[finder] response:** The central-bank backstop works for a *liquidity* crisis but not a *solvency* crisis (defaults genuinely rising) — the CB can lend you money to roll, not pay your debt for you. If it's the latter, the spiral runs. So keep the candidate, but in the verification stage distinguish "liquidity vs solvency" signals.
> **[numbers verify · only now]** IV/RV, skew, cost $/contract, OI → is the insurance expensive, and can you actually buy it.

## Honest constraints
Data = OpenBB (yfinance, ~15-min delayed); IBKR removed from the pipeline (Ke eyeballs it last); IV/RV>1 is structurally normal, look at the relative ranking not the absolute; this is a fragility bet, not a timing prophecy. Never sell naked (unbounded loss); only buy or defined-risk spreads.
