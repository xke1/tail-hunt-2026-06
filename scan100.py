"""
scan100.py — 真·暴力 OpenBB 扫描器(秒级, 无AI agent, 无垃圾CSV)
扫 100+ 标的, 算"又平静又贴高点=凸性可能最便宜"的埋伏分, 全部排序打印到屏幕。
这是快通道(纯数据计算); 联网读社会脆弱是慢通道(另跑)。
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from openbb import obb

U = [
 "SPY","QQQ","IWM","DIA","VTI",
 "XLF","XLE","XLK","XLU","XLP","XLV","XLI","XLRE","XLB","XLC","XLY",
 "HYG","LQD","JNK","TLT","IEF","SHY","AGG","EMB","BKLN",
 "VXX","UVXY",
 "GLD","SLV","USO","UNG","DBC","CPER","WEAT","CORN",
 "EEM","FXI","EWZ","EWJ","EWG","INDA","EWW","EWY",
 "SMH","SOXX","KRE","KBE","XBI","IBB","ARKK","TAN","ICLN","ITB","XHB","JETS","XOP","OIH",
 "NVDA","ORCL","MSFT","META","GOOGL","AMD","AVGO","AAPL","AMZN","TSLA","SMCI","PLTR","MU","DELL","ANET","VRT",
 "CEG","VST","TLN","NRG",
 "JPM","BAC","C","GS","MS","WFC","SCHW","COF",
 "HD","LOW","NKE","SBUX","MCD","DIS",
 "UNH","LLY","PFE","JNJ",
 "XOM","CVX","OXY",
 "COIN","MSTR","HOOD","SQ","AFRM","UPST","CVNA",
 "O","SPG","ASML","AMAT","LRCX","KLAC",
]

def rvol(c, w=20):
    return (np.log(c/c.shift(1)).rolling(w).std()*np.sqrt(252))

rows, fail = [], []
for s in U:
    try:
        c = obb.equity.price.historical(symbol=s, provider="yfinance", start_date="2024-06-01").to_df()["close"]
        c.index = pd.to_datetime(c.index)
        rv = rvol(c).dropna(); rvn = float(rv.iloc[-1])
        rvp = round(float((rv < rvn).mean()*100),1)          # 当前实现波动在自身历史分位
        px = float(c.iloc[-1]); hi = float(c.tail(252).max())
        dd = round((px/hi-1)*100,1)                            # 离52周高点%
        amb = round((100-rvp) + (100+max(dd,-100)),0)          # 埋伏分: 越平静+越贴高点越高
        rows.append({"s":s,"rv":round(rvn*100,1),"rvp":rvp,"dd":dd,"amb":amb})
    except Exception as e:
        fail.append(s)

df = pd.DataFrame(rows).sort_values("amb", ascending=False).reset_index(drop=True)
print(f"扫描完成: {len(df)} 标的 (失败{len(fail)}: {','.join(fail) if fail else '无'})\n")
print(f"{'#':>3} {'标的':<6}{'实现波动%':>9}{'波动分位':>8}{'离高点%':>8}{'埋伏分':>7}")
for i,r in df.iterrows():
    print(f"{i+1:>3} {r['s']:<6}{r['rv']:>8.1f}%{r['rvp']:>7.0f}%{r['dd']:>7.1f}%{r['amb']:>7.0f}")
