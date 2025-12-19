#!/bin/bash
set -euo pipefail
# 创建并准备 Python 虚拟环境，安装依赖

# 安装前检查 Python3 是否安装
if ! command -v python3 &> /dev/null; then
    echo "Python3 未安装，请先安装 Python3。"
    exit 1
fi

# 检查 venv 模块是否可用
if ! python3 -m venv --help &> /dev/null; then
    echo "Python3 的 venv 模块不可用，请确保已安装该模块。"
    exit 1
fi

create_venv() {
    if [ ! -d ".venv" ]; then
        echo "创建虚拟环境..."
        python3 -m venv .venv
    else
        echo "虚拟环境已存在，跳过创建。"
    fi
}

install_dependencies() {
    echo "升级 pip..."
    python -m pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        echo "安装依赖..."
        pip install -r requirements.txt
    else
        echo "未找到 requirements.txt，跳过安装依赖。"
    fi
}

create_venv
source .venv/bin/activate
install_dependencies
echo "完成。在当前 shell 已激活。如需再次使用：source .venv/bin/activate"
