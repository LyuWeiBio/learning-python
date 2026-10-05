# -*- coding: utf-8 -*-
"""
第 28 章：无监督学习——聚类与降维
对应教材：第四部分-机器学习实战/28-聚类与降维.md

演示：K-Means 聚类、肘部法则选 K、轮廓系数评估、
      PCA 降维与可视化、鸢尾花聚类 vs 真实标签对比。
注：matplotlib 用 Agg 后端，图表 savefig 到 output/，不调用 plt.show()。
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from sklearn.datasets import make_blobs, load_iris
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

OUT = Path(__file__).parent / "output"
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams["font.sans-serif"] = ["Noto Serif CJK SC"]
plt.rcParams["axes.unicode_minus"] = False


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. K-Means 聚类")

# 生成 4 团数据（假装不知道是 4 团）
X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.8, random_state=42)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)      # 训练并返回每个样本的簇编号

print("前 10 个样本的簇：", labels[:10])
print("簇中心：\n", kmeans.cluster_centers_.round(2))
print("Inertia（簇内误差）：", round(kmeans.inertia_, 1))  # 越小越紧凑

# 可视化聚类结果
plt.figure()
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap="viridis", alpha=0.6)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            c="red", marker="X", s=200, label="簇中心")
plt.title("K-Means 聚类结果")
plt.legend()
plt.savefig(OUT / "ch28_kmeans.png", dpi=150, bbox_inches="tight")
plt.close()
print("已保存：ch28_kmeans.png")

section("2. 肘部法则选 K")

inertias = []
K_range = range(1, 8)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    inertias.append(km.inertia_)

plt.figure()
plt.plot(K_range, inertias, marker="o")
plt.xlabel("K（簇数）")
plt.ylabel("Inertia")
plt.title("肘部法则")
plt.savefig(OUT / "ch28_elbow.png", dpi=150, bbox_inches="tight")
plt.close()
print("K 与 inertia：", dict(zip(K_range, [round(i) for i in inertias])))
print("已保存：ch28_elbow.png")
# 观察：K=1→4 急剧下降，之后趋平——"肘部"在 K=4，正是真实簇数

section("3. 轮廓系数评估聚类质量")

score = silhouette_score(X, labels)
print(f"轮廓系数：{score:.3f}（越接近 1 越好）")

# 用轮廓系数辅助选 K
print("不同 K 的轮廓系数：")
for k in [2, 3, 4, 5]:
    lb = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(X)
    print(f"K={k}: {silhouette_score(X, lb):.3f}")

section("4. PCA 降维与可视化")

iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)   # PCA 前先标准化

pca = PCA(n_components=2)          # 降到 2 维
X_pca = pca.fit_transform(X_scaled)

print("降维前：", X_scaled.shape)   # (150, 4)
print("降维后：", X_pca.shape)      # (150, 2)
print("各主成分解释的方差比例：", pca.explained_variance_ratio_.round(3))
print("累计解释比例：", round(pca.explained_variance_ratio_.sum(), 3))

plt.figure(figsize=(7, 5))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=iris.target, cmap="viridis")
plt.xlabel("主成分 1")
plt.ylabel("主成分 2")
plt.title("鸢尾花数据 PCA 降维可视化")
plt.colorbar(scatter, label="品种")
plt.savefig(OUT / "ch28_pca.png", dpi=150, bbox_inches="tight")
plt.close()
print("已保存：ch28_pca.png")

section("5. 综合：先聚类，再和真实品种对比")

# 假装没有标签，用 K-Means 聚成 3 类
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

# 调整兰德指数：衡量聚类与真实标签的一致性（1 表示完全一致）
ari = adjusted_rand_score(iris.target, cluster_labels)
print(f"聚类与真实品种的一致性 (ARI)：{ari:.3f}")
# 说明在完全没有标签的情况下，K-Means 也能大致发现真实结构

print("\n第 28 章演示完毕 ✅")
