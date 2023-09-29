#!/usr/bin/python
# -*-coding:utf-8 -*-
import time
import json
import pickle
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import platform
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import traceback
import datetime
import time
import random


# 获取发表内容
def query_sleep_content():
    current_date = datetime.date.today()
    sleep_money = "来自未来的你提醒"
    sleep_money += "\r\n"
    sleep_money += "22点放下手机去睡觉"
    sleep_money += "\r\n"
    sleep_money += str(current_date)

    return sleep_money


def init_browser(chromedriver_path: str):
    # 采用谷歌浏览器
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--no-sandbox')  # 参数是让Chrome在root权限下跑
    chrome_options.add_argument('--disable-gpu')
    # chrome_opt.add_argument('start-maximized')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('window-size=1920x1480')
    sys = platform.system()
    print(sys)
    if sys == "Windows":
        print("sys=OS is Windows!!!")
        # if len(chromedriver_path) == 0:
        #     path = r"D:\local\Python\tool\chromedriver.exe"
        # else:
        #     path = chromedriver_path
    elif sys == "Linux":
        print("sys=OS is centos!!!")
        # if len(chromedriver_path) == 0:
        #     path = r"/root/local/python/chromedriver/chromedriver"
        # else:
        #     path = chromedriver_path
        # chrome_options.add_argument("--headless")  # 参数是不用打开图形界面
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('headless')
        chrome_options.add_argument('no-sandbox')
        chrome_options.add_argument('disable-dev-shm-usage')

        # headless将在无头模式下启动Chrome浏览上下文
    # chrome_options.binary_location = chromedriver_path  Chrome has crashed. 不能这样写
    # 创建Chrome浏览器对象
    service_path = Service(chromedriver_path)  # 将文件路径作为参数传入Service对象
    driver = webdriver.Chrome(service=service_path, options=chrome_options)
    return driver


# # 检测cookies的有效性
# def check_cookies():
#     # 读取本地cookies
#     cookies = read_cookies()
#     s = requests.Session()
#     for cookie in cookies:
#         s.cookies.set(cookie['name'], cookie['value'])
#     response = s.get("https://weibo.com")
#     response.encoding = response.apparent_encoding
#     html_t = response.text
#     # 检测页面是否包含微博用户名
#     if '用户7720733258' in html_t:
#         return True
#     else:
#         return False

def gen_url_Cookies(driver, cook_path: str, url: str):
    print("gen_url_Cookies begin")

    is_gen_cook = False
    if not os.path.exists(cook_path):
        print("cook_path not exists，please login")
        is_gen_cook = True  # 过期
    if not is_gen_cook:
        print(r"cool is is right")
        logging.debug(r"cool is is right")
        return  # 没有过期

    # 用法：https://selenium-python.readthedocs.io/getting-started.html
    driver.get(url)
    time.sleep(50)  # 留时间进行扫码
    # 在Python中，Pickle模块就用来实现数据序列化和反序列化。
    print("login succe")
    cookies = driver.get_cookies()
    # 该方法实现的是将序列化后的对象obj以二进制形式写入文件file中，进行保存

    # https://zhuanlan.zhihu.com/p/271674011
    pickle.dump(cookies, open(cook_path, "wb"))

    jsCookies = json.dumps(cookies)  # 转换成字符串保存
    # with open(r"/root/bin/cookies.txt", 'w') as f:
    #     f.write(jsCookies)
    print("dump cookies succed" + jsCookies)


def loginWithCookies(browser, cookpath, url):
    browser.get(url)
    cookies = pickle.load(open(cookpath, "rb"))
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        browser.add_cookie(cookie)
    time.sleep(3)
    browser.refresh()
    print("toutiao loginWithCookies")


# https://yuba.douyu.com/homepage/main 新鲜事
def post_danmu_douyu(browser, coook_path, content, run_count, url, run_times):
    print("post_danmu_douyu begin")

    browser.get(url)  # 这句话必须添加
    print("post_danmu_douyu browser.get")

    cookies = pickle.load(open(coook_path, "rb"))
    print(cookies)
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        browser.add_cookie(cookie)

    browser.refresh()  # 刷新网页,cookies才成功
    time.sleep(5)
    print(browser.current_url)

    time.sleep(8)

    # send_barrage(20)

    for i in range(run_count):
        my_content = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".ChatSend-txt  ")))
        time.sleep(1)
        my_content.send_keys(content)
        time.sleep(2)
        my_content.send_keys(Keys.ENTER)

        # 模拟发布按钮
        weitoutiao_send_btn = browser.find_element(By.CSS_SELECTOR, ".ChatSend-button ")
        ActionChains(browser).move_to_element(weitoutiao_send_btn).perform()
        time.sleep(1)
        ActionChains(browser).click(weitoutiao_send_btn).perform()

        # 生成0到100范围内的随机整数
        random_number = run_times + random.randint(0, 55)
        print(" send:" + str(i) + " next：" + str(random_number))
        time.sleep(random_number)


def send_danmu_to_douyu(msg, run_count, url, times):
    sys = platform.system()
    if sys == "Windows":
        weibo_driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        weibo_coook_path = r"D:\doc\2023\05-third\chromedriver_win32\danmu_douyu.pkl"
    else:
        weibo_driver_path = r"/root/bin/chromedriver"
        weibo_coook_path = r"/root/bin/danmu_douyu.pkl"

    try:
        driver = init_browser(weibo_driver_path)
        gen_url_Cookies(driver, weibo_coook_path, url)
        post_danmu_douyu(driver, weibo_coook_path, msg, run_count, url, times)

        driver.quit()

        logging.info(msg)
    except Exception as e:
        print(e)
        driver.quit()
        traceback.print_exc()
        return False
    return True


if __name__ == '__main__':
    # msg = "彻底践行番茄工作法：25分钟专注，5分钟休息"
    # 练习成为演讲者:第一天
    msg = "欢迎来到番茄专注自习室 \n"
    msg += "书单：每天最重要的2小时,富人的逻辑,有钱人和你想的不一样\n"
    run_count = 1000
    # times = 40
    times = 70
    room_id = "https://www.douyu.com/1480416"
    send_danmu_to_douyu(msg, run_count, room_id, times)