"""测 read-only 删除后, IBKR 免费延迟数据能否给股价 + 期权模型greeks(IV/delta...)"""
from ib_async import IB, Stock, Option
ib = IB()
ok=False
for p in (4001,4002,7496,7497):
    try: ib.connect("127.0.0.1",p,clientId=21,timeout=4); ok=True; print(f"连上 {p}"); break
    except: pass
if not ok: print("Gateway 没开/连不上"); raise SystemExit
ib.reqMarketDataType(3)  # 3=延迟(免费)
s=Stock("HYG","SMART","USD"); ib.qualifyContracts(s)
[t]=ib.reqTickers(s)
print(f"HYG 延迟报价: last={t.marketPrice()} close={t.close} bid={t.bid} ask={t.ask}")
o=Option("HYG","20260918",74,"P","SMART"); ib.qualifyContracts(o)
tk=ib.reqMktData(o,"",False,False); ib.sleep(5)
g=tk.modelGreeks
print(f"HYG 74P Sep18: bid={tk.bid} ask={tk.ask} last={tk.last}")
print(f"  模型greeks: {('IV='+str(round(g.impliedVol,4))+' delta='+str(round(g.delta,3))+' gamma='+str(round(g.gamma,4))) if g and g.impliedVol else '无(延迟数据可能不带greeks 或 需订阅)'}")
ib.disconnect()
