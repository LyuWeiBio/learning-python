#!/usr/bin/env bash
# 为 Cloud Agent / 新机器准备本教程的运行环境：
#   1. 确认有 Python 3.10+（缺失时尝试用 apt 安装）
#   2. 确认 pip 可用、venv 可用（第 18 章示例要用）
#   3. 安装 requirements.txt 里的第三方库，装完后逐个验证能否导入
#
# 设计原则：可重复运行；网络失败自动重试；只有核心库装不上才算失败，
# 可选部分（jupyter、python 命令别名等）失败只给警告。
#
# 可用环境变量：
#   PYTHON=python3.12   指定使用的解释器（默认 python3）
#   PIP_INDEX_URL=...   指定 PyPI 镜像（pip 原生支持）
set -Eeuo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
REPO_DIR="$(pwd)"
REQ_FILE="$REPO_DIR/requirements.txt"
PYTHON="${PYTHON:-python3}"
CORE_MODULES=(numpy pandas matplotlib sklearn)
FALLBACK_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"
WARNINGS=()

log()  { printf '[install] %s\n' "$*"; }
warn() { printf '[install] 警告：%s\n' "$*" >&2; WARNINGS+=("$*"); }
die()  { printf '[install] 错误：%s\n' "$*" >&2; exit 1; }
trap 'printf "[install] 错误：第 %s 行的命令失败（退出码 %s）\n" "$LINENO" "$?" >&2' ERR

[[ -f "$REQ_FILE" ]] || die "找不到 $REQ_FILE"

# ---------- 权限与 apt ----------
if [[ "$(id -u)" -eq 0 ]]; then
  CAN_ROOT=1
elif command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
  CAN_ROOT=1
else
  CAN_ROOT=0
fi

as_root() {
  if [[ "$(id -u)" -eq 0 ]]; then
    "$@"
  else
    # sudo 默认会清掉代理变量，这里显式带过去
    local -a keep=()
    local v
    for v in http_proxy https_proxy HTTP_PROXY HTTPS_PROXY no_proxy NO_PROXY; do
      [[ -n "${!v:-}" ]] && keep+=("$v=${!v}")
    done
    sudo -n env "${keep[@]+"${keep[@]}"}" "$@"
  fi
}

have_apt() { command -v apt-get >/dev/null 2>&1 && [[ "$CAN_ROOT" -eq 1 ]]; }

retry() {  # retry <次数> <命令...>：失败后等待 5、10、20… 秒再试
  local tries="$1" n=1 delay=5
  shift
  until "$@"; do
    if (( n >= tries )); then
      return 1
    fi
    log "第 $n 次失败，${delay} 秒后重试：$*"
    sleep "$delay"
    n=$((n + 1)); delay=$((delay * 2))
  done
}

APT_UPDATED=0
apt_install() {  # apt_install <包名...>：全部装上返回 0
  have_apt || return 1
  local -a apt_opts=(-o DPkg::Lock::Timeout=300 -o Acquire::Retries=3)
  if [[ "$APT_UPDATED" -eq 0 ]]; then
    log "apt-get update ..."
    retry 3 as_root env DEBIAN_FRONTEND=noninteractive apt-get "${apt_opts[@]}" update -qq || return 1
    APT_UPDATED=1
  fi
  log "apt-get install $*"
  retry 2 as_root env DEBIAN_FRONTEND=noninteractive \
    apt-get "${apt_opts[@]}" install -y -qq --no-install-recommends "$@"
}

# ---------- 1. Python ----------
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  log "没有找到 $PYTHON，尝试用 apt 安装 python3 ..."
  apt_install python3 python3-pip python3-venv || die "没有 $PYTHON，且无法自动安装。请先安装 Python 3.10 或更新版本。"
fi
PY_VER="$("$PYTHON" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
"$PYTHON" -c 'import sys; sys.exit(sys.version_info < (3, 10))' \
  || die "本教程需要 Python 3.10+，当前 $PYTHON 是 $PY_VER。可以用 PYTHON=python3.12 bash $0 指定其他解释器。"
log "使用 $(command -v "$PYTHON")（Python $PY_VER）"

# ---------- 2. venv（第 18 章示例会创建虚拟环境） ----------
venv_works() {
  local tmp ok=1
  tmp="$(mktemp -d)"
  "$PYTHON" -m venv "$tmp/venv" >/dev/null 2>&1 && ok=0
  rm -rf "$tmp"
  return "$ok"
}
if ! venv_works; then
  log "venv 模块不可用，尝试安装 python${PY_VER}-venv ..."
  apt_install "python${PY_VER}-venv" || apt_install python3-venv || true
  venv_works || warn "venv 仍不可用：第 18 章创建虚拟环境的示例会失败（不影响其他章节）。"
fi

# ---------- 3. pip ----------
pip_works() { "$PYTHON" -m pip --version >/dev/null 2>&1; }
if ! pip_works; then
  log "pip 不可用，尝试安装 ..."
  apt_install python3-pip || true
fi
if ! pip_works; then
  log "尝试用 get-pip.py 安装 pip ..."
  tmp_getpip="$(mktemp)"
  if retry 3 "$PYTHON" -c 'import sys, urllib.request; urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", sys.argv[1])' "$tmp_getpip"; then
    user_flag=()
    [[ "$(id -u)" -eq 0 ]] || user_flag=(--user)
    PIP_BREAK_SYSTEM_PACKAGES=1 "$PYTHON" "$tmp_getpip" "${user_flag[@]+"${user_flag[@]}"}" -q || true
  fi
  rm -f "$tmp_getpip"
fi
pip_works || die "无法为 $PYTHON 准备 pip。请手动安装（例如 sudo apt-get install python3-pip）后重试。"
log "$("$PYTHON" -m pip --version)"

# ---------- 4. 安装 requirements.txt ----------
# 一次性环境里直接装进系统 Python，这样 python3 不用激活虚拟环境就能导入。
# PIP_BREAK_SYSTEM_PACKAGES 用环境变量而不是命令行参数：老版本 pip 不认识
# --break-system-packages 会直接报错，而环境变量会被安全地忽略。
export PIP_BREAK_SYSTEM_PACKAGES=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_INPUT=1
export PIP_DEFAULT_TIMEOUT="${PIP_DEFAULT_TIMEOUT:-60}"

pip_install() {  # pip_install <额外参数...>
  "$PYTHON" -m pip install -q "$@"
}

core_req="$(mktemp)"
grep -viE '^[[:space:]]*jupyter' "$REQ_FILE" >"$core_req" || true

installed=0
if retry 3 pip_install -r "$REQ_FILE"; then
  installed=1
elif retry 2 pip_install --ignore-installed -r "$REQ_FILE"; then
  # 常见原因：系统自带的旧版库（apt 装的）无法被 pip 卸载
  installed=1
elif [[ -z "${PIP_INDEX_URL:-}" ]] && retry 2 pip_install -i "$FALLBACK_INDEX_URL" -r "$REQ_FILE"; then
  warn "默认 PyPI 源安装失败，已改用镜像 $FALLBACK_INDEX_URL 完成安装。"
  installed=1
elif retry 2 pip_install -r "$core_req"; then
  warn "完整依赖装不上，已只安装核心库（跳过 jupyter）。"
  installed=1
fi
rm -f "$core_req"
[[ "$installed" -eq 1 ]] || die "安装 requirements.txt 失败，请查看上面 pip 的报错。"

# ---------- 5. 可选：让 python 命令也可用（教程里的命令写的是 python） ----------
if ! command -v python >/dev/null 2>&1 && [[ "$PYTHON" == "python3" ]]; then
  apt_install python-is-python3 >/dev/null 2>&1 \
    || warn "没有 python 命令，请把教程里的 python 换成 python3 使用。"
fi

# ---------- 6. 验证 ----------
missing=()
for m in "${CORE_MODULES[@]}"; do
  "$PYTHON" -c "import $m" >/dev/null 2>&1 || missing+=("$m")
done
(( ${#missing[@]} == 0 )) || die "安装后仍无法导入：${missing[*]}"

"$PYTHON" - <<'PY'
import numpy, pandas, matplotlib, sklearn
print("[install] numpy %s | pandas %s | matplotlib %s | scikit-learn %s" % (
    numpy.__version__, pandas.__version__, matplotlib.__version__, sklearn.__version__))
PY

if (( ${#WARNINGS[@]} )); then
  log "完成，但有 ${#WARNINGS[@]} 条警告（见上方）。"
else
  log "完成。可运行 $PYTHON 代码示例/verify.py 验证全部示例。"
fi
