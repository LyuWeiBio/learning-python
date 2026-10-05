# -*- coding: utf-8 -*-
"""
第 04 章：字符串处理
对应教材：第一部分-Python入门基础/04-字符串处理.md

演示：创建字符串、转义字符、拼接与重复、索引、切片、常用字符串方法。
注：4.7 节的 input() 用固定值演示。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 创建字符串")

s1 = '单引号字符串'
s2 = "双引号字符串"
s3 = "他说：'你好'"            # 字符串内部有引号时用另一种引号包裹
print(s1, s2)
print(s3)

poem = """床前明月光，
疑是地上霜。"""                # 三引号创建多行字符串
print(poem)

section("2. 转义字符")

print("第一行\n第二行")        # \n 换行
print("姓名\t年龄")            # \t 制表符，用于对齐
print("路径：C:\\Users")       # 想打印一个反斜杠要写两个
print(r"C:\Users\name\test")  # 原始字符串（r 前缀）：不转义

section("3. 拼接、重复与长度")

first, second = "Py", "thon"
print(first + second)         # Python（用 + 拼接）
print("=" * 20)              # 打印 20 个等号（用 * 重复）
print("哈" * 3)               # 哈哈哈

name, age = "小明", 18
print(f"{name} 今年 {age} 岁")  # 更推荐用 f-string 拼接变量

print(len("Hello"))           # 5
print(len("你好世界"))         # 4，一个汉字算一个字符

section("4. 索引：取出单个字符")

s = "Python"
print(s[0])      # P，第一个字符（索引从 0 开始）
print(s[3])      # h
print(s[-1])     # n，负索引从右数
print(s[-2])     # o

section("5. 切片：取出一段子串")

s = "Python"
print(s[0:3])     # Pyt（含头不含尾）
print(s[2:5])     # tho
print(s[1:])      # ython（从 1 到末尾）
print(s[:3])      # Pyt（从开头到 3 之前）
print(s[-2:])     # on（最后两个）

# 带步长的切片
s = "0123456789"
print(s[::2])     # 02468（每隔一个取一个）
print(s[::-1])    # 9876543210（步长 -1 表示反转！）

# md 练习题第 1 题
s = "programming"
print(s[:4])      # prog
print(s[-3:])     # ing
print(s[::-1])    # gnimmargorp

section("6. 常用字符串方法")

s = "Hello World"
print(s.upper())      # HELLO WORLD
print(s.lower())      # hello world
print(s.title())      # Hello World（每个单词首字母大写）

s = "   hello   "
print(s.strip())      # 去掉两端空白
print(s.lstrip())     # 只去左边
print(s.rstrip())     # 只去右边

s = "我爱Java，Java很好"
print(s.replace("Java", "Python"))   # 我爱Python，Python很好

s = "hello@example.com"
print(s.find("@"))              # 5，找不到返回 -1
print("@" in s)                 # True，用 in 判断是否包含
print(s.startswith("hello"))    # True
print(s.endswith(".com"))       # True
print(s.count("l"))             # 3

# split：按分隔符切成列表；join：把列表连接成字符串
fruits = "苹果,香蕉,橙子".split(",")
print(fruits)                   # ['苹果', '香蕉', '橙子']
print("-".join(fruits))         # 苹果-香蕉-橙子

# md 练习题第 2 题：规范化姓名
name = "  jOHN  "
print(name.strip().title())     # John

# md 练习题第 3 题：域名提取
email = "student@pku.edu.cn"
print(email.split("@")[1])      # pku.edu.cn

# md 练习题第 4 题：单词计数
sentence = "the quick brown fox jumps over the lazy dog"
print(len(sentence.split()))    # 9

# md 练习题第 5 题：回文判断
s = "level"
print(s == s[::-1])             # True

section("7. 综合小例子：邮箱格式初检")

# 原写法：email = input("请输入邮箱：").strip()；本脚本用固定值演示
email = "student@example.com".strip()
if "@" in email and "." in email:
    user = email.split("@")[0]
    print(f"你好，{user}！邮箱格式看起来没问题。")
else:
    print("这似乎不是一个有效的邮箱。")

print("\n第 04 章演示完毕 ✅")
