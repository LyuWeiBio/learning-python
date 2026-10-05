# -*- coding: utf-8 -*-
"""
第 06 章：循环语句
对应教材：第一部分-Python入门基础/06-循环语句.md

演示：for + range、while、break/continue、累加与计数、循环 else、
      嵌套循环（乘法表）。
注：死循环示范、input() 交互示例已用固定值改写（可安全运行）。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. for 循环与 range() 的三种形式")

for ch in "abc":
    print(ch)                 # 遍历序列：依次打印 a、b、c

for i in range(5):
    print(i, end=" ")         # range(n) → 0..n-1（含头不含尾）
print()

for i in range(1, 6):
    print(i, end=" ")         # range(start, stop) → 1..5
print()

for i in range(0, 10, 2):
    print(i, end=" ")         # range(start, stop, step) → 0 2 4 6 8
print()

for i in range(5, 0, -1):
    print(i, end=" ")         # 步长为负：倒数 5 4 3 2 1
print()

for fruit in ["苹果", "香蕉", "橙子"]:
    print(f"我喜欢吃{fruit}")  # 循环变量起有意义的名字

section("2. 经典模式：累加与计数")

# 累加：循环外初始化 → 循环内更新 → 循环后使用
total = 0
for i in range(1, 101):
    total += i
print(f"1~100 的和：{total}")  # 5050

# 计数：统计满足条件的个数
count = 0
for i in range(1, 101):
    if i % 3 == 0:
        count += 1
print(f"1~100 中有 {count} 个数能被 3 整除")  # 33

section("3. while 循环")

count = 1
while count <= 5:
    print(count, end=" ")
    count += 1                # 千万别忘了更新条件变量，否则死循环！
print("\n循环结束")

# md 练习题第 1 题：用 while 计算 1~100 的和
total, i = 0, 1
while i <= 100:
    total += i
    i += 1
print(f"while 求和：{total}")  # 5050

section("4. break 与 continue")

# break：找到第一个能被 7 整除的数就停止
for i in range(1, 100):
    if i % 7 == 0:
        print(f"找到了：{i}")
        break

# continue：只打印奇数（偶数跳过本次）
for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(i, end=" ")
print()

# md 练习题第 4 题：猜数字（预设答案 7，模拟猜测序列）
answer = 7
guesses = [5, 9, 7]           # 原写法是 input() 反复输入；用固定序列演示
for guess in guesses:
    if guess == answer:
        print("恭喜，猜对了！")
        break
    elif guess > answer:
        print(f"{guess} → 大了")
    else:
        print(f"{guess} → 小了")

section("5. 循环中的 else")

# 判断质数：循环正常结束（没被 break）才执行 else
n = 13
for i in range(2, n):
    if n % i == 0:
        print(f"{n} 不是质数")
        break
else:
    print(f"{n} 是质数")

section("6. 嵌套循环：九九乘法表")

for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i * j}", end="\t")
    print()                   # 每行末尾换行

# md 练习题第 3 题：直角三角形
for i in range(1, 6):
    print("*" * i)

# md 练习题第 5 题：1~50 中既是偶数又能被 3 整除的数
count = 0
for i in range(1, 51):
    if i % 2 == 0 and i % 3 == 0:   # 即能被 6 整除
        print(i, end=" ")
        count += 1
print(f"\n共 {count} 个")            # 6 12 18 24 30 36 42 48，共 8 个

print("\n第 06 章演示完毕 ✅")
