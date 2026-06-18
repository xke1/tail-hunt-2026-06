"""
test_openbb.py — OpenBB 部署验证(尾部猎手数据层)

跑通三个探针 = 部署成功:
  1. 免费股票报价 (yfinance, 无 key)
  2. FRED 高收益债 OAS 信用利差 (BAMLH0A0HYM2) —— 你的"信用通道"旗舰论点核心序列
  3. 免费期权链 (yfinance) —— 漏斗2粗筛,IV/greeks 残缺(见 README)

诚实约定:只打印真实拉到的数字;拉不到就报错说"缺",不编。
运行:  source .venv/bin/activate && python test_openbb.py
"""
from openbb import obb

LINE = "=" * 64


def probe_1_equity_quote():
    print(LINE)
    print("探针 1 / 股票报价 (yfinance, 免费无 key)")
    print(LINE)
    sym = "HYG"  # 高收益债 ETF, 你的信用通道标的之一
    df = obb.equity.price.quote(symbol=sym, provider="yfinance").to_df()
    cols = [c for c in ("last_price", "prev_close", "open", "high", "low", "volume") if c in df.columns]
    print(f"  {sym} 最新报价快照:")
    print(df[cols].T.to_string() if cols else df.T.to_string())
    return True


def probe_2_fred_credit_spread():
    print(LINE)
    print("探针 2 / FRED 高收益债 OAS 利差 BAMLH0A0HYM2 (需免费 key)")
    print(LINE)
    series_id = "BAMLH0A0HYM2"  # ICE BofA US High Yield Index Option-Adjusted Spread
    df = obb.economy.fred_series(symbol=series_id, provider="fred").to_df()
    tail = df.tail(5)
    print("  最近 5 个观测值 (单位: 百分点):")
    print(tail.to_string())
    clean = df.dropna()
    print(f"\n  >> 最新 OAS = {float(clean.iloc[-1].iloc[0])} (日期 {clean.index[-1]})")
    print("     [解读: 数字越高=市场要求的信用风险补偿越高=信用通道越脆]")
    return True


def probe_3_options_chain():
    print(LINE)
    print("探针 3 / 免费期权链 (yfinance) —— 漏斗2粗筛")
    print(LINE)
    sym = "SPY"
    chains = obb.derivatives.options.chains(symbol=sym, provider="yfinance").to_df()
    print(f"  {sym} 期权链: 共 {len(chains)} 行 (call+put, 多到期日)")
    exps = sorted(chains["expiration"].unique())
    print(f"  可用到期日 {len(exps)} 个, 最近: {exps[0]}  最远: {exps[-1]}")
    cols = [c for c in ("expiration", "strike", "option_type", "bid", "ask",
                        "volume", "open_interest", "implied_volatility") if c in chains.columns]
    near = chains[chains["expiration"] == exps[0]]
    puts = near[near["option_type"] == "put"].head(5)
    print(f"\n  最近到期 {exps[0]} 的前 5 个 put(尾部保护腿的原料):")
    print(puts[cols].to_string(index=False))
    print("\n  [诚实警告: yfinance 的 implied_volatility 是它自己估的, 不可靠;")
    print("   无完整 greeks / 无历史曲面 / 延迟报价。够粗筛, 不够精确定价。]")
    return True


def main():
    print("\nOpenBB 版本:", obb.system.version, "\n")
    results = {}
    for name, fn in (("equity_quote", probe_1_equity_quote),
                     ("fred_credit_spread", probe_2_fred_credit_spread),
                     ("options_chain", probe_3_options_chain)):
        try:
            results[name] = fn()
        except Exception as e:  # noqa: BLE001
            results[name] = False
            print(f"  !! 探针失败 [{name}]: {type(e).__name__}: {e}")
        print()

    print(LINE)
    print("结果汇总 (PROVEN = 真跑出数字):")
    for k, v in results.items():
        print(f"  {'PROVEN ✓' if v else 'FAILED ✗'}  {k}")
    print(LINE)
    if all(results.values()):
        print("部署验证通过 ✓ —— 三个免费探针全部拉到真实数据。")
    else:
        print("部分探针失败 —— 见上方报错, 缺什么数据已如实标出。")


if __name__ == "__main__":
    main()
