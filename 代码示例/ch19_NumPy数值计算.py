# -*- coding: utf-8 -*-
"""
第 19 章：NumPy 数值计算
对应教材：第三部分-数据分析基础/19-NumPy数值计算.md

演示：创建数组、数组属性、索引与切片、向量化运算、布尔索引、
      聚合统计与 axis、reshape、广播。
"""

import numpy as np


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 创建数组")

a = np.array([1, 2, 3, 4])
print(a, type(a))

b = np.array([[1, 2, 3], [4, 5, 6]])   # 二维数组（矩阵）
print(b)

print(np.zeros((2, 3)))        # 2行3列全 0
print(np.ones((2, 2)))         # 全 1
print(np.full((2, 2), 7))      # 全 7
print(np.arange(0, 10, 2))     # [0 2 4 6 8]，类似 range 但返回数组
print(np.linspace(0, 1, 5))    # 0~1 间均匀取 5 个
print(np.eye(3))               # 3x3 单位矩阵

np.random.seed(42)                    # 固定随机种子，保证结果可复现
print(np.random.rand(2, 3))           # [0,1) 均匀分布
print(np.random.randn(3))             # 标准正态分布
print(np.random.randint(1, 7, size=5))  # 掷5次骰子

section("2. 数组的属性")

b = np.array([[1, 2, 3], [4, 5, 6]])
print(b.shape)      # (2, 3)  形状：2行3列
print(b.ndim)       # 2       维度数
print(b.size)       # 6       元素总数
print(b.dtype)      # int64   数据类型（整个数组只能是一种类型）

section("3. 索引与切片")

a = np.array([10, 20, 30, 40, 50])
print(a[0], a[-1], a[1:4])

b = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
print(b[0, 0])      # 1     二维用 [行, 列]
print(b[1, 2])      # 6
print(b[0])         # [1 2 3]  整个第0行
print(b[:, 1])      # [2 5 8]  整个第1列（非常常用）
print(b[0:2, 1:3])  # 前2行、第1~2列

section("4. 向量化运算（NumPy 的灵魂）")

a = np.array([1, 2, 3, 4])
print(a + 10)       # [11 12 13 14]  自动对每个元素运算，无需循环
print(a * 2)
print(a ** 2)

b = np.array([10, 20, 30, 40])
print(a + b)        # 对应元素相加（列表的 + 是拼接！）
print(a * b)

a = np.array([1, 4, 9, 16])
print(np.sqrt(a))   # [1. 2. 3. 4.]  数学函数同样作用于每个元素
print(np.exp([0, 1]))

section("5. 布尔索引：按条件筛选")

a = np.array([15, 8, 23, 42, 4, 16])
mask = a > 15
print(mask)         # [False False True True False True]
print(a[mask])      # [23 42 16]
print(a[a > 15])    # 同上，更常见的写法

# 多条件用 &（与）、|（或），每个条件要加括号
print(a[(a > 10) & (a < 30)])   # [15 23 16]

# 结合赋值：把小于 10 的值改成 0
a[a < 10] = 0
print(a)            # [15  0 23 42  0 16]

# md 练习题第 3 题：及格筛选
scores = np.array([88, 45, 92, 60, 33, 78, 95])
passed = scores[scores >= 60]
print("及格：", passed, "人数：", passed.size)  # 5

# md 练习题第 4 题：摄氏转华氏（一行向量化）
c = np.array([0, 25, 37, 100])
print(c * 9 / 5 + 32)   # [ 32.   77.   98.6 212. ]

section("6. 聚合统计与 axis")

a = np.array([3, 1, 4, 1, 5, 9, 2, 6])
print(a.sum(), a.mean(), a.max(), a.min())   # 求和/均值/最大/最小
print(a.std())      # 标准差
print(a.argmax())   # 5，最大值所在的索引

b = np.array([[1, 2, 3],
              [4, 5, 6]])
print(b.sum())            # 21（所有元素之和）
print(b.sum(axis=0))      # [5 7 9]  axis=0 跨行、按列汇总
print(b.sum(axis=1))      # [6 15]   axis=1 跨列、按行汇总

# md 练习题第 5 题：学生/课程平均分
scores = np.array([[85, 90, 78],
                   [72, 88, 95],
                   [60, 75, 80],
                   [98, 92, 89]])
print("每个学生平均分：", scores.mean(axis=1))   # 按行
print("每门课平均分：", scores.mean(axis=0))     # 按列

section("7. reshape 与转置")

a = np.arange(12)
b = a.reshape(3, 4)       # 变成 3 行 4 列
print(b)
print(b.reshape(2, 6))
print(b.reshape(-1))      # 拉平成一维；-1 表示自动计算
print(b.T)                # 转置（行列互换）

section("8. 广播（Broadcasting）")

a = np.array([[1, 2, 3],
              [4, 5, 6]])
print(a + 100)            # 100 被广播到每个元素

# 每列减去该列的均值（数据标准化的常用操作）
col_mean = a.mean(axis=0)
print(col_mean)           # [2.5 3.5 4.5]
print(a - col_mean)       # 每行都减去这个均值向量

print("\n第 19 章演示完毕 ✅")
