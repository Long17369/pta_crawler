#!/bin/bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境（Linux/macOS）
source .venv/bin/activate

# 安装所需库
pip install -r requirements.txt

echo "虚拟环境已创建并安装依赖库。"
