# -*- coding: utf-8 -*-
"""
第 10 章：函数进阶
对应教材：第一部分-Python入门基础/10-函数进阶.md

演示：作用域（局部/全局）、*args 与 **kwargs、可变参数解包、
      lambda、sorted(key=...)/map/filter、递归。
注：md 10.1 节的报错示范行（print(x) 报错）按要求没有收录；
    md 10.4 节 `>` 开头的 REPL 风格示例已改写为普通代码。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 作用域：局部 vs 全局")


def foo():
    x = 10          # 局部变量，只在函数内部有效
    print(x)


foo()               # 10
# print(x)          # 故意错误示范：外面看不到 x（已省略）

message = "全局的问候"


def show():
    print(message)   # 函数内部可以读取全局变量


show()

count = 0


def add():
    global count     # 用 global 声明后才能修改全局变量
    count = count + 1


add()
print(count)        # 1

section("2. 可变参数 *args 和 **kwargs")


def total(*args):
    print("args 是元组：", args)
    return sum(args)


print(total(1, 2, 3))         # 6
print(total(10, 20, 30, 40))  # 100


def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")


show_info(name="小明", age=18, city="北京")

# 解包：调用时用 * / ** 把序列/字典拆开
def add3(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add3(*nums))                 # 等价于 add3(1, 2, 3) → 6
params = {"a": 1, "b": 2, "c": 3}
print(add3(**params))              # 等价于 add3(a=1, b=2, c=3) → 6

section("3. 匿名函数 lambda")

square = lambda x: x ** 2          # lambda 参数: 表达式（一行小函数）
print(square(5))                  # 25

add = lambda a, b: a + b
print(add(3, 4))                  # 7

section("4. 高阶函数：sorted(key=...)、map、filter")

words = ["banana", "apple", "cherry", "fig"]
print(sorted(words, key=len))            # 按单词长度排序

students = [("小明", 88), ("小红", 95), ("小刚", 72)]
print(sorted(students, key=lambda s: s[1]))                       # 按分数升序
print(sorted(students, key=lambda s: s[1], reverse=True))          # 按分数降序

nums = [1, 2, 3, 4]
print(list(map(lambda x: x ** 2, nums)))                 # map：每个元素做同样操作
print(list(filter(lambda x: x % 2 == 0, nums)))          # filter：筛选满足条件的

# 很多时候列表推导式更直观（md 10.4 节 REPL 风格示例已改写）
print([x ** 2 for x in nums])                           # 等价于 map
print([x for x in nums if x % 2 == 0])                  # 等价于 filter

section("5. 递归：函数调用自己")


def factorial(n):
    if n <= 1:               # 基线条件（递归的出口，必须有！）
        return 1
    return n * factorial(n - 1)   # 递归调用


print(factorial(5))          # 120


def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


print([fib(i) for i in range(10)])

# md 练习题第 1 题：可变参数求平均
def average(*args):
    if not args:            # 防止除以 0
        return 0
    return sum(args) / len(args)

print(average(1, 2, 3, 4))  # 2.5

# md 练习题第 2 题：按长度排序
words = ["python", "go", "java", "c", "rust"]
print(sorted(words, key=len))

# md 练习题第 4 题：按字典值排序
scores = {"小明": 88, "小红": 95, "小刚": 72}
for name, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
    print(f"{name}: {score}")

# md 练习题第 5 题：递归求和
def sum_to(n):
    if n <= 1:
        return n
    return n + sum_to(n - 1)

print(sum_to(100))          # 5050

print("\n第 10 章演示完毕 ✅")
