from typing import Optional, Any, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import shutil
from drive import *
from loguru import logger

# 常见浏览器可执行文件和默认安装路径，用于快速探测已安装浏览器
_BROWSER_EXECUTABLES = {
    "edge": ["msedge", "msedge.exe"],
    "chrome": ["chrome", "chrome.exe", "google-chrome", "google-chrome-stable"],
    "firefox": ["firefox", "firefox.exe"],
}

_BROWSER_DEFAULT_PATHS = {
    "edge": [
        r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        r"C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
    ],
    "chrome": [
        r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    ],
    "firefox": [
        r"C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        r"C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe",
    ],
}

_BROWSER_PRIORITY = ["edge", "chrome", "firefox"]


def _browser_installed(browser: str) -> bool:
    for exe in _BROWSER_EXECUTABLES.get(browser, []):
        if shutil.which(exe):
            return True
    for path in _BROWSER_DEFAULT_PATHS.get(browser, []):
        if os.path.exists(path):
            return True
    return False


def _launch_browser(browser: str) -> webdriver.Remote:
    # 使用 Selenium Manager 自动下载驱动；仅在找不到浏览器时抛出可读错误
    if browser == "chrome":
        from selenium.webdriver.chrome.service import Service as ChromeService

        return webdriver.Chrome(service=ChromeService())
    if browser == "edge":
        from selenium.webdriver.edge.service import Service as EdgeService

        return webdriver.Edge(service=EdgeService())
    if browser == "firefox":
        from selenium.webdriver.firefox.service import Service as FirefoxService

        return webdriver.Firefox(service=FirefoxService())
    raise ValueError("不支持的浏览器驱动类型，请使用 chrome、edge、firefox 或 auto。")


def get_driver(drive_name: Optional[str] = None) -> webdriver.Remote:
    """
    获取浏览器驱动，自动检测本机浏览器并由 Selenium Manager 下载对应驱动。
    :param drive_name: 浏览器类型，支持 chrome、edge、firefox、auto（默认）。
    :return: 浏览器驱动对象
    """
    preference = drive_name or globals().get("drive_name") or "auto"
    target = preference.lower()

    if target != "auto":
        if not _browser_installed(target):
            raise ValueError(
                f"未检测到已安装的 {target} 浏览器，请安装后重试或使用 auto。"
            )
        print(f"使用指定的 {target} 浏览器，驱动由 Selenium 自动下载。")
        return _launch_browser(target)

    available = [b for b in _BROWSER_PRIORITY if _browser_installed(b)]
    if not available:
        raise ValueError("未检测到可用浏览器，请安装 Edge/Chrome/Firefox 后重试。")

    last_error = None
    for browser in available:
        try:
            print(f"检测到 {browser} 浏览器，正在启动（驱动由 Selenium 自动下载）。")
            return _launch_browser(browser)
        except Exception as exc:
            last_error = exc
            continue
    raise RuntimeError("浏览器启动失败，请检查浏览器安装状态。") from last_error


login_url = "https://pintia.cn/auth/login"


def login(email: str = "", password: str = "") -> List[dict[str, Any]]:
    drive = get_driver()
    drive.get(login_url)
    try:
        WebDriverWait(drive, 3600).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
        )
    except Exception as e:
        logger.exception(f"发生错误{e}")
        ...
    email_input = drive.find_element(
        By.XPATH, '//input[@placeholder="电子邮箱或手机号码"]'
    )
    email_input.send_keys(email)
    password_input = drive.find_element(By.XPATH, '//input[@placeholder="密码"]')
    password_input.send_keys(password)
    if email and password:
        login_button = drive.find_element(By.XPATH, '//button[@type="submit"]')
        login_button.click()
    else:
        logger.info("请手动输入账号密码并登录")
    try:
        WebDriverWait(drive, 3600).until(EC.url_changes(login_url))
    except Exception as e:
        logger.exception(f"发生错误{e}")
        ...
    try:
        WebDriverWait(drive, 3600).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
        )
    except Exception as e:
        logger.exception(f"发生错误{e}")
        ...
    cookies = drive.get_cookies()
    drive.close()
    return cookies
