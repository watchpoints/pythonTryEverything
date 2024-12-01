from selenium import webdriver
import time

# 启动浏览器
driver = webdriver.Chrome()

# 打开知乎页面
driver.get("https://www.zhihu.com/people/69-2-35-34")

# 等待页面加载
time.sleep(5)

# 获取所有cookie
cookies = driver.get_cookies()

# 查找包含__zse_ck参数的cookie值
zse_ck = None
for cookie in cookies:
    if '__zse_ck' in cookie['name']:
        zse_ck = cookie['value']
        break

# 打印获取到的__zse_ck参数值
if zse_ck:
    print("获取到的__zse_ck值为:", zse_ck)
else:
    print("未找到包含__zse_ck参数的cookie")

# 关闭浏览器
driver.quit()