# -*- coding: utf-8 -*-
"""
第 08 章：字典与集合
对应教材：第一部分-Python入门基础/08-字典与集合.md

演示：字典的创建/增改删、get() 安全取值、遍历、计数应用、
      字典推导式、嵌套字典、集合去重与集合运算。
注：md 练习题第 3 题的 input() 用固定值演示。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 字典：键值对的集合")

student = {
    "name": "小明",
    "age": 18,
    "major": "计算机",
}
print(student)
print(student["name"])     # 小明，用键取值
print(student["age"])      # 18

section("2. 增、改、删")

student = {"name": "小明", "age": 18}
student["age"] = 19            # 键存在 → 修改
student["city"] = "北京"       # 键不存在 → 新增
print(student)

del student["city"]            # 删除某个键
age = student.pop("age")       # 删除并返回该键的值
print(age, student)

section("3. 安全取值：get() 与 in")

student = {"name": "小明", "age": 18}
print(student.get("name"))          # 小明
print(student.get("phone"))         # None，不报错
print(student.get("phone", "未填")) # 未填，指定默认值
print("age" in student)             # True

section("4. 遍历字典")

student = {"name": "小明", "age": 18, "major": "计算机"}
for key in student:                 # 默认遍历键
    print(key)
for value in student.values():      # 遍历值
    print(value)
for key, value in student.items():  # 同时遍历键和值（最常用）
    print(f"{key} = {value}")

section("5. 字典的典型应用：计数")

text = "hello"
counter = {}
for ch in text:
    counter[ch] = counter.get(ch, 0) + 1   # get(ch, 0) 妙处：第一次返回 0
print(counter)     # {'h': 1, 'e': 1, 'l': 2, 'o': 1}

# md 练习题第 2 题：词频统计
text = "the quick brown fox the lazy dog the"
counter = {}
for word in text.split():
    counter[word] = counter.get(word, 0) + 1
print(counter)

section("6. 字典推导式与 zip")

squares = {x: x ** 2 for x in range(1, 6)}
print(squares)      # {1:1, 2:4, 3:9, 4:16, 5:25}

names = ["a", "b", "c"]
scores = [90, 85, 95]
result = {name: score for name, score in zip(names, scores)}   # zip 配对
print(result)

section("7. 嵌套字典")

students = {
    "s01": {"name": "小明", "scores": [90, 85]},
    "s02": {"name": "小红", "scores": [95, 92]},
}
print(students["s01"]["name"])        # 小明
print(students["s02"]["scores"][0])   # 95

section("8. 集合：无序不重复")

s = {1, 2, 3, 3, 2, 1}
print(s)              # {1, 2, 3}，重复的自动去掉了

empty = set()         # 注意：空集合必须用 set()，{} 是空字典！
print(type(empty))

# 去重是集合最常见的用途
nums = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(nums))
print(sorted(unique))

# md 练习题第 4 题：列表去重并排序
data = [3, 1, 2, 3, 1, 4, 2, 5]
print(sorted(set(data)))            # [1, 2, 3, 4, 5]

s = {1, 2, 3}
s.add(4)              # 添加
s.discard(2)          # 删除（元素不存在也不报错）
print(s)

section("9. 集合运算")

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a & b)      # {3, 4}        交集
print(a | b)      # {1,2,3,4,5,6} 并集
print(a - b)      # {1, 2}        差集
print(a ^ b)      # {1,2,5,6}     对称差
print(3 in a)     # True（集合查找极快）

# md 练习题第 5 题：共同好友
a = {"张三", "李四", "王五"}
b = {"李四", "王五", "赵六"}
print("共同好友：", a & b)
print("好友总数：", len(a | b))     # 4

# md 练习题第 3 题：安全查询（模拟输入“苹果”）
prices = {"苹果": 5, "香蕉": 3}
name = "苹果"         # 原写法：name = input("请输入商品名：")
price = prices.get(name)
print(f"{name} 的价格是 {price} 元" if price is not None else "无此商品")

print("\n第 08 章演示完毕 ✅")
