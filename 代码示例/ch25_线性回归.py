# -*- coding: utf-8 -*-
"""
第 25 章：监督学习——线性回归实战
对应教材：第四部分-机器学习实战/25-线性回归实战.md

演示：生成房价数据 → 训练 LinearRegression → 解读系数 →
      MAE/RMSE/R² 评估 → 预测 vs 真实散点图（保存到 output/）→ 预测新房子。
注：matplotlib 用 Agg 后端，不调用 plt.show()。
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

OUT = Path(__file__).parent / "output"
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams["font.sans-serif"] = ["Noto Serif CJK SC"]
plt.rcParams["axes.unicode_minus"] = False


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 准备数据（合成房价数据）")

rng = np.random.default_rng(0)
n = 400

area = rng.uniform(50, 200, n)          # 面积 50~200 平米
rooms = rng.integers(1, 6, n)           # 1~5 个房间
age = rng.uniform(0, 30, n)             # 房龄 0~30 年

# 真实规律：价格 ≈ 0.8*面积 + 20*房间 - 1.5*房龄 + 50 + 噪声（单位：万元）
price = 0.8 * area + 20 * rooms - 1.5 * age + 50 + rng.normal(0, 10, n)

df = pd.DataFrame({"面积": area, "房间数": rooms, "房龄": age, "价格": price})
print(df.head())
print(df.describe().round(1))

section("2. 准备特征与标签，划分数据")

X = df[["面积", "房间数", "房龄"]]      # 特征
y = df["价格"]                          # 标签

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print("训练集：", X_train.shape, "测试集：", X_test.shape)

section("3. 训练线性回归模型")

model = LinearRegression()
model.fit(X_train, y_train)

coefs = {name: round(float(c), 2) for name, c in zip(X.columns, model.coef_)}
print("各特征系数：", coefs)
print("截距：", round(float(model.intercept_), 2))
# 与我们设定的真实规律（0.8 / 20 / -1.5 / 50）几乎一致：模型学到了规律！
# 系数解读：面积每增 1 平米价格涨约 0.8 万；房龄系数为负，符合常识

section("4. 预测与评估")

y_pred = model.predict(X_test)

for real, pred in list(zip(y_test[:5], y_pred[:5])):
    print(f"真实 {real:.1f} | 预测 {pred:.1f}")

mae = mean_absolute_error(y_test, y_pred)
rmse = root_mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MAE  平均绝对误差：{mae:.2f} 万元")
print(f"RMSE 均方根误差：{rmse:.2f} 万元")
print(f"R²   决定系数：{r2:.3f}")

section("5. 可视化：预测 vs 真实")

plt.figure(figsize=(6, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
lims = [y_test.min(), y_test.max()]
plt.plot(lims, lims, "r--", label="理想预测 (y=x)")  # 点越贴近对角线越准
plt.xlabel("真实价格")
plt.ylabel("预测价格")
plt.title("预测值 vs 真实值")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "ch25_pred_vs_true.png", dpi=150, bbox_inches="tight")
plt.close()
print("已保存：ch25_pred_vs_true.png")

section("6. 用模型预测新房子")

new_house = pd.DataFrame({"面积": [120], "房间数": [3], "房龄": [5]})
print(f"预测价格：{model.predict(new_house)[0]:.1f} 万元")

# md 练习题第 2 题：只用“面积”一个特征
X1 = df[["面积"]]
Xtr, Xte, ytr, yte = train_test_split(X1, y, test_size=0.2, random_state=42)
m = LinearRegression().fit(Xtr, ytr)
print("只用面积 R²：", round(r2_score(yte, m.predict(Xte)), 3),
      "（低于全特征，说明丢掉了房间数/房龄的信息）")

# md 练习题第 3 题：糖尿病数据集（回归任务）
from sklearn.datasets import load_diabetes
data = load_diabetes()
Xtr, Xte, ytr, yte = train_test_split(data.data, data.target, test_size=0.2, random_state=42)
m2 = LinearRegression().fit(Xtr, ytr)
pred = m2.predict(Xte)
print("糖尿病数据 R²：", round(r2_score(yte, pred), 3))
print("糖尿病数据 RMSE：", round(root_mean_squared_error(yte, pred), 2))

print("\n第 25 章演示完毕 ✅")
