"""
deep_read.py v3 — 像真人读整张表(OpenBB-only, 无IBKR, 快, 全strike)
逐strike: IV + IV/RV + skew + 成本$; RV基准; 可部署结构. 按 OUTPUT_TEMPLATE 的 deep-block 产出。
IBKR 已从管线移除(Ke 最后自己上 IBKR 肉眼复核)。
用法: python deep_read.py HYG
"""
import sys, warnings; warnings.filterwarnings("ignore")
from datetime import date
import numpy as np, pandas as pd
from openbb import obb

SYM=sys.argv[1] if len(sys.argv)>1 else "HYG"; TODAY=date.today()
h=obb.equity.price.historical(symbol=SYM,provider="yfinance",start_date="2024-06-01").to_df()
c=h["close"]; c.index=pd.to_datetime(c.index); spot=float(c.iloc[-1])
rv20=(np.log(c/c.shift(1)).rolling(20).std()*np.sqrt(252)).dropna()
rv=float(rv20.iloc[-1]); rvp=round(float((rv20<rv).mean()*100),1)
ch=obb.derivatives.options.chains(symbol=SYM,provider="yfinance").to_df()
puts=ch[ch["option_type"]=="put"]; exps=sorted(ch["expiration"].unique())
EXP=next((e for e in exps if (pd.Timestamp(e).date()-TODAY).days>=80),exps[-1])
dte=(pd.Timestamp(EXP).date()-TODAY).days
def mid(r):
    b=float(r.get("bid") or 0); a=float(r.get("ask") or 0)
    return (b+a)/2 if a>0 else float(r.get("last_price") or 0)

print(f"\n{'='*80}\n{SYM} deep-read (OpenBB) | 现价{spot:.2f} | 到期{EXP}({dte}天) | RV={rv*100:.1f}%(第{rvp:.0f}百分位)\n{'='*80}")
leg=puts[puts["expiration"]==EXP].sort_values("strike")
print(f"  PUTS 逐strike(ATM→20%价外):")
print(f"  {'strike':>7}{'价外%':>7}{'bid':>6}{'ask':>6}{'$/张':>6}{'IV%':>7}{'IV/RV':>7}{'OI':>9}")
data=[]
for _,r in leg.iterrows():
    k=r["strike"]
    if k>spot*1.02 or k<spot*0.80: continue
    iv=r.get("implied_volatility"); iv=float(iv) if iv==iv and iv else None
    m=mid(r); ivrv=(iv/rv) if iv else None
    print(f"  {k:>7.0f}{(k/spot-1)*100:>6.1f}%{float(r.get('bid') or 0):>6.2f}{float(r.get('ask') or 0):>6.2f}{m*100:>6.0f}{(iv*100 if iv else 0):>6.1f}%{(ivrv if ivrv else 0):>7.2f}{int(r.get('open_interest') or 0):>9}")
    data.append({"k":k,"iv":iv,"mid":m,"oi":int(r.get('open_interest') or 0)})

# 幻觉检查: IV应随价外加深而单调上升(skew); 突降=可疑
susp=[]
prev=None
for d in sorted(data,key=lambda x:-x["k"]):  # 从ATM往价外
    if prev and d["iv"] and prev and d["iv"]<prev*0.6: susp.append(d["k"])
    if d["iv"]: prev=d["iv"]
atm=min(data,key=lambda d:abs(d["k"]-spot)); otm=min(data,key=lambda d:abs(d["k"]-spot*0.90))
print(f"\n解读:")
print(f"  ATM(~{atm['k']:.0f}) IV={atm['iv']*100 if atm['iv'] else 0:.1f}% / RV {rv*100:.1f}% → IV/RV={atm['iv']/rv if atm['iv'] else 0:.2f}")
print(f"  10%价外({otm['k']:.0f}) put: 成本${otm['mid']*100:.0f}/张 ({otm['mid']/spot*100:.2f}%现价), IV={otm['iv']*100 if otm['iv'] else 0:.1f}%, OI={otm['oi']}")
print(f"  skew: ATM {atm['iv']*100 if atm['iv'] else 0:.1f}% → 10%OTM {otm['iv']*100 if otm['iv'] else 0:.1f}% ({'陡=尾部偏贵' if otm['iv'] and atm['iv'] and otm['iv']>atm['iv'] else '平'})")
print(f"  幻觉检查(IV是否随价外单调): {'✓正常单调' if not susp else '⚠️IV突降可疑 strike='+str(susp)+'(yfinance脏价)'}")
print(f"  可部署(禁裸卖): 单腿买{otm['k']:.0f}put ${otm['mid']*100:.0f}(最大亏=权利金); 或价差 买{otm['k']:.0f}/卖更深档 降成本封顶")
print(f"  数据源: OpenBB(yfinance, ~15分延迟); IBKR交叉核对=由你最后肉眼上IBKR复核")
