# -*- coding: utf-8 -*-
"""
第 07 章：列表与元组
对应教材：第一部分-Python入门基础/07-列表与元组.md

演示：列表的创建/索引/切片/修改、常用方法、遍历、列表推导式、
      元组与元组解包。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 列表的创建与访问")

fruits = ["苹果", "香蕉", "橙子"]
numbers = [10, 20, 30, 40]
mixed = [1, "你好", 3.14, True]    # 列表可以混装不同类型
print(fruits, numbers, mixed)

print(fruits[0])     # 苹果
print(fruits[-1])    # 葡萄（负索引）
print(fruits[1:3])   # ['香蕉', '橙子']（切片规则与字符串一样）

# 列表是可变的：可以直接修改某个位置的元素
fruits[1] = "西瓜"
print(fruits)

section("2. 列表的常用方法")

lst = [1, 2, 3]
lst.append(4)           # 末尾追加
lst.insert(0, 99)       # 在索引 0 处插入
lst.extend([5, 6])      # 把另一个列表的元素逐个追加
print(lst)              # [99, 1, 2, 3, 4, 5, 6]
# 注意：append([5,6]) 会把 [5,6] 当一个元素加进去，extend 是逐个加

lst = [10, 20, 30, 20]
lst.remove(20)          # 删除第一个值为 20 的元素
print(lst.pop())        # 弹出并返回最后一个元素：20
print(lst.pop(0))       # 弹出指定索引：10
print(lst)              # [30]

lst = [10, 20, 30, 20]
print(len(lst))         # 4
print(20 in lst)        # True
print(lst.index(30))    # 2，第一次出现的索引
print(lst.count(20))    # 2

nums = [3, 1, 4, 1, 5, 9, 2]
nums.sort()             # 原地升序排序（改变原列表，返回 None）
print(nums)
nums.sort(reverse=True) # 降序
print(nums)
nums.reverse()          # 反转顺序
print(nums)

original = [3, 1, 2]
new = sorted(original)  # sorted 不改变原列表，返回新列表
print(original, new)

section("3. 遍历列表")

fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:    # 直接遍历元素（最常用）
    print(fruit)

for i, fruit in enumerate(fruits):   # 需要索引时用 enumerate
    print(f"{i}: {fruit}")

section("4. 列表推导式")

# [表达式 for 变量 in 序列]：一行生成新列表
squares = [x ** 2 for x in range(1, 6)]
print(squares)          # [1, 4, 9, 16, 25]

# 带条件筛选：[表达式 for 变量 in 序列 if 条件]
evens = [x for x in range(1, 21) if x % 2 == 0]
print(evens)

words = ["hello", "world"]
print([w.upper() for w in words])

# md 练习题第 3 题：1~30 中能被 3 整除的数
result = [x for x in range(1, 31) if x % 3 == 0]
print(result)

section("5. 元组：不可变的列表")

point = (3, 5)
print(point[0])         # 3，索引方式和列表一样
# point[0] = 10         # 故意错误示范：元组不能修改（已省略）

colors = ("红", "绿", "蓝")
print(len(colors))      # 3

single = (5,)           # 单个元素的元组必须加逗号，(5) 只是数字 5
print(type(single))

section("6. 元组解包")

point = (3, 5)
x, y = point            # 一次性把多个值赋给多个变量
print(x, y)

def min_max(nums):
    return min(nums), max(nums)   # 返回一个元组

low, high = min_max([3, 1, 4, 1, 5])
print(low, high)        # 1 5

# md 练习题第 2 题：求平均分
scores = [88, 92, 79, 95, 63]
avg = sum(scores) / len(scores)
print(f"平均分：{avg:.1f}")

# md 练习题第 4 题：找最大值及其位置
nums = [12, 45, 7, 23, 45, 9]
biggest = max(nums)
print(f"最大值 {biggest}，位于索引 {nums.index(biggest)}")

# md 练习题第 5 题：元组解包
student = ("张三", 18, "计算机")
name, age, major = student
print(f"我叫{name}，今年{age}岁，学{major}专业")

print("\n第 07 章演示完毕 ✅")
