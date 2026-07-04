# 第 24 章：机器学习概述与 scikit-learn 入门

> **所属部分**：第四部分 · 机器学习实战
> **预计学习时间**：45 分钟
> **前置知识**：第三部分（NumPy / Pandas）；已安装 scikit-learn

## 本章学习目标

- 理解什么是机器学习，以及它与传统编程的区别。
- 分清监督学习、无监督学习的区别。
- 掌握核心术语：特征、标签、训练集、测试集、模型。
- 理解 scikit-learn 统一的 `fit` / `predict` 工作流。
- 亲手训练出第一个分类模型（鸢尾花识别）。

---

## 24.1 什么是机器学习

**传统编程**是：人来写规则，程序按规则处理数据得到结果。

```
规则 + 数据  ──►  结果
```

**机器学习**反过来：我们给计算机大量“数据 + 答案”，让它**自己总结出规则（模型）**，再用这个规则去预测新数据。

```
数据 + 答案  ──►  规则（模型）  ──►  预测新数据
```

举个例子：要识别垃圾邮件，传统方法要人工写一堆“如果包含‘中奖’就是垃圾”的规则，永远写不全。机器学习则是喂给它成千上万封已标好“垃圾/正常”的邮件，让它自己学会区分。

**机器学习特别适合**：规则复杂到难以手写、但有大量历史数据的问题，比如图像识别、语音识别、推荐、预测。

---

## 24.2 机器学习的主要类型

### 监督学习（Supervised Learning）

训练数据**带有正确答案（标签）**，模型学习“输入→输出”的映射。又分两类：

- **分类（Classification）**：预测**离散类别**。如判断邮件是否垃圾、图片是猫还是狗、肿瘤良性还是恶性。
- **回归（Regression）**：预测**连续数值**。如预测房价、气温、销售额。

### 无监督学习（Unsupervised Learning）

训练数据**没有标签**，模型自己发现数据中的结构。如：

- **聚类（Clustering）**：把相似的样本分成若干组，如用户分群。
- **降维（Dimensionality Reduction）**：在保留信息的前提下压缩特征数量。

> 本部分第 25 章讲回归，第 26 章讲分类，第 27 章讲模型评估与调参，第 28 章讲聚类与降维。还有强化学习等类型，本教程不涉及。

---

## 24.3 核心术语

用一张学生成绩表来理解：

| 身高 | 体重 | 每周运动小时 | → | 是否健康 |
| --- | --- | --- | --- | --- |
| 170 | 65 | 5 | | 是 |
| 160 | 80 | 1 | | 否 |

- **样本（sample）**：每一行数据（一个学生）。
- **特征（feature）**：用来做预测的输入，即前几列（身高、体重、运动时间）。通常记作 **X**。
- **标签/目标（label / target）**：要预测的答案，即最后一列（是否健康）。通常记作 **y**。
- **模型（model）**：从数据中学到的“规则”。
- **训练（training / fit）**：用数据教模型学规则的过程。
- **预测（predict）**：用训练好的模型对新样本给出结果。

### 训练集与测试集

我们要评估模型“学得好不好”，不能拿它做过的题来考它。所以把数据分成两部分：

- **训练集**：用来训练模型（通常 70%~80%）。
- **测试集**：模型没见过的数据，用来检验它的真实水平（通常 20%~30%）。

> 这就像备考：训练集是练习题，测试集是最终考试。用练习题的答案去考试当然满分，但那不能反映真实水平。

---

## 24.4 scikit-learn 简介

**scikit-learn**（简称 sklearn）是 Python 最流行的传统机器学习库，它的最大优点是**接口统一**：无论什么算法，都遵循同样的三步套路。

```python
from sklearn.某模块 import 某模型

model = 某模型()          # 1. 创建模型
model.fit(X_train, y_train)   # 2. 训练（喂入特征和标签）
predictions = model.predict(X_test)   # 3. 预测
```

学会这个套路，你就能用几乎所有 sklearn 模型——换算法只需换第一行！这是 sklearn 设计的精髓。

---

## 24.5 第一个机器学习项目：鸢尾花分类

鸢尾花（Iris）数据集是机器学习界的“Hello World”：根据花的 4 个尺寸特征，判断它属于 3 个品种中的哪一种。sklearn 自带这个数据集。

### 第一步：加载数据

```python
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data              # 特征：150 朵花 × 4 个尺寸
y = iris.target            # 标签：每朵花的品种（0/1/2）

print("特征形状：", X.shape)          # (150, 4)
print("特征名：", iris.feature_names)  # 花萼长/宽、花瓣长/宽
print("品种名：", iris.target_names)   # setosa, versicolor, virginica
print("前 3 个样本：\n", X[:3])
print("前 3 个标签：", y[:3])           # [0 0 0]
```

### 第二步：划分训练集和测试集

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,        # 20% 作测试集
    random_state=42,      # 固定随机种子，保证可复现
    stratify=y,           # 按标签分层抽样，保证各类别比例一致
)
print("训练集：", X_train.shape)   # (120, 4)
print("测试集：", X_test.shape)    # (30, 4)
```

- `random_state=42`：固定“随机”划分方式，让每次运行结果一样（数字随意，42 是惯例）。
- `stratify=y`：确保训练集和测试集里三个品种的比例和原始数据一致。

### 第三步：创建并训练模型

我们用 **K 近邻（KNN）**算法——它的思想极其朴素：要判断一个新样本属于哪类，就看它“最近的 K 个邻居”里哪类最多。

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=3)   # 看最近的 3 个邻居
model.fit(X_train, y_train)                   # 训练
```

### 第四步：预测与评估

```python
from sklearn.metrics import accuracy_score

y_pred = model.predict(X_test)
print("预测结果：", y_pred)
print("真实标签：", y_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"准确率：{accuracy:.2%}")     # 约 100%
# 也可以直接用 model.score(X_test, y_test)
```

**准确率（accuracy）**就是“预测对的样本数 ÷ 总样本数”。鸢尾花很容易区分，KNN 在这个配置下能达到很高的准确率（约 97%~100%）。

### 第五步：预测新的花

```python
import numpy as np

new_flower = np.array([[5.1, 3.5, 1.4, 0.2]])   # 一朵新花的 4 个尺寸
pred = model.predict(new_flower)
print("预测品种：", iris.target_names[pred[0]])   # setosa
```

🎉 恭喜！你刚刚完成了一个完整的机器学习项目：从加载数据、划分、训练到预测。

---

## 24.6 完整代码回顾

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# 1. 数据
iris = load_iris()
X, y = iris.data, iris.target

# 2. 划分
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# 3. 建模 + 训练
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# 4. 预测 + 评估
y_pred = model.predict(X_test)
print(f"准确率：{accuracy_score(y_test, y_pred):.2%}")
```

短短十几行，就是一个完整的机器学习流程。记住这个骨架，后面的章节都是在它基础上深入。

---

## 本章小结

- 机器学习让计算机从“数据+答案”中自己学规则，适合规则复杂、数据充足的问题。
- 类型：监督学习（分类=预测类别、回归=预测数值）、无监督学习（聚类、降维）。
- 术语：特征 X、标签 y、样本、模型、训练（fit）、预测（predict）。
- 划分训练集/测试集：用没见过的数据评估模型真实水平。
- sklearn 统一套路：`model = 模型()` → `model.fit(X_train, y_train)` → `model.predict(X_test)`。
- 用 KNN 完成了鸢尾花分类，`accuracy_score` 评估准确率。

---

## 练习题

1. **概念判断**：以下任务分别属于分类、回归还是聚类？(a) 预测明天气温；(b) 判断评论是好评还是差评；(c) 把顾客自动分成几个群体；(d) 预测二手车价格。
2. **改变 K 值**：把鸢尾花例子里的 `n_neighbors` 改成 1、5、10，分别看准确率有无变化。
3. **改变划分比例**：把 `test_size` 改成 0.3，重新训练评估，观察训练集/测试集大小和准确率。
4. **换个数据集**：用 `from sklearn.datasets import load_wine` 加载红酒数据集，套用本章的流程训练一个 KNN 分类器并输出准确率。
5. **理解 stratify**：查阅并用一句话解释，为什么分类任务中划分数据时推荐使用 `stratify=y`。

---

## 参考答案

<details>
<summary>点击展开查看参考答案</summary>

**第 1 题**：(a) 回归（连续数值）；(b) 分类（离散类别）；(c) 聚类（无标签分群）；(d) 回归。

**第 2 题**：

```python
for k in [1, 5, 10]:
    m = KNeighborsClassifier(n_neighbors=k)
    m.fit(X_train, y_train)
    print(f"k={k}: {m.score(X_test, y_test):.2%}")
```

鸢尾花较简单，不同 K 值准确率都很高，可能略有差异。K 值是一个需要调节的“超参数”（第 27 章详述）。

**第 3 题**：

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)
# 训练集变为 105 个，测试集 45 个；准确率仍然很高
```

**第 4 题**：

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42, stratify=wine.target)
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)
print(f"准确率：{model.score(X_test, y_test):.2%}")
```

> 提示：红酒数据的各特征量纲差异大，KNN 准确率可能不高。第 27 章会学到用“标准化”来改善——这是一个很好的伏笔。

**第 5 题**：`stratify=y` 让训练集和测试集中各类别的比例与原始数据保持一致，避免出现“某个类别在测试集中过多或过少”导致评估失真，尤其在类别不平衡时很重要。

</details>

---

⬅️ 上一章：[第 23 章 · 探索性数据分析（EDA）实战](../第三部分-数据分析基础/23-探索性数据分析实战.md)
➡️ 下一章：[第 25 章 · 监督学习：线性回归实战](25-线性回归实战.md)
