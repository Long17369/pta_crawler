param(
    [switch]$Activate = $false,
    [string]$Python = ""
)

function Get-PythonCmd {
    param([string]$Override)
    if ($Override) { return @{Exe=$Override; Args=@()} }
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) { return @{Exe='py'; Args=@('-3')} }
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) { return @{Exe='python'; Args=@()} }
    throw "未检测到 Python，请先安装并配置 PATH。"
}

$cmd = Get-PythonCmd -Override $Python

# 检查 venv 支持
try {
    & $cmd.Exe $cmd.Args -m venv --help *> $null
} catch {
    throw "当前 Python 不支持 venv，请使用 Python 3.3+。"
}

# 创建虚拟环境
if (-not (Test-Path ".venv")) {
    Write-Host "创建虚拟环境..."
    & $cmd.Exe $cmd.Args -m venv .venv
} else {
    Write-Host "虚拟环境已存在，跳过创建。"
}

$venvPy = Join-Path ".venv\Scripts" "python.exe"
if (-not (Test-Path $venvPy)) {
    throw "未找到虚拟环境 Python：$venvPy"
}

Write-Host "升级 pip..."
& $venvPy -m pip install --upgrade pip

if (Test-Path "requirements.txt") {
    Write-Host "安装依赖..."
    & $venvPy -m pip install -r requirements.txt
} else {
    Write-Host "未找到 requirements.txt，跳过安装依赖。"
}

if ($Activate) {
    Write-Host "激活虚拟环境..."
    . ".\.venv\Scripts\Activate.ps1"
    Write-Host "已激活。使用 'deactivate' 可退出。"
} else {
    Write-Host "完成。激活方法：`n- PowerShell: & .\\.venv\\Scripts\\Activate.ps1`n- CMD: call .venv\\Scripts\\activate"
}
