"""
rank.py — tail-hunt 核心排行榜引擎(OpenBB-only, 快, 无IBKR)
扫110+标的: 全部算价格类指标(RV/分位/回撤/埋伏分, 快); top30 加期权(ATM-IV/OTM-IV/skew/IV-RV).
输出: 排行榜(全部) + top15 screen-block(数据+为什么在榜). 全在对话, 不写垃圾CSV。
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from openbb import obb
from datetime import date
TODAY=date.today()

U=["SPY","QQQ","IWM","DIA","VTI","XLF","XLE","XLK","XLU","XLP","XLV","XLI","XLRE","XLB","XLC","XLY",
 "HYG","LQD","JNK","TLT","IEF","SHY","AGG","EMB","BKLN","VXX","UVXY","GLD","SLV","USO","UNG","DBC","CPER","WEAT","CORN",
 "EEM","FXI","EWZ","EWJ","EWG","INDA","EWW","EWY","SMH","SOXX","KRE","KBE","XBI","IBB","ARKK","TAN","ICLN","ITB","XHB","JETS","XOP","OIH",
 "NVDA","ORCL","MSFT","META","GOOGL","AMD","AVGO","AAPL","AMZN","TSLA","SMCI","PLTR","MU","DELL","ANET","VRT","CEG","VST","TLN","NRG",
 "JPM","BAC","C","GS","MS","WFC","SCHW","COF","HD","LOW","NKE","SBUX","MCD","DIS","UNH","LLY","PFE","JNJ","XOM","CVX","OXY",
 "COIN","MSTR","HOOD","AFRM","UPST","CVNA","O","SPG","ASML","AMAT","LRCX","KLAC"]

def rvol(c,w=20): return (np.log(c/c.shift(1)).rolling(w).std()*np.sqrt(252))
def mid(r):
    b=float(r.get("bid") or 0); a=float(r.get("ask") or 0)
    return (b+a)/2 if a>0 else float(r.get("last_price") or 0)

print(f"rank.py 扫描中… {len(U)} 标的 (价格类全扫, top30加期权)")
rows,fail=[],[]
for s in U:
    try:
        c=obb.equity.price.historical(symbol=s,provider="yfinance",start_date="2024-06-01").to_df()["close"]
        c.index=pd.to_datetime(c.index); rv=rvol(c).dropna(); rvn=float(rv.iloc[-1])
        rvp=round(float((rv<rvn).mean()*100),1); px=float(c.iloc[-1]); hi=float(c.tail(252).max())
        dd=round((px/hi-1)*100,1); amb=round((100-rvp)+(100+max(dd,-100)),0)
        rows.append({"s":s,"px":round(px,2),"rv":round(rvn*100,1),"rvp":rvp,"dd":dd,"amb":amb,
                     "atmiv":None,"otmiv":None,"skew":None,"ivrv":None,"cost":None})
    except Exception: fail.append(s)
df=pd.DataFrame(rows).sort_values("amb",ascending=False).reset_index(drop=True)

# top30 加期权
top=df.head(30)["s"].tolist()
for i,r in df.iterrows():
    if r["s"] not in top: continue
    try:
        ch=obb.derivatives.options.chains(symbol=r["s"],provider="yfinance").to_df()
        p=ch[ch["option_type"]=="put"]; exps=sorted(p["expiration"].unique())
        e=next((x for x in exps if (pd.Timestamp(x).date()-TODAY).days>=80),exps[-1] if exps else None)
        if e is None: continue
        leg=p[p["expiration"]==e].copy(); leg["d"]=(leg["strike"]-r["px"]).abs()
        atm=leg.sort_values("d").iloc[0]; leg["d2"]=(leg["strike"]-r["px"]*0.93).abs(); otm=leg.sort_values("d2").iloc[0]
        aiv=atm.get("implied_volatility"); oiv=otm.get("implied_volatility")
        df.at[i,"atmiv"]=round(float(aiv)*100,1) if aiv else None
        df.at[i,"otmiv"]=round(float(oiv)*100,1) if oiv else None
        df.at[i,"skew"]=round((float(oiv)-float(aiv))*100,1) if aiv and oiv else None
        df.at[i,"ivrv"]=round(float(aiv)/(r["rv"]/100),2) if aiv and r["rv"] else None
        df.at[i,"cost"]=round(mid(otm)/r["px"]*100,2)
    except Exception: pass

print(f"\n{'='*86}\ntail-hunt 排行榜 | {TODAY} | 扫{len(df)}标的(失败{len(fail)}) | 埋伏分=越平静+越贴高点越高")
print(f"{'='*86}")
print(f"{'#':>3} {'标的':<6}{'现价':>8}{'RV%':>6}{'RV位':>6}{'离高%':>7}{'ATM-IV':>7}{'OTM-IV':>7}{'skew':>6}{'IV/RV':>6}{'埋伏分':>6}")
for i,r in df.iterrows():
    f=lambda v,suf="": (f"{v}{suf}" if v is not None else "—")
    print(f"{i+1:>3} {r['s']:<6}{r['px']:>8.2f}{r['rv']:>6.1f}{r['rvp']:>5.0f}%{r['dd']:>7.1f}{f(r['atmiv']):>7}{f(r['otmiv']):>7}{f(r['skew']):>6}{f(r['ivrv']):>6}{r['amb']:>6.0f}")

print(f"\n{'='*86}\nTop15 screen-block(为什么在榜 + IV/RV便宜判据)\n{'='*86}")
for i,r in df.head(15).iterrows():
    iv_judge = ("IV/RV="+str(r['ivrv'])+(" 便宜(IV<RV)" if r['ivrv'] and r['ivrv']<1 else " 不便宜(付skew溢价)" if r['ivrv'] else "")) if r['ivrv'] else "期权数据缺"
    print(f"[{i+1}] {r['s']} (现价{r['px']}) — 平静度RV第{r['rvp']:.0f}百分位, 离52周高{r['dd']:.1f}%")
    print(f"     为什么在榜: 埋伏分{r['amb']:.0f}(越平静+越贴高点=市场越不设防); {iv_judge}; skew={r['skew']}")
print(f"\n注: 这是【③便宜+部分①平静】的快筛排名; ②未消化(非共识)+真①Taleb脆弱 要联网层补; 不是买单。")
