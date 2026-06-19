# tail-hunt — A Lottery That Makes You Read the World

🌐 **English** | [中文](./README.zh.md)

> Small-capital options. Convexity first. Betting the right tail.

---

## What this is

Options are gambling too — nobody knows what the future holds. But unlike a lottery ticket, this one has skin in *understanding*: you can't place the bet without first reading what's actually happening in the world.

I open-sourced a system built for exactly this. **Multi-agent, multiple-negation.** It judges any opportunity by the **intersection of three dimensions**:

1. **Will the underlying itself move violently?** — absolute fragility
2. **Is the premium still cheap?** — cheap convexity
3. **How has the market already reacted to this risk?** — is it digested / consensus?

Only when all three line up does it tell you there's an opportunity worth opening **today**. And even when there isn't — just say *"pick the tallest of the dwarves"* in the workspace, and the AI hands you a shortlist of tickers worth going to look at carefully on the exchange (IBKR).

Discussion, poking holes, and falsification are all welcome. **This is not investment advice — especially not for large capital.**

---

## The honest core

Honestly, this is closer to a **lottery with unknown EV** than an edge machine. I don't claim alpha. Its value is that, on a fixed schedule, it **forces you to understand the world and feel in the game** — and you pay for that engagement with a small, recurring loss. A scratch ticket teaches you nothing and feels like nothing; this one makes you understand *what's breaking*.

---

## Design details

- **Logic-first, numbers-verify.** Fragility is *reasoned*, not *measured*. You can't compute "this will break" from implied vol — you argue it with a causal chain, then use numbers only to check whether the insurance is cheap.
- **Independent skeptic agents — not marking its own homework.** Each candidate is attacked by a *separate* agent whose only job is to kill it with hard, sourced evidence. It survives only if it can't be killed. (So far: **6/6 ideas killed.**)
- **Five anti-self-deception rules** baked into the skill: ① order-lock (pure logic before any number) ② reasoning-trace (≥5-step causal chains, no bare conclusions) ③ falsification-first (write how it dies before proposing it) ④ real adversarial spiral (specific kill-shots, new angle each round, argue until it can't be killed) ⑤ killable reasoning, not long reasoning (elaborate packaging of a bad idea is the higher-order self-deception).
- **Always produces a map — even with no trade:** a global fragility dashboard (8 domains) + a per-category watchlist (agriculture / rates / energy / metals / equities / crypto…) + a **dead-ends museum** (every killed idea with its kill-shot — *why we didn't bet is the most useful part*).
- **Three lessons it has already paid for:** (a) *Is it actually un-crowded?* (shorting long bonds felt non-consensus but is one of the most crowded trades). (b) *Is the vehicle right?* (ETF contango/mismatch can eat your whole edge — WEAT ≠ the wheat that's tight; UNG is down ~89% over a decade). (c) *Is the catalyst direction right?*
- **Data:** free OpenBB layer (~15-min delayed, IV unreliable). **Execution:** IBKR, small capital, **only buy or defined-risk spreads, never naked** (unbounded loss is forbidden).
- **Most days it says "nothing today" — that's a feature, not a bug.** Crowded stories are already expensive; refusing to bet is where the value is.

---

## What's inside

- `.claude/skills/tail-hunt/` — **the core**: `SKILL.en.md` (how it reasons) + `OUTPUT_TEMPLATE.en.md` (output format) + the anti-self-deception rules. (Chinese originals: `SKILL.md` / `OUTPUT_TEMPLATE.md`.)
- `rank.py` — leaderboard engine (~110 tickers: realized vol / IV / IV-RV / skew, ~2 min).
- `deep_read.py` — full option-table deep read for one ticker (per-strike IV/RV/skew + hallucination check).
- `tail_scanner.py` / `hist_analog.py` / `credit_drill.py` / `hyg_ladder.py` — data probes.
- `ibkr_bridge.py` — read-only IBKR bridge (`ib_async`).
- `output/` — full, timestamped record of every run (including the dead-ends).

---

## Run it

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FRED_API_KEY=your_free_key   # https://fredaccount.stlouisfed.org/apikeys
python rank.py            # leaderboard
python deep_read.py HYG   # deep-read one ticker
```
The OpenBB MCP wiring for Claude Code is in `.mcp.json`. The skill itself is in `.claude/skills/tail-hunt/`.

---

## Honest notes

- **Research & exchange, not advice.** Your money, your call.
- **I don't know if it has positive EV.** Its value is "understanding the world + engagement," not a promise of profit.
- Free data is delayed; precise vol surfaces need paid sources (Theta/Polygon).
- AI-assisted build, with PROVEN-vs-reasoned labels and independent adversarial verification throughout.

---

**Anyone into small-capital options / speculation — come share, poke holes, falsify.**
GitHub: [@xke1](https://github.com/xke1)
