# AGENTS.md

## Cursor Cloud specific instructions

本仓库是一套**中文 Python 教程内容仓库**（Markdown 章节 + 两个可运行示例脚本），没有任何长期运行的服务（无 Web/后端/数据库/API）。所谓“运行应用”即执行 `代码示例/` 下的示例脚本。

### 环境
- Python 3.10+（仓库基于 3.12 编写；VM 自带 3.12）。
- 依赖通过 `requirements.txt` 用 `pip` 安装（numpy / pandas / matplotlib / scikit-learn / jupyter）。
- 更新脚本会在 `.venv/` 中安装依赖。使用前先激活：`source .venv/bin/activate`。
  - 注意：创建 venv 依赖系统包 `python3.12-venv`（一次性系统依赖，不在更新脚本内）。

### 运行示例（端到端验证）
```bash
source .venv/bin/activate
python 代码示例/eda_销售数据分析.py      # 第23章：EDA 数据分析
python 代码示例/ml/churn_project.py       # 第29章：客户流失预测（完整 ML 流程）
```
- EDA 脚本在无图形界面环境下会自动切到 matplotlib `Agg` 后端，并把图表保存到 `代码示例/eda_output/`（该目录已被 `.gitignore` 忽略）。
- ML 脚本会在 `代码示例/ml/churn_model.joblib` 保存模型（同样被 `.gitignore` 忽略）。

### 无 lint / test / build
仓库没有定义 lint、自动化测试或构建命令（无 `pyproject.toml`/`Makefile`/`package.json`/CI）。练习题与答案内嵌在 Markdown 章节中，并非自动化测试。验证“可运行”即运行上面两个脚本。
