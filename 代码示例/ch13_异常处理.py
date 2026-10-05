# -*- coding: utf-8 -*-
"""
第 13 章：异常处理
对应教材：第二部分-Python进阶/13-异常处理.md

演示：try/except 捕获、捕获多种异常、as e 获取异常对象、
      else 与 finally、raise 主动抛出、自定义异常、健壮输入函数。
注：md 中所有 input() 用固定值演示（已注释原写法）。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 捕获异常：try / except")

# 原写法：num = int(input("请输入一个整数："))；用固定值演示两种场景
for raw in ["42", "abc"]:
    try:
        num = int(raw)
        print(f"你输入的是 {num}")
    except ValueError:
        print("输入的不是有效整数！")

section("2. 捕获多种异常 + 获取异常对象")

# 原写法：a = int(input("被除数：")); b = int(input("除数："))
for a_raw, b_raw in [("10", "2"), ("10", "0"), ("x", "2")]:
    try:
        a = int(a_raw)
        b = int(b_raw)
        print(a / b)
    except ValueError:
        print("请输入整数！")
    except ZeroDivisionError:
        print("除数不能为 0！")

# 用一个元组同时捕获多种
try:
    num = int("abc")
except (ValueError, TypeError):
    print("值或类型有误")

# as e 拿到异常对象
try:
    num = int("abc")
except ValueError as e:
    print(f"出错了：{e}")
    print(f"异常类型：{type(e).__name__}")

# 注意：避免裸 except: 吞掉所有错误；尽量捕获具体的异常类型

section("3. else 与 finally")

try:
    num = int("18")          # 原写法：int(input("请输入："))
except ValueError:
    print("输入无效")
else:
    print(f"输入成功：{num}")  # try 没出错时才执行
finally:
    print("无论如何都会执行（常用于清理资源）")

section("4. raise：主动抛出异常")


def set_age(age):
    if age < 0:
        raise ValueError("年龄不能为负数")
    if age > 150:
        raise ValueError("年龄不合理")
    print(f"年龄设置为 {age}")


set_age(25)                  # 正常
try:
    set_age(-5)              # 抛出 ValueError
except ValueError as e:
    print(f"错误：{e}")

section("5. 自定义异常")


class InsufficientBalanceError(Exception):
    """余额不足时抛出。"""
    pass


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientBalanceError(f"余额 {balance} 不足以支取 {amount}")
    return balance - amount


try:
    withdraw(100, 200)
except InsufficientBalanceError as e:
    print(f"取款失败：{e}")

section("6. 实战：健壮的输入函数")


def input_int(prompt, demo_inputs):
    """不断重试直到拿到合法整数（用固定输入序列代替 input()）。"""
    for raw in demo_inputs:              # 原写法：while True: raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            print("请输入一个整数，再试一次。")
    raise ValueError("没有合法输入")


age = input_int("请输入年龄：", ["abc", "25"])   # 第一次无效，重试后成功
print(f"你的年龄是 {age}")

# md 练习题第 1 题：安全除法
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # None

# md 练习题第 2 题：列表安全取值
def get_item(lst, index):
    try:
        return lst[index]
    except IndexError:
        return "越界"

print(get_item([1, 2, 3], 1))    # 2
print(get_item([1, 2, 3], 9))    # 越界

# md 练习题第 3 题：安全读文件
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "文件不存在"

print(read_file("一定不存在的文件.txt"))

# md 练习题第 4 题：校验分数
def set_score(score):
    if not 0 <= score <= 100:
        raise ValueError(f"分数 {score} 不合法，应在 0~100 之间")
    print(f"分数：{score}")

try:
    set_score(150)
except ValueError as e:
    print(f"错误：{e}")

print("\n第 13 章演示完毕 ✅")
