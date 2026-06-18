"""
hist_analog.py — 信用利差历史类比分析

问题: 现在 HY OAS 这么低(自满), 历史上出现过吗? 之后发生了什么?
方法: 拿 FRED 全历史(1996至今), 找出"和现在一样低"的时期, 算它们之后 3/6/12 个月利差怎么变。
诚实: 这是【历史基准率(base rate)】, 不是预测。过去不保证未来。
"""
import warnings; warnings.filterwarnings("ignore")
import json, urllib.request
import numpy as np, pandas as pd

# 直接调 FRED 官方 API 拉全历史(OpenBB 的 fred provider 卡在~3年, 绕开它)
# FRED key 从环境变量读, 不硬编(开源安全): export FRED_API_KEY=你的key
import os
FRED_KEY = os.environ.get("FRED_API_KEY", "")
if not FRED_KEY:
    raise SystemExit("请先 export FRED_API_KEY=你的免费FREDkey (https://fredaccount.stlouisfed.org/apikeys)")
url = (f"https://api.stlouisfed.org/fred/series/observations?series_id=BAMLH0A0HYM2"
       f"&api_key={FRED_KEY}&file_type=json&observation_start=1996-12-31")
data = json.load(urllib.request.urlopen(url))["observations"]
df = pd.DataFrame(data)
df = df[df["value"] != "."]                       # FRED 用 "." 表示缺值
oas = pd.Series(df["value"].astype(float).values,
                index=pd.to_datetime(df["date"]))
cur = float(oas.iloc[-1]); cur_date = oas.index[-1].date()
pct = round(float((oas < cur).mean()*100), 1)

print("="*70)
print(f"高收益债 OAS(信用利差)历史类比 | 全历史 {oas.index[0].date()} ~ {cur_date}")
print("="*70)
print(f"当前值: {cur:.2f}%  = 历史第 {pct} 百分位  (历史均值 {oas.mean():.2f}%, 历史最低 {oas.min():.2f}%)")

# 定义"和现在一样低"= OAS <= 当前+0.3
thr = cur + 0.3
low = oas[oas <= thr]
print(f"\n'和现在一样低'定义: OAS <= {thr:.2f}%  → 历史上有 {len(low)} 天命中 ({len(low)/len(oas)*100:.1f}% 的时间)")

# 历史低利差时期(按年分组看)
print("\n历史上落到这么低的时期(按年):")
yrs = low.groupby(low.index.year).size()
for y, n in yrs.items():
    print(f"  {y}: {n} 天")

# 远期变化: 命中低位后 3/6/12 月利差怎么走
def fwd_change(series, mask_val, days):
    vals = series.values
    out = []
    for i in range(len(vals)-days):
        if vals[i] <= mask_val:
            out.append(vals[i+days] - vals[i])
    return np.array(out)

print(f"\n落到低位(<= {thr:.2f}%)之后, 利差的变化(单位: 百分点; 正=走阔=信用恶化):")
print(f"{'之后':<8}{'样本':>7}{'中位变化':>10}{'均值变化':>10}{'走阔概率':>10}{'最大走阔':>10}")
for label, d in [("3个月", 63), ("6个月", 126), ("12个月", 252)]:
    ch = fwd_change(oas, thr, d)
    if len(ch) == 0:
        continue
    widen_prob = (ch > 0).mean()*100
    print(f"{label:<8}{len(ch):>7}{np.median(ch):>+9.2f}{ch.mean():>+10.2f}{widen_prob:>9.0f}%{ch.max():>+10.2f}")

print("""
读法:
  - "走阔概率"高 = 从这么低的位置, 历史上多数时候利差是【变宽】(信用变差)的, 不是继续变窄。
  - "最大走阔" = 历史上从低位算起最猛的一次扩张幅度(就是崩盘那几次)。
  - 这是不对称: 从地板出发, 向下空间小, 向上(走阔)空间大 —— 这就是买便宜凸性的数学依据。
  - ⚠️ 但: 低利差可以持续很久才走阔(自满能维持1-2年), 所以这是"赔率", 不是"择时信号"。
""")
