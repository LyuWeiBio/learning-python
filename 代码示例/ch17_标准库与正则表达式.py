# -*- coding: utf-8 -*-
"""
第 17 章：常用标准库与正则表达式
对应教材：第二部分-Python进阶/17-常用标准库与正则表达式.md

演示：json 转换与读写、Counter 与 defaultdict、os/pathlib
      （只在脚本同目录 output/ 下操作）、re 查找替换、文本分析综合示例。
"""

from pathlib import Path

WORK = Path(__file__).parent / "output"
WORK.mkdir(parents=True, exist_ok=True)


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. json：数据交换的通用格式")

import json

data = {
    "name": "小明",
    "age": 18,
    "hobbies": ["篮球", "编程"],
    "is_student": True,
}

# Python 字典 → JSON 字符串（ensure_ascii=False 让中文正常显示）
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)

# JSON 字符串 → Python 字典
obj = json.loads(json_str)
print(obj["name"])       # 小明
print(obj["hobbies"][0]) # 篮球

# 读写 JSON 文件
with open(WORK / "data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
with open(WORK / "data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print("从文件读回：", loaded["name"])

section("2. collections：Counter 与 defaultdict")

from collections import Counter, defaultdict

words = "apple banana apple cherry banana apple".split()
counter = Counter(words)
print(counter)                    # Counter({'apple': 3, ...})
print(counter["apple"])           # 3
print(counter.most_common(2))     # 出现最多的前 2 个
print(Counter("mississippi"))

# defaultdict：自动给不存在的键一个默认值
words = ["apple", "avocado", "banana", "cherry", "cranberry"]
groups = defaultdict(list)        # 默认值是空列表
for w in words:
    groups[w[0]].append(w)        # 不用先判断键是否存在
print(dict(groups))

# md 练习题第 3 题：按姓氏分组
from collections import defaultdict
names = ["张伟", "李娜", "张强", "王芳", "李明", "王磊"]
groups = defaultdict(list)
for name in names:
    groups[name[0]].append(name)
print(dict(groups))

section("3. os 与 pathlib")

import os

print("当前工作目录：", os.getcwd())
print("output 目录文件：", os.listdir(WORK))
print("data.json 存在？", os.path.exists(WORK / "data.json"))

# glob：遍历当前目录下所有 .py 文件
for py_file in Path(__file__).parent.glob("ch*.py"):
    pass
print("ch*.py 示例脚本数量：",
      len(list(Path(__file__).parent.glob("ch*.py"))))

section("4. 正则表达式：re 查找与替换")

import re

text = "我的电话是 138-1234-5678，备用 139-8888-6666。"

# findall：找出所有匹配，返回列表
phones = re.findall(r"\d{3}-\d{4}-\d{4}", text)
print(phones)        # ['138-1234-5678', '139-8888-6666']

# search：找第一个匹配（找不到返回 None）
m = re.search(r"\d{3}", text)
if m:
    print(m.group())    # 138

# sub：替换
print(re.sub(r"\d{4}", "****", text))     # 把 4 位连续数字替换成 ****

# split：按模式切分
print(re.split(r"[，。]", text))          # 按中文逗号句号切分

# 提取邮箱
text2 = "联系 alice@example.com 或 bob@test.org 咨询"
emails = re.findall(r"[\w.]+@[\w.]+\.\w+", text2)
print(emails)

# md 练习题第 4 题：提取所有数字
s = "订单A123共99元，订单B456共150元"
print(re.findall(r"\d+", s))     # ['123', '99', '456', '150']

# md 练习题第 5 题：校验手机号
def is_phone(s):
    return bool(re.fullmatch(r"1\d{10}", s))

print(is_phone("13812345678"))   # True
print(is_phone("023-8888"))      # False

section("5. 综合示例：文本词频分析")

text = """Python is great. Python is easy.
I love Python and data science. Data science uses Python."""

words = re.findall(r"[a-zA-Z]+", text.lower())   # 提取单词并转小写
counter = Counter(words)
print("总词数：", len(words))
print("出现最多的 3 个词：", counter.most_common(3))

# md 练习题第 1 题：JSON 往返 + 平均分
data = {"name": "小明", "age": 18, "scores": [88, 92, 79]}
with open(WORK / "student.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
with open(WORK / "student.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
scores = loaded["scores"]
print(f"平均分：{sum(scores) / len(scores):.1f}")

print("\n第 17 章演示完毕 ✅")
