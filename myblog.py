#!/usr/bin/python
# -*-coding:utf-8 -*-
import time
import json
import pickle
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
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


# 初始化浏览器 打开微博登录页面
def init_browser(chromedriver_path: str):
    # 采用谷歌浏览器
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 参数是让Chrome在root权限下跑
    chrome_options.add_argument('--disable-gpu')
    # chrome_opt.add_argument('start-maximized')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('blink-settings=imagesEnabled=false') # 无图模式
    sys = platform.system()
    print(sys)
    if sys == "Windows":
        print("sys=OS is Windows!!!")
    elif sys == "Linux":
        print("sys=OS is centos!!!")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')

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
    time.sleep(60)  # 留时间进行扫码
    # 在Python中，Pickle模块就用来实现数据序列化和反序列化。
    print("login succe")
    cookies = driver.get_cookies()
    # 该方法实现的是将序列化后的对象obj以二进制形式写入文件file中，进行保存

    # https://zhuanlan.zhihu.com/p/271674011
    pickle.dump(cookies, open(cook_path, "wb"))

    jsCookies = json.dumps(cookies)  # 转换成字符串保存
    # with open(r"/root/bin/cookies.txt", 'w') as f:
    #     f.write(jsCookies)
    print("dump cookies succed")


def loginWithCookies(browser, cookpath, url):
    browser.get(url)
    cookies = pickle.load(open(cookpath, "rb"))
    print(cookies)
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        browser.add_cookie(cookie)
    time.sleep(2)
    browser.refresh()
    print("loginWithCookies")


"""
  kill 进程 防止 命令执行失败
"""


def KillChromebeta():
    os.system("ps -ef | grep google-chrome  | grep -v grep | awk '{print $2}' | xargs kill")
    os.system("ps -ef | grep chrome-beta | grep -v grep | awk '{print $2}' | xargs kill")


"""
   博客发表接口
   class="comment-area"
   "reply-btn send-btn-b clearTpaErr
"""


def InterfaceSendToBlog(browser, post_url, bodyMsg, submit, content):
    print(r"push {post_url}  begin")
    # load
    browser.get(post_url)
    time.sleep(3)

    # 填写内容
    weitoutiao_content = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".PostContainer_webpcBox_2GefL")))
    time.sleep(1)
    weitoutiao_content.send_keys(content)
    time.sleep(1)
    # https://blog.csdn.net/weixin_44065501/article/details/89314538
    weitoutiao_content.send_keys(Keys.ENTER)
    time.sleep(2)

    # class ="byte-btn byte-btn-primary byte-btn-size-default byte-btn-shape-square publish-content" type="button" > < span > 发布 < / span > < / button >
    weitoutiao_send_btn = browser.find_element(By.CSS_SELECTOR,
                                               ".Button_webpcButton_2jdHV.Button_primary_3fC65.Button_small_1FrvR")
    time.sleep(2)
    if weitoutiao_send_btn is None:
        print("submit is miss")
    # 模拟鼠标点击动作
    # https://juejin.cn/post/7119756252850159647
    # weitoutiao_send_btn.send_keys(Keys.SPACE)
    weitoutiao_send_btn.click()
    time.sleep(1)
    print(r"push {post_url} ok")
    logging.info(r"push {post_url} ok")
