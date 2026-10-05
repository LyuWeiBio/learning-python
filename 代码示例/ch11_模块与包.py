# -*- coding: utf-8 -*-
"""
第 11 章：模块与包
对应教材：第二部分-Python进阶/11-模块与包.md

演示：import 的三种写法、math/random/datetime 标准库、
      自建模块（在临时目录生成 mytools.py 再导入）、
      if __name__ == "__main__"、dir()/help() 探索模块。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. import 的三种写法")

import math

print(math.pi)          # 3.141592653589793
print(math.sqrt(16))    # 4.0
print(math.floor(3.7))  # 3，向下取整
print(math.ceil(3.2))   # 4，向上取整

from math import pi, sqrt   # 只导入需要的部分

print(pi)               # 3.141592653589793
print(sqrt(25))         # 5.0

import math as m        # 起别名（数据科学里常用，如 import numpy as np）
print(m.gcd(12, 18))    # 6，最大公约数

section("2. 常用标准库速览")

print(math.sqrt(2))
print(math.pow(2, 10))      # 1024.0
print(math.factorial(5))    # 120，阶乘
print(math.gcd(12, 18))     # 6

import random

random.seed(42)                             # 固定随机种子，结果可复现
print(random.random())                      # [0,1) 随机小数
print(random.randint(1, 6))                 # 掷骰子：1~6
print(random.choice(["石头", "剪刀", "布"]))
nums = [1, 2, 3, 4, 5]
random.shuffle(nums)                        # 原地打乱
print("打乱后：", nums)
print(random.sample(range(1, 50), 6))       # 模拟彩票：1~49 取 6 个不重复

from datetime import datetime, timedelta

now = datetime.now()
print(now)                                  # 当前时间
print(now.year, now.month, now.day)
print(now.strftime("%Y-%m-%d %H:%M"))       # 格式化成字符串
print((now + timedelta(days=1)).strftime("%Y-%m-%d"))  # 时间运算

section("3. 创建并导入自己的模块")

import os
import sys
import tempfile

# 在临时目录里创建一个模块 mytools.py（md 11.4 节的内容）
tmpdir = tempfile.mkdtemp(prefix="ch11_demo_")
with open(os.path.join(tmpdir, "mytools.py"), "w", encoding="utf-8") as f:
    f.write('''"""自建模块演示（md 11.4 节）。"""

PI = 3.14159


def circle_area(r):
    return PI * r ** 2


def greet(name):
    return f"你好，{name}"


if __name__ == "__main__":
    # 只有直接运行 mytools.py 时才执行；被 import 时不执行
    print("正在测试 circle_area：", circle_area(10))
    print("直接运行时 __name__ =", __name__)
''')

sys.path.insert(0, tmpdir)      # 让 import 能找到临时目录
import mytools                 # 导入自己的模块

print(mytools.circle_area(5))  # 78.53975
print(mytools.greet("小明"))   # 你好，小明
from mytools import circle_area
print(circle_area(3))
print("被导入时 mytools.__name__ =", mytools.__name__)  # "mytools" 而非 "__main__"

section("4. 查看模块内容")

print(dir(math)[:5], "...")    # 列出 math 里所有可用的名字（截取前 5 个）
print(math.sqrt.__doc__.strip().splitlines()[0])  # help(math.sqrt) 的文档首行

# md 练习题第 2 题：掷两个骰子 1000 次，统计点数和为 7 的占比
random.seed(1)
count, times = 0, 1000
for _ in range(times):
    if random.randint(1, 6) + random.randint(1, 6) == 7:
        count += 1
print(f"点数和为 7 的比例：{count / times:.2%}")   # 理论值约 16.7%

# md 练习题第 3 题：今天到 2030-01-01 还有多少天
from datetime import date
today = date.today()
print(f"距 2030-01-01 还有 {(date(2030, 1, 1) - today).days} 天")

print("\n第 11 章演示完毕 ✅")
