# -*- coding: utf-8 -*-
"""
第 03 章：运算符与表达式
对应教材：第一部分-Python入门基础/03-运算符与表达式.md

演示：算术/比较/逻辑/复合赋值运算符、连续比较、运算符优先级。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 算术运算符")

print(7 / 2)     # 3.5   ← 注意：普通除法结果是浮点数
print(7 // 2)    # 3     ← 整除，向下取整
print(7 % 2)     # 1     ← 取余（余数）
print(2 ** 10)   # 1024  ← 幂运算，2 的 10 次方

# 取余判断奇偶
n = 17
print(n % 2)     # 1，余数不为 0 → 奇数

# 整除 + 取余搭配：秒换算成分和秒
total_seconds = 125
minutes = total_seconds // 60    # 2 分
seconds = total_seconds % 60     # 5 秒
print(f"{minutes} 分 {seconds} 秒")

section("2. 比较运算符（结果永远是布尔值）")

print(3 == 3)    # True（注意是两个等号！一个等号是赋值）
print(3 != 5)    # True
print(3 > 5)     # False
print(3 <= 3)    # True

# Python 支持连续比较，符合数学直觉
age = 25
print(18 <= age < 60)    # True，等价于 (18<=age) and (age<60)

section("3. 逻辑运算符")

age = 25
has_ticket = True

print(age >= 18 and has_ticket)    # True，两个条件都满足
print(age < 12 or has_ticket)      # True，第二个条件满足即可
print(not has_ticket)              # False，取反

# md 练习题第 1 题：是否成年且未满 60 岁
age = 20
print(age >= 18 and age < 60)      # True

# md 练习题第 3 题：判断闰年
year = 2024
is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
print(is_leap)                     # True

section("4. 复合赋值运算符")

score = 100
score -= 20      # 扣 20 分
print(score)     # 80
score += 5       # 加 5 分
print(score)     # 85

section("5. 运算符优先级")

print(2 + 3 * 4)       # 14，先乘后加
print((2 + 3) * 4)     # 20，括号改变了顺序
print(2 ** 3 ** 2)     # 512，幂从右往左算：2**(3**2)

# md 练习题第 2 题：3725 秒换算成小时/分/秒
seconds = 3725
h = seconds // 3600          # 1
m = (seconds % 3600) // 60   # 2
s = seconds % 60             # 5
print(f"{h} 小时 {m} 分 {s} 秒")

# md 练习题第 4 题：猜结果
print(10 % 3)                # 1
print(10 // 3)               # 3
print(2 ** 5)                # 32
print(5 > 3 and 2 > 4)       # False（and 一假则假）
print(not (5 == 5))          # False（not 取反）

section("6. 表达式与语句")

price, count, shipping = 9.9, 3, 5.0
total = price * count + shipping    # 右边是一个算术表达式
print(f"总价：{total:.1f}")

print("\n第 03 章演示完毕 ✅")
