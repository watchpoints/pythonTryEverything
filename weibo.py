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
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    sys = platform.system()
    print(sys)
    if sys == "Windows":
        print("sys=OS is Windows!!!")
        chrome_options.add_argument('--headless')
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
    driver.get("https://weibo.com/newlogin")
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
def post_weibo(browser, content):
    print("post_weibo begin")
    # load
    browser.get("https://weibo.com/")
    browser.refresh()
    browser.implicitly_wait(60)
    print(r"get https://weibo.com is ok")
    logging.debug(r"get https://weibo.com is ok")
    
    # 微头条内容框
    # presence_of_element_located（locator）：判断某个元素是否存在DOM中
    # 如果判断条件成立，就执行下一步，否则继续等待，直到超过设定的最长等待时间，然后抛出TimeOutEcpection的异常信息。
    weitoutiao_content = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".Form_input_2gtXx")))
    # CSS选择器 https://www.w3school.com.cn/cssref/css_selectors.asp
    # https://github.com/seleniumhq/selenium/issues/1480
    # div CLASS .intro id .
    time.sleep(2)
    weitoutiao_content.send_keys(content)
    print("write msg")
    logging.debug(r"write msg")
    # https://blog.csdn.net/weixin_44065501/article/details/89314538
    weitoutiao_content.send_keys(Keys.ENTER)
    print("step1-------------")

    # 点击发布
    # 鼠标动作模拟操作：https://my.oschina.net/u/4273790/blog/3807807
    # actions = ActionChains(browser)
    weitoutiao_send_btn = browser.find_element(By.CSS_SELECTOR,
                                               ".woo-button-main.woo-button-flat.woo-button-primary.woo-button-m.woo-button-round.Tool_btn_2Eane")  # 双击按钮
    time.sleep(2)
    weitoutiao_send_btn.send_keys(Keys.SPACE)
    time.sleep(3)
    print(r"push {content} succed")


def post_sleep_weibo():
    sleeptime = random.randint(0, 10)
    print(sleeptime)
    time.sleep(sleeptime)
    sys = platform.system()
    if sys == "Windows":
        weibo_driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        weibo_coook_path = r"D:\doc\2023\05-third\chromedriver_win32\weibo.pkl"
        liunx_weibo_login = "https://weibo.com/newlogin"
        liunx_weibo = "https://weibo.com/"
    else:
        weibo_driver_path = r"/root/bin/chromedriver"
        weibo_coook_path = r"/root/bin/cookies.pkl"
        liunx_weibo_login = "https://weibo.com/newlogin"
        liunx_weibo = "https://weibo.com/"

    liunx_msg = query_sleep_content()

    try:
        driver = init_browser(weibo_driver_path)
        gen_url_Cookies(driver, weibo_coook_path, liunx_weibo_login)
        loginWithCookies(driver, weibo_coook_path, liunx_weibo)
        post_weibo(driver, liunx_msg)
        # 脚本退出时，一定要主动调用 driver.quit !!!
        # https://cloud.tencent.com/developer/article/1404558
        driver.quit()

        logging.info(liunx_msg)
    except Exception as e:
        print(e)
        traceback.print_exc()
        driver.quit()


def send_msg_to_weibo(msg):
    sys = platform.system()
    if sys == "Windows":
        weibo_driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        weibo_coook_path = r"D:\doc\2023\05-third\chromedriver_win32\weibo.pkl"
        liunx_weibo_login = "https://weibo.com/newlogin"
        liunx_weibo = "https://weibo.com/"
    else:
        weibo_driver_path = r"/root/bin/chromedriver"
        weibo_coook_path = r"/root/bin/weibo.pkl"
        liunx_weibo_login = "https://weibo.com/newlogin"
        liunx_weibo = "https://weibo.com/"

    try:
        driver = init_browser(weibo_driver_path)
        gen_url_Cookies(driver, weibo_coook_path, liunx_weibo_login)
        loginWithCookies(driver, weibo_coook_path, liunx_weibo)
        post_weibo(driver, msg)
        # 脚本退出时，一定要主动调用 driver.quit !!!
        # https://cloud.tencent.com/developer/article/1404558
        driver.quit()
    except Exception as e:
        print(e)
        traceback.print_exc()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        driver.quit()
        return False
    return True

if __name__ == '__main__':
    send_msg_to_weibo(query_sleep_content())
    # init_log()
    # driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
    # coook_path = r"D:\doc\2023\05-third\chromedriver_win32\cookies.pkl"
    # weibo_login = "https://weibo.com/newlogin"
    # weibo = "https://weibo.com/"
    #
    # msg = query_sleep_content()
    #
    # try:
    #     webdriver = init_browser(driver_path)
    #     gen_url_Cookies(webdriver, coook_path, weibo_login)
    #     loginWithCookies(webdriver, coook_path, weibo)
    #     post_weibo(webdriver, msg)
    #     webdriver.close()
    #
    #     logging.info(msg)
    # except Exception as e:
    #     print(e)
    #     traceback.print_exc()
