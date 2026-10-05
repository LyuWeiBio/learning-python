# -*- coding: utf-8 -*-
"""
第 05 章：条件语句
对应教材：第一部分-Python入门基础/05-条件语句.md

演示：if / if-else / if-elif-else、缩进规则、嵌套条件、真假性、
      三元表达式、pass 占位符。
注：5.2 节的「缩进错误示范」是教学用反例，按要求没有收录；
    input() 全部用固定值演示（已注释原写法）。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 最简单的 if")

age = 20
if age >= 18:               # 条件后必须有冒号 :，下一行缩进 4 个空格
    print("你是成年人")
    print("可以独立签署合同")
print("程序结束")           # 缩进结束，条件语句结束：无论如何都会执行

section("2. if-else：二选一")

score = 55
if score >= 60:
    print("及格")
else:                      # else 后也要冒号，不能写条件
    print("不及格")

section("3. if-elif-else：多选一")

score = 85
if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")
# 注意条件顺序：>=60 必须放在最后，否则 85 分会被先匹配到“及格”

weather = "雨"
if weather == "晴":
    print("出门散步")
elif weather == "雨":
    print("带把伞")
# 没有 else 也可以

section("4. 嵌套条件")

age, has_ticket = 20, True
if age >= 18:
    if has_ticket:
        print("欢迎入场")
    else:
        print("请先购票")
else:
    print("未成年人谢绝入内")

# 能用 and/or 表达的，尽量避免深层嵌套
if age >= 18 and has_ticket:
    print("欢迎入场（and 改写版）")

section("5. 值的真假性（Truthy / Falsy）")

# 为 False 的值：False、0、0.0、""、空容器、None；其余几乎都为 True
name = "小明"              # 原写法：name = input("请输入名字：").strip()
if name:                   # 等价于 if name != ""
    print(f"你好，{name}")
else:
    print("你没有输入名字")

for value in [0, "", [], None, "abc", [1]]:
    print(f"{value!r} 的真假：{bool(value)}")

section("6. 三元表达式")

score = 75
result = "及格" if score >= 60 else "不及格"   # 值A if 条件 else 值B
print(result)

# md 练习题第 5 题：改写为三元表达式
n = 7
label = "偶数" if n % 2 == 0 else "奇数"
print(label)               # 奇数

section("7. pass 占位符")

score = 80
if score >= 60:
    pass    # TODO: 以后再实现（语法上必须有内容，用 pass 占位）
else:
    print("不及格")
print("pass 分支执行完毕")

# md 练习题第 2 题：BMI 计算器（模拟输入 1.70 米、60 千克）
height, weight = 1.70, 60.0
bmi = weight / height ** 2
print(f"你的 BMI 是 {bmi:.1f}")
if bmi < 18.5:
    print("偏瘦")
elif bmi < 24:
    print("正常")
elif bmi < 28:
    print("偏胖")
else:
    print("肥胖")

# md 练习题第 3 题：闰年判断（模拟输入 2024）
year = 2024
if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year} 年是闰年")
else:
    print(f"{year} 年不是闰年")

print("\n第 05 章演示完毕 ✅")
