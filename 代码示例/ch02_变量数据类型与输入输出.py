# -*- coding: utf-8 -*-
"""
第 02 章：变量、数据类型与输入输出
对应教材：第一部分-Python入门基础/02-变量数据类型与输入输出.md

说明：
- md 中所有 input() 示例，本脚本用固定的示例值代替（已注释原写法），
  以便在无人值守时也能直接运行。
- md 2.1/2.3 节的「错误示范」按要求没有收录。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 变量：赋值与命名")

# 用等号 = 把右边的值赋给左边的变量
age = 18
name = "小红"
height = 1.68
print(name)      # 小红
print(age)       # 18
print(height)    # 1.68

# 变量的值可以随时改变
score = 60
print(score)     # 60
score = 95       # 重新赋值，覆盖旧值
print(score)     # 95

# 用旧值计算出新值
count = 10
count = count + 5
print(count)     # 15

# 命名习惯：有意义的英文名 + 下划线连接（snake_case）
student_count = 42
total_price = 99.9
print(student_count, total_price)

section("2. 四种基本数据类型与 type()")

age = 18            # int
price = 9.9         # float
name = "Python"     # str
is_student = True   # bool（注意首字母大写）

print(type(18))         # <class 'int'>
print(type(3.14))       # <class 'float'>
print(type("你好"))     # <class 'str'>
print(type(True))       # <class 'bool'>

# 布尔值常用来表示“是否成立”
is_adult = age >= 18
print(is_adult)         # True

section("3. 类型转换")

num_str = "100"
num = int(num_str)
print(num + 1)          # 101

age = 18
age_str = str(age)
print("我今年" + age_str + "岁")   # 我今年18岁

print(float(5))         # 5.0
print(int(3.99))        # 3（直接截断，不是四舍五入！）

section("4. input() 读取输入（用固定值演示）")

# 原写法：name = input("请输入你的名字：")；本脚本用示例值代替
name = "小明"           # 模拟用户输入“小明”
print("你好，" + name)

# input() 永远返回字符串，做数学运算前必须转换
age = 18                # 模拟输入 18，原写法：age = int(input("请输入你的年龄："))
print("明年你" + str(age + 1) + "岁")

# 常见错误演示与修正：字符串拼接会得到 "35"，要转成数字
a, b = 3, 5             # 模拟输入 3 和 5，原写法：a = int(input("第一个数："))
print(a + b)            # 8

section("5. print() 的更多用法")

name = "小红"
age = 18
print("姓名", name, "年龄", age)   # 多个值自动用空格分隔：姓名 小红 年龄 18

print("2024", "01", "01", sep="-")   # sep 控制分隔符：2024-01-01
print("不换行", end="")              # end 控制行尾字符，默认换行
print("接着这一行")                   # 不换行接着这一行

section("6. f-string：最推荐的格式化方式")

name = "小明"
age = 18
print(f"我叫{name}，今年{age}岁")

a, b = 3, 5
print(f"{a} + {b} = {a + b}")       # {} 里可以直接写表达式

pi = 3.1415926
print(f"圆周率约为 {pi:.2f}")        # 保留 2 位小数：3.14

# md 练习题第 1 题：变量交换
a, b = 1, 2
a, b = b, a
print(f"a={a} b={b}")               # a=2 b=1

# md 练习题第 2 题：单位换算（模拟输入 170）
cm = 170.0
print(f"{cm / 100} 米")             # 1.7 米

# md 练习题第 5 题：类型判断
print(type(10))         # <class 'int'>
print(type(10.0))       # <class 'float'>
print(type("10"))       # <class 'str'>
print(type(10 > 5))     # <class 'bool'>

print("\n第 02 章演示完毕 ✅")
