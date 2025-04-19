from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from drive import *

if drive_name.lower() == "chrome":
    driver_path = ".\\drive\\chromedriver.exe"
    from selenium.webdriver.chrome.service import Service
    drive = webdriver.Chrome(
        service=Service(executable_path=driver_path)
    )
elif drive_name.lower() == "edge":
    driver_path = ".\\drive\\msedgedriver.exe"
    from selenium.webdriver.edge.service import Service
    drive = webdriver.Edge(
        service=Service(executable_path=driver_path)
    )
elif drive_name.lower() == "firefox":
    driver_path = ".\\drive\\geckodriver.exe"
    from selenium.webdriver.firefox.service import Service
    drive = webdriver.Firefox(
        service=Service(executable_path=driver_path)
    )
elif drive_name.lower() == "auto":
    if os.path.exists(".\\drive\\chromedriver.exe"):
        driver_path = ".\\drive\\chromedriver.exe"
        from selenium.webdriver.chrome.service import Service
        drive = webdriver.Chrome(
            service=Service(executable_path=driver_path)
        )
    elif os.path.exists(".\\drive\\msedgedriver.exe"):
        driver_path = ".\\drive\\msedgedriver.exe"
        from selenium.webdriver.edge.service import Service
        drive = webdriver.Edge(
            service=Service(executable_path=driver_path)
        )
    elif os.path.exists(".\\drive\\geckodriver.exe"):
        driver_path = ".\\drive\\geckodriver.exe"
        from selenium.webdriver.firefox.service import Service
        drive = webdriver.Firefox(
            service=Service(executable_path=driver_path)
        )
    else:
        raise ValueError("请下载驱动并放入 drive 文件夹")
else:
    raise ValueError("不支持的浏览器驱动类型，请使用 chrome、edge、firefox 或 自行添加。")



login_url="https://pintia.cn/auth/login"

def login(email: str = "", password: str = ""):
    drive.get(login_url)
    try:
        WebDriverWait(drive, 3600).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
        )
    except Exception as e:
        print(f'发生错误{e}')
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
        print("请手动输入账号密码并登录")
    try:
        WebDriverWait(drive, 3600).until(
            EC.url_changes(login_url)
        )
    except Exception as e:
        print(f'发生错误{e}')
        ...
    try:
        WebDriverWait(drive, 3600).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
        )
    except Exception as e:
        print(f'发生错误{e}')
        ...
    cookies = drive.get_cookies()
    drive.close()
    return cookies
