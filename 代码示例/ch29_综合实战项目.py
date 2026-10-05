# -*- coding: utf-8 -*-
"""
第 29 章：综合实战项目——从数据到模型
对应教材：第四部分-机器学习实战/29-综合实战项目.md

演示机器学习项目 8 步走：加载与探索 → 划分 → 预处理管道
(ColumnTransformer) → 交叉验证选型 → 网格搜索调参 → 测试集评估 →
特征重要性 → 保存/加载模型（joblib）。
注：本脚本为自包含的精简版（小数据、缩减的调参网格），保证快速运行；
    完整版见代码示例/ml/churn_project.py（本章配套脚本，不动）。
"""

import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report, roc_auc_score)

OUT = Path(__file__).parent / "output"
OUT.mkdir(parents=True, exist_ok=True)


def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def build_dataset(n: int = 600) -> pd.DataFrame:
    """生成一份带分类特征和缺失值的客户流失数据（精简版）。"""
    rng = np.random.default_rng(2024)

    age = rng.integers(18, 70, n)
    tenure = rng.integers(1, 72, n)                       # 在网月数
    monthly_charge = np.round(rng.uniform(30, 200, n), 1)  # 月消费
    complaints = rng.poisson(1.0, n)                       # 投诉次数
    plan = rng.choice(["基础", "标准", "尊享"], n, p=[0.5, 0.3, 0.2])
    contract = rng.choice(["月付", "年付"], n, p=[0.6, 0.4])

    # 构造流失倾向：投诉多、在网短、月付、消费高 → 更易流失
    plan_risk = pd.Series(plan).map({"基础": 0.4, "标准": 0.0, "尊享": -0.3}).to_numpy()
    contract_risk = np.where(contract == "月付", 0.8, -0.8)
    logit = (-1.0 + 0.5 * complaints - 0.03 * tenure
             + 0.006 * monthly_charge + plan_risk + contract_risk
             + rng.normal(0, 0.5, n))
    prob = 1 / (1 + np.exp(-logit))
    churn = (rng.uniform(0, 1, n) < prob).astype(int)

    df = pd.DataFrame({
        "年龄": age.astype(float), "在网月数": tenure, "月消费": monthly_charge,
        "投诉次数": complaints, "套餐": plan, "合约类型": contract,
        "是否流失": churn,
    })
    df.loc[rng.choice(n, 30, replace=False), "年龄"] = np.nan   # 人为制造缺失
    df.loc[rng.choice(n, 20, replace=False), "套餐"] = None
    return df


numeric_features = ["年龄", "在网月数", "月消费", "投诉次数"]
categorical_features = ["套餐", "合约类型"]

section("步骤 1–2：加载与探索数据、划分训练/测试集")

df = build_dataset()
print("形状：", df.shape)
print(df.head())
print("流失比例：", df["是否流失"].value_counts(normalize=True).round(3).to_dict())
print("缺失值：", df.isnull().sum().to_dict())

X = df.drop(columns=["是否流失"])
y = df["是否流失"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print("训练集：", X_train.shape, "测试集：", X_test.shape)

section("步骤 3：构建预处理管道")

numeric_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),   # 中位数填充
    ("scaler", StandardScaler()),                    # 标准化
])
categorical_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),  # 众数填充
    ("onehot", OneHotEncoder(handle_unknown="ignore")),    # 独热编码
])
preprocessor = ColumnTransformer([
    ("num", numeric_pipe, numeric_features),
    ("cat", categorical_pipe, categorical_features),
])
print("数值列：中位数填充+标准化；分类列：众数填充+独热编码")

section("步骤 4：候选模型交叉验证选型")

candidates = {
    "逻辑回归": LogisticRegression(max_iter=5000),
    "随机森林": RandomForestClassifier(n_estimators=50, random_state=42),
}
for name, clf in candidates.items():
    pipe = Pipeline([("prep", preprocessor), ("clf", clf)])
    scores = cross_val_score(pipe, X_train, y_train, cv=3, scoring="roc_auc")
    print(f"{name}: 交叉验证 AUC = {scores.mean():.3f} (±{scores.std():.3f})")
# 复杂模型未必更好，用数据说话

section("步骤 5：对随机森林网格搜索调参")

rf_pipe = Pipeline([
    ("prep", preprocessor),
    ("clf", RandomForestClassifier(random_state=42)),
])
param_grid = {
    "clf__n_estimators": [50, 100],
    "clf__max_depth": [4, 6, None],
}
grid = GridSearchCV(rf_pipe, param_grid, cv=3, scoring="roc_auc", n_jobs=-1)
grid.fit(X_train, y_train)
print("最佳参数：", grid.best_params_)
print(f"最佳交叉验证 AUC：{grid.best_score_:.3f}")

section("步骤 6：在测试集上做最终评估")

best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)[:, 1]

print(f"准确率：{accuracy_score(y_test, y_pred):.3f}")
print(f"测试集 AUC：{roc_auc_score(y_test, y_proba):.3f}")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=["未流失", "流失"]))
# 测试集只在最后评估一次

section("步骤 7：解读特征重要性")

ohe = best_model.named_steps["prep"].named_transformers_["cat"].named_steps["onehot"]
all_names = numeric_features + list(ohe.get_feature_names_out(categorical_features))
importances = pd.Series(
    best_model.named_steps["clf"].feature_importances_, index=all_names
).sort_values(ascending=False)
print(importances.round(3).to_string())

section("步骤 8：保存模型并预测新客户")

import joblib

model_path = OUT / "ch29_churn_model.joblib"
joblib.dump(best_model, model_path)     # 保存整个 Pipeline（含预处理）
print("模型已保存到：", model_path)

loaded = joblib.load(model_path)        # 加载后直接可用
new_customer = pd.DataFrame([{
    "年龄": 30, "在网月数": 3, "月消费": 150.0,
    "投诉次数": 4, "套餐": "基础", "合约类型": "月付",
}])
prob = loaded.predict_proba(new_customer)[0, 1]
print(f"新客户流失概率：{prob:.1%} → 预测：{'会流失' if prob > 0.5 else '不会流失'}")

print("\n第 29 章演示完毕 🎓")
