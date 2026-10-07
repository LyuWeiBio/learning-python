# 第 20 章：Pandas 数据结构与操作

> **所属部分**：第三部分 · 数据分析基础
> **预计学习时间**：45 分钟
> **前置知识**：第 19 章（NumPy）；已安装 pandas
> **配套代码**：[`代码示例/ch20_Pandas数据结构.py`](../代码示例/ch20_Pandas数据结构.py)

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

用过 Excel 的话，可以这样对照：

| Excel | Pandas |
| --- | --- |
| 一张工作表 | `DataFrame` |
| 一列数据 | `Series` |
| 第一行的列标题 | `df.columns`（列名） |
| 最左边的行号 | `df.index`（行索引） |
| 筛选 / 排序按钮 | `df[条件]` / `df.sort_values()` |
| 数据透视表 | `groupby` / `pivot_table`（第 21 章） |

> **在 `.py` 脚本里要 `print` 才能看到结果**。如果用的是 Jupyter Notebook，单元格最后一行的表达式会自动显示（而且是更好看的表格），不用写 `print`。本章代码为了在两种环境里都能用，统一写了 `print`。

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

真实数据通常来自文件。Pandas 读取 CSV 极其简单（下面的 `data.csv` 请换成你自己的数据文件）：

```python
# 读取 CSV（最常用）
df = pd.read_csv("data.csv")

# 读取 Excel（需额外安装 openpyxl）
# df = pd.read_excel("data.xlsx")

# 保存
df.to_csv("output.csv", index=False)   # index=False 不保存行索引
```

Pandas 还能读 JSON、SQL、剪贴板等各种来源，`read_csv` 是最常打交道的。

> **中文 CSV 的编码问题**（和第 12 章是同一个问题）：
>
> - `read_csv` 默认按 `utf-8` 读取。如果报 `UnicodeDecodeError: 'utf-8' codec can't decode byte ...`，说明文件多半是 `gbk` 编码（常见于 Excel 另存的 CSV），改成 `pd.read_csv("data.csv", encoding="gbk")`。
> - 保存的 CSV 要给 Excel 打开时，用 `df.to_csv("output.csv", index=False, encoding="utf-8-sig")`，否则中文会乱码。
> - 报 `FileNotFoundError` 时，回顾第 12 章的“当前工作目录”。

---

## 20.5 查看数据

拿到数据第一件事就是“看看它长什么样”：

```python
print(df.head())        # 前 5 行（可传数字，如 head(3)）
print(df.tail(2))       # 后 2 行
print(df.shape)         # (4, 4)  4 行 4 列
print(df.columns)       # 所有列名
print(df.dtypes)        # 每列的数据类型
df.info()               # 综合信息：行数、列名、类型、非空数量（它自己会打印，不用再套 print）
print(df.describe())    # 数值列的统计摘要：count/mean/std/min/max/分位数
```

> `info()` 会直接把信息打印出来，返回值是 `None`。如果写成 `print(df.info())`，末尾会多出一行 `None`，不是出错了。

`df.info()` 的输出长这样：

```
RangeIndex: 4 entries, 0 to 3
Data columns (total 4 columns):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   姓名      4 non-null      object
 1   年龄      4 non-null      int64
 2   城市      4 non-null      object
 3   成绩      4 non-null      int64
dtypes: int64(2), object(2)
```

重点看三处：**一共多少行**（`4 entries`）、**每列有多少个非空值**（`Non-Null Count`，比总行数少就说明有缺失值）、**每列的类型**（`Dtype`：`int64` 整数、`float64` 小数、`object` 文本——pandas 3.x 中文本列显示为 `str`）。如果一列本该是数字却显示为 `object`/`str`，说明里面混进了文字，计算前需要清洗（第 21 章）。

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

> 列名必须**一字不差**：多一个空格（`"成绩 "`）、中英文括号不同都会报 `KeyError`。拿不准时先 `print(df.columns)` 看看真实的列名。

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

上面的例子里，行索引恰好是 `0, 1, 2, 3`，所以 `loc[0]` 和 `iloc[0]` 看起来一样。一旦**排序或筛选**之后，两者就不同了：

```python
df2 = df.sort_values("成绩", ascending=False)
print(df2)
#    姓名  年龄  城市  成绩
# 3  小丽  21  深圳  95
# 1  小红  20  上海  92
# 0  小明  18  北京  88
# 2  小刚  19  广州  79

print(df2.loc[0, "姓名"])       # 小明 ← 行标签是 0 的那一行
print(df2.iloc[0]["姓名"])      # 小丽 ← 当前排在第 0 位的那一行
```

**记法**：`iloc` 的 `i` 代表 integer position（整数位置）——“第几行”；`loc` 看的是最左边那一列**行标签**——“叫什么名字的行”。

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

> 想**修改满足条件的那几行**的某一列，要用 `df.loc[条件, "列名"] = 新值`，例如把所有 90 分以上的“班级”改成“尖子班”：
>
> ```python
> df.loc[df["成绩"] >= 90, "班级"] = "尖子班"
> ```
>
> 不要写成 `df[df["成绩"] >= 90]["班级"] = "尖子班"`（两组方括号连写），那样改的只是一份临时副本，原表不会变（见本章“新手常见错误”）。

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

> `sort_values`、`drop` 等大多数方法都**返回一个新的 DataFrame**，不会修改原来的 `df`。想保留结果，要赋值：`df = df.sort_values("成绩")`。（和第 04 章字符串方法的道理一样。）

---

## 新手常见错误

### ❶ 选多列时少了一层方括号

```python
print(df["姓名", "成绩"])
```

```
KeyError: ('姓名', '成绩')
```

**原因**：`df["姓名", "成绩"]` 被理解成“找一个名字叫 `('姓名', '成绩')` 的列”。
**改法**：`df[["姓名", "成绩"]]`——外层方括号表示“选列”，内层方括号是列名列表。

### ❷ 列名写得不完全一致

```python
print(df["成绩 "])        # 多了一个空格
```

```
KeyError: '成绩 '
```

**原因**：`KeyError` 后面显示的就是找不到的列名。从 Excel 导出的数据，列名里常常藏着空格。
**改法**：`print(df.columns)` 查看真实列名；可以统一去掉列名两端的空格：`df.columns = df.columns.str.strip()`。

### ❸ 多条件筛选用了 `and` / `or`

```python
print(df[df["成绩"] > 85 and df["年龄"] < 21])
```

```
ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
```

**原因**：和第 19 章 NumPy 一样，`and` 不能用在一整列 True/False 上。
**改法**：`df[(df["成绩"] > 85) & (df["年龄"] < 21)]`。

### ❹ `loc` 和 `iloc` 用混了

```python
df.loc[0:2, 0]            # loc 里写了列的位置 0
df.iloc[0, "姓名"]        # iloc 里写了列名
```

```
KeyError: 0
ValueError: Location based indexing can only have [integer, integer slice ...] types
```

**原因**：`loc` 只认**标签**（列名），`iloc` 只认**位置**（整数）。
**改法**：`df.loc[0:2, "姓名"]` 或 `df.iloc[0:3, 0]`。

### ❺ 连写两组方括号来修改数据（不报错，但没改成功）

```python
df[df["成绩"] > 85]["成绩"] = 100
print(df)                  # 成绩一个都没变！
```

**原因**：`df[条件]` 先生成了一份副本，再对副本的“成绩”列赋值，原表 `df` 不受影响。根据 pandas 版本不同，可能毫无提示，也可能出现 `ChainedAssignmentError` 或 `SettingWithCopyWarning` 警告——**看到这类警告，就是在提醒你改用 `.loc`**。
**改法**：一步到位：`df.loc[df["成绩"] > 85, "成绩"] = 100`。

### ❻ 调用了方法却没保存结果

```python
df.sort_values("成绩")
print(df)                  # 顺序没变
```

**原因**：`sort_values` 返回排好序的新表，原表没变。这个错误**不会报错**。
**改法**：`df = df.sort_values("成绩")`。

---

## 本章小结

- Pandas 处理**带标签的表格数据**；`Series`（一列）、`DataFrame`（整张表）。
- 用字典创建 DataFrame；`pd.read_csv` 读取、`to_csv(index=False)` 保存。
- 查看：`head/tail/shape/columns/dtypes/info/describe`。
- 选列：`df["列"]`（一列）、`df[["列1","列2"]]`（多列）。
- 选行：`iloc` 按位置（含头不含尾）、`loc` 按标签（切片含尾）。
- 条件筛选：`df[df["列"] > x]`，多条件用 `&`/`|` 并加括号。
- 新增列 `df["新列"] = ...`；按条件改值用 `df.loc[条件, "列"] = 值`；`sort_values` 排序。
- 大多数方法返回新表，要保留结果就重新赋值：`df = df.sort_values(...)`。

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

## 解题提示

<details>
<summary>💡 卡住了？先看提示（只给思路，不给答案）</summary>

- **第 1 题**：形状用 `.shape`（属性，不加括号），前 3 行用 `.head(3)`，统计摘要用 `.describe()`。
- **第 2 题**：两列直接相乘，会自动逐行计算；新列用 `df["总价"] = ...` 创建。
- **第 3 题**：分两步：先 `df[df["单价"] > 5]` 筛出行，再接 `[["商品", "单价"]]` 选列（注意双层方括号）。也可以一步写成 `df.loc[df["单价"] > 5, ["商品", "单价"]]`。
- **第 4 题**：两个条件分别写成 `(df["产地"] == "海南")` 和 `(df["数量"] > 10)`，中间用 `&` 连接，**每个条件都加括号**。
- **第 5 题**：`sort_values` 的第一个参数是列名；从高到低需要 `ascending=False`。注意要先做完第 2 题，才有“总价”这一列。

</details>

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
