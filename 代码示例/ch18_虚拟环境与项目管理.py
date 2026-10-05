# -*- coding: utf-8 -*-
"""
第 18 章：虚拟环境与项目管理
对应教材：第二部分-Python进阶/18-虚拟环境与项目管理.md

演示：pip 常用命令（只读版本，安全）、用 venv 创建虚拟环境
      （在临时目录，不联网）、requirements.txt 的读写、
      规范项目结构示意、PEP 8 命名规范、类型注解。
注：md 中「pip install requests」等联网安装命令只作为文本说明打印，
    本脚本不实际执行，以保证离线可运行。
"""


def section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


section("1. pip：包管理工具（只读演示）")

import subprocess
import sys

# 最稳妥的写法：python -m pip（明确用当前 Python 的 pip）
print(subprocess.run(
    [sys.executable, "-m", "pip", "--version"],
    capture_output=True, text=True).stdout.strip())

# pip list 查看已安装的库（只读，不安装/卸载任何东西）
out = subprocess.run(
    [sys.executable, "-m", "pip", "list", "--format=freeze"],
    capture_output=True, text=True).stdout
print("已安装的库（前 5 行）：")
print("\n".join(out.splitlines()[:5]))

print("\n常用 pip 命令（说明，md 18.1 节）：")
print("  pip install requests          # 安装第三方库（需联网）")
print("  pip install numpy pandas      # 一次装多个")
print('  pip install "django>=4.0"     # 指定版本')
print("  pip uninstall requests        # 卸载")
print("  pip list                      # 查看已安装的库")
print("  pip show numpy                # 查看某个库的详细信息")

section("2. 用 venv 创建虚拟环境（临时目录演示）")

import tempfile

tmpdir = tempfile.mkdtemp(prefix="ch18_venv_")
venv_path = tempfile.mkdtemp(prefix="demo_venv_")  # 放置 venv 的临时父目录
import os

venv_dir = os.path.join(venv_path, ".venv")
# 创建虚拟环境（不联网；3.12 下很快）
subprocess.run([sys.executable, "-m", "venv", venv_dir],
               check=True, capture_output=True)
print("虚拟环境已创建：", venv_dir)
print("目录内容：", sorted(os.listdir(venv_dir)))
# 注：真实使用中用「source .venv/bin/activate」激活，本脚本演示创建即可

section("3. requirements.txt：依赖清单")

from pathlib import Path

req_path = Path(tmpdir) / "requirements.txt"
# 导出当前环境的依赖（冻结版本）
with open(req_path, "w", encoding="utf-8") as f:
    subprocess.run([sys.executable, "-m", "pip", "freeze"],
                   stdout=f, check=True)
print("requirements.txt 已生成，前 3 行：")
print("\n".join(req_path.read_text(encoding="utf-8").splitlines()[:3]))

# requirements.txt 里两种写法含义（md 练习题第 2 题）
print("\n写法区别：")
print("  pandas==2.2.0  → 锁定精确版本，保证可复现")
print("  pandas>=2.0    → 最低版本要求，灵活但结果可能随时间变化")
print("安装清单命令：pip install -r requirements.txt")

section("4. 规范的项目结构")

print("""
my_project/
├── .venv/                # 虚拟环境（不提交 git，写进 .gitignore）
├── .gitignore            # git 忽略清单
├── README.md             # 项目说明
├── requirements.txt      # 依赖清单
├── src/                  # 源代码
│   ├── __init__.py
│   ├── main.py           # 程序入口（用 if __name__ == "__main__":）
│   └── utils.py          # 工具函数
└── tests/                # 测试代码
    └── test_utils.py
""")

section("5. PEP 8：代码风格与命名规范")


# md 练习题第 4 题：改正不符合 PEP 8 的命名
class MyClass:                 # 类名用 CapWords（大驼峰）
    def get_value(self):       # 方法用 snake_case
        max_count = 10         # 变量用 snake_case
        return max_count


print(MyClass().get_value())

section("6. 类型注解（Type Hints）")


def greet(name: str, times: int = 1) -> str:
    return f"你好，{name}！" * times


age: int = 18
scores: list[int] = [88, 92, 79]


def average(nums: list[float]) -> float:
    return sum(nums) / len(nums)


print(greet("小明", 2))
print(f"平均分：{average(scores):.1f}")


# md 练习题第 3 题：补上类型注解
def repeat(text: str, n: int) -> str:
    return text * n


print(repeat("ab", 3))

print("\n第 18 章演示完毕 ✅")
