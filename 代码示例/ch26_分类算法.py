# -*- coding: utf-8 -*-
"""
第 26 章：监督学习——分类算法实战
对应教材：第四部分-机器学习实战/26-分类算法实战.md

演示：乳腺癌二分类 → 逻辑回归（Pipeline+标准化）→ 决策树 →
      混淆矩阵 → 精确率/召回率/F1 → classification_report → 模型对比。
数据集为 sklearn 内置（本地加载，无需联网）。
"""

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_score, recall_score, f1_score,
                             classification_report)
import pandas as pd


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 任务与数据：乳腺癌诊断")

data = load_breast_cancer()
X, y = data.data, data.target

print("样本数、特征数：", X.shape)          # (569, 30)
print("类别：", list(data.target_names))    # ['malignant' 'benign']
print("标签含义：0=恶性, 1=良性")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

section("2. 算法一：逻辑回归")

# make_pipeline 把标准化+模型串起来，防止数据泄露
logreg = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=5000),
)
logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)
print(f"逻辑回归准确率：{accuracy_score(y_test, y_pred):.3f}")

# 预测概率：每行 [恶性概率, 良性概率]
proba = logreg.predict_proba(X_test[:5])
print(proba.round(3))

section("3. 算法二：决策树")

tree = DecisionTreeClassifier(max_depth=4, random_state=42)
tree.fit(X_train, y_train)
print(f"决策树准确率：{tree.score(X_test, y_test):.3f}")

# 决策树能告诉你哪些特征最重要
importances = pd.Series(tree.feature_importances_, index=data.feature_names)
print("最重要的 5 个特征：")
print(importances.sort_values(ascending=False).head(5).round(3))

section("4. 混淆矩阵：分类到底错在哪")

cm = confusion_matrix(y_test, y_pred)
print(cm)
print("""
矩阵含义（以"恶性=阳性"为例）：
  TP 真阳性：恶性且预测恶性 ✅
  TN 真阴性：良性且预测良性 ✅
  FP 假阳性：良性却预测成恶性（误诊）
  FN 假阴性：恶性却预测成良性（漏诊，最危险！）
""")

section("5. 精确率、召回率、F1")

# sklearn 默认以 label=1（这里是"良性"）为阳性
print(f"精确率：{precision_score(y_test, y_pred):.3f}")
print(f"召回率：{recall_score(y_test, y_pred):.3f}")
print(f"F1 分数：{f1_score(y_test, y_pred):.3f}")

# 我们真正担心的是"漏诊恶性"，用 pos_label=0 单独看恶性的召回率
print(f"恶性召回率：{recall_score(y_test, y_pred, pos_label=0):.3f}")

section("6. classification_report：一步到位")

print(classification_report(y_test, y_pred, target_names=data.target_names))

section("7. 模型对比")

models = {
    "逻辑回归": logreg,
    "决策树": tree,
}
for name, model in models.items():
    acc = model.score(X_test, y_test)
    print(f"{name}: 准确率 {acc:.3f}")
# 没有万能的最优算法，要针对具体数据尝试、对比、选择

# md 练习题第 2 题：树的深度对准确率的影响
print("\n决策树深度 vs 测试集准确率：")
for d in range(1, 6):
    t = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_train, y_train)
    print(f"depth={d}: {t.score(X_test, y_test):.3f}")

# md 练习题第 4 题：随机森林对比
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=50, random_state=42)  # 减少树的数量以提速
rf.fit(X_train, y_train)
print(f"随机森林准确率：{rf.score(X_test, y_test):.3f}")

print("\n第 26 章演示完毕 ✅")
