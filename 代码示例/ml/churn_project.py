"""
第 29 章综合实战项目：电信客户流失预测（端到端机器学习流程）。

运行方式：
    python 代码示例/ml/churn_project.py

流程：生成数据 → EDA → 预处理(ColumnTransformer) → 训练多个模型
      → 交叉验证选模 → 网格搜索调参 → 测试集评估 → 保存模型。

数据用固定随机种子生成，可完整复现，无需联网下载。
"""

import os
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)


def build_dataset(n: int = 1500) -> pd.DataFrame:
    """生成一份带分类特征和缺失值的客户流失数据。"""
    rng = np.random.default_rng(2024)

    age = rng.integers(18, 70, n)
    tenure = rng.integers(1, 72, n)                       # 在网月数
    monthly_charge = np.round(rng.uniform(30, 200, n), 1)  # 月消费
    complaints = rng.poisson(1.0, n)                       # 投诉次数
    plan = rng.choice(["基础", "标准", "尊享"], n, p=[0.5, 0.3, 0.2])
    contract = rng.choice(["月付", "年付"], n, p=[0.6, 0.4])

    # 构造一个"流失倾向"：投诉多、在网短、月付、消费高 → 更易流失
    plan_risk = pd.Series(plan).map({"基础": 0.4, "标准": 0.0, "尊享": -0.3}).to_numpy()
    contract_risk = np.where(contract == "月付", 0.8, -0.8)
    logit = (
        -1.0
        + 0.5 * complaints
        - 0.03 * tenure
        + 0.006 * monthly_charge
        + plan_risk
        + contract_risk
        + rng.normal(0, 0.5, n)
    )
    prob = 1 / (1 + np.exp(-logit))
    churn = (rng.uniform(0, 1, n) < prob).astype(int)

    df = pd.DataFrame(
        {
            "年龄": age.astype(float),
            "在网月数": tenure,
            "月消费": monthly_charge,
            "投诉次数": complaints,
            "套餐": plan,
            "合约类型": contract,
            "是否流失": churn,
        }
    )

    # 人为制造缺失值
    df.loc[rng.choice(n, 60, replace=False), "年龄"] = np.nan
    df.loc[rng.choice(n, 40, replace=False), "套餐"] = None
    return df


def main() -> None:
    print("=" * 60)
    print("步骤 1：加载与初步探索数据")
    print("=" * 60)
    df = build_dataset()
    print("形状：", df.shape)
    print(df.head())
    print("\n流失比例：")
    print(df["是否流失"].value_counts(normalize=True).round(3).to_dict())
    print("\n缺失值：")
    print(df.isnull().sum().to_dict())

    print("\n" + "=" * 60)
    print("步骤 2：划分特征/标签，切分训练集与测试集")
    print("=" * 60)
    X = df.drop(columns=["是否流失"])
    y = df["是否流失"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print("训练集：", X_train.shape, " 测试集：", X_test.shape)

    numeric_features = ["年龄", "在网月数", "月消费", "投诉次数"]
    categorical_features = ["套餐", "合约类型"]

    print("\n" + "=" * 60)
    print("步骤 3：构建预处理管道（数值/分类分别处理）")
    print("=" * 60)
    numeric_pipe = Pipeline(
        [("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        [
            ("num", numeric_pipe, numeric_features),
            ("cat", categorical_pipe, categorical_features),
        ]
    )
    print("预处理器构建完成：数值列填充中位数+标准化，分类列填充众数+独热编码")

    print("\n" + "=" * 60)
    print("步骤 4：候选模型交叉验证选型")
    print("=" * 60)
    candidates = {
        "逻辑回归": LogisticRegression(max_iter=5000),
        "随机森林": RandomForestClassifier(random_state=42),
    }
    for name, clf in candidates.items():
        pipe = Pipeline([("prep", preprocessor), ("clf", clf)])
        scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="roc_auc")
        print(f"{name}: 交叉验证 AUC = {scores.mean():.3f} (±{scores.std():.3f})")

    print("\n" + "=" * 60)
    print("步骤 5：对随机森林做网格搜索调参")
    print("=" * 60)
    rf_pipe = Pipeline(
        [("prep", preprocessor), ("clf", RandomForestClassifier(random_state=42))]
    )
    param_grid = {
        "clf__n_estimators": [100, 200],
        "clf__max_depth": [4, 6, 8, None],
    }
    grid = GridSearchCV(rf_pipe, param_grid, cv=5, scoring="roc_auc", n_jobs=-1)
    grid.fit(X_train, y_train)
    print("最佳参数：", grid.best_params_)
    print(f"最佳交叉验证 AUC：{grid.best_score_:.3f}")

    print("\n" + "=" * 60)
    print("步骤 6：在测试集上做最终评估")
    print("=" * 60)
    best_model = grid.best_estimator_
    y_pred = best_model.predict(X_test)
    y_proba = best_model.predict_proba(X_test)[:, 1]

    print(f"准确率：{accuracy_score(y_test, y_pred):.3f}")
    print(f"测试集 AUC：{roc_auc_score(y_test, y_proba):.3f}")
    print("\n混淆矩阵：")
    print(confusion_matrix(y_test, y_pred))
    print("\n分类报告：")
    print(classification_report(y_test, y_pred, target_names=["未流失", "流失"]))

    print("=" * 60)
    print("步骤 7：查看特征重要性")
    print("=" * 60)
    ohe = best_model.named_steps["prep"].named_transformers_["cat"].named_steps["onehot"]
    cat_names = ohe.get_feature_names_out(categorical_features)
    all_names = numeric_features + list(cat_names)
    importances = pd.Series(
        best_model.named_steps["clf"].feature_importances_, index=all_names
    ).sort_values(ascending=False)
    print(importances.round(3).to_string())

    print("\n" + "=" * 60)
    print("步骤 8：保存模型")
    print("=" * 60)
    try:
        import joblib

        model_path = os.path.join(os.path.dirname(__file__), "churn_model.joblib")
        joblib.dump(best_model, model_path)
        print(f"模型已保存到：{model_path}")

        # 演示：加载模型并对一位新客户预测
        loaded = joblib.load(model_path)
        new_customer = pd.DataFrame(
            [{"年龄": 30, "在网月数": 3, "月消费": 150.0, "投诉次数": 4, "套餐": "基础", "合约类型": "月付"}]
        )
        p = loaded.predict_proba(new_customer)[0, 1]
        print(f"新客户流失概率：{p:.1%} → 预测：{'会流失' if p > 0.5 else '不会流失'}")
    except Exception as exc:  # noqa: BLE001
        print("保存/加载模型时出错：", exc)

    print("\n项目完成！")


if __name__ == "__main__":
    main()
