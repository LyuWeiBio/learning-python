# 第 22 章：Matplotlib 数据可视化

> **所属部分**：第三部分 · 数据分析基础
> **预计学习时间**：45 分钟
> **前置知识**：第 19–21 章；已安装 matplotlib
> **配套代码**：[`代码示例/ch22_Matplotlib数据可视化.py`](../代码示例/ch22_Matplotlib数据可视化.py)

## 本章学习目标

- 会用 Matplotlib 绘制折线图、柱状图、散点图、直方图、饼图。
- 会给图表添加标题、坐标轴标签、图例。
- 解决中文显示为方框的问题。
- 会绘制多子图，会把图表保存为图片。
- 会用 Pandas 直接画图。

---

## 22.1 Matplotlib 简介

**Matplotlib** 是 Python 最基础、最经典的绘图库。“一图胜千言”，可视化能帮我们快速发现数据中的规律、异常和趋势。核心接口是 `pyplot`，约定别名 `plt`：

```python
import matplotlib.pyplot as plt
import numpy as np
```

### 先想清楚：该用哪种图？

| 你想看什么 | 用什么图 | 例子 |
| --- | --- | --- |
| 随时间的**变化趋势** | 折线图 `plot` | 每月销售额 |
| 几个类别**谁大谁小** | 柱状图 `bar` | 各城市销量 |
| 两个数值之间**有没有关系** | 散点图 `scatter` | 身高与体重 |
| 一组数据**怎么分布** | 直方图 `hist` / 箱线图 `boxplot` | 成绩分布 |
| 各部分**占整体的比例** | 饼图 `pie` | 部门人数占比 |

选错图型是新手最常见的“隐性错误”：比如用折线图连接几个没有先后顺序的类别，读者会误以为它们之间有趋势。

### 解决中文乱码（重要！）

Matplotlib 默认不支持中文，直接写中文标题会显示成方框 `□□□`。在画图前加上下面的配置：

```python
import matplotlib.pyplot as plt

# 根据你的系统选择一个存在的中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]        # Windows 常用黑体
# plt.rcParams["font.sans-serif"] = ["PingFang SC"] # macOS
# plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei"]  # 部分 Linux
plt.rcParams["axes.unicode_minus"] = False           # 正常显示负号
```

**更省心的写法**：一次给出多个候选字体，Matplotlib 会按顺序使用第一个能找到的，同一份代码在不同系统上都能工作：

```python
plt.rcParams["font.sans-serif"] = [
    "SimHei", "Microsoft YaHei",            # Windows
    "PingFang SC", "Heiti TC", "Arial Unicode MS",   # macOS
    "WenQuanYi Zen Hei", "Noto Sans CJK SC",         # Linux
]
plt.rcParams["axes.unicode_minus"] = False
```

**不知道自己电脑上有哪些中文字体？** 运行下面的代码列出来，再把其中一个名字填进上面的列表：

```python
from matplotlib import font_manager

names = sorted({f.name for f in font_manager.fontManager.ttflist})
keywords = ["Hei", "Song", "Kai", "YaHei", "PingFang", "CJK", "WenQuanYi", "Arial Unicode"]
print([n for n in names if any(k in n for k in keywords)])
```

设置了不存在的字体时，终端里会出现类似 `findfont: ... none of the following families were found: SimHei` 的提示；中文仍显示为方框时，会出现 `UserWarning: Glyph 19978 (\N{CJK UNIFIED IDEOGRAPH-4E0A}) missing from font(s) DejaVu Sans`（字体里缺少这个汉字）。看到它们，就说明字体没配好。

> 如果系统没有中文字体导致仍然乱码，最简单的办法是**图表文字全部用英文**。本章示例为通用起见混合使用，你可按需替换。

---

## 22.2 折线图：观察趋势

```python
import matplotlib.pyplot as plt

months = [1, 2, 3, 4, 5, 6]
sales = [120, 135, 128, 160, 175, 190]

plt.plot(months, sales)
plt.title("上半年销售趋势")
plt.xlabel("月份")
plt.ylabel("销售额（万元）")
plt.show()          # 显示图表（在脚本中）
```

`plt.show()` 会弹出图表窗口。在 Jupyter Notebook 里图表会直接内嵌显示。

> **运行到 `plt.show()` 程序“卡住”了？** 这是正常的：弹出图表窗口后，程序会停在这一行等你看图，**关闭图表窗口后**才会继续执行后面的代码。一个脚本里有多个 `plt.show()`，就会依次弹出多个窗口。

画图的基本套路永远是这几步：

1. 准备数据（x 和 y 的**长度必须相同**）；
2. 调用画图函数，如 `plt.plot(x, y)`；
3. 添加标题、坐标轴标签、图例等装饰；
4. `plt.show()` 显示，或 `plt.savefig()` 保存。

美化与多条线：

```python
plt.plot(months, sales, color="blue", marker="o", linestyle="-", label="2023")
plt.plot(months, [100, 120, 130, 140, 150, 165], color="red", marker="s", label="2022")
plt.legend()        # 显示图例（需要每条线有 label）
plt.grid(True)      # 显示网格
plt.show()
```

常用参数：`color`（颜色）、`marker`（数据点标记 `o s ^ *`）、`linestyle`（线型 `- -- : -.`）。

---

## 22.3 柱状图：比较大小

```python
categories = ["苹果", "香蕉", "橙子", "葡萄"]
counts = [45, 30, 25, 18]

plt.bar(categories, counts, color="skyblue")
plt.title("各水果销量")
plt.ylabel("销量")
plt.show()

# 横向柱状图用 barh
plt.barh(categories, counts)
plt.show()
```

---

## 22.4 散点图：观察两个变量的关系

散点图用于展示两个数值变量之间是否相关，是机器学习中探索特征关系的常用工具：

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
height = np.random.normal(170, 8, 50)      # 50 个身高
weight = height * 0.5 - 20 + np.random.normal(0, 3, 50)  # 与身高正相关的体重

plt.scatter(height, weight, alpha=0.6)     # alpha 是透明度
plt.title("身高与体重关系")
plt.xlabel("身高 (cm)")
plt.ylabel("体重 (kg)")
plt.show()
```

---

## 22.5 直方图：观察数据分布

直方图把数据分成若干区间（bin），统计每个区间的频数，用来看数据的分布形态：

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)
scores = np.random.normal(75, 10, 200)     # 200 个成绩，均值75、标准差10

plt.hist(scores, bins=20, color="orange", edgecolor="black")
plt.title("成绩分布直方图")
plt.xlabel("分数")
plt.ylabel("人数")
plt.show()
```

`bins` 控制分成多少个区间，影响直方图的粗细。

---

## 22.6 饼图：观察占比

```python
labels = ["技术", "销售", "运营", "行政"]
sizes = [40, 30, 20, 10]

plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
plt.title("部门人数占比")
plt.axis("equal")     # 让饼图是正圆
plt.show()
```

`autopct="%1.1f%%"` 会在每块上显示百分比。

---

## 22.7 多子图：一张画布多个图

用 `plt.subplots()` 在一个画布上排布多个图表：

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))   # 1行2列

axes[0].plot([1, 2, 3], [4, 5, 6])
axes[0].set_title("折线图")

axes[1].bar(["A", "B", "C"], [3, 7, 5])
axes[1].set_title("柱状图")

plt.tight_layout()    # 自动调整间距，避免重叠
plt.show()
```

`fig` 是**整张画布**，`axes` 是画布上的**一个个小图**（坐标系）。`plt.subplots(1, 2)` 得到的 `axes` 是一个装着 2 个小图的数组，用 `axes[0]`、`axes[1]` 分别取出来画。

注意：用面向对象接口（`axes[0]`）时，设置标题/标签的方法名带 `set_` 前缀，如 `set_title`、`set_xlabel`。这是更专业、更灵活的写法。

| `plt.xxx()` 写法 | 对应的 `ax.xxx()` 写法 |
| --- | --- |
| `plt.title("标题")` | `ax.set_title("标题")` |
| `plt.xlabel("x")` | `ax.set_xlabel("x")` |
| `plt.ylabel("y")` | `ax.set_ylabel("y")` |
| `plt.plot(...)`、`plt.bar(...)` | `ax.plot(...)`、`ax.bar(...)`（画图函数同名） |

> 子图的取法和布局有关：`plt.subplots(2, 2)` 得到的是 2×2 的二维数组，要用 `axes[0, 1]`（第 0 行第 1 列）这样的写法；`plt.subplots()`（不写行列，只有一个图）得到的 `ax` 就是单个小图，**不能**再写 `ax[0]`。

---

## 22.8 保存图表

在没有图形界面的环境（如服务器）或想把图存成文件时，用 `savefig`：

```python
plt.plot([1, 2, 3], [1, 4, 9])
plt.title("示例")
plt.savefig("chart.png", dpi=150, bbox_inches="tight")   # 保存为图片
# plt.savefig("chart.pdf")   # 也能存成 PDF/SVG 等
plt.close()           # 关闭图，释放内存
```

> `savefig` 要在 `show()` **之前**调用（`show` 之后画布可能被清空）。`bbox_inches="tight"` 能裁掉多余白边。

---

## 22.9 用 Pandas 直接画图

Pandas 的 DataFrame/Series 内置了 `.plot()`，底层就是 Matplotlib，画常见图非常快：

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "月份": [1, 2, 3, 4, 5],
    "销量": [100, 120, 90, 140, 160],
    "成本": [60, 70, 55, 80, 90],
})

df.plot(x="月份", y=["销量", "成本"], marker="o")   # 折线图
plt.title("销量与成本")
plt.show()

df.plot(x="月份", y="销量", kind="bar")             # 柱状图（kind 指定类型）
plt.show()

df["销量"].plot(kind="hist")                        # 直方图
plt.show()
```

`kind` 可选：`line`（默认）、`bar`、`barh`、`hist`、`box`、`scatter`、`pie` 等。做探索性分析时，`df.plot()` 是快速出图的利器。

---

## 新手常见错误

### ❶ 中文显示成方框

```
UserWarning: Glyph 19978 (\N{CJK UNIFIED IDEOGRAPH-4E0A}) missing from font(s) DejaVu Sans.
```

**原因**：默认字体里没有汉字。
**改法**：按 22.1 节设置 `font.sans-serif`；先用字体列表代码确认电脑上有哪些中文字体。

### ❷ x 和 y 长度不一致

```python
plt.plot([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5])
```

```
ValueError: x and y must have same first dimension, but have shapes (6,) and (5,)
```

**原因**：6 个 x 值配 5 个 y 值，有一个点没法画（`same first dimension` = 第一个维度要相同）。
**改法**：检查两组数据，用 `len()` 确认长度一致。

### ❸ 保存的图片是一片空白

```python
plt.plot([1, 2, 3], [1, 4, 9])
plt.show()
plt.savefig("chart.png")     # 得到一张空白图
```

**原因**：`show()` 关闭窗口后，当前画布已被清空，`savefig` 保存的是一张新的空画布。这个错误**不会报错**。
**改法**：**先 `savefig`，再 `show`**。

### ❹ 子图的取法不对

```python
fig, ax = plt.subplots()          # 只有一个图
ax[0].plot([1], [1])

fig, axes = plt.subplots(2, 2)    # 2 行 2 列
axes[0].plot([1], [1])
```

```
TypeError: 'Axes' object is not subscriptable
AttributeError: 'numpy.ndarray' object has no attribute 'plot'
```

**原因**：只有一个子图时，`ax` 本身就是那个小图，不能再用 `[0]` 取；2×2 布局时，`axes[0]` 取到的是**第一整行**（一个装着 2 个小图的数组），还不是单个小图。
**改法**：单图直接 `ax.plot(...)`；2×2 用 `axes[0, 0].plot(...)`。

### ❺ 在子图上用了 `plt` 的方法名

```python
axes[0].title("折线图")
```

```
TypeError: 'Text' object is not callable
```

**原因**：在 `ax` 对象上，`title` 是一个属性而不是方法，设置标题的方法叫 `set_title`。
**改法**：`axes[0].set_title("折线图")`，对照 22.7 节的对照表。

---

## 本章小结

- `import matplotlib.pyplot as plt`；中文需设 `font.sans-serif` 和 `axes.unicode_minus=False`。
- 图表类型：`plot`（折线）、`bar/barh`（柱状）、`scatter`（散点）、`hist`（直方）、`pie`（饼图）。
- 装饰：`title/xlabel/ylabel/legend/grid`；线条 `color/marker/linestyle`。
- 选图：趋势用折线、比较用柱状、关系用散点、分布用直方、占比用饼图。
- 多子图：`fig, axes = plt.subplots(行, 列)`，用 `axes[i].set_xxx()` 设置；2×2 布局用 `axes[行, 列]`。
- `savefig("x.png", dpi=150, bbox_inches="tight")` 保存图片（在 show 之前）。
- Pandas `.plot(kind=...)` 一行出图，适合快速探索。

---

## 练习题

1. **折线图**：给定某商品一周 7 天的价格 `[10, 12, 11, 13, 15, 14, 16]`，画出价格随天数变化的折线图，加标题和坐标轴标签。
2. **柱状图**：给定 4 个班级的平均分 `{"一班":85,"二班":78,"三班":92,"四班":80}`，画柱状图比较。
3. **直方图**：用 `np.random.normal(60, 15, 500)` 生成 500 个数据，画直方图（分 30 组）观察其分布。
4. **散点图**：生成两个相关的变量并画散点图，观察它们是否呈线性关系。
5. **多子图 + 保存**：在一张画布上并排画一个折线图和一个柱状图，然后用 `savefig` 保存为 `result.png`。

---

## 解题提示

<details>
<summary>💡 卡住了？先看提示（只给思路，不给答案）</summary>

- **第 1 题**：x 是天数 1~7（`list(range(1, 8))`），y 是价格；套用“准备数据 → `plt.plot` → 装饰 → `plt.show()`”四步。
- **第 2 题**：`plt.bar` 需要两组数据：类别名和数值。字典的 `.keys()` 和 `.values()` 正好分别对应。
- **第 3 题**：`plt.hist(数据, bins=30)`；加上 `edgecolor="black"` 能看清每根柱子的边界。
- **第 4 题**：参考 22.4 节：先随机生成 x，再让 y = 某个倍数 × x + 一点随机噪声，这样两者就“相关”了。
- **第 5 题**：参考 22.7 节的 `plt.subplots(1, 2)`；记住 `savefig` 要写在 `show` 之前。

</details>

---

## 参考答案

<details>
<summary>点击展开查看参考答案</summary>

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "PingFang SC", "WenQuanYi Zen Hei"]   # 按你的系统调整
plt.rcParams["axes.unicode_minus"] = False

# 第 1 题
days = list(range(1, 8))
prices = [10, 12, 11, 13, 15, 14, 16]
plt.plot(days, prices, marker="o")
plt.title("一周价格走势")
plt.xlabel("天")
plt.ylabel("价格")
plt.show()

# 第 2 题
data = {"一班": 85, "二班": 78, "三班": 92, "四班": 80}
plt.bar(data.keys(), data.values(), color="skyblue")
plt.title("各班平均分")
plt.show()

# 第 3 题
vals = np.random.normal(60, 15, 500)
plt.hist(vals, bins=30, edgecolor="black")
plt.title("数据分布")
plt.show()

# 第 4 题
x = np.random.rand(100)
y = 2 * x + np.random.normal(0, 0.1, 100)
plt.scatter(x, y, alpha=0.6)
plt.title("x 与 y 的关系")
plt.show()

# 第 5 题
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot([1, 2, 3], [1, 4, 9], marker="o")
axes[0].set_title("折线图")
axes[1].bar(["A", "B", "C"], [5, 3, 7])
axes[1].set_title("柱状图")
plt.tight_layout()
plt.savefig("result.png", dpi=150, bbox_inches="tight")
plt.show()
```

</details>

---

⬅️ 上一章：[第 21 章 · Pandas 数据清洗与聚合](21-Pandas数据清洗与聚合.md)
➡️ 下一章：[第 23 章 · 探索性数据分析（EDA）实战](23-探索性数据分析实战.md)
