# -*- coding: utf-8 -*-
"""
第 20 章：Pandas 数据结构与操作
对应教材：第三部分-数据分析基础/20-Pandas数据结构与操作.md

演示：Series 与 DataFrame、CSV 读写（在 output/ 下）、
      查看数据、选列、loc/iloc 选行、条件筛选、新增列、排序。
"""

import pandas as pd
import numpy as np
from pathlib import Path

WORK = Path(__file__).parent / "output"
WORK.mkdir(parents=True, exist_ok=True)


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. Series：带标签的一维数据")

s = pd.Series([10, 20, 30, 40])
print(s)              # 左边是索引（index），右边是值

s = pd.Series([85, 92, 78], index=["语文", "数学", "英语"])
print(s["数学"])      # 92，用标签取值
print(s.mean())       # Series 也支持各种统计

section("2. DataFrame：二维表格")

data = {
    "姓名": ["小明", "小红", "小刚", "小丽"],
    "年龄": [18, 20, 19, 21],
    "城市": ["北京", "上海", "广州", "深圳"],
    "成绩": [88, 92, 79, 95],
}
df = pd.DataFrame(data)     # 字典创建：键是列名，值是该列数据
print(df)

section("3. 读写文件")

df.to_csv(WORK / "students.csv", index=False)   # index=False 不保存行索引
df2 = pd.read_csv(WORK / "students.csv")        # 读回
print("读回后形状：", df2.shape)

section("4. 查看数据")

print(df.head())        # 前 5 行
print(df.tail(2))       # 后 2 行
print(df.shape)         # (4, 4)  4 行 4 列
print(df.columns)       # 所有列名
print(df.dtypes)        # 每列的数据类型
print(df.info())        # 综合信息：行数、列名、类型、非空数量
print(df.describe())    # 数值列统计摘要：count/mean/std/min/max/分位数

section("5. 选择列")

print(df["姓名"])              # 选一列 → Series
print(df[["姓名", "成绩"]])    # 选多列 → 双层方括号，返回 DataFrame

section("6. 选择行：loc 与 iloc")

# iloc：按位置（含头不含尾，和列表一样）
print(df.iloc[0])           # 第 0 行
print(df.iloc[0:2])         # 第 0~1 行
print(df.iloc[0, 1])        # 第 0 行第 1 列：18
print(df.iloc[:, 0])        # 所有行的第 0 列

# loc：按标签（切片含尾！）
print(df.loc[0])            # 索引标签为 0 的行
print(df.loc[0, "姓名"])    # 小明
print(df.loc[0:2, ["姓名", "成绩"]])   # 取 0、1、2 三行

section("7. 条件筛选（最常用！）")

print(df[df["成绩"] > 85])
# 多条件：& 与、| 或，每个条件加括号
print(df[(df["成绩"] > 85) & (df["年龄"] < 21)])
# isin：某列的值在给定集合中
print(df[df["城市"].isin(["北京", "上海"])])
# 筛选后只看某些列
print(df[df["成绩"] > 85][["姓名", "成绩"]])

section("8. 新增与修改列")

df["是否优秀"] = df["成绩"] >= 90   # 基于已有列计算新增
df["班级"] = "一班"                  # 新增常数列
df["成绩+5"] = df["成绩"] + 5        # 基于运算新增
df["年龄"] = df["年龄"] + 1          # 修改整列
df = df.drop(columns=["成绩+5"])     # 删除列
print(df)

section("9. 排序")

print(df.sort_values("成绩", ascending=False))   # 按成绩降序
print(df.sort_values(["城市", "成绩"]))          # 按多列排序

# md 练习题：商品数据综合操作
df = pd.DataFrame({
    "商品": ["苹果", "香蕉", "橙子", "葡萄", "西瓜"],
    "单价": [8, 4, 6, 12, 3],
    "数量": [10, 20, 15, 8, 30],
    "产地": ["山东", "海南", "江西", "新疆", "海南"],
})
print(df.shape)
print(df.head(3))
print(df.describe())

df["总价"] = df["单价"] * df["数量"]
print(df[df["单价"] > 5][["商品", "单价"]])
print(df[(df["产地"] == "海南") & (df["数量"] > 10)])
print(df.sort_values("总价", ascending=False))

print("\n第 20 章演示完毕 ✅")
