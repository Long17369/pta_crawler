@echo off
setlocal

REM 选择 Python 命令（优先使用 py -3）
where py >nul 2>&1
if %ERRORLEVEL%==0 (
    set "PY_CMD=py -3"
) else (
    set "PY_CMD=python"
)

REM 检查 Python 是否可用
%PY_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo 未检测到可用的 Python，请安装并确保已添加到 PATH。
    exit /b 1
)

REM 检查 venv 模块
%PY_CMD% -m venv --help >nul 2>&1
if errorlevel 1 (
    echo 当前 Python 不支持 venv，请使用 Python 3.3 及以上版本。
    exit /b 1
)

REM 创建虚拟环境
if not exist .venv (
    echo 创建虚拟环境...
    %PY_CMD% -m venv .venv
) else (
    echo 虚拟环境已存在，跳过创建。
)

REM 使用虚拟环境内 Python 升级 pip 并安装依赖
set "VENV_PY=.venv\Scripts\python.exe"
if not exist "%VENV_PY%" (
    echo 未找到虚拟环境 Python：%VENV_PY%
    exit /b 1
)

echo 升级 pip...
"%VENV_PY%" -m pip install --upgrade pip
if errorlevel 1 (
    echo 升级 pip 失败！
    exit /b 1
)

if exist requirements.txt (
    echo 安装依赖...
    "%VENV_PY%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo 安装依赖失败！
        exit /b 1
    )
) else (
    echo 未找到 requirements.txt，跳过安装依赖。
)

echo 完成。激活方法：
echo - CMD: ^call .venv\Scripts\activate
echo - PowerShell: ^& .\.venv\Scripts\Activate.ps1
endlocal
