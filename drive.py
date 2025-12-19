"""
浏览器驱动配置
- auto: 自动检测已安装浏览器并由 Selenium Manager 下载对应驱动
- edge/chrome/firefox: 手动指定浏览器（若指定的浏览器未安装将报错）
"""

# 默认自动选择浏览器并自动下载驱动
drive_name = "auto"
