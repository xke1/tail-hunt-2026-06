# tail-hunt — 小资金期权"尾部猎手" / Small-Capital Options Tail Hunter

> 一个用 AI 漏斗找"便宜的、肥的、被低估的尾部"的开源系统。
> An open research system: an AI funnel that hunts **cheap, fat, mispriced tails** in US options — built for **small-capital, convexity-first speculation**.

**这个 repo 是干嘛的**:小资金期权交流。我对各种投机倒把都感兴趣,期权更多是它的投机属性——用很小的钱、买便宜的凸性、赌右尾。欢迎对小资金期权有兴趣的人来交流、分享心得、挑刺、贡献。

**核心信仰**:
- 一直小亏、赌右尾(barbell 凸性)。90% 的时间在流血,靠偶尔一次大的。
- edge 大半是**情绪补偿费 + 崩盘溢价**——赢的结构反人性(没人愿意一直小亏)。
- **脆弱是【推理】出来的,不是【数字测量】出来的**。你不能用 IV 算出"这东西会崩",只能用因果链论证它会崩,再用数字看保险贵不贵。

---

## 系统长什么样

```
数据层(OpenBB, 免费): 扫宏观/利差/期权链 → 量化排行榜(RV/IV/IV-RV/skew)
        ↓
AI 漏斗(逻辑主导): 联网读文字 ⊕ 数字, 交叉找"矛盾 / 共享尾巴"
        ↓
靶心 = 三重交集(缺一不开火):
   ① 绝对脆弱(Taleb 测试: 反身循环/隐藏杠杆/无安全边际/集中/脆弱假设)
   ② 未消化(市场没把脆弱连起来 price: 矛盾 / 共享尾 / 含义未传导)
   ③ 便宜(IV/RV、skew、流动性——数字只验证, 不是脆弱的替代)
        ↓
反自欺: 独立 skeptic agent 用具体杀招攻击每个候选, 攻不倒才留下
        ↓
输出: 全域局势盘 + 脆弱度排行榜 + 分类侦察清单 + (≤1 推荐 或 诚实"今天没有")
```

**执行层**:IBKR(`ib_async`),小资金、现金账户、只买或定义风险价差、**禁裸卖**(无限亏损绝对禁止)。

---

## repo 里有什么

- `.claude/skills/tail-hunt/` — **核心**:SKILL.md(怎么想)+ OUTPUT_TEMPLATE.md(输出长啥样)。逻辑主导、5 条防自欺铁律、独立 skeptic 对抗。
- `rank.py` — 排行榜引擎(110 标的,RV/IV/IV-RV/skew/埋伏分,~2分钟)。
- `deep_read.py` — 单标的整张期权表深读(逐 strike IV/RV/skew + 幻觉检查)。
- `tail_scanner.py` / `hist_analog.py` / `credit_drill.py` / `hyg_ladder.py` — 各种数据探针。
- `ibkr_bridge.py` — IBKR `ib_async` 只读桥(拉报价/期权链结构)。
- `output/` — **每次推理的完整结果**(带时间戳)。
- **dead-ends museum**(在 output 里):至今 6/6 候选被独立 skeptic 杀死的完整记录——HYG/KRE/ORCL(信用簇=共识)、TLT(伪非共识,做空长债其实最挤)、WEAT(载体错:持 SRW 非减产的 HRW + contango)、UNG(roll 绞肉机十年 -89%)。**这些"为什么不开仓"比"开了什么"更值钱。**

---

## 三个真金白银的教训(找尾部前必查)

1. **真的不挤吗?** —— TLT 自以为非共识,其实做空长债是 2026 最挤交易之一(CFTC 创纪录净空)。
2. **载体对吗?** —— ETF 的 contango/错配能吃光你的 edge(WEAT≠HRW、UNG 十年 -89%)。要表达 view 用单名/期货/价差,别碰 contango ETF。
3. **催化剂方向对吗?** —— WEAT 把 El Nino 对小麦的方向搞反了(El Nino 对 HRW 带偏湿、缓解干旱)。

---

## 怎么跑

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# 免费数据 key(可选, 部分脚本要): 去 https://fredaccount.stlouisfed.org/apikeys 申请
export FRED_API_KEY=你的key
python rank.py            # 排行榜
python deep_read.py HYG   # 单标的深读
```
OpenBB MCP 接进 Claude Code 见 `.mcp.json`。tail-hunt skill 用法见 `.claude/skills/tail-hunt/SKILL.md`。

---

## 诚实声明(必须读)

- **这是研究 + 交流,不是投资建议。** 自己的钱自己负责。
- **免费数据延迟 ~15 分钟**,IV 不可靠;精确曲面要付费源(Theta/Polygon)。
- **系统大多数时候说"今天没有"——这是特性不是 bug。** 拥挤的共识处 IV 早已贵,没有便宜的非共识尾。能拒绝交易,才是它最值钱的地方。
- 用 AI 辅助构建(全程标 PROVEN/EXPECTED、独立对抗验证)。

---

欢迎 PR / issue / 喷。小资金期权,凸性优先,赌右尾。
GitHub: [@xke1](https://github.com/xke1)
