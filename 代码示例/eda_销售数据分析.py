"""
第 23 章配套脚本：电商销售数据的探索性数据分析（EDA）。

运行方式：
    python 代码示例/eda_销售数据分析.py

说明：
- 数据是用固定随机种子生成的，可完整复现。
- 图表默认弹窗显示；若在无图形界面的环境（如服务器）运行，
  会自动改用无界面后端并把图保存到 代码示例/eda_output/ 目录。
"""

import os

import numpy as np
import pandas as pd
import matplotlib

# 无图形界面时自动切换后端，保证脚本在任何环境都能跑
if not os.environ.get("DISPLAY") and os.name != "nt":
    matplotlib.use("Agg")

import matplotlib.pyplot as plt

# 中文显示（按系统选择存在的字体；找不到时退回英文也不影响逻辑）
plt.rcParams["font.sans-serif"] = ["SimHei", "WenQuanYi Micro Hei", "PingFang SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "eda_output")


def build_dataset(n: int = 500) -> pd.DataFrame:
    """生成一份模拟电商销售数据。"""
    # 使用与第 23 章正文相同的随机接口和种子，运行本脚本即可复现正文所述数据
    np.random.seed(42)
    df = pd.DataFrame(
        {
            "订单ID": range(1, n + 1),
            "类别": np.random.choice(["电子产品", "服装", "食品", "家居", "图书"], n),
            "地区": np.random.choice(["华北", "华东", "华南", "西部"], n, p=[0.3, 0.3, 0.25, 0.15]),
            "销售额": np.round(np.random.gamma(2, 300, n), 2),
            "数量": np.random.randint(1, 11, n),
            "客户年龄": np.random.randint(18, 65, n).astype(float),
        }
    )
    df["利润"] = np.round(df["销售额"] * np.random.uniform(0.05, 0.3, n), 2)
    # 人为制造缺失值
    missing_idx = np.random.choice(n, 25, replace=False)
    df.loc[missing_idx, "客户年龄"] = np.nan
    return df


def show_or_save(fig, filename: str) -> None:
    """有界面则显示，无界面则保存到文件。"""
    if matplotlib.get_backend().lower() == "agg":
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        path = os.path.join(OUTPUT_DIR, filename)
        fig.savefig(path, dpi=120, bbox_inches="tight")
        print(f"[图表已保存] {path}")
        plt.close(fig)
    else:
        plt.show()


def main() -> None:
    df = build_dataset()

    print("=" * 50)
    print("第一步：整体认识数据")
    print("=" * 50)
    print("形状：", df.shape)
    print(df.head())
    print("\n数值列摘要：")
    print(df.describe().round(2))

    print("\n" + "=" * 50)
    print("第二步：数据质量检查")
    print("=" * 50)
    print("各列缺失值：\n", df.isnull().sum())
    print("重复行数：", df.duplicated().sum())
    df["客户年龄"] = df["客户年龄"].fillna(df["客户年龄"].median())
    print("填充后客户年龄缺失：", df["客户年龄"].isnull().sum())

    print("\n" + "=" * 50)
    print("第三步：单变量分析")
    print("=" * 50)
    print("类别分布：\n", df["类别"].value_counts())
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].hist(df["销售额"], bins=30, edgecolor="black")
    axes[0].set_title("销售额分布")
    axes[1].hist(df["客户年龄"], bins=20, edgecolor="black", color="orange")
    axes[1].set_title("客户年龄分布")
    fig.tight_layout()
    show_or_save(fig, "01_单变量分布.png")

    print("\n" + "=" * 50)
    print("第四步：多变量相关性")
    print("=" * 50)
    num_cols = ["销售额", "数量", "客户年龄", "利润"]
    print(df[num_cols].corr().round(3))

    print("\n" + "=" * 50)
    print("第五步：分组洞察")
    print("=" * 50)
    category_stats = (
        df.groupby("类别")
        .agg(总销售额=("销售额", "sum"), 平均利润=("利润", "mean"), 订单数=("订单ID", "count"))
        .sort_values("总销售额", ascending=False)
    )
    print(category_stats.round(2))

    fig, ax = plt.subplots(figsize=(8, 4))
    category_stats["总销售额"].plot(kind="bar", ax=ax, title="各类别总销售额")
    fig.tight_layout()
    show_or_save(fig, "02_各类别总销售额.png")

    print("\n地区利润：")
    print(df.groupby("地区")["利润"].sum().sort_values(ascending=False).round(2))

    print("\n" + "=" * 50)
    print("第六步：分箱分析")
    print("=" * 50)
    df["年龄段"] = pd.cut(
        df["客户年龄"], bins=[0, 25, 35, 45, 100], labels=["青年", "青壮年", "中年", "中老年"]
    )
    print("各年龄段平均销售额：")
    print(df.groupby("年龄段", observed=True)["销售额"].mean().round(2))

    print("\n分析完成！")


if __name__ == "__main__":
    main()
