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
import txtdb


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
    chrome_options.add_argument('window-size=1920x1480')
    sys = platform.system()
    if sys == "Windows":
        print("sys=OS is Windows!!!")    
    elif sys == "Linux":
        print("sys=OS is centos!!!")
        chrome_options.add_argument('headless')
        chrome_options.add_argument('no-sandbox')
        chrome_options.add_argument('disable-dev-shm-usage')
    else:
        print("this is  macos ")
    service_path = Service(chromedriver_path)  # 将文件路径作为参数传入Service对象
    driver = webdriver.Chrome(service=service_path, options=chrome_options)
    return driver

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
    time.sleep(80)  # 留时间进行扫码
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


# 格言提醒
def post_baijia(browser, content):
    print("post_baijia begin")

    # load
    browser.get("https://baijiahao.baidu.com/builder/rc/edit?type=events")
    browser.refresh()
    browser.implicitly_wait(10)
    print(r"get https://baijiahao.baidu.com/builder/rc/edit?type=eventsis ok")
    logging.debug(r"get https://baijiahao.baidu.com/builder/rc/edit?type=events is ok")

    # 内容框
    weitoutiao_content = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".cheetah-input.txt-area")))
    
    # CSS选择器 https://www.w3school.com.cn/cssref/css_selectors.asp
    # https://github.com/seleniumhq/selenium/issues/1480
    # div CLASS .intro id .
    time.sleep(2)
    weitoutiao_content.send_keys(content)
    print("write msg")

    # https://blog.csdn.net/weixin_44065501/article/details/89314538
    weitoutiao_content.send_keys(Keys.ENTER)
    print("send_keys")
    
    time.sleep(10)
    # 点击发布
    weitoutiao_send_btn = browser.find_element(By.CSS_SELECTOR,
                                               ".cheetah-btn.cheetah-btn-primary.cheetah-btn-circle.cheetah-btn-icon-only.cheetah-public._2hCPbPjXJs5rEp0wGcWkgo.events-op-bar-pub-btn.events-op-bar-pub-btn-blue")  # 双击按钮
    time.sleep(3)
    weitoutiao_send_btn.send_keys(Keys.SPACE)
    time.sleep(4)
    print(r"push {content} succed")


def send_msg_to_baidubaijia(msg):
    sys = platform.system()
    print(sys)
    if sys == "Windows":
        weibo_driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        weibo_coook_path = r"D:\doc\2023\05-third\chromedriver_win32\weibo.pkl"
        liunx_weibo_login = "https://baijiahao.baidu.com/builder/rc/edit?type=events"
        liunx_weibo = "https://baijiahao.baidu.com/builder/rc/edit?type=events"
    elif sys == 'Darwin':
        weibo_driver_path = r"/Users/wangchuanyi/local/chromedriver"
        weibo_coook_path = r"/Users/wangchuanyi/local/blog/baijia.pkl"
        liunx_weibo_login = "https://baijiahao.baidu.com/builder/rc/edit?type=events"
        liunx_weibo = "https://baijiahao.baidu.com/builder/rc/edit?type=events"
    else:
        weibo_driver_path = r"/root/bin/chromedriver"
        weibo_coook_path = r"/root/bin/baijia.pkl"
        liunx_weibo_login = "https://baijiahao.baidu.com/builder/rc/edit?type=events"
        liunx_weibo = "https://baijiahao.baidu.com/builder/rc/edit?type=events"

    try:
        driver = init_browser(weibo_driver_path)
        gen_url_Cookies(driver, weibo_coook_path, liunx_weibo_login)
        loginWithCookies(driver, weibo_coook_path, liunx_weibo)
        post_baijia(driver, msg)
        driver.quit()
    except Exception as e:
        #mymonitor.sendEmail("post DailyGetUpEvent to weibo failed")
        print(e)
        traceback.print_exc()
        driver.quit()
        return False
    return True


if __name__ == '__main__':
    msg = txtdb.get_up_everyday()
    send_msg_to_baidubaijia(msg)
