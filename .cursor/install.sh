#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# 第 18 章示例脚本需要 venv 模块（Ubuntu 默认镜像未预装）
if ! python3 -c "import ensurepip" 2>/dev/null; then
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3.12-venv
fi

python3 -m pip install --break-system-packages -r requirements.txt
