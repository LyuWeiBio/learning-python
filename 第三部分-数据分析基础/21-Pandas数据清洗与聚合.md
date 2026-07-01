# 第 21 章：Pandas 数据清洗与聚合

> **所属部分**：第三部分 · 数据分析基础
> **预计学习时间**：45 分钟
> **前置知识**：第 20 章（Pandas 基础）

## 本章学习目标

- 会处理缺失值（`isnull`、`dropna`、`fillna`）。
- 会处理重复值、转换数据类型。
- 会用 `apply`、`map` 对数据做自定义变换。
- 掌握 `value_counts` 与分组聚合 `groupby`。
- 了解表格的合并（`merge`、`concat`）。

> 真实世界的数据往往是“脏”的——有缺失、有重复、格式混乱。**数据清洗**通常占数据分析师 60%~80% 的时间，本章至关重要。

---

## 21.1 准备示例数据

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "姓名": ["小明", "小红", "小刚", "小丽", "小明"],
    "部门": ["技术", "销售", "技术", None, "销售"],
    "薪资": [15000, 12000, np.nan, 18000, 15000],
    "年龄": [25, 30, 28, 35, 25],
})
print(df)
```

其中 `None` 和 `np.nan` 都表示**缺失值**（Not a Number / 空）。

---

## 21.2 检测缺失值

```python
print(df.isnull())          # 每个位置是否为缺失（True/False 表格）
print(df.isnull().sum())    # 每列的缺失值个数（最常用！）
print(df.isnull().sum().sum())   # 总缺失数
```

`df.isnull().sum()` 是拿到数据后必做的检查，一眼看出哪列缺失多少。

---

## 21.3 处理缺失值

### 方式一：删除（dropna）

```python
print(df.dropna())              # 删除任何含缺失值的行
print(df.dropna(subset=["薪资"]))  # 只在"薪资"缺失时删除该行
print(df.dropna(axis=1))        # 删除含缺失值的列（较少用）
```

### 方式二：填充（fillna）

删除会丢失数据，很多时候更好的做法是**填充**：

```python
# 用固定值填充
print(df.fillna(0))

# 用该列的均值填充数值列（常见做法）
mean_salary = df["薪资"].mean()
df["薪资"] = df["薪资"].fillna(mean_salary)

# 用众数/固定类别填充分类列
df["部门"] = df["部门"].fillna("未知")

print(df)
```

选择删除还是填充，取决于缺失比例和业务含义：缺失很少可删；缺失较多、且能合理估计时宜填充。

---

## 21.4 处理重复值

```python
print(df.duplicated())          # 每行是否与之前重复
print(df.duplicated().sum())    # 重复行数
df2 = df.drop_duplicates()      # 删除完全重复的行
df3 = df.drop_duplicates(subset=["姓名"])  # 按"姓名"去重，保留第一次
```

---

## 21.5 数据类型转换

```python
# 查看类型
print(df.dtypes)

# 转换类型
df["年龄"] = df["年龄"].astype(int)
df["薪资"] = df["薪资"].astype(float)

# 字符串转数字（含错误处理）
# pd.to_numeric(series, errors="coerce")  无法转换的会变成 NaN
```

---

## 21.6 apply 与 map：自定义变换

### map：对 Series 逐元素变换

```python
# 用字典做映射
df["部门编码"] = df["部门"].map({"技术": 1, "销售": 2, "未知": 0})

# 用函数变换
df["薪资档次"] = df["薪资"].map(lambda x: "高" if x >= 15000 else "普通")
```

### apply：更通用的变换

`apply` 既能作用于 Series，也能按行/按列作用于 DataFrame：

```python
# 对某列每个元素应用函数
df["年龄段"] = df["年龄"].apply(lambda x: "青年" if x < 30 else "中年")

# 按行计算（axis=1），可访问整行数据
df["描述"] = df.apply(lambda row: f"{row['姓名']}-{row['部门']}", axis=1)
print(df)
```

---

## 21.7 字符串处理：.str

对文本列，用 `.str` 就能批量调用字符串方法（第 04 章学过的那些）：

```python
s = pd.Series(["  Alice ", "BOB", "charlie"])
print(s.str.strip())        # 去空格
print(s.str.lower())        # 转小写
print(s.str.len())          # 每个字符串长度
print(s.str.contains("a"))  # 是否包含 "a"
print(s.str.replace("o", "0"))
```

处理邮箱、地址、姓名等文本列时，`.str` 系列非常好用。

---

## 21.8 value_counts：统计频数

统计某列每个值出现的次数，做类别分析必备：

```python
print(df["部门"].value_counts())
# 技术    2
# 销售    2
# 未知    1

print(df["部门"].value_counts(normalize=True))  # 换成占比
print(df["部门"].nunique())      # 有几种不同的值
print(df["部门"].unique())       # 列出所有不同的值
```

---

## 21.9 分组聚合：groupby（本章重点）

`groupby` 实现“**分组—计算**”，是 Pandas 最强大的功能之一。思路是“**拆分-应用-合并**”：先按某列把数据分成若干组，对每组做统计，再把结果合起来。

```python
import pandas as pd

sales = pd.DataFrame({
    "部门": ["技术", "销售", "技术", "销售", "技术"],
    "姓名": ["A", "B", "C", "D", "E"],
    "薪资": [15000, 12000, 20000, 13000, 18000],
})

# 按部门分组，求每组的平均薪资（.round(2) 让小数更整洁）
print(sales.groupby("部门")["薪资"].mean().round(2))
# 部门
# 技术    17666.67
# 销售    12500.00
# Name: 薪资, dtype: float64

# 每组的人数
print(sales.groupby("部门").size())

# 每组多个统计量
print(sales.groupby("部门")["薪资"].agg(["mean", "max", "min", "count"]))

# 按多列分组
# sales.groupby(["部门", "职级"])["薪资"].sum()
```

`groupby(列)[目标列].聚合函数()` 是最常用的模式：例如“**每个部门**的**平均薪资**”“**每个城市**的**销量总和**”。`agg` 可以一次算多个指标。

---

## 21.10 合并表格（了解）

实际项目常需把多张表拼在一起。

### concat：简单堆叠

```python
df_a = pd.DataFrame({"名字": ["A", "B"], "分数": [80, 90]})
df_b = pd.DataFrame({"名字": ["C", "D"], "分数": [70, 85]})
print(pd.concat([df_a, df_b], ignore_index=True))   # 上下拼接
```

### merge：按键关联（类似 SQL 的 JOIN）

```python
students = pd.DataFrame({"学号": [1, 2, 3], "姓名": ["小明", "小红", "小刚"]})
scores = pd.DataFrame({"学号": [1, 2, 3], "成绩": [88, 92, 79]})

result = pd.merge(students, scores, on="学号")   # 按"学号"关联
print(result)
#    学号  姓名  成绩
# 0   1  小明  88
# 1   2  小红  92
# 2   3  小刚  79
```

`merge` 通过共同的“键”（如学号）把两张表的信息拼到一起，是关系型数据处理的核心。

---

## 本章小结

- 缺失值：`isnull().sum()` 检测；`dropna()` 删除、`fillna()` 填充（可用均值/固定值）。
- 重复值：`duplicated()` / `drop_duplicates()`；类型转换 `astype`。
- 自定义变换：`map`（Series 逐元素/字典映射）、`apply`（更通用，可 `axis=1` 按行）。
- 文本列用 `.str.xxx()` 批量处理字符串。
- `value_counts()` 统计频数，`nunique`/`unique` 看类别。
- **`groupby(列)[目标].聚合()`** 分组聚合，`agg` 一次多指标。
- 合并：`concat`（堆叠）、`merge(on=键)`（按键关联）。

---

## 练习题

用以下数据：

```python
import pandas as pd
import numpy as np
df = pd.DataFrame({
    "城市": ["北京", "上海", "北京", "广州", "上海", "北京"],
    "类别": ["电子", "服装", "电子", "食品", "电子", "服装"],
    "销量": [120, 85, np.nan, 60, 95, 70],
    "利润": [30, 20, 25, 15, 22, 18],
})
```

1. **缺失值**：统计每列缺失值个数，然后用“销量”列的均值填充缺失。
2. **频数统计**：统计每个城市出现的次数。
3. **分组求和**：按城市分组，求各城市的总利润。
4. **分组多指标**：按类别分组，求每个类别的销量均值和利润总和。
5. **新增列 + 分组**：新增一列 `利润率` = 利润 / 销量，然后求各城市的平均利润率。

---

## 参考答案

<details>
<summary>点击展开查看参考答案</summary>

```python
import pandas as pd
import numpy as np
df = pd.DataFrame({
    "城市": ["北京", "上海", "北京", "广州", "上海", "北京"],
    "类别": ["电子", "服装", "电子", "食品", "电子", "服装"],
    "销量": [120, 85, np.nan, 60, 95, 70],
    "利润": [30, 20, 25, 15, 22, 18],
})

# 第 1 题
print(df.isnull().sum())
df["销量"] = df["销量"].fillna(df["销量"].mean())

# 第 2 题
print(df["城市"].value_counts())

# 第 3 题
print(df.groupby("城市")["利润"].sum())

# 第 4 题
print(df.groupby("类别").agg(销量均值=("销量", "mean"),
                             利润总和=("利润", "sum")))

# 第 5 题
df["利润率"] = df["利润"] / df["销量"]
print(df.groupby("城市")["利润率"].mean())
```

</details>

---

⬅️ 上一章：[第 20 章 · Pandas 数据结构与操作](20-Pandas数据结构与操作.md)
➡️ 下一章：[第 22 章 · Matplotlib 数据可视化](22-Matplotlib数据可视化.md)
