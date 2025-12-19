@echo off
REM 创建虚拟环境
python -m venv .venv

REM 激活虚拟环境（Windows）
call .venv\Scripts\activate

REM 安装所需库
pip install -r requirements.txt

@echo 虚拟环境已创建并安装依赖库。
