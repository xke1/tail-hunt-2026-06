"""
credit_drill.py — 漏斗第二层(vol-surface-drill)真数据版

背景: 两个独立系统(文员web搜 + tail_scanner OpenBB算)都指向"信用通道凸性最便宜"。
本脚本用真实期权数据去【验证】这个声称: 现在买信用通道(LQD/HYG/JNK)的 put 到底贵不贵。

缩写:
  put = 看跌期权(赌下跌的保险); ATM = at-the-money 平值; OTM = out-of-the-money 价外(更便宜更凸)
  IV = implied volatility 隐含波动率; OI = open interest 未平仓量(流动性); mid = 买卖价中点
  bid/ask = 买价/卖价; DTE = days to expiration 距到期天数

诚实铁律:
  - bid/ask/OI/strike 来自 yfinance(延迟~15分), 可信度中
  - IV 是 yfinance 自己估的, **不可靠**, 只看相对不看绝对
  - "贵不贵"的终判要 IV 历史分位(Theta/Polygon), 免费数据给不了 → 标 ❌
运行: source .venv/bin/activate && python credit_drill.py
"""
import warnings; warnings.filterwarnings("ignore")
from datetime import datetime, date
import pandas as pd
from openbb import obb

TODAY = date.today()
TARGET_DTE = 90          # 想要的到期天数(~3个月,给催化剂时间发酵)
OTM_LEVELS = [0.00, 0.05, 0.10]   # ATM, 5% OTM, 10% OTM
NAMES = ["LQD", "HYG", "JNK"]


def nearest_expiry(expiries, target_dte):
    best, bestdiff = None, 1e9
    for e in expiries:
        d = (pd.Timestamp(e).date() - TODAY).days
        if d < 20:        # 太近的不要(没催化剂时间)
            continue
        if abs(d - target_dte) < bestdiff:
            best, bestdiff = e, abs(d - target_dte)
    return best


def drill(sym):
    print("=" * 72)
    print(f"标的: {sym}")
    # 现价: 用历史最新收盘(比 quote 列名稳定)
    spot = float(obb.equity.price.historical(symbol=sym, provider="yfinance").to_df()["close"].iloc[-1])
    chains = obb.derivatives.options.chains(symbol=sym, provider="yfinance").to_df()
    puts = chains[chains["option_type"] == "put"].copy()
    exp = nearest_expiry(sorted(puts["expiration"].unique()), TARGET_DTE)
    dte = (pd.Timestamp(exp).date() - TODAY).days
    print(f"现价: {spot:.2f} | 选到期: {exp} (距今 {dte} 天)")
    leg = puts[puts["expiration"] == exp].copy()
    # ATM IV 参考(最接近现价的 put)
    leg["dist"] = (leg["strike"] - spot).abs()
    atm_iv = leg.sort_values("dist").iloc[0].get("implied_volatility")
    print(f"\n{'目标':<8}{'行权价':>8}{'bid':>7}{'ask':>7}{'中点':>7}{'权利金%现价':>11}{'IV(不可靠)':>11}{'OI':>7}")
    rows = []
    for otm in OTM_LEVELS:
        target_strike = spot * (1 - otm)
        leg["d2"] = (leg["strike"] - target_strike).abs()
        r = leg.sort_values("d2").iloc[0]
        bid = float(r.get("bid") or 0); ask = float(r.get("ask") or 0)
        mid = (bid + ask) / 2 if ask > 0 else float(r.get("last_price") or 0)
        prem_pct = mid / spot * 100
        iv = r.get("implied_volatility"); oi = r.get("open_interest")
        tag = f"{int(otm*100)}% OTM" if otm > 0 else "ATM"
        print(f"{tag:<8}{r['strike']:>8.1f}{bid:>7.2f}{ask:>7.2f}{mid:>7.2f}{prem_pct:>10.2f}%"
              f"{(iv if iv is not None else float('nan')):>11.3f}{int(oi or 0):>7}")
        rows.append({"sym": sym, "expiry": str(exp), "dte": dte, "otm": f"{int(otm*100)}%",
                     "strike": r["strike"], "mid": round(mid,2),
                     "prem_pct_of_spot": round(prem_pct,2),
                     "iv_unreliable": round(float(iv),3) if iv is not None else None,
                     "open_interest": int(oi or 0)})
    # 粗略 skew: 10% OTM put IV 相对 ATM IV
    try:
        otm_iv = rows[-1]["iv_unreliable"]; a_iv = round(float(atm_iv),3)
        skew = round(otm_iv - a_iv, 3)
        print(f"\n  粗略 skew (10%OTM put IV - ATM IV): {skew:+.3f}  "
              f"[正=尾部需求高/保护偏贵; 负=尾部被冷落/可能便宜] (IV不可靠,仅方向)")
    except Exception:
        pass
    return rows


def main():
    print(f"\n信用通道 vol-surface-drill | 真数据验证 | {datetime.now():%Y-%m-%d %H:%M}\n")
    all_rows = []
    for sym in NAMES:
        try:
            all_rows += drill(sym)
        except Exception as e:
            print(f"  !! {sym} 抓取失败: {type(e).__name__}: {e}")
        print()
    pd.DataFrame(all_rows).to_csv("/Users/ke/Downloads/openbb/credit_drill.csv", index=False)
    print("=" * 72)
    print("结果存: ~/Downloads/openbb/credit_drill.csv")
    print("""
诚实节(必须读):
  ✓ 可信: 行权价/bid/ask/中点/OI/权利金%  —— 这是你真要付的钱(延迟~15分)
  △ 不可信: IV 绝对值(yfinance自估), 只能看相对/方向
  ❌ 给不了: "这个IV在历史上算便宜还是贵"(IV分位) —— 要 Theta/Polygon 付费源
  → 所以本表能告诉你"埋伏一注要花多少钱(权利金%)", 但不能终判"现在是不是便宜的时候"
""")


if __name__ == "__main__":
    main()
