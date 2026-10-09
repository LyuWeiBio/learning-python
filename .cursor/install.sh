#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if ! dpkg -s python3-venv >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-venv
fi

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

# Login shells and agents can invoke `python3` / `pip` without activating manually.
sudo ln -sf "$(pwd)/.venv/bin/python3" /usr/local/bin/python3
sudo ln -sf "$(pwd)/.venv/bin/pip" /usr/local/bin/pip

if [[ ! -f /etc/profile.d/learning-python-mplbackend.sh ]]; then
  printf '%s\n' 'export MPLBACKEND=Agg' | sudo tee /etc/profile.d/learning-python-mplbackend.sh >/dev/null
fi
