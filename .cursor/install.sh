#!/usr/bin/env bash
# 被 sh / dash 调用时（例如写成 "sh .cursor/install.sh"）自动改用 bash 重新执行
if [ -z "${BASH_VERSION:-}" ]; then exec bash "$0" "$@"; fi
#
# 为 Cursor Cloud Agent（以及其他新机器）准备本教程的运行环境：
#   1. 确认有 Python 3.10+（缺失时尝试用 apt 安装）
#   2. 确认 venv 可用（第 18 章示例要创建虚拟环境）、pip 可用
#   3. 安装 requirements.txt 里的第三方库，装完逐个验证能否导入
#
# 设计原则：
#   - 可重复运行（幂等），第二次运行只需几秒
#   - apt 被占用时等待；某个软件源坏掉时继续用其余的源；网络错误自动重试
#   - 必需项（Python、pip、核心库）装不上就失败退出，并给出中文原因
#   - 可选项（jupyter、python 命令别名）装不上只给警告
#   - 在 Cursor Cloud 上自动启用严格模式：venv 不可用也算失败。
#     Build 失败时 Cursor 会继续使用上一个成功的 Build，而“带着警告的成功”会顶替它。
#
# 可用环境变量：
#   PYTHON=python3.12   指定使用的解释器（默认 python3）
#   USE_CN_MIRROR=1     PyPI 连不上时改用清华镜像（默认不切换，以免绕过你自己的源）
#   STRICT=1 / 0        强制开启 / 关闭严格模式
#   PIP_INDEX_URL 等    pip 的原生配置（环境变量或 pip.conf）都会被沿用
set -Eeuo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}" 2>/dev/null || printf '%s' "${BASH_SOURCE[0]}")"
cd "$(dirname "$SCRIPT_PATH")/.."
REPO_DIR="$(pwd)"
REQ_FILE="$REPO_DIR/requirements.txt"
PYTHON="${PYTHON:-python3}"
CORE_MODULES=(numpy pandas matplotlib sklearn)
CN_MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple"
WARNINGS=()

if [[ -z "${STRICT:-}" ]]; then
  if [[ -n "${CURSOR_AGENT_SOCKET:-}" || -e /run/cursor/api.sock || -d /run/cursor ]]; then
    STRICT=1
  else
    STRICT=0
  fi
fi

log()  { printf '[install] %s\n' "$*"; }
warn() { printf '[install] 警告：%s\n' "$*" >&2; WARNINGS+=("$*"); }
die()  { printf '[install] 错误：%s\n' "$*" >&2; exit 1; }
# 只在主 shell 里报告（否则 $(...) 里的失败会报两遍）
on_err() { (( BASH_SUBSHELL )) || printf '[install] 错误：第 %s 行的命令失败（退出码 %s）\n' "$2" "$1" >&2; }
trap 'on_err "$?" "$LINENO"' ERR

# 所有临时文件放在一个目录里，任何方式退出都会清理
TMP_ROOT=""
trap '[[ -z "$TMP_ROOT" ]] || rm -rf "$TMP_ROOT"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
# TMPDIR 指向不存在的目录时退回 /tmp
TMP_ROOT="$(mktemp -d 2>/dev/null || mktemp -d /tmp/lp-install.XXXXXX)" || die "无法创建临时目录"

[[ -f "$REQ_FILE" ]] || die "找不到 $REQ_FILE"
log "仓库目录：$REPO_DIR（严格模式：$([[ "$STRICT" == 1 ]] && echo 开 || echo 关)）"

retry() {  # retry <次数> <命令...>：失败后等待 5、10、20… 秒再试
  local tries="$1" n=1 delay=5
  shift
  until "$@"; do
    (( n >= tries )) && return 1
    log "第 $n 次失败，${delay} 秒后重试：$*"
    sleep "$delay"
    n=$((n + 1)); delay=$((delay * 2))
  done
}

# ---------- 权限与 apt ----------
if [[ "$(id -u)" -eq 0 ]]; then
  CAN_ROOT=1
elif command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
  CAN_ROOT=1
else
  CAN_ROOT=0   # 没有 root 也没有免密 sudo：只能跳过所有 apt 步骤
fi

as_root() {
  if [[ "$(id -u)" -eq 0 ]]; then
    "$@"
  else
    # sudo 默认会清掉代理变量，这里显式带过去
    local -a keep=()
    local v
    for v in http_proxy https_proxy HTTP_PROXY HTTPS_PROXY no_proxy NO_PROXY all_proxy ALL_PROXY; do
      [[ -n "${!v:-}" ]] && keep+=("$v=${!v}")
    done
    sudo -n env "${keep[@]+"${keep[@]}"}" "$@"
  fi
}

have_apt() { command -v apt-get >/dev/null 2>&1 && [[ "$CAN_ROOT" -eq 1 ]]; }

# LC_ALL=C：下面要按英文原文判断 apt 的报错（中文系统里 apt 会输出中文）
apt_run() {
  as_root env LC_ALL=C DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=a apt-get \
    -o DPkg::Lock::Timeout=300 -o Acquire::Retries=3 \
    -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold "$@" </dev/null
}

APT_UPDATED=0   # 本次运行是否已经 update 过
APT_INDEX_OK=0  # 那次 update 是否干净（没有任何源下载失败）
apt_update() {
  # update 失败也继续用现有索引去 install：一个坏掉的第三方源 / PPA 就会让 update
  # 返回非 0，但官方源的索引通常已经更新好了。反过来，网络不通时 update 常常只打印
  # W: 警告、退出码仍是 0，所以这里看输出而不是只看退出码。
  local i out rc
  APT_UPDATED=1
  APT_INDEX_OK=0
  log "apt-get update ..."
  # DPkg::Lock::Timeout 管不到 update 用的 /var/lib/apt/lists/lock，
  # 开机后的 apt-daily / unattended-upgrades 常常占着它，这里自己等（最多约 5 分钟）
  for (( i = 1; i <= 30; i++ )); do
    rc=0
    out="$(apt_run update -qq 2>&1)" || rc=$?
    if (( rc != 0 )) && grep -q 'Could not get lock' <<<"$out"; then
      (( i == 1 )) && log "apt 正被其他进程使用（可能是系统自动更新），等待它结束 ..."
      sleep 10
      continue
    fi
    [[ -z "$out" ]] || printf '%s\n' "$out" >&2
    if (( rc == 0 )) && ! grep -qE '^(W|E|Err):' <<<"$out"; then
      APT_INDEX_OK=1
    else
      log "apt-get update 没有完全成功（见上方），先用现有的软件包索引继续。"
    fi
    return 0
  done
  log "等待 apt 锁超时，先用现有的软件包索引继续。"
}

apt_install() {  # apt_install <包名...>：全部装上返回 0
  have_apt || return 1
  local n out
  for n in 1 2 3; do
    (( APT_UPDATED )) || apt_update
    log "apt-get install $*"
    if out="$(apt_run install -y -qq --no-install-recommends "$@" 2>&1)"; then
      return 0
    fi
    printf '%s\n' "$out" >&2
    if grep -q "dpkg was interrupted" <<<"$out"; then
      log "上次的软件包安装被中断过，先执行 dpkg --configure -a 修复 ..."
      as_root env LC_ALL=C DEBIAN_FRONTEND=noninteractive \
        dpkg --force-confdef --force-confold --configure -a </dev/null >&2 || true
      continue
    fi
    # 索引是完整的、只是确实没有这个包：重试没有意义
    if (( APT_INDEX_OK )) && grep -qE 'Unable to locate package|has no installation candidate' <<<"$out"; then
      return 1
    fi
    (( n < 3 )) || break
    # 其余情况（网络中断、索引过期导致 .deb 404 ……）：稍等后重新 update 再试
    log "apt-get install 失败，$((n * 10)) 秒后重新 update 再试 ..."
    sleep $((n * 10))
    APT_UPDATED=0
  done
  return 1
}

# ---------- 1. Python ----------
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  case "$PYTHON" in
    python3)      py_pkgs=(python3 python3-pip python3-venv) ;;
    python3.[0-9]*) py_pkgs=("$PYTHON" "$PYTHON-venv") ;;  # 例如 PYTHON=python3.12
    *)            py_pkgs=() ;;
  esac
  if (( ${#py_pkgs[@]} )); then
    log "没有找到 $PYTHON，尝试用 apt 安装 ${py_pkgs[*]} ..."
    apt_install "${py_pkgs[@]}" || true
  fi
  command -v "$PYTHON" >/dev/null 2>&1 \
    || die "没有 $PYTHON，且无法自动安装。请先安装 Python 3.10 或更新版本。"
fi
PY_VER="$("$PYTHON" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
if ! "$PYTHON" -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
  newer=""
  for v in 3.14 3.13 3.12 3.11 3.10; do
    command -v "python$v" >/dev/null 2>&1 && { newer="python$v"; break; }
  done
  if [[ -n "$newer" ]]; then
    die "本教程需要 Python 3.10+，当前 $PYTHON 是 $PY_VER。检测到 $newer，可以运行：PYTHON=$newer bash $SCRIPT_PATH"
  fi
  die "本教程需要 Python 3.10+，当前 $PYTHON 是 $PY_VER，系统里也没有更新的版本。请换用 Ubuntu 22.04 / Debian 12 或更新的系统，或者先安装 Python 3.10+。"
fi
log "使用 $(command -v "$PYTHON")（Python $PY_VER）"

# ---------- 2. venv（第 18 章示例会创建带 pip 的虚拟环境） ----------
venv_works() {
  local d="$TMP_ROOT/venv-check" ok=1
  rm -rf "$d"
  "$PYTHON" -m venv "$d" >/dev/null 2>&1 && ok=0
  rm -rf "$d"
  return "$ok"
}
if ! venv_works; then
  log "venv 模块不可用，尝试安装 python${PY_VER}-venv ..."
  apt_install "python${PY_VER}-venv" || apt_install python3-venv || true
  if ! venv_works; then
    msg="venv 不可用，第 18 章创建虚拟环境的示例会失败。请用管理员权限安装 python${PY_VER}-venv（例如 sudo apt-get install python${PY_VER}-venv）。"
    [[ "$STRICT" == 1 ]] && die "$msg"
    warn "$msg"
  fi
fi

# ---------- 3. pip ----------
pip_works() { "$PYTHON" -m pip --version >/dev/null 2>&1; }
# 只有 site-packages 写不进去时才用 --user（在虚拟环境里用 --user 会直接报错）
user_flag=()
if [[ "$(id -u)" -ne 0 ]] && ! "$PYTHON" -c 'import os, sys, sysconfig
p = sysconfig.get_paths()["purelib"]
while not os.path.exists(p): p = os.path.dirname(p)
sys.exit(not os.access(p, os.W_OK))' 2>/dev/null; then
  user_flag=(--user)
fi
if ! pip_works; then
  log "pip 不可用，尝试安装 ..."
  apt_install python3-pip || true
fi
if ! pip_works; then
  # 非 Debian 系的 Python（官方安装包、pyenv、Fedora 等）自带 ensurepip，不需要联网
  "$PYTHON" -m ensurepip --upgrade "${user_flag[@]+"${user_flag[@]}"}" >/dev/null 2>&1 || true
fi
# 从 PyPI 下载 pip 的 wheel，直接用它安装自己：只需要能访问 PyPI
# （不少受限网络只放行 pypi.org / files.pythonhosted.org，bootstrap.pypa.io 反而不通）
bootstrap_pip_from_wheel() {
  local whl
  # 选“支持当前 Python 的最新版 pip”，而不是盲目取最新版（新版 pip 会陆续放弃老的 Python）
  whl="$("$PYTHON" - "$TMP_ROOT" <<'PY'
import json, os, re, sys, urllib.request as u
m = json.load(u.urlopen("https://pypi.org/pypi/pip/json", timeout=60))
def fits(spec):  # pip 的 requires_python 只用 ">=3.x" 这种写法
    return all(sys.version_info[:2] >= tuple(map(int, v.split(".")))
               for v in re.findall(r">=\s*(\d+\.\d+)", spec or ""))
stable = [v for v in m["releases"] if re.fullmatch(r"\d+(\.\d+)*", v)]
for v in sorted(stable, key=lambda s: tuple(map(int, s.split("."))), reverse=True):
    files = [f for f in m["releases"][v] if f["packagetype"] == "bdist_wheel"
             and not f.get("yanked") and fits(f.get("requires_python"))]
    if files:
        url = files[0]["url"]
        break
else:
    sys.exit(1)
p = os.path.join(sys.argv[1], url.rsplit("/", 1)[1])
with open(p, "wb") as f:
    f.write(u.urlopen(url, timeout=120).read())
print(p)
PY
)" || return 1
  PIP_BREAK_SYSTEM_PACKAGES=1 "$PYTHON" "$whl/pip" install -q --no-index "${user_flag[@]+"${user_flag[@]}"}" "$whl"
}
bootstrap_get_pip() {
  local getpip="$TMP_ROOT/get-pip.py" url
  # 老版本 Python 要用 pip/<版本>/get-pip.py（不存在时会 404，再用通用版本）
  for url in "https://bootstrap.pypa.io/pip/$PY_VER/get-pip.py" "https://bootstrap.pypa.io/get-pip.py"; do
    # 必须带超时：urlretrieve 默认没有超时，代理不回应时会永远卡住
    "$PYTHON" -c 'import sys, urllib.request as u; open(sys.argv[2], "wb").write(u.urlopen(sys.argv[1], timeout=60).read())' "$url" "$getpip" 2>/dev/null \
      && PIP_BREAK_SYSTEM_PACKAGES=1 "$PYTHON" "$getpip" "${user_flag[@]+"${user_flag[@]}"}" -q \
      && return 0
  done
  return 1
}
if ! pip_works; then
  log "从 PyPI 下载 pip 安装 ..."
  retry 2 bootstrap_pip_from_wheel || true
fi
if ! pip_works; then
  log "尝试用 get-pip.py 安装 pip ..."
  retry 2 bootstrap_get_pip || true
fi
pip_works || die "无法为 $PYTHON 准备 pip。请手动安装（例如 sudo apt-get install python3-pip）后重试。"
log "$("$PYTHON" -m pip --version)"

# ---------- 4. 安装 requirements.txt ----------
# 一次性环境里直接装进系统 Python，这样 python3 不用激活虚拟环境就能导入。
# PIP_BREAK_SYSTEM_PACKAGES 用环境变量而不是命令行参数：老版本 pip 不认识
# --break-system-packages 会直接报错，而环境变量会被安全地忽略。
export PIP_BREAK_SYSTEM_PACKAGES=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_INPUT=1 PIP_ROOT_USER_ACTION=ignore
export PIP_DEFAULT_TIMEOUT="${PIP_DEFAULT_TIMEOUT:-60}"

index_configured() {  # 用户自己配置了软件源（环境变量或 pip.conf）
  [[ -n "${PIP_INDEX_URL:-}${PIP_EXTRA_INDEX_URL:-}${PIP_FIND_LINKS:-}${PIP_NO_INDEX:-}" ]] && return 0
  # 先存下输出再匹配：直接接 grep -q 时 pip 可能被 SIGPIPE 打断，pipefail 下会误判为“没配置”
  local cfg
  cfg="$("$PYTHON" -m pip config list 2>/dev/null)" || true
  grep -qiE '\.(index-url|extra-index-url|find-links|no-index)=' <<<"$cfg"
}
index_reachable() {  # 用 pip 自己的网络设置（代理、证书、pip.conf）探测软件源，最多约 1 分钟
  local i
  for i in 1 2 3; do
    # --no-cache-dir：不然 10 分钟内访问过的索引页会直接从缓存返回，测不出网络
    "$PYTHON" -m pip index versions pip --no-cache-dir --retries 0 --timeout 15 >/dev/null 2>&1 && return 0
    (( i < 3 )) && sleep $((i * 5))
  done
  return 1
}
net_hint() {
  if index_configured; then
    printf '连不上你配置的 pip 软件源（PIP_INDEX_URL 或 pip.conf），请检查网络、代理和源地址。'
  else
    printf '连不上 pypi.org，请检查网络或代理设置。在国内网络可以用镜像重试：USE_CN_MIRROR=1 bash %s' "$SCRIPT_PATH"
  fi
}
# 先花几秒探测网络。连不上时不立刻放弃（本地缓存里可能已经有全部安装包），
# 但让 pip 不重试、缩短超时：否则每个请求重试 5 次、每次等 60 秒，累计要等十几分钟才失败
NET_DOWN=0
if "$PYTHON" -m pip index --help >/dev/null 2>&1 && ! index_reachable; then
  if ! index_configured && [[ "${USE_CN_MIRROR:-0}" == 1 ]] && PIP_INDEX_URL="$CN_MIRROR" index_reachable; then
    warn "连不上 pypi.org，按 USE_CN_MIRROR=1 改用镜像 $CN_MIRROR"
    export PIP_INDEX_URL="$CN_MIRROR"
  else
    NET_DOWN=1
    warn "$(net_hint)"
    log "先尝试只用本地缓存安装（pip 不重试、超时缩短）..."
    export PIP_RETRIES=0 PIP_DEFAULT_TIMEOUT=20
  fi
fi

PIP_LOG="$TMP_ROOT/pip.log"
CONSTRAINTS="$TMP_ROOT/constraints.txt"
: >"$CONSTRAINTS"
# Debian/Ubuntu 的 certifi 打过补丁，指向系统证书库 /etc/ssl/certs。
# jupyter 的依赖会把它“升级”成 PyPI 版（自带 Mozilla 证书包），装进 /usr/local 后
# 会遮住系统版，系统里所有用 requests 的程序从此不再信任本机安装的企业/代理证书。
# 固定成系统版本即可，pip 会自动选一个兼容的 requests。
sys_certifi="$("$PYTHON" -c 'import certifi, importlib.metadata as m
if certifi.where().startswith("/etc/"): print(m.version("certifi"))' 2>/dev/null || true)"
[[ -z "$sys_certifi" ]] || printf 'certifi==%s\n' "$sys_certifi" >>"$CONSTRAINTS"

pip_try() {  # pip_try <参数...>：pip 输出照常显示，同时存一份用于判断失败原因
  "$PYTHON" -m pip install -q "${user_flag[@]+"${user_flag[@]}"}" "$@" 2>&1 | tee "$PIP_LOG"
}
net_error() {  # 失败是网络造成的（忽略 pip 自动重试成功前打印的 “Retrying …” 警告）
  local errs
  errs="$(grep -v 'Retrying (Retry(' "$PIP_LOG")" || true
  grep -qiE 'Max retries exceeded|ProxyError|NewConnectionError|ConnectTimeout|timed out|Connection (reset|aborted|refused)|name resolution|from versions: none|SSLError|IncompleteRead|do not match the hashes' <<<"$errs"
}
install_reqs() {  # install_reqs <requirements 文件>：成功返回 0
  local req="$1" pass pkg net_tries=0
  local -a cflag=() cache=()
  [[ -s "$CONSTRAINTS" ]] && cflag=(-c "$CONSTRAINTS")
  for (( pass = 1; pass <= 8; pass++ )); do
    pip_try "${cache[@]+"${cache[@]}"}" "${cflag[@]+"${cflag[@]}"}" -r "$req" && return 0
    # 1) apt 装的旧版库挡路（“Cannot uninstall X … installed by debian”）：
    #    只给这一个包装新版本，不用 --ignore-installed 把整棵依赖树都重装一遍
    pkg="$(sed -nE "s/.*Cannot uninstall '?([A-Za-z0-9_.-]+)'?.*/\1/p" "$PIP_LOG" | head -n 1)"
    if [[ -n "$pkg" ]]; then
      log "系统自带的 $pkg 无法被 pip 升级，单独为它安装新版本 ..."
      pip_try --ignore-installed --no-deps "${cflag[@]+"${cflag[@]}"}" "$pkg" || return 1
      continue
    fi
    # 2) 固定 certifi 导致无解时，放开这个限制
    if (( ${#cflag[@]} )) && grep -qiE 'ResolutionImpossible|conflicting dependencies' "$PIP_LOG"; then
      log "保留系统 certifi 时依赖无解，改为不加限制安装 ..."
      cflag=()
      continue
    fi
    # 3) 网络问题：pip 自己已对每个请求重试 5 次，这里再整体重试 2 次就够了。
    #    重试时不用缓存：中途被打断的下载会在缓存里留下残缺文件，之后每次都读到它
    if net_error && (( NET_DOWN == 0 && net_tries < 2 )); then
      net_tries=$((net_tries + 1))
      cache=(--no-cache-dir)
      log "网络错误，$((net_tries * 15)) 秒后重试（不使用缓存）..."
      sleep $((net_tries * 15))
      continue
    fi
    return 1
  done
  return 1
}

core_req="$TMP_ROOT/requirements-core.txt"
grep -viE '^[[:space:]]*jupyter' "$REQ_FILE" >"$core_req" || true

log "安装 requirements.txt（首次约需几分钟）..."
if install_reqs "$REQ_FILE"; then
  :
# 网络正常却出了网络错误、已经重试过了，就没必要再只装核心库试一遍；
# 而离线时核心库可能已经在缓存里，值得再试一次（很快）
elif { (( NET_DOWN )) || ! net_error; } && install_reqs "$core_req"; then
  warn "jupyter 没装上（见上方 pip 报错），已只安装核心库，不影响 verify.py。"
elif net_error; then
  die "安装 requirements.txt 失败：$(net_hint)"
else
  die "安装 requirements.txt 失败，请查看上面 pip 的报错。"
fi

# ---------- 5. 可选：让 python 命令也可用（教程里的命令写的是 python） ----------
if ! command -v python >/dev/null 2>&1 && [[ "$PYTHON" == "python3" ]]; then
  apt_install python-is-python3 >/dev/null \
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

# 普通用户安装时，jupyter 等命令在 ~/.local/bin，非登录 shell 的 PATH 里常常没有它
if (( ${#user_flag[@]} )) && [[ -x "${HOME:-/nonexistent}/.local/bin/jupyter" ]] \
   && [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  log "提示：jupyter 装在 $HOME/.local/bin，请把它加入 PATH（Python 导入不受影响）。"
fi

if (( ${#WARNINGS[@]} )); then
  log "完成，但有 ${#WARNINGS[@]} 条警告（见上方）。"
else
  log "完成。可运行 $PYTHON 代码示例/verify.py 验证全部示例。"
fi
