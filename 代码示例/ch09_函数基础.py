# -*- coding: utf-8 -*-
"""
第 09 章：函数基础
对应教材：第一部分-Python入门基础/09-函数基础.md

演示：def 定义与调用、参数、return（与 print 的区别）、返回多个值、
      默认参数、关键字参数、文档字符串。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 定义与调用函数")


def greet():
    print("你好！")
    print("欢迎学习 Python")


greet()        # 调用（定义之后必须调用才会执行）
greet()        # 可以反复调用

section("2. 参数：给函数传入数据")


def greet(name):            # name 是形参
    print(f"你好，{name}！")


greet("小明")               # "小明" 是实参
greet("小红")


def add(a, b):
    print(a + b)


add(3, 5)                   # 8，按位置依次对应形参

section("3. 返回值：return")


def add(a, b):
    return a + b


result = add(3, 5)          # 把返回值存进变量
print(result)               # 8
print(add(10, 20) * 2)      # 返回值可以直接参与运算：60


# return 与 print 的区别（重点！）
def add_print(a, b):
    print(a + b)            # 只显示，不返回


def add_return(a, b):
    return a + b            # 返回结果


x = add_print(3, 5)        # 屏幕显示 8，但 x 是 None！
y = add_return(3, 5)       # y 得到 8，可继续使用
print(f"x={x}, y={y}")


def check(score):
    if score >= 60:
        return "及格"
    return "不及格"          # return 会立即结束函数


print(check(80))

section("4. 返回多个值")


def min_max(numbers):
    return min(numbers), max(numbers)   # 返回一个元组


low, high = min_max([3, 7, 1, 9, 4])
print(low, high)            # 1 9（解包接收）

section("5. 默认参数")


def greet(name, greeting="你好"):   # 有默认值的参数必须放在后面
    print(f"{greeting}，{name}！")


greet("小明")                    # 用默认值
greet("小红", "早上好")          # 覆盖默认值

section("6. 关键字参数")


def create_user(name, age, city):
    print(f"{name}, {age}岁, 来自{city}")


create_user("小明", 18, "北京")               # 按位置传
create_user(age=18, city="上海", name="小红")  # 关键字传，顺序可打乱

section("7. 文档字符串（docstring）")


def circle_area(radius):
    """计算圆的面积。

    参数:
        radius: 圆的半径
    返回:
        面积（浮点数）
    """
    return 3.14159 * radius ** 2


print(circle_area(5))
print(circle_area.__doc__.splitlines()[0])   # 查看文档首行

section("8. 综合例子：成绩处理")


def analyze_scores(scores):
    """接收成绩列表，返回(平均分, 最高分, 及格率)。"""
    average = sum(scores) / len(scores)
    highest = max(scores)
    passed = len([s for s in scores if s >= 60])
    pass_rate = passed / len(scores)
    return average, highest, pass_rate


data = [88, 55, 92, 70, 45]
avg, high, rate = analyze_scores(data)
print(f"平均分：{avg:.1f}")
print(f"最高分：{high}")
print(f"及格率：{rate:.0%}")     # :.0% 会自动转成百分比

# md 练习题第 1 题：温度转换
def c_to_f(c):
    return c * 9 / 5 + 32

print(c_to_f(0), c_to_f(100))   # 32.0 212.0

# md 练习题第 2 题：判断质数
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

print([n for n in range(1, 51) if is_prime(n)])

# md 练习题第 3 题：默认参数
def power(base, exp=2):
    return base ** exp

print(power(5), power(2, 10))    # 25 1024

# md 练习题第 4 题：返回多个值
def divide(a, b):
    return a // b, a % b

q, r = divide(17, 5)
print(f"商 {q}，余 {r}")          # 商 3，余 2

# md 练习题第 5 题：统计函数
def word_stats(sentence):
    words = sentence.split()
    return len(words), sum(len(w) for w in words) / len(words)

n, avg = word_stats("hello world python programming")
print(f"{n} 个单词，平均长度 {avg:.1f}")

print("\n第 09 章演示完毕 ✅")
