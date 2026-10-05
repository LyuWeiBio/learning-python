# -*- coding: utf-8 -*-
"""
第 16 章：迭代器、生成器与装饰器
对应教材：第二部分-Python进阶/16-迭代器生成器与装饰器.md

演示：可迭代对象与迭代器、生成器（yield）与生成器表达式、
      装饰器原理、@ 语法糖、functools.wraps、重试装饰器。
注：16.3 节原示例的 time.sleep(0.5) 缩短为 0.2，保证脚本快速运行；
    16.4 节重试装饰器的随机失败用固定失败次数代替，保证确定性运行。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 可迭代对象与迭代器")

nums = [10, 20, 30]
it = iter(nums)          # 得到迭代器
print(next(it))          # 10
print(next(it))          # 20
print(next(it))          # 30
# print(next(it))        # 故意错误示范：StopIteration（已省略）

section("2. 生成器：用 yield 惰性产生数据")


def count_up_to(n):
    i = 1
    while i <= n:
        yield i          # 每次 yield 一个值，然后"暂停"
        i += 1


gen = count_up_to(5)
for num in gen:
    print(num, end=" ")  # 1 2 3 4 5
print()

# 生成器表达式：像列表推导式但用圆括号，几乎不占内存
gen = (x ** 2 for x in range(5))
print(sum(gen))          # 30，边生成边求和

# md 练习题第 1 题：斐波那契生成器
def fib_gen(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print(list(fib_gen(10)))

# md 练习题第 2 题：偶数平方生成器
gen = (x ** 2 for x in range(1, 101) if x % 2 == 0)
print(sum(gen))          # 171700

section("3. 函数是一等公民 + 手写装饰器")


def shout(text):
    return text.upper()


yell = shout             # 把函数赋给变量（注意没有括号）
print(yell("hello"))     # HELLO

import time


def timer(func):
    """装饰器：打印函数运行耗时。"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)      # 调用原函数
        end = time.time()
        print(f"{func.__name__} 耗时 {end - start:.4f} 秒")
        return result
    return wrapper       # 返回增强后的新函数


def slow_add(a, b):
    time.sleep(0.2)      # 原示例 0.5 秒，这里缩短以便快速演示
    return a + b


slow_add = timer(slow_add)   # 用装饰器"包裹"原函数
print(slow_add(3, 5))

section("4. @ 语法糖 + functools.wraps")

import functools


def timer2(func):
    @functools.wraps(func)       # 保留原函数的 __name__、__doc__
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@timer2                    # 等价于 slow2 = timer2(slow2)
def slow2():
    """一个示例函数"""
    return "ok"


print(slow2())
print("装饰后函数名：", slow2.__name__)     # slow2（而非 wrapper）
print("装饰后文档：", slow2.__doc__)

# md 练习题第 3 题：日志装饰器
def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 执行完毕")
        return result
    return wrapper


@log_call
def add(a, b):
    return a + b


print(add(3, 5))

section("5. 带参数的重试装饰器")

attempts = {"n": 0}


def retry(times=3):
    """出错时最多重试 times 次的装饰器。"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"第 {i + 1} 次失败：{e}")
            print("重试次数用尽")
        return wrapper
    return decorator


@retry(times=3)
def risky():
    attempts["n"] += 1
    if attempts["n"] < 3:        # 前两次固定失败，第三次成功（确定性演示）
        raise ValueError("随机失败")
    return "成功！"


print(risky())

print("\n第 16 章演示完毕 ✅")
