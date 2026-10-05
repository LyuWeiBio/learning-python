# -*- coding: utf-8 -*-
"""
第 12 章：文件与目录操作
对应教材：第二部分-Python进阶/12-文件与目录操作.md

演示：open() 读写与追加模式、with 语句、逐行读取、pathlib、
      csv 读写、综合示例（日志记录器）。
注：所有演示文件都写在脚本同目录的 output/ 下，不污染仓库其它位置。
"""

from pathlib import Path

# 脚本同目录的 output/ 作为工作目录
WORK = Path(__file__).parent / "output"
WORK.mkdir(parents=True, exist_ok=True)


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. 写入与读取（with 语句）")

# 写入：w 模式会清空原文件；处理中文务必指定 utf-8 编码
with open(WORK / "test.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")
# with 块结束，文件自动关闭，无需手动 close()

# 追加：a 模式不清空原文件，在末尾追加
with open(WORK / "test.txt", "a", encoding="utf-8") as f:
    f.write("追加的第三行\n")

# 一次性读取全部
with open(WORK / "test.txt", "r", encoding="utf-8") as f:
    print(f.read())

section("2. 写入多行与逐行读取")

lines = ["苹果", "香蕉", "橙子"]
with open(WORK / "fruits.txt", "w", encoding="utf-8") as f:
    for fruit in lines:
        f.write(fruit + "\n")       # write 不会自动加换行，要手动加 \n

with open(WORK / "fruits.txt", "a", encoding="utf-8") as f:
    f.write("葡萄\n")

# 逐行读取（推荐处理大文件，省内存）
with open(WORK / "fruits.txt", "r", encoding="utf-8") as f:
    for line in f:
        print("水果：", line.strip())   # strip() 去掉每行末尾的换行符

# 读成列表
with open(WORK / "fruits.txt", "r", encoding="utf-8") as f:
    print(f.readlines())               # ['苹果\n', '香蕉\n', ...]

section("3. 用 pathlib 处理路径")

p = WORK / "fruits.txt"                # 用 / 拼接路径，跨平台
print("路径：", p)
print("存在？", p.exists())
print("文件名：", p.name)
print("扩展名：", p.suffix)
print("父目录：", p.parent.name)

# 创建目录（parents=True 自动创建多级，exist_ok=True 已存在也不报错）
Path(WORK / "data").mkdir(parents=True, exist_ok=True)

# pathlib 直接读写小文件
Path(WORK / "hello.txt").write_text("你好", encoding="utf-8")
print(Path(WORK / "hello.txt").read_text(encoding="utf-8"))

# 安全读取：文件存在才读
def safe_read(path):
    p = Path(path)
    if p.exists():
        return p.read_text(encoding="utf-8")
    return "文件不存在"

print(safe_read(WORK / "hello.txt"))
print(safe_read(WORK / "不存在.txt"))

section("4. 读写 CSV 文件")

import csv

data = [
    ["姓名", "年龄", "城市"],
    ["小明", 18, "北京"],
    ["小红", 20, "上海"],
]
# 写 CSV 时加 newline=""，避免 Windows 出现多余空行
with open(WORK / "people.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(data)

with open(WORK / "people.csv", "r", encoding="utf-8") as f:
    for row in csv.reader(f):
        print(row)                     # 每行是一个列表

# md 练习题第 5 题：成绩写入 CSV 再算平均分
records = [["姓名", "成绩"], ["小明", 88], ["小红", 95], ["小刚", 72]]
with open(WORK / "scores.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(records)

scores = []
with open(WORK / "scores.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)                       # 跳过表头
    for row in reader:
        scores.append(int(row[1]))
print(f"平均分：{sum(scores) / len(scores):.1f}")   # 85.0

section("5. 综合示例：日志记录器")

from datetime import datetime

def log(message, filename=None):
    """把带时间戳的日志追加到文件。"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

log("程序启动", WORK / "app.log")
log("用户登录", WORK / "app.log")
log("程序结束", WORK / "app.log")

with open(WORK / "app.log", "r", encoding="utf-8") as f:
    print(f.read())

# md 练习题第 1 题：把 1~10 写入 numbers.txt 再求和
with open(WORK / "numbers.txt", "w", encoding="utf-8") as f:
    for i in range(1, 11):
        f.write(f"{i}\n")

total = 0
with open(WORK / "numbers.txt", "r", encoding="utf-8") as f:
    for line in f:
        total += int(line.strip())
print("1~10 的和：", total)            # 55

print("\n第 12 章演示完毕 ✅")
