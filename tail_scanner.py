"""
tail_scanner.py — 尾部猎手"暴力找机会"扫描器(第一节)

回应三个不满:
  1. 不要几个月前的 → 全是今天/最新可得的真数(运行时间戳打在输出里)
  2. 要数据支撑     → 每个结论都算了历史分位/比率,带真实数字
  3. 要暴力         → 循环扫宏观 + 一池标的,批量算批量排

两层:
  第一层 宏观尾巴扫描(FRED, 免费可靠): 哪条结构性尾巴现在最便宜(分位最低=最自满)
  第二层 标的凸性粗筛(yfinance, 免费但IV不可靠): 哪些票现在最"平静"=埋伏成本可能低

诚实: 第二层 IV 来自 yfinance 不可靠, 只当粗排; 精确定价要 Theta/Polygon。
运行: source .venv/bin/activate && python tail_scanner.py
"""
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from openbb import obb

NOW = datetime.now().strftime("%Y-%m-%d %H:%M")
LINE = "=" * 78


def pctile(series, value):
    """value 在 series 里的百分位(0-100)。"""
    s = series.dropna()
    return round(float((s < value).mean() * 100), 1)


# ----------------------------------------------------------------------------
# 第一层:宏观尾巴扫描
# ----------------------------------------------------------------------------
MACRO = [
    ("BAMLH0A0HYM2", "高收益债 OAS", "low_is_cheap_tail"),   # 低=信用自满=尾巴便宜
    ("BAMLC0A0CM",   "投资级 OAS",   "low_is_cheap_tail"),
    ("VIXCLS",       "VIX 股指波动", "low_is_cheap_tail"),   # 低=平静=股指尾巴便宜
    ("T10Y2Y",       "10Y-2Y 利差",  "context"),             # 倒挂=衰退预警
    ("BAMLH0A0HYM2", "", ""),  # placeholder removed below
]

def scan_macro():
    print(LINE); print(f"第一层 · 宏观尾巴扫描  (数据时间: 见各行 | 运行: {NOW})"); print(LINE)
    rows = []
    seen = set()
    for sid, name, kind in MACRO:
        if not name or sid in seen:
            continue
        seen.add(sid)
        try:
            df = obb.economy.fred_series(symbol=sid, provider="fred").to_df().dropna()
            latest = float(df.iloc[-1].iloc[0]); date = df.index[-1]
            col = df.iloc[:, 0]
            p_all = pctile(col, latest)
            p_5y = pctile(col.iloc[-1260:], latest)  # 近~5年
            flag = ""
            if kind == "low_is_cheap_tail" and p_5y <= 20:
                flag = "  ← 尾巴便宜(自满)"
            elif kind == "low_is_cheap_tail" and p_5y >= 80:
                flag = "  ← 尾巴贵(恐慌)"
            elif kind == "context" and latest < 0:
                flag = "  ← 收益率曲线倒挂"
            rows.append((name, latest, p_all, p_5y, str(date), flag))
        except Exception as e:
            rows.append((name, None, None, None, f"失败:{type(e).__name__}", ""))
    print(f"{'指标':<14}{'最新值':>9}{'全史分位':>9}{'近5年分位':>10}  {'日期':<12}{'信号'}")
    for name, val, pa, p5, date, flag in rows:
        if val is None:
            print(f"{name:<14}{'—':>9}{'—':>9}{'—':>10}  {date}")
        else:
            print(f"{name:<14}{val:>9.2f}{pa:>8.1f}%{p5:>9.1f}%  {date:<12}{flag}")
    print("\n  读法: 低收益债/VIX 分位 = 市场自满 = 买尾部凸性最便宜的时候(你埋伏的入口)")
    return rows


# ----------------------------------------------------------------------------
# 第二层:标的凸性粗筛
# ----------------------------------------------------------------------------
UNIVERSE = [
    "SPY","QQQ","IWM","DIA",                  # 股指
    "HYG","LQD","JNK","TLT","IEF",            # 信用/利率
    "XLF","XLE","XLK","XLU","XLP","XLV","XLI","XLRE",  # 板块
    "EEM","FXI","EWZ",                        # 新兴市场
    "GLD","SLV","USO","UNG",                  # 商品
    "KRE","SMH","ARKK","SOXL",                # 高beta/脆弱
]

def realized_vol(close, window=20):
    ret = np.log(close / close.shift(1))
    return ret.rolling(window).std() * np.sqrt(252)  # 年化

def scan_universe():
    print("\n" + LINE); print(f"第二层 · 标的凸性粗筛  ({len(UNIVERSE)}只 | 运行: {NOW})"); print(LINE)
    out = []
    failed = []
    for sym in UNIVERSE:
        try:
            h = obb.equity.price.historical(symbol=sym, start_date="2024-01-01",
                                            provider="yfinance").to_df()
            close = h["close"]
            rv = realized_vol(close).dropna()
            rv_now = float(rv.iloc[-1])
            rv_pct = pctile(rv, rv_now)              # 当前实现波动在自身历史的分位
            price = float(close.iloc[-1])
            high = float(close.tail(252).max())
            ddown = round((price / high - 1) * 100, 1)  # 离52周高点回撤%
            out.append({"sym": sym, "rv_now": round(rv_now*100,1),
                        "rv_pct": rv_pct, "ddown": ddown, "price": round(price,2)})
        except Exception as e:
            failed.append((sym, type(e).__name__))
    df = pd.DataFrame(out)
    # 埋伏分 = 越平静(低实现波动分位) + 越贴高点(自满) → 凸性可能越便宜
    df["ambush"] = (100 - df["rv_pct"]) + (100 + df["ddown"].clip(-100, 0))
    df = df.sort_values("ambush", ascending=False).reset_index(drop=True)
    print(f"{'排名':<5}{'标的':<7}{'实现波动%':>10}{'波动分位':>9}{'离高点%':>9}{'埋伏分':>8}")
    for i, r in df.iterrows():
        print(f"{i+1:<5}{r['sym']:<7}{r['rv_now']:>9.1f}%{r['rv_pct']:>8.1f}%{r['ddown']:>8.1f}%{r['ambush']:>8.0f}")
    if failed:
        print(f"\n  抓取失败({len(failed)}): {', '.join(s for s,_ in failed)}")
    print("\n  读法: 埋伏分高 = 又平静又贴高点 = 市场最不设防 = 买便宜凸性的候选")
    print("  ⚠️ 这是粗筛(实现波动可靠, 但'期权是否真便宜'要看IV, yfinance IV不可靠 → 精确要付费源)")
    return df


if __name__ == "__main__":
    print(f"\n尾部猎手扫描器 | 运行时间 {NOW}\n")
    scan_macro()
    df = scan_universe()
    df.to_csv("/Users/ke/Downloads/openbb/tail_opportunities.csv", index=False)
    print(f"\n结果已存: ~/Downloads/openbb/tail_opportunities.csv")
