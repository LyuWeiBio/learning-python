# -*- coding: utf-8 -*-
"""
第 24 章：机器学习概述与 scikit-learn 入门
对应教材：第四部分-机器学习实战/24-机器学习概述与sklearn入门.md

演示：sklearn 统一工作流（fit/predict）、鸢尾花分类完整流程、
      KNN、换数据集（红酒）、换 K 值对比。
数据集为 sklearn 内置（本地加载，无需联网）。
"""

from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import numpy as np


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 加载鸢尾花数据集")

iris = load_iris()
X = iris.data              # 特征：150 朵花 × 4 个尺寸
y = iris.target            # 标签：每朵花的品种（0/1/2）

print("特征形状：", X.shape)          # (150, 4)
print("特征名：", iris.feature_names)
print("品种名：", list(iris.target_names))
print("前 3 个样本：\n", X[:3])
print("前 3 个标签：", y[:3])

section("2. 划分训练集和测试集")

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,        # 20% 作测试集
    random_state=42,      # 固定随机种子，保证可复现
    stratify=y,           # 按标签分层，保证各类别比例一致
)
print("训练集：", X_train.shape)   # (120, 4)
print("测试集：", X_test.shape)    # (30, 4)

section("3. 创建并训练模型（K 近邻）")

# KNN 思想：要判断新样本属于哪类，看它最近的 K 个邻居里哪类最多
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)         # 训练

section("4. 预测与评估")

y_pred = model.predict(X_test)
print("预测结果：", y_pred)
print("真实标签：", y_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"准确率：{accuracy:.2%}")
# 也可以直接用 model.score(X_test, y_test)

section("5. 预测新的花")

new_flower = np.array([[5.1, 3.5, 1.4, 0.2]])
pred = model.predict(new_flower)
print("预测品种：", iris.target_names[pred[0]])   # setosa

# md 练习题第 2 题：改变 K 值
print("\n不同 K 值的准确率：")
for k in [1, 5, 10]:
    m = KNeighborsClassifier(n_neighbors=k)
    m.fit(X_train, y_train)
    print(f"k={k}: {m.score(X_test, y_test):.2%}")

# md 练习题第 4 题：换红酒数据集
wine = load_wine()
Xtr, Xte, ytr, yte = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42, stratify=wine.target)
model_wine = KNeighborsClassifier(n_neighbors=3)
model_wine.fit(Xtr, ytr)
print(f"红酒数据集 KNN 准确率：{model_wine.score(Xte, yte):.2%}")

print("\n第 24 章演示完毕 ✅")
