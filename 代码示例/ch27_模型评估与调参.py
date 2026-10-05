# -*- coding: utf-8 -*-
"""
第 27 章：模型评估、交叉验证与调参
对应教材：第四部分-机器学习实战/27-模型评估与调参.md

演示：过拟合 vs 欠拟合判断、cross_val_score 交叉验证、
      Pipeline 防数据泄露、GridSearchCV 网格搜索、
      RandomizedSearchCV 随机搜索、规范建模流程。
数据集为 sklearn 内置红酒数据（本地加载，无需联网）。
"""

from sklearn.datasets import load_wine
from sklearn.model_selection import (train_test_split, cross_val_score,
                                     GridSearchCV, RandomizedSearchCV)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


data = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42, stratify=data.target)

section("1. 过拟合 vs 欠拟合：同时看训练/测试得分")

# 不限深度的决策树容易过拟合
t = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
print("训练集得分：", round(t.score(X_train, y_train), 3))   # 1.0
print("测试集得分：", round(t.score(X_test, y_test), 3))     # 明显更低
print("→ 训练极好、测试差：典型过拟合")

section("2. 交叉验证：更可靠的评估")

# Pipeline 把标准化和模型绑在一起：交叉验证时每折都只在该折训练部分做标准化
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier()),
])

scores = cross_val_score(pipe, X_train, y_train, cv=5)   # 5 折
print("每折得分：", scores.round(3))
print(f"平均得分：{scores.mean():.3f} (±{scores.std():.3f})")

section("3. GridSearchCV：自动搜索最佳超参数")

param_grid = {
    "knn__n_neighbors": [3, 5, 7, 9, 11],
    "knn__weights": ["uniform", "distance"],
}

grid = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy")
grid.fit(X_train, y_train)

print("最佳超参数：", grid.best_params_)
print(f"最佳交叉验证得分：{grid.best_score_:.3f}")
print(f"在测试集上的得分：{grid.score(X_test, y_test):.3f}")
# grid.best_estimator_：用最佳超参数、在全部训练集上重训好的模型，可直接 predict

section("4. RandomizedSearchCV：组合多时更高效")

rand = RandomizedSearchCV(
    pipe, {"knn__n_neighbors": list(range(1, 30))},
    n_iter=10, cv=5, random_state=42)
rand.fit(X_train, y_train)
print("随机搜索最佳：", rand.best_params_)

section("5. 规范的建模流程")

print("""
1. 划分训练集/测试集（测试集"封存"，只在最后用一次）。
2. 用 Pipeline 组合预处理和模型。
3. 用交叉验证 + GridSearchCV 在训练集上调参、选模型。
4. 用 best_estimator_ 在测试集上做最终评估。
5. 满意后，用全部数据重新训练，部署上线。
黄金原则：测试集只能在最后用一次，调参用交叉验证。
""")

# md 练习题第 2 题：逻辑回归 10 折交叉验证
pipe_lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000))
scores = cross_val_score(pipe_lr, X_train, y_train, cv=10)
print(f"逻辑回归 10 折平均得分：{scores.mean():.3f}")

# md 练习题第 3 题：网格搜索决策树的最佳 max_depth
grid = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    {"max_depth": list(range(1, 11))}, cv=5)
grid.fit(X_train, y_train)
print("决策树最佳深度：", grid.best_params_,
      "交叉验证得分：", round(grid.best_score_, 3))

print("\n第 27 章演示完毕 ✅")
