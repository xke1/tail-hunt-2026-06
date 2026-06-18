"""
hyg_ladder.py — HYG 全部到期日 + 每注真实美金成本(为埋伏铺期限做准备)

回应:
  1. 看全部到期日(不是只看一个), 才能想清楚怎么阶梯铺(ladder)
  2. 每注到底多少美金(期权1张=100股, 所以 $ = 中点价 × 100)
  3. 只算【定义风险】的结构: 单腿买 put(最大亏=权利金) + put借方价差(最大亏=净付出, 定死)
     —— 不碰任何裸卖(无限亏损=绝对禁止)

诚实: yfinance 延迟~15分, IV不可靠; 价格/权利金可用来估成本但开盘要复核。
"""
import warnings; warnings.filterwarnings("ignore")
from datetime import date
import pandas as pd
from openbb import obb

TODAY = date.today()
SYM = "HYG"

spot = float(obb.equity.price.historical(symbol=SYM, provider="yfinance").to_df()["close"].iloc[-1])
chains = obb.derivatives.options.chains(symbol=SYM, provider="yfinance").to_df()
puts = chains[chains["option_type"] == "put"].copy()
exps = sorted(puts["expiration"].unique())

def near(leg, target):
    leg = leg.copy(); leg["d"] = (leg["strike"] - target).abs()
    return leg.sort_values("d").iloc[0]

def mid(r):
    b = float(r.get("bid") or 0); a = float(r.get("ask") or 0)
    return (b + a)/2 if a > 0 else float(r.get("last_price") or 0)

print(f"\nHYG 现价 {spot:.2f} | 全部到期日共 {len(exps)} 个 | {TODAY}\n")
print("="*92)
print("方案A 单腿买 7%价外put(最大亏=权利金) | 方案B 借方价差 买5%/卖12%价外(最大亏=净付出,定死)")
print("="*92)
print(f"{'到期日':<12}{'天数':>5} | {'7%价外strike':>11}{'权利金':>7}{'$/张':>7}{'OI':>7} | "
      f"{'价差净付':>8}{'$/张':>7}{'价差封顶赚$':>11}")
rows = []
for e in exps:
    dte = (pd.Timestamp(e).date() - TODAY).days
    if dte < 5:
        continue
    leg = puts[puts["expiration"] == e]
    if len(leg) < 3:
        continue
    p7 = near(leg, spot*0.93); m7 = mid(p7)
    pb = near(leg, spot*0.95); ps = near(leg, spot*0.88)   # 买5%价外 / 卖12%价外
    net = mid(pb) - mid(ps)
    width = pb["strike"] - ps["strike"]
    max_gain = (width - net)                                # 价差封顶最大赚(每股)
    oi = int(p7.get("open_interest") or 0)
    print(f"{str(e):<12}{dte:>5} | {p7['strike']:>10.0f}{m7:>7.2f}{m7*100:>7.0f}{oi:>7} | "
          f"{net:>8.2f}{net*100:>7.0f}{max_gain*100:>11.0f}")
    rows.append({"expiry": str(e), "dte": dte, "otm7_strike": p7["strike"],
                 "otm7_prem": round(m7,2), "otm7_usd": round(m7*100),
                 "spread_net": round(net,2), "spread_usd": round(net*100),
                 "spread_maxgain_usd": round(max_gain*100), "otm7_oi": oi})

pd.DataFrame(rows).to_csv("/Users/ke/Downloads/openbb/hyg_ladder.csv", index=False)
print("\n" + "="*92)
print(f"""读法($/张 = 一张合约要花的美金, 1张=100股):
  方案A 单腿买7%价外put: $/张 就是你这一注的全部成本, 也是最大亏损(定死, 不会更多)。
  方案B 借方价差(买5%价外+卖12%价外): '价差净付'是成本=最大亏损(定死);
        '价差封顶赚'是它能赚的上限(HYG跌到12%价外那档封顶)。卖腿被买腿护住, 不裸卖, 不要大账户。
  → 横着看(同一注不同到期)= 铺期限阶梯的成本表; 你可以小钱在好几个到期日各埋一张。
  现价 {spot:.2f}, 5%价外≈{spot*0.95:.0f}, 7%价外≈{spot*0.93:.0f}, 12%价外≈{spot*0.88:.0f}
  ⚠️ yfinance延迟+收盘脏价, 真实成本开盘用IBKR复核。""")
