"""
ibkr_bridge.py — IBKR 桥(让 Claude 能看到 Ke 在 IBKR 看到的数据)

用 ib_async 连本地 IB Gateway / TWS, 拉实时报价 + 期权链(strike/到期/greeks)。
连不上会打印你要做的设置步骤(不报错崩溃)。

前提(你这边要做的):
  1. 下载并打开 IB Gateway(轻量) 或 TWS(完整客户端), 登录你的 IBKR 账户。
  2. 开启 API: TWS/Gateway → Configure/Settings → API → Settings →
     勾选 "Enable ActiveX and Socket Clients", 并把 127.0.0.1 加入信任 IP。
  3. 记下端口(Socket port):
       IB Gateway: 实盘 4001 / 模拟 4002
       TWS:        实盘 7496 / 模拟 7497
  4. 确认市场数据订阅(否则给的是延迟价, 但桥照样能跑通)。
运行: source .venv/bin/activate && python ibkr_bridge.py [可选:股票代码, 默认HYG]
"""
import sys
from ib_async import IB, Stock

SYM = sys.argv[1] if len(sys.argv) > 1 else "HYG"
PORTS = [(4002, "IB Gateway 模拟"), (4001, "IB Gateway 实盘"),
         (7497, "TWS 模拟"), (7496, "TWS 实盘")]

def setup_help():
    print("""
❌ 连不上 IBKR。这是正常的(你还没开 Gateway 或没开 API)。请按以下做:
  1. 打开 IB Gateway 或 TWS 并登录。
  2. 设置里开 API: 勾 "Enable ActiveX and Socket Clients"; 信任 IP 加 127.0.0.1。
  3. 确认端口在 {4001,4002,7496,7497} 之一(本脚本会自动试这几个)。
  4. 重新跑: python ibkr_bridge.py
""")

def main():
    ib = IB()
    for port, name in PORTS:
        try:
            ib.connect("127.0.0.1", port, clientId=11, timeout=4)
            print(f"✅ 已连上 {name}  (127.0.0.1:{port})")
            break
        except Exception:
            continue
    else:
        setup_help(); return

    try:
        # 纯只读: 不调 reqMarketDataType(会触发 Read-Only API 写权限弹窗)。
        # 价格/IV 由 OpenBB/yfinance 免费供; IBKR 这里只读结构+账户(只读最安全)。
        # 1) 报价(无市场数据订阅时为 nan, 正常)
        stock = Stock(SYM, "SMART", "USD")
        ib.qualifyContracts(stock)
        [tk] = ib.reqTickers(stock)
        px = tk.marketPrice() or tk.close
        print(f"\n{SYM} 报价: last/mark={px}  bid={tk.bid}  ask={tk.ask}  close={tk.close}")

        # 2) 期权链结构(到期日 + 行权价)
        params = ib.reqSecDefOptParams(stock.symbol, "", stock.secType, stock.conId)
        if params:
            p = params[0]
            exps = sorted(p.expirations)[:8]
            strikes = sorted(p.strikes)
            print(f"\n期权链: 交易所 {p.exchange}")
            print(f"  最近 8 个到期: {exps}")
            print(f"  行权价范围: {strikes[0]} ~ {strikes[-1]} (共 {len(strikes)} 档)")
        print("\n✅ IBKR 桥跑通: 报价 + 期权链结构都拉到了。下一步可加 greeks/逐 strike 拉取。")
    finally:
        ib.disconnect()

if __name__ == "__main__":
    main()
