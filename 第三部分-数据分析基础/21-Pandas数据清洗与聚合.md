# 第 21 章：Pandas 数据清洗与聚合

> **所属部分**：第三部分 · 数据分析基础
> **预计学习时间**：45 分钟
> **前置知识**：第 20 章（Pandas 基础）
> **配套代码**：[`代码示例/ch21_Pandas数据清洗与聚合.py`](../代码示例/ch21_Pandas数据清洗与聚合.py)

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

其中 `None` 和 `np.nan` 都表示**缺失值**（Not a Number / 空）。打印出来是这样的：

```
   姓名   部门       薪资  年龄
0  小明   技术  15000.0  25
1  小红   销售  12000.0  30
2  小刚   技术      NaN  28
3  小丽  NaN  18000.0  35
4  小明   销售  15000.0  25
```

注意两个细节：缺失值显示为 `NaN`（较老的 pandas 版本里，文本列的缺失可能显示为 `None`）；“薪资”列因为混进了 `NaN`，整数都变成了小数（`15000.0`）——`NaN` 在计算机里属于小数类型。

---

## 21.2 检测缺失值

```python
print(df.isnull())          # 每个位置是否为缺失（True/False 表格）
print(df.isnull().sum())    # 每列的缺失值个数（最常用！）
print(df.isnull().sum().sum())   # 总缺失数
```

`df.isnull().sum()` 是拿到数据后必做的检查，一眼看出哪列缺失多少：

```
姓名    0
部门    1
薪资    1
年龄    0
dtype: int64
```

为什么 `.sum()` 能数出个数？因为 `True` 在计算时当作 1、`False` 当作 0，把一列 True/False 加起来，就是 True 的个数。

> **不能用 `== np.nan` 判断缺失**：`np.nan == np.nan` 的结果是 `False`（规定“缺失值不等于任何值，包括它自己”），所以 `df[df["薪资"] == np.nan]` 永远筛不出东西。判断缺失一律用 `isnull()`（或同义的 `isna()`），例如 `df[df["薪资"].isnull()]`。

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

> 和第 20 章一样，`dropna()`、`fillna()` 都**返回新的数据**，不会修改原表。所以上面写的是 `df["薪资"] = df["薪资"].fillna(...)`；删除缺失行要写 `df = df.dropna()`。

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

# 字符串转数字（含错误处理）：无法转换的会变成 NaN
s = pd.Series(["12000", "1.5万", "13000"])
print(pd.to_numeric(s, errors="coerce"))
# 0    12000.0
# 1        NaN     ← "1.5万" 转不了，变成缺失值，之后可以再单独处理
# 2    13000.0
```

> 含有 `NaN` 的列不能直接 `astype(int)`，会报 `IntCastingNaNError: Cannot convert non-finite values (NA or inf) to integer`。先处理缺失（`fillna` 或 `dropna`），再转换类型。

---

## 21.6 apply 与 map：自定义变换

### map：对 Series 逐元素变换

```python
# 用字典做映射（字典里没写到的值会变成 NaN，所以要把所有可能的值都列全）
df["部门编码"] = df["部门"].map({"技术": 1, "销售": 2, "未知": 0})

# 用函数变换（需先运行 §21.3 填充薪资缺失值，否则 NaN 会被归为"普通"）
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

统计某列每个值出现的次数，做类别分析必备（需先运行 §21.3 的填充代码，`部门` 列才有"未知"）：

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

以“求每个部门的平均薪资”为例：

```
   原始数据            ① 拆分（按部门）          ② 应用（求均值）    ③ 合并
 部门  薪资
 技术  15000        技术组：15000, 20000, 18000  →  17666.67         部门  薪资
 销售  12000   →                                                   技术  17666.67
 技术  20000        销售组：12000, 13000         →  12500.00         销售  12500.00
 销售  13000
 技术  18000
```

在 Excel 里，这相当于“数据透视表”。

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

把中文需求翻译成代码的方法：“**按 A** 分组，求 **B** 的 **C**” → `df.groupby("A")["B"].C()`。

如果想对**不同的列**做**不同的统计**，并给结果列起名字，可以用“命名聚合”：

```python
print(sales.groupby("部门").agg(
    平均薪资=("薪资", "mean"),     # 新列名=("原列名", "统计方法")
    人数=("姓名", "count"),
))
#             平均薪资  人数
# 部门
# 技术  17666.666667   3
# 销售  12500.000000   2
```

> 分组结果的**行索引是分组的值**（上面的“技术”“销售”）。想把它变回普通的一列、得到一张常规表格，在末尾加 `.reset_index()`：`sales.groupby("部门")["薪资"].mean().reset_index()`。

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

## 新手常见错误

### ❶ 用 `== np.nan` 找缺失值

```python
print(df[df["薪资"] == np.nan])     # Empty DataFrame，什么也没找到
```

**原因**：`NaN` 不等于任何值，包括它自己。这个错误**不会报错**。
**改法**：`df[df["薪资"].isnull()]`。

### ❷ 对含缺失值的列转整数

```python
df["薪资"].astype(int)
```

```
IntCastingNaNError: Cannot convert non-finite values (NA or inf) to integer
```

**原因**：整数类型里没有办法表示 `NaN`（`non-finite values` = 非有限值，包括 NaN 和无穷大）。
**改法**：先 `fillna(...)` 或 `dropna()`，再 `astype(int)`。

### ❸ 文本格式的数字无法转换

```python
pd.Series(["12,000"]).astype(int)
```

```
ValueError: invalid literal for int() with base 10: '12,000'
```

**原因**：千分位逗号、单位（“元”“万”）、空格等字符让字符串无法直接转成数字。
**改法**：先用 `.str.replace(",", "")` 等方法清理文本，再转换；或用 `pd.to_numeric(s, errors="coerce")` 把转不了的变成 `NaN`，再单独排查。

### ❹ 对整张表 `groupby` 后直接求均值

```python
sales.groupby("部门").mean()
```

```
TypeError: agg function failed [how->mean,dtype->object]
```

（pandas 3.x 中显示为 `TypeError: dtype 'str' does not support operation 'mean'`。）

**原因**：表里还有“姓名”这样的文本列，文本没法求平均。
**改法**：明确指定要统计的列：`sales.groupby("部门")["薪资"].mean()`；或者加参数 `numeric_only=True` 只统计数字列。

### ❺ `merge` 时两张表的键名不一致

```python
pd.merge(students, scores, on="学号")   # scores 里这一列其实叫 "ID"
```

```
KeyError: '学号'
```

**原因**：`on="学号"` 要求两张表里**都有**名为“学号”的列。
**改法**：先 `print(df.columns)` 核对；列名不同时用 `pd.merge(students, scores, left_on="学号", right_on="ID")`。

---

## 本章小结

- 缺失值：`isnull().sum()` 检测；`dropna()` 删除、`fillna()` 填充（可用均值/固定值）；判断缺失不能用 `== np.nan`。
- 重复值：`duplicated()` / `drop_duplicates()`；类型转换 `astype`。
- 自定义变换：`map`（Series 逐元素/字典映射）、`apply`（更通用，可 `axis=1` 按行）。
- 文本列用 `.str.xxx()` 批量处理字符串。
- `value_counts()` 统计频数，`nunique`/`unique` 看类别。
- **`groupby(列)[目标].聚合()`** 分组聚合，`agg` 一次多指标；命名聚合 `agg(新名=("列", "方法"))`；`reset_index()` 把分组结果变回普通表格。
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

## 解题提示

<details>
<summary>💡 卡住了？先看提示（只给思路，不给答案）</summary>

- **第 1 题**：统计缺失用 `isnull().sum()`；填充用 `fillna()`，填充值是 `df["销量"].mean()`。别忘了把结果赋值回 `df["销量"]`。
- **第 2 题**：“每个值出现几次”用 `value_counts()`。
- **第 3 题**：套用公式“按 A 分组，求 B 的 C”：A = 城市，B = 利润，C = sum。
- **第 4 题**：对两列做不同的统计，用 21.9 节的“命名聚合”：`agg(新列名=("原列名", "方法"), ...)`。
- **第 5 题**：先用两列相除创建“利润率”列，再“按城市分组，求利润率的平均值”。注意要先做第 1 题填好缺失值，否则有一行利润率是 `NaN`。

</details>

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
