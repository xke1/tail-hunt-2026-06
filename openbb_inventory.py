"""
openbb_inventory.py — OpenBB 全数据地图(我"认真看一遍每个 widget"的底图)

把 OpenBB 所有命令(=Workspace 的 widget)列出来:命令路径 / 能用哪些数据源 / 有没有免费源能拉。
这是扫描器的底图: 知道"我能免费暴力拉什么、哪些要付费"。
运行: source .venv/bin/activate && python openbb_inventory.py
"""
import warnings; warnings.filterwarnings("ignore")
import pandas as pd
from openbb import obb

# 我们装了的免费源(无 key 或免费 key)
FREE = {"yfinance", "fred", "federal_reserve", "sec", "econdb", "imf",
        "oecd", "bls", "cftc", "eia", "government_us", "tradingeconomics", "tmx", "cboe"}
PAID = {"fmp", "intrinio", "tiingo", "benzinga", "polygon", "nasdaq"}

cmds = obb.coverage.commands   # {'.economy.fred_series': [providers...], ...}
rows = []
for path, provs in cmds.items():
    path = path.strip(".")
    cat = path.split(".")[0]
    provs = provs or []
    free_provs = [p for p in provs if p in FREE]
    rows.append({
        "category": cat,
        "command": path,
        "providers": ",".join(provs),
        "free_providers": ",".join(free_provs),
        "free_available": "YES" if free_provs else "no(需付费)",
    })

df = pd.DataFrame(rows).sort_values(["category", "command"]).reset_index(drop=True)
df.to_csv("/Users/ke/Downloads/openbb/openbb_inventory.csv", index=False)

print(f"OpenBB 命令(widget)总数: {len(df)}")
print(f"有免费源能拉的: {(df['free_available']=='YES').sum()}  |  只能付费的: {(df['free_available']!='YES').sum()}\n")
print("按类别统计(总数 / 其中免费可拉):")
g = df.groupby("category").agg(总数=("command","size"),
                               免费可拉=("free_available", lambda s:(s=="YES").sum()))
print(g.to_string())
print("\n尾部猎手最相关类别的免费可拉命令样例:")
for cat in ["economy", "fixedincome", "derivatives", "equity", "etf"]:
    sub = df[(df.category==cat) & (df.free_available=="YES")]["command"].tolist()
    print(f"\n[{cat}] 免费可拉 {len(sub)} 个, 样例:")
    for c in sub[:8]:
        print("   ", c)
print("\n完整地图存: ~/Downloads/openbb/openbb_inventory.csv")
