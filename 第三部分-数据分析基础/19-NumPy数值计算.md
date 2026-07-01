# 第 19 章：NumPy 数值计算

> **所属部分**：第三部分 · 数据分析基础
> **预计学习时间**：45 分钟
> **前置知识**：第一、二部分；已安装 numpy（`pip install numpy`）

## 本章学习目标

- 理解 NumPy 的核心——多维数组 `ndarray`，以及它为何比列表快。
- 会创建数组、查看形状与数据类型。
- 掌握数组的索引、切片与布尔索引。
- 掌握向量化运算与广播机制。
- 会做常用聚合统计（求和、均值、按轴计算）。

---

## 19.1 为什么需要 NumPy

Python 的列表很灵活，但做大量数值计算时又慢又费内存。**NumPy**（Numerical Python）是整个 Python 科学计算生态的基石，Pandas、scikit-learn、深度学习框架底层都依赖它。

它的核心优势：

- **快**：底层用 C 实现，对整个数组批量运算（向量化），比 Python 循环快几十上百倍。
- **省内存**：同类型数据紧凑存储。
- **功能强**：丰富的数学、线性代数、随机数函数。

约定俗成，导入时起别名 `np`：

```python
import numpy as np
```

---

## 19.2 创建数组

数组（`ndarray`）是 NumPy 的核心数据结构：一个**同类型**元素的多维网格。

```python
import numpy as np

# 从列表创建
a = np.array([1, 2, 3, 4])
print(a)            # [1 2 3 4]
print(type(a))      # <class 'numpy.ndarray'>

# 二维数组（矩阵）
b = np.array([[1, 2, 3], [4, 5, 6]])
print(b)
# [[1 2 3]
#  [4 5 6]]
```

常用的“快捷创建”函数：

```python
print(np.zeros((2, 3)))        # 2行3列全 0
print(np.ones((2, 2)))         # 全 1
print(np.full((2, 2), 7))      # 全 7
print(np.arange(0, 10, 2))     # [0 2 4 6 8]，类似 range 但返回数组
print(np.linspace(0, 1, 5))    # [0. 0.25 0.5 0.75 1.] 在0~1间均匀取5个
print(np.eye(3))               # 3x3 单位矩阵
```

随机数组（数据分析和机器学习常用）：

```python
np.random.seed(42)                    # 固定随机种子，保证结果可复现
print(np.random.rand(2, 3))           # [0,1) 均匀分布
print(np.random.randn(3))             # 标准正态分布
print(np.random.randint(1, 7, size=5)) # 掷5次骰子
```

---

## 19.3 数组的属性

```python
b = np.array([[1, 2, 3], [4, 5, 6]])

print(b.shape)      # (2, 3)  形状：2行3列
print(b.ndim)       # 2       维度数
print(b.size)       # 6       元素总数
print(b.dtype)      # int64   数据类型
```

- `shape` 是最常打交道的属性，做数据分析时经常需要确认数据的“形状”。
- `dtype` 表示元素类型（`int64`、`float64` 等）。整个数组只能是一种类型。

---

## 19.4 索引与切片

一维数组和列表用法一样：

```python
a = np.array([10, 20, 30, 40, 50])
print(a[0])         # 10
print(a[-1])        # 50
print(a[1:4])       # [20 30 40]
```

二维数组用 `[行, 列]`（逗号分隔，比列表的 `[行][列]` 更简洁）：

```python
b = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

print(b[0, 0])      # 1     第0行第0列
print(b[1, 2])      # 6     第1行第2列
print(b[0])         # [1 2 3]  整个第0行
print(b[:, 1])      # [2 5 8]  整个第1列（所有行的第1列）
print(b[0:2, 1:3])  # 前2行、第1~2列
```

`b[:, 1]` 这种“取某一列”的写法非常常用，务必掌握。

---

## 19.5 向量化运算（NumPy 的灵魂）

对数组做算术运算，会**自动对每个元素**进行，无需写循环：

```python
a = np.array([1, 2, 3, 4])

print(a + 10)       # [11 12 13 14]  每个元素都加 10
print(a * 2)        # [2 4 6 8]
print(a ** 2)       # [1 4 9 16]

b = np.array([10, 20, 30, 40])
print(a + b)        # [11 22 33 44]  两数组对应元素相加
print(a * b)        # [10 40 90 160]
```

对比一下 Python 列表：`[1,2,3] + [4,5,6]` 是拼接成 `[1,2,3,4,5,6]`，而 NumPy 是对应相加。这种“对整个数组批量操作”就叫**向量化**，既简洁又高效。

NumPy 还提供大量数学函数，同样作用于每个元素：

```python
a = np.array([1, 4, 9, 16])
print(np.sqrt(a))       # [1. 2. 3. 4.]
print(np.exp([0, 1]))   # [1. 2.718...]
print(np.log(a))        # 自然对数
```

---

## 19.6 布尔索引：按条件筛选

这是数据分析里极其强大的功能——用条件表达式筛选出满足条件的元素：

```python
a = np.array([15, 8, 23, 42, 4, 16])

mask = a > 15           # 得到布尔数组 [False False True True False True]
print(mask)
print(a[mask])          # [23 42 16]  只取 True 对应的元素
print(a[a > 15])        # 同上，更常见的写法

# 多条件用 & (与) 和 | (或)，每个条件要加括号
print(a[(a > 10) & (a < 30)])   # [15 23 16]

# 结合赋值：把所有小于 10 的值改成 0
a[a < 10] = 0
print(a)                # [15  0 23 42  0 16]
```

> 注意：多条件必须用 `&`、`|`（而不是 `and`、`or`），且每个条件用括号括起来。

---

## 19.7 聚合统计与 axis

NumPy 内置各种统计函数：

```python
a = np.array([3, 1, 4, 1, 5, 9, 2, 6])

print(a.sum())      # 31   求和
print(a.mean())     # 3.875 平均值
print(a.max())      # 9    最大值
print(a.min())      # 1
print(a.std())      # 标准差
print(a.argmax())   # 5    最大值所在的索引
```

对二维数组，可以用 `axis` 指定按行还是按列统计：

```python
b = np.array([[1, 2, 3],
              [4, 5, 6]])

print(b.sum())            # 21   所有元素之和
print(b.sum(axis=0))      # [5 7 9]   沿"行"方向压缩→每列的和
print(b.sum(axis=1))      # [6 15]    沿"列"方向压缩→每行的和
```

记忆技巧：**`axis=0` 是“跨行、按列汇总”（结果是每列一个值），`axis=1` 是“跨列、按行汇总”（结果是每行一个值）**。这个概念在 Pandas 里还会反复用到。

---

## 19.8 改变形状：reshape

```python
a = np.arange(12)             # [0 1 2 ... 11]
b = a.reshape(3, 4)           # 变成 3 行 4 列
print(b)
print(b.reshape(2, 6))        # 2 行 6 列
print(b.reshape(-1))          # 拉平成一维；-1 表示"自动计算"
print(b.T)                    # 转置（行列互换）
```

`reshape` 时元素总数必须匹配（3×4 = 12）。`-1` 是个方便的占位，让 NumPy 自动算出该维度大小。

---

## 19.9 广播（Broadcasting）简介

当两个形状不同的数组做运算时，NumPy 会尝试“广播”——自动扩展较小的数组以匹配较大的。最常见的是数组与标量：

```python
a = np.array([[1, 2, 3],
              [4, 5, 6]])
print(a + 100)      # 100 被广播到每个元素

# 每列减去该列的均值（常用于数据标准化）
col_mean = a.mean(axis=0)      # [2.5 3.5 4.5]
print(a - col_mean)            # 每行都减去这个均值向量
```

广播规则较细，初学先记住“数组与标量、数组与一行/一列之间常能自动对齐”，遇到形状报错时再回来查规则。

---

## 本章小结

- NumPy 的核心是 `ndarray`：同类型的多维数组，向量化运算快、省内存。
- 创建：`np.array`、`zeros/ones/full`、`arange/linspace`、`random.*`；`seed` 固定随机。
- 属性：`shape`（形状）、`ndim`、`size`、`dtype`。
- 索引：二维用 `[行, 列]`；`b[:, 1]` 取列；**布尔索引** `a[a>15]` 按条件筛选（多条件用 `&`/`|`）。
- 向量化：`a + 10`、`a * b` 逐元素运算；`np.sqrt` 等数学函数。
- 聚合：`sum/mean/max/std/argmax`；`axis=0` 按列、`axis=1` 按行。
- `reshape` 改形状，`-1` 自动推断；`.T` 转置；广播自动对齐形状。

---

## 练习题

1. **创建与统计**：创建一个 1~20 的数组，求它的和、均值、最大值。
2. **矩阵操作**：用 `arange` 和 `reshape` 生成一个 3×3、值为 1~9 的矩阵，打印它的第 2 列、对角线之外你能取到的第 1 行。
3. **布尔筛选**：给定 `scores = np.array([88, 45, 92, 60, 33, 78, 95])`，筛选出所有及格（≥60）的成绩，并统计及格人数。
4. **向量化计算**：给定摄氏温度数组 `c = np.array([0, 25, 37, 100])`，一行代码把它们全部转成华氏度（F = C×9/5+32）。
5. **按轴统计**：给定一个 4 名学生 3 门课的成绩矩阵，分别求“每个学生的平均分”和“每门课的平均分”。

```python
scores = np.array([[85, 90, 78],
                   [72, 88, 95],
                   [60, 75, 80],
                   [98, 92, 89]])
```

---

## 参考答案

<details>
<summary>点击展开查看参考答案</summary>

**第 1 题**：

```python
import numpy as np
a = np.arange(1, 21)
print(a.sum(), a.mean(), a.max())   # 210 10.5 20
```

**第 2 题**：

```python
m = np.arange(1, 10).reshape(3, 3)
print(m)
print(m[:, 1])      # [2 5 8]  第2列
print(m[0])         # [1 2 3]  第1行
```

**第 3 题**：

```python
scores = np.array([88, 45, 92, 60, 33, 78, 95])
passed = scores[scores >= 60]
print(passed)                # [88 92 60 78 95]
print("及格人数：", passed.size)   # 5
```

**第 4 题**：

```python
c = np.array([0, 25, 37, 100])
f = c * 9 / 5 + 32
print(f)            # [ 32.   77.   98.6 212. ]
```

**第 5 题**：

```python
scores = np.array([[85, 90, 78],
                   [72, 88, 95],
                   [60, 75, 80],
                   [98, 92, 89]])
print("每个学生平均分：", scores.mean(axis=1))   # 按行
print("每门课平均分：", scores.mean(axis=0))     # 按列
```

</details>

---

⬅️ 上一章：[第 18 章 · 虚拟环境与项目管理](../第二部分-Python进阶/18-虚拟环境与项目管理.md)
➡️ 下一章：[第 20 章 · Pandas 数据结构与操作](20-Pandas数据结构与操作.md)
