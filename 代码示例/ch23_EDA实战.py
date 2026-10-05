# -*- coding: utf-8 -*-
"""
第 23 章：探索性数据分析（EDA）实战
对应教材：第三部分-数据分析基础/23-探索性数据分析实战.md

演示 EDA 六步：加载数据 → 查质量 → 单变量分析 → 多变量分析 →
                分组洞察 → 总结结论。
数据用代码生成（固定随机种子，可复现）。
注：matplotlib 用 Agg 后端，图表 savefig 到 output/，不调用 plt.show()。
"""

import matplotlib
matplotlib.use("Agg")        # 非交互后端
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path(__file__).parent / "output"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["Noto Serif CJK SC"]
plt.rcParams["axes.unicode_minus"] = False


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("第 1 步：加载数据，整体认识")

# 23.2 准备数据：生成模拟电商销售数据
np.random.seed(42)
n = 500

df = pd.DataFrame({
    "订单ID": range(1, n + 1),
    "类别": np.random.choice(["电子产品", "服装", "食品", "家居", "图书"], n),
    "地区": np.random.choice(["华北", "华东", "华南", "西部"], n, p=[0.3, 0.3, 0.25, 0.15]),
    "销售额": np.round(np.random.gamma(2, 300, n), 2),
    "数量": np.random.randint(1, 11, n),
    "客户年龄": np.random.randint(18, 65, n).astype(float),
})
df["利润"] = np.round(df["销售额"] * np.random.uniform(0.05, 0.3, n), 2)

# 人为制造一些缺失值，模拟真实的"脏数据"
missing_idx = np.random.choice(n, 25, replace=False)
df.loc[missing_idx, "客户年龄"] = np.nan

print(df.shape)          # (500, 7)
print(df.head())
print(df.info())
print(df.describe().round(1))

section("第 2 步：检查数据质量")

print("各列缺失值：")
print(df.isnull().sum())       # 客户年龄有缺失
print("重复行数：", df.duplicated().sum())

# 用中位数填充年龄（比均值更抗异常值）
df["客户年龄"] = df["客户年龄"].fillna(df["客户年龄"].median())
print("填充后缺失：", df["客户年龄"].isnull().sum())

section("第 3 步：单变量分析")

# 数值变量的分布：直方图
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(df["销售额"], bins=30, edgecolor="black")
axes[0].set_title("销售额分布")
axes[1].hist(df["客户年龄"], bins=20, edgecolor="black", color="orange")
axes[1].set_title("客户年龄分布")
plt.tight_layout()
plt.savefig(OUT / "ch23_univariate.png", dpi=150, bbox_inches="tight")
plt.close()
print("已保存：ch23_univariate.png")
# 观察：销售额分布明显右偏（多数订单金额较小，少数大额拉长右尾）

# 类别变量的分布
print(df["类别"].value_counts())
print(df["地区"].value_counts(normalize=True))   # 各地区占比

ax = df["类别"].value_counts().plot(kind="bar", title="各类别订单数")
ax.figure.tight_layout()
ax.figure.savefig(OUT / "ch23_category.png", dpi=150, bbox_inches="tight")
plt.close("all")

section("第 4 步：多变量分析")

# 相关系数矩阵（只对数值列）
num_cols = ["销售额", "数量", "客户年龄", "利润"]
corr = df[num_cols].corr()
print(corr.round(2))
# 销售额与利润呈较强正相关（利润按销售额比例算的）；
# 数量、客户年龄与销售额几乎不相关

plt.figure()
plt.scatter(df["销售额"], df["利润"], alpha=0.5)
plt.xlabel("销售额")
plt.ylabel("利润")
plt.title("销售额 vs 利润")
plt.savefig(OUT / "ch23_corr.png", dpi=150, bbox_inches="tight")
plt.close()
print("已保存：ch23_corr.png")

section("第 5 步：分组洞察")

# 每个类别的总销售额和平均利润
category_stats = df.groupby("类别").agg(
    总销售额=("销售额", "sum"),
    平均利润=("利润", "mean"),
    订单数=("订单ID", "count"),
).sort_values("总销售额", ascending=False)
print(category_stats.round(1))

# 每个地区的总利润
region_profit = df.groupby("地区")["利润"].sum().sort_values(ascending=False)
print(region_profit.round(1))

ax = category_stats["总销售额"].plot(kind="bar", title="各类别总销售额")
ax.figure.tight_layout()
ax.figure.savefig(OUT / "ch23_groupby.png", dpi=150, bbox_inches="tight")
plt.close("all")
print("已保存：ch23_groupby.png")

# 交叉分析：每个地区 × 每个类别的平均销售额（透视表）
pivot = df.pivot_table(values="销售额", index="地区", columns="类别", aggfunc="mean")
print(pivot.round(1))

# 分箱分析：按年龄段看消费
df["年龄段"] = pd.cut(df["客户年龄"],
                      bins=[0, 25, 35, 45, 100],
                      labels=["青年", "青壮年", "中年", "中老年"])
print(df.groupby("年龄段", observed=True)["销售额"].mean().round(1))

section("第 6 步：总结结论")

print("""
- 数据共 500 条订单，客户年龄有 25 条缺失，已用中位数填充。
- 销售额分布明显右偏：多数订单集中在中低金额，存在少量大额订单。
- 销售额与利润呈较强正相关（相关系数约 0.8+），数量/年龄与销售额几乎不相关。
- 各类别的订单数比较接近（等概率随机分配），真实业务数据往往有头部品类。
""")

print("\n第 23 章演示完毕 ✅")
