# tail-hunt — 一张"读得懂世界"的彩票 / A Lottery That Makes You Read the World

> 小资金期权,凸性优先,赌右尾。
> Small-capital options. Convexity first. Betting the right tail.

---

## 老实说,这是什么 / What this honestly is

**老实说,这更像一张彩票——我也不知道它有没有正期望(EV)。**
但它比普通彩票强在一点:每隔固定时间,它**逼你去读世界正在发生什么、哪里在悄悄变脆弱**,然后用很小的钱押一个"右尾"。你大概率每次小亏一点,偶尔——可能——中一次大的。

重点不是确定性。重点是:**刮刮乐让你什么都学不到、毫无参与感;而这个"彩票"让你看懂世界、有参与感、和市场互动。** 你为这点参与感和理解力付的,就是那一点点小亏。

**Honestly? This is closer to a lottery ticket than an edge machine — I genuinely don't know if it has positive EV.**
But it beats a lottery in one way: on a fixed schedule it **forces you to read what's actually happening in the world**, find where things are quietly getting fragile, and place a tiny bet on a "right tail." You'll usually lose a little; once in a while you *might* win big.

The point isn't certainty. It's that **a scratch ticket teaches you nothing and feels like nothing — while this "lottery" makes you understand the world and feel in the game.** The small recurring loss is what you pay for that engagement and understanding.

---

## 它每次做什么 / What it does each run

每跑一次,它会:
1. **扫世界**——读新闻、宏观、利差、期权,找"哪里在变脆弱"。
2. **找便宜的尾巴**——脆弱、还没被市场定价、保险又便宜,三个都中才考虑。
3. **自己攻击自己**——派一个独立的"杠精"用具体证据来杀掉每个想法,杀不死的才留下。
4. **给你一张地图**——全局局势 + 分类侦察清单(农产品看啥、股票看啥…),最后给≤1个值得埋伏的,或者诚实地说**"今天没有"**。

Each run it: scans the world for fragility → looks for tails that are **fragile + not-yet-priced + still cheap** → **attacks its own ideas** with an independent skeptic that tries to kill them with hard evidence → hands you a map (global picture + a per-category watchlist) and either ≤1 idea worth ambushing, or an honest **"nothing today."**

> 大多数时候它会说"今天没有"——**这是特性,不是 bug**。拥挤的故事保险早就贵了,没便宜的尾。能拒绝出手,才是它最值钱的地方。
> Most days it says "nothing today" — **that's a feature, not a bug.** Crowded stories are already expensive; the value is in refusing to bet.

---

## repo 里有什么 / What's inside

- `.claude/skills/tail-hunt/` — 核心"剧本":怎么想 + 输出长啥样 + 防自欺的规矩。 *(the core: how it reasons, the output format, the anti-self-deception rules)*
- `rank.py` / `deep_read.py` / `*_scanner.py` — 数据扫描器(用免费 OpenBB)。 *(data scanners on free OpenBB data)*
- `ibkr_bridge.py` — IBKR 只读桥(`ib_async`)。 *(read-only IBKR bridge)*
- `output/` — **每次推理的完整记录(带时间戳)**。 *(full timestamped record of every run)*
- **失败博物馆 / dead-ends museum**(在 output 里):至今 **6/6 个想法都被自己的杠精杀了**——信用债太拥挤、做空长债其实最挤、买错了载体(ETF 的损耗吃光收益)、把催化剂方向搞反。**"为什么没下注"比"下了什么"更值得读。** *(6/6 ideas killed so far, each with sourced kill-shots — why we DIDN'T bet is the most useful part.)*

---

## 怎么跑 / Run it

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FRED_API_KEY=你的免费key   # https://fredaccount.stlouisfed.org/apikeys
python rank.py            # 排行榜 leaderboard
python deep_read.py HYG   # 单标的深读 deep-read one ticker
```

---

## 诚实声明 / Honest notes

- **研究 + 交流,不是投资建议。** 自己的钱自己负责。 *(Research & exchange, not advice. Your money, your call.)*
- **我不知道它有没有正 EV。** 它的价值我说不清是"赚钱",更确定的是"读懂世界 + 参与感"。 *(I don't know if it has positive EV. Its value is "understanding the world + engagement" more than "making money.")*
- 免费数据延迟、IV 不准;只买或定义风险价差,**禁裸卖**。 *(Free data is delayed; only buy or defined-risk spreads, never naked.)*
- 用 AI 辅助构建,全程标注"真拉到的数 vs 推理",独立对抗验证。 *(AI-assisted, with PROVEN-vs-reasoned labels and independent adversarial checks.)*

---

**欢迎对小资金期权 / 投机有兴趣的人来交流、分享心得、挑刺、贡献。**
Anyone into small-capital options / speculation — come share, poke holes, contribute.
GitHub: [@xke1](https://github.com/xke1)
