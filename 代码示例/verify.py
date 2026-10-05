# -*- coding: utf-8 -*-
"""
一键验证：用当前解释器顺序运行 ch01..ch29 全部配套示例脚本。

用法：
    python verify.py

每章打印 PASS/FAIL（含报错摘要），最后汇总统计；
任一失败则退出码为非 0。
"""

import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).parent

# 章节列表：(编号, 文件名)
SCRIPTS = [
    ("01", "ch01_开发环境搭建.py"),
    ("02", "ch02_变量数据类型与输入输出.py"),
    ("03", "ch03_运算符与表达式.py"),
    ("04", "ch04_字符串处理.py"),
    ("05", "ch05_条件语句.py"),
    ("06", "ch06_循环语句.py"),
    ("07", "ch07_列表与元组.py"),
    ("08", "ch08_字典与集合.py"),
    ("09", "ch09_函数基础.py"),
    ("10", "ch10_函数进阶.py"),
    ("11", "ch11_模块与包.py"),
    ("12", "ch12_文件与目录操作.py"),
    ("13", "ch13_异常处理.py"),
    ("14", "ch14_面向对象编程上.py"),
    ("15", "ch15_面向对象编程下.py"),
    ("16", "ch16_迭代器生成器与装饰器.py"),
    ("17", "ch17_标准库与正则表达式.py"),
    ("18", "ch18_虚拟环境与项目管理.py"),
    ("19", "ch19_NumPy数值计算.py"),
    ("20", "ch20_Pandas数据结构.py"),
    ("21", "ch21_Pandas数据清洗与聚合.py"),
    ("22", "ch22_Matplotlib数据可视化.py"),
    ("23", "ch23_EDA实战.py"),
    ("24", "ch24_sklearn入门.py"),
    ("25", "ch25_线性回归.py"),
    ("26", "ch26_分类算法.py"),
    ("27", "ch27_模型评估与调参.py"),
    ("28", "ch28_聚类与降维.py"),
    ("29", "ch29_综合实战项目.py"),
]


def error_summary(stderr: str, stdout: str) -> str:
    """从输出中提取报错信息摘要（最后一行 Traceback 信息）。"""
    text = (stderr or "") + (stdout or "")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    for ln in reversed(lines):
        if "Error" in ln or "error" in ln.lower():
            return ln.strip()[:200]
    return lines[-1][:200] if lines else "未知错误"


def main() -> int:
    print("=" * 60)
    print(f"开始验证：共 {len(SCRIPTS)} 个脚本，解释器：{sys.executable}")
    print("=" * 60)

    passed, failed = 0, 0
    failures = []
    start_all = time.time()

    for num, fname in SCRIPTS:
        path = BASE / fname
        if not path.exists():
            print(f"[{num}] {fname}: FAIL（文件不存在）")
            failed += 1
            failures.append((num, fname, "文件不存在"))
            continue
        t0 = time.time()
        try:
            proc = subprocess.run(
                [sys.executable, str(path)],
                cwd=BASE,
                capture_output=True,
                text=True,
                timeout=120,
            )
            elapsed = time.time() - t0
            if proc.returncode == 0:
                print(f"[{num}] {fname}: PASS（{elapsed:.1f}s）")
                passed += 1
            else:
                summary = error_summary(proc.stderr, proc.stdout)
                print(f"[{num}] {fname}: FAIL（{elapsed:.1f}s）→ {summary}")
                failed += 1
                failures.append((num, fname, summary))
        except subprocess.TimeoutExpired:
            print(f"[{num}] {fname}: FAIL（超时 120s）")
            failed += 1
            failures.append((num, fname, "超时 120s"))
        except Exception as e:  # noqa: BLE001
            print(f"[{num}] {fname}: FAIL（{e}）")
            failed += 1
            failures.append((num, fname, str(e)[:200]))

    print("=" * 60)
    print(f"验证完成：PASS {passed} / {len(SCRIPTS)}，"
          f"FAIL {failed}，总耗时 {time.time() - start_all:.1f}s")
    if failures:
        print("\n失败明细：")
        for num, fname, summary in failures:
            print(f"  [{num}] {fname}: {summary}")
        return 1
    print("全部通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
