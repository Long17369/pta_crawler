from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

login_url="https://pintia.cn/auth/login"

def login(email: str = "", password: str = ""):
    drive = webdriver.Edge(
        service=Service(executable_path=".\\edgedrive\\msedgedriver.exe")
    )
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
