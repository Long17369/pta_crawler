# PTA

## 项目描述

PTA 是一个用于与 PTA 在线考试和题库系统交互的工具。  
它提供了自动化的登录、题目集获取、考试信息获取、提交记录管理等功能，  
并支持将提交记录导出为 JSON 文件或代码文件。

## 功能

- 自动登录 PTA 系统（支持浏览器登录和 API 登录）。
- 获取题目集、考试信息和题目列表。
- 管理提交记录，包括获取提交详情和导出数据。
- 支持将提交记录按题目导出为 JSON 文件和代码文件。

## 安装

1. 克隆此仓库：

   ```bash
   git clone <仓库地址>
   ```

2. 确保使用 Python 版本 3.10.6 或更高版本。

3. 创建虚拟环境：

   运行以下命令以创建虚拟环境并安装依赖库：

   ```bash
   createnv.bat
   ```

4. 安装浏览器驱动（以 Chrome 为例）：

   - 确保已安装 Chrome 浏览器。
   - 下载与 Chrome 浏览器版本匹配的 [ChromeDriver](https://chromedriver.chromium.org/downloads)。
   - 将下载的驱动程序解压到项目根目录下的drive目录

   **其余浏览器**
   - Firefox 浏览器：下载与 Firefox 浏览器版本匹配的 [GeckoDriver](https://github.com/mozilla/geckodriver/releases)。
   - Edge 浏览器：下载与 Edge 浏览器版本匹配的 [EdgeDriver](https://developer.microsoft.com/microsoft-edge/tools/webdriver/)。

   请将下载好的驱动放入drive目录并修改 [drive.py](drive.py) 的 `drive_name` 参数

## 使用

1. 启动项目：

   ```bash
   python main.py
   ```

2. 按提示输入登录信息和选择题目集，程序会自动处理并导出数据。

## 文件结构

- `pta_class`：核心功能模块。
- `main.py`：主程序入口。
- `output/`：导出的 JSON 和代码文件存储目录。
