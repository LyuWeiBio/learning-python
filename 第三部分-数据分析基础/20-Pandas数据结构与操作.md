# 第 20 章：Pandas 数据结构与操作

> **所属部分**：第三部分 · 数据分析基础
> **预计学习时间**：45 分钟
> **前置知识**：第 19 章（NumPy）；已安装 pandas

## 本章学习目标

- 理解 Pandas 的两大数据结构：`Series` 与 `DataFrame`。
- 会创建 DataFrame，会从 CSV 读取数据。
- 掌握查看数据的常用方法：`head`、`info`、`describe`。
- 会选择列、选择行（`loc` / `iloc`）。
- 会用条件筛选行、新增列。

---

## 20.1 Pandas 是什么

如果说 NumPy 处理的是“纯数字矩阵”，那么 **Pandas** 处理的就是**带标签的表格数据**（就像 Excel 表格）——有行、有列、有列名。它是数据分析中使用最频繁的库，几乎所有的数据清洗、统计、变换都靠它。

约定别名 `pd`：

```python
import pandas as pd
import numpy as np
```

Pandas 有两个核心数据结构：

- **Series**：一维带标签数组（相当于表格的**一列**）。
- **DataFrame**：二维表格（相当于**整张表**，由多个 Series 组成）。

---

## 20.2 Series：带标签的一维数据

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40])
print(s)
# 0    10
# 1    20
# 2    30
# 3    40
# dtype: int64
```

左边的 `0 1 2 3` 是**索引（index）**，右边是值。可以自定义索引：

```python
s = pd.Series([85, 92, 78], index=["语文", "数学", "英语"])
print(s["数学"])        # 92，用标签取值
print(s.mean())         # 85.0，Series 也支持各种统计
```

---

## 20.3 DataFrame：二维表格

最常用的创建方式是用字典（键是列名，值是该列的数据）：

```python
import pandas as pd

data = {
    "姓名": ["小明", "小红", "小刚", "小丽"],
    "年龄": [18, 20, 19, 21],
    "城市": ["北京", "上海", "广州", "深圳"],
    "成绩": [88, 92, 79, 95],
}
df = pd.DataFrame(data)
print(df)
#    姓名  年龄  城市  成绩
# 0  小明  18  北京  88
# 1  小红  20  上海  92
# 2  小刚  19  广州  79
# 3  小丽  21  深圳  95
```

每一列是一个 Series，共享同一个行索引。

---

## 20.4 读写文件

真实数据通常来自文件。Pandas 读取 CSV 极其简单：

```python
# 读取 CSV（最常用）
df = pd.read_csv("data.csv")

# 读取 Excel（需额外安装 openpyxl）
# df = pd.read_excel("data.xlsx")

# 保存
df.to_csv("output.csv", index=False)   # index=False 不保存行索引
```

Pandas 还能读 JSON、SQL、剪贴板等各种来源，`read_csv` 是最常打交道的。

---

## 20.5 查看数据

拿到数据第一件事就是“看看它长什么样”：

```python
print(df.head())        # 前 5 行（可传数字，如 head(3)）
print(df.tail(2))       # 后 2 行
print(df.shape)         # (4, 4)  4 行 4 列
print(df.columns)       # 所有列名
print(df.dtypes)        # 每列的数据类型
print(df.info())        # 综合信息：行数、列名、类型、非空数量
print(df.describe())    # 数值列的统计摘要：count/mean/std/min/max/分位数
```

`info()` 和 `describe()` 是探索数据的“黄金搭档”：前者看结构和缺失情况，后者看数值分布。

---

## 20.6 选择列

```python
# 选一列 → 返回 Series
print(df["姓名"])

# 选多列 → 用列名列表，返回 DataFrame
print(df[["姓名", "成绩"]])
```

> 记住：选**一列**用 `df["列名"]`；选**多列**要用**双层方括号** `df[["列1", "列2"]]`（里面是一个列表）。

---

## 20.7 选择行：loc 与 iloc

这是初学者最容易混淆、也最重要的部分：

- **`loc`**：基于**标签**（行索引名、列名）选择。
- **`iloc`**：基于**位置**（从 0 开始的整数下标）选择。

```python
# iloc：按位置
print(df.iloc[0])           # 第 0 行（返回 Series）
print(df.iloc[0:2])         # 第 0~1 行
print(df.iloc[0, 1])        # 第 0 行第 1 列的值 → 18
print(df.iloc[:, 0])        # 所有行的第 0 列

# loc：按标签
print(df.loc[0])            # 索引标签为 0 的行
print(df.loc[0, "姓名"])    # 索引 0、列名"姓名" → 小明
print(df.loc[0:2, ["姓名", "成绩"]])   # 注意：loc 切片含尾！
```

> **重要差异**：`iloc[0:2]` 取 0、1 两行（含头不含尾，和列表一样）；而 `loc[0:2]` 取 0、1、2 三行（**含尾**，因为它是按标签）。

---

## 20.8 条件筛选（最常用！）

和 NumPy 的布尔索引一样，用条件筛选出符合要求的行：

```python
# 筛选成绩 > 85 的学生
print(df[df["成绩"] > 85])

# 多条件：& 与、| 或，每个条件加括号
print(df[(df["成绩"] > 85) & (df["年龄"] < 21)])

# isin：某列的值在给定集合中
print(df[df["城市"].isin(["北京", "上海"])])

# 筛选后只看某些列
print(df[df["成绩"] > 85][["姓名", "成绩"]])
```

条件筛选是数据分析的日常操作，务必练熟。

---

## 20.9 新增与修改列

```python
# 新增一列（基于已有列计算）
df["是否优秀"] = df["成绩"] >= 90
print(df)

# 新增一列常数
df["班级"] = "一班"

# 基于运算新增
df["成绩+5"] = df["成绩"] + 5

# 修改整列
df["年龄"] = df["年龄"] + 1     # 所有人年龄+1

# 删除列
df = df.drop(columns=["成绩+5"])
```

新增列时，等号右边可以是一个 Series、一个计算表达式或一个常数，Pandas 会自动对齐到每一行。

---

## 20.10 排序

```python
# 按成绩降序
print(df.sort_values("成绩", ascending=False))

# 按多列排序
print(df.sort_values(["城市", "成绩"]))

# 按索引排序
print(df.sort_index())
```

---

## 本章小结

- Pandas 处理**带标签的表格数据**；`Series`（一列）、`DataFrame`（整张表）。
- 用字典创建 DataFrame；`pd.read_csv` 读取、`to_csv(index=False)` 保存。
- 查看：`head/tail/shape/columns/dtypes/info/describe`。
- 选列：`df["列"]`（一列）、`df[["列1","列2"]]`（多列）。
- 选行：`iloc` 按位置（含头不含尾）、`loc` 按标签（切片含尾）。
- 条件筛选：`df[df["列"] > x]`，多条件用 `&`/`|` 并加括号。
- 新增列 `df["新列"] = ...`；`sort_values` 排序。

---

## 练习题

准备数据（后面几题都用它）：

```python
import pandas as pd
df = pd.DataFrame({
    "商品": ["苹果", "香蕉", "橙子", "葡萄", "西瓜"],
    "单价": [8, 4, 6, 12, 3],
    "数量": [10, 20, 15, 8, 30],
    "产地": ["山东", "海南", "江西", "新疆", "海南"],
})
```

1. **查看**：打印这份数据的形状、前 3 行，以及数值列的统计摘要。
2. **新增列**：新增一列 `总价` = 单价 × 数量。
3. **筛选**：筛选出单价大于 5 的商品，只显示“商品”和“单价”两列。
4. **多条件**：筛选出产地是“海南”**且**数量大于 10 的商品。
5. **排序**：按 `总价` 从高到低排序，输出结果。

---

## 参考答案

<details>
<summary>点击展开查看参考答案</summary>

```python
import pandas as pd
df = pd.DataFrame({
    "商品": ["苹果", "香蕉", "橙子", "葡萄", "西瓜"],
    "单价": [8, 4, 6, 12, 3],
    "数量": [10, 20, 15, 8, 30],
    "产地": ["山东", "海南", "江西", "新疆", "海南"],
})

# 第 1 题
print(df.shape)          # (5, 4)
print(df.head(3))
print(df.describe())

# 第 2 题
df["总价"] = df["单价"] * df["数量"]
print(df)

# 第 3 题
print(df[df["单价"] > 5][["商品", "单价"]])

# 第 4 题
print(df[(df["产地"] == "海南") & (df["数量"] > 10)])

# 第 5 题
print(df.sort_values("总价", ascending=False))
```

</details>

---

⬅️ 上一章：[第 19 章 · NumPy 数值计算](19-NumPy数值计算.md)
➡️ 下一章：[第 21 章 · Pandas 数据清洗与聚合](21-Pandas数据清洗与聚合.md)
