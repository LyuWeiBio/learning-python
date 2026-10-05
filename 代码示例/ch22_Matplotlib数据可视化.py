# -*- coding: utf-8 -*-
"""
第 22 章：Matplotlib 数据可视化
对应教材：第三部分-数据分析基础/22-Matplotlib数据可视化.md

演示：折线图、柱状图、散点图、直方图、饼图、多子图、
      保存图表、Pandas 直接画图。
注：必须用 Agg 后端（无图形界面也能运行），图表全部
    savefig 到脚本同目录 output/，不调用 plt.show()。
"""

import matplotlib
matplotlib.use("Agg")        # 非交互后端：只保存图片，不弹窗
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path(__file__).parent / "output"
OUT.mkdir(parents=True, exist_ok=True)

# 系统有 Noto Serif CJK SC 中文字体，中文可正常显示
plt.rcParams["font.sans-serif"] = ["Noto Serif CJK SC"]
plt.rcParams["axes.unicode_minus"] = False   # 正常显示负号


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 折线图：观察趋势")

months = [1, 2, 3, 4, 5, 6]
sales = [120, 135, 128, 160, 175, 190]

plt.figure()
plt.plot(months, sales, color="blue", marker="o", linestyle="-", label="2023")
plt.plot(months, [100, 120, 130, 140, 150, 165], color="red", marker="s", label="2022")
plt.legend()        # 显示图例（需要每条线有 label）
plt.grid(True)      # 显示网格
plt.title("上半年销售趋势")
plt.xlabel("月份")
plt.ylabel("销售额（万元）")
plt.savefig(OUT / "ch22_line.png", dpi=150, bbox_inches="tight")
plt.close()         # 关闭图，释放内存
print("已保存：ch22_line.png")

section("2. 柱状图：比较大小")

categories = ["苹果", "香蕉", "橙子", "葡萄"]
counts = [45, 30, 25, 18]

plt.figure()
plt.bar(categories, counts, color="skyblue")
plt.title("各水果销量")
plt.ylabel("销量")
plt.savefig(OUT / "ch22_bar.png", dpi=150, bbox_inches="tight")
plt.close()
print("已保存：ch22_bar.png")

# md 练习题第 2 题：各班平均分柱状图
data = {"一班": 85, "二班": 78, "三班": 92, "四班": 80}
plt.figure()
plt.bar(data.keys(), data.values(), color="skyblue")
plt.title("各班平均分")
plt.savefig(OUT / "ch22_bar_class.png", dpi=150, bbox_inches="tight")
plt.close()

section("3. 散点图：观察两个变量的关系")

np.random.seed(0)
height = np.random.normal(170, 8, 50)
weight = height * 0.5 - 20 + np.random.normal(0, 3, 50)

plt.figure()
plt.scatter(height, weight, alpha=0.6)     # alpha 是透明度
plt.title("身高与体重关系")
plt.xlabel("身高 (cm)")
plt.ylabel("体重 (kg)")
plt.savefig(OUT / "ch22_scatter.png", dpi=150, bbox_inches="tight")
plt.close()
print("已保存：ch22_scatter.png")

section("4. 直方图：观察数据分布")

np.random.seed(0)
scores = np.random.normal(75, 10, 200)

plt.figure()
plt.hist(scores, bins=20, color="orange", edgecolor="black")
plt.title("成绩分布直方图")
plt.xlabel("分数")
plt.ylabel("人数")
plt.savefig(OUT / "ch22_hist.png", dpi=150, bbox_inches="tight")
plt.close()
print("已保存：ch22_hist.png")

section("5. 饼图：观察占比")

labels = ["技术", "销售", "运营", "行政"]
sizes = [40, 30, 20, 10]

plt.figure()
plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
plt.title("部门人数占比")
plt.axis("equal")     # 让饼图是正圆
plt.savefig(OUT / "ch22_pie.png", dpi=150, bbox_inches="tight")
plt.close()
print("已保存：ch22_pie.png")

section("6. 多子图：一张画布多个图")

fig, axes = plt.subplots(1, 2, figsize=(10, 4))   # 1行2列

axes[0].plot([1, 2, 3], [4, 5, 6])
axes[0].set_title("折线图")

axes[1].bar(["A", "B", "C"], [3, 7, 5])
axes[1].set_title("柱状图")

plt.tight_layout()    # 自动调整间距，避免重叠
plt.savefig(OUT / "ch22_subplots.png", dpi=150, bbox_inches="tight")
plt.close()
print("已保存：ch22_subplots.png")

section("7. 用 Pandas 直接画图")

df = pd.DataFrame({
    "月份": [1, 2, 3, 4, 5],
    "销量": [100, 120, 90, 140, 160],
    "成本": [60, 70, 55, 80, 90],
})

ax = df.plot(x="月份", y=["销量", "成本"], marker="o")   # 折线图
ax.set_title("销量与成本")
ax.figure.savefig(OUT / "ch22_pandas_line.png", dpi=150, bbox_inches="tight")
plt.close("all")

ax = df.plot(x="月份", y="销量", kind="bar")             # 柱状图
ax.set_title("销量柱状图")
ax.figure.savefig(OUT / "ch22_pandas_bar.png", dpi=150, bbox_inches="tight")
plt.close("all")
print("已保存：ch22_pandas_line.png / ch22_pandas_bar.png")

print("\n第 22 章演示完毕 ✅")
