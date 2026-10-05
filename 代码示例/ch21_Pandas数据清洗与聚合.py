# -*- coding: utf-8 -*-
"""
第 21 章：Pandas 数据清洗与聚合
对应教材：第三部分-数据分析基础/21-Pandas数据清洗与聚合.md

演示：缺失值检测与处理、重复值、类型转换、apply/map、
      .str 文本处理、value_counts、groupby 分组聚合、
      concat 与 merge 合并表格。
"""

import pandas as pd
import numpy as np


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


# 21.1 准备示例数据（故意混入缺失值）
df = pd.DataFrame({
    "姓名": ["小明", "小红", "小刚", "小丽", "小明"],
    "部门": ["技术", "销售", "技术", None, "销售"],
    "薪资": [15000, 12000, np.nan, 18000, 15000],
    "年龄": [25, 30, 28, 35, 25],
})
print(df)

section("1. 检测缺失值")

print(df.isnull())                  # 每个位置是否为缺失
print(df.isnull().sum())            # 每列缺失个数（最常用！）
print("总缺失数：", df.isnull().sum().sum())

section("2. 处理缺失值：删除 vs 填充")

print(df.dropna())                  # 删除任何含缺失值的行
print(df.dropna(subset=["薪资"]))   # 只在"薪资"缺失时删除该行

# 填充：缺失很少可删；能合理估计时宜填充
df["薪资"] = df["薪资"].fillna(df["薪资"].mean())   # 数值列用均值填充
df["部门"] = df["部门"].fillna("未知")              # 分类列用固定类别填充
print(df)

section("3. 处理重复值与类型转换")

print(df.duplicated())                    # 每行是否与之前重复
print("重复行数：", df.duplicated().sum())
print(df.drop_duplicates(subset=["姓名"]))  # 按"姓名"去重，保留第一次

print(df.dtypes)
df["年龄"] = df["年龄"].astype(int)       # 转换类型
print(df.dtypes)

section("4. apply 与 map：自定义变换")

# map：对 Series 逐元素变换（字典映射）
df["部门编码"] = df["部门"].map({"技术": 1, "销售": 2, "未知": 0})
# map + 函数：薪资档次（需先填充缺失，否则 NaN 会被归为"普通"）
df["薪资档次"] = df["薪资"].map(lambda x: "高" if x >= 15000 else "普通")

# apply：更通用；axis=1 按行计算，可访问整行数据
df["年龄段"] = df["年龄"].apply(lambda x: "青年" if x < 30 else "中年")
df["描述"] = df.apply(lambda row: f"{row['姓名']}-{row['部门']}", axis=1)
print(df)

section("5. 字符串处理：.str")

s = pd.Series(["  Alice ", "BOB", "charlie"])
print(s.str.strip())        # 去空格
print(s.str.lower())        # 转小写
print(s.str.len())          # 每个字符串长度
print(s.str.contains("a"))  # 是否包含 "a"
print(s.str.replace("o", "0"))

section("6. value_counts：统计频数")

print(df["部门"].value_counts())
print(df["部门"].value_counts(normalize=True))  # 换成占比
print(df["部门"].nunique())      # 有几种不同的值
print(df["部门"].unique())       # 列出所有不同的值

section("7. 分组聚合：groupby（本章重点）")

sales = pd.DataFrame({
    "部门": ["技术", "销售", "技术", "销售", "技术"],
    "姓名": ["A", "B", "C", "D", "E"],
    "薪资": [15000, 12000, 20000, 13000, 18000],
})

# 拆分-应用-合并：按部门分组，求每组的平均薪资
print(sales.groupby("部门")["薪资"].mean().round(2))
print(sales.groupby("部门").size())                              # 每组人数
print(sales.groupby("部门")["薪资"].agg(["mean", "max", "min", "count"]))

section("8. 合并表格")

df_a = pd.DataFrame({"名字": ["A", "B"], "分数": [80, 90]})
df_b = pd.DataFrame({"名字": ["C", "D"], "分数": [70, 85]})
print(pd.concat([df_a, df_b], ignore_index=True))   # 上下拼接

students = pd.DataFrame({"学号": [1, 2, 3], "姓名": ["小明", "小红", "小刚"]})
scores = pd.DataFrame({"学号": [1, 2, 3], "成绩": [88, 92, 79]})
print(pd.merge(students, scores, on="学号"))        # 按键关联（类似 SQL JOIN）

# md 练习题：销售数据综合清洗聚合
df = pd.DataFrame({
    "城市": ["北京", "上海", "北京", "广州", "上海", "北京"],
    "类别": ["电子", "服装", "电子", "食品", "电子", "服装"],
    "销量": [120, 85, np.nan, 60, 95, 70],
    "利润": [30, 20, 25, 15, 22, 18],
})
print(df.isnull().sum())                    # 第 1 题：统计缺失
df["销量"] = df["销量"].fillna(df["销量"].mean())   # 用均值填充
print(df["城市"].value_counts())            # 第 2 题：城市频数
print(df.groupby("城市")["利润"].sum())     # 第 3 题：按城市求总利润
print(df.groupby("类别").agg(销量均值=("销量", "mean"),
                             利润总和=("利润", "sum")))   # 第 4 题
df["利润率"] = df["利润"] / df["销量"]      # 第 5 题
print(df.groupby("城市")["利润率"].mean())

print("\n第 21 章演示完毕 ✅")
