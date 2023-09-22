#!/usr/bin/python
# -*-coding:utf-8 -*-
import time
import json
import pickle
from selenium import webdriver
from selenium.webdriver import ActionChains
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
import myblog
import mail_msg
from kernel import interface_db
import pyperclip
from kernel import mymonitor

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
    chrome_options.add_argument('--no-sandbox')  # 参数是让Chrome在root权限下跑
    chrome_options.add_argument('--disable-gpu')
    # chrome_opt.add_argument('start-maximized')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('window-size=1920x1480')
    # 忽略无用的日志
    # https://www.cnblogs.com/pinkhurley/p/15584505.html
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

    sys = platform.system()
    print(sys)
    if sys == "Windows":
        print("sys=OS is Windows!!!")
    elif sys == "Linux":
        print("sys=OS is centos!!!")
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
        print("cook_path not exists，please login >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        is_gen_cook = True  # 过期
    if not is_gen_cook:
        print(r"the cooks is ok >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        logging.debug(r"cool is is right")
        return  # 没有过期

    # 用法：https://selenium-python.readthedocs.io/getting-started.html
    driver.get(url)
    time.sleep(120)  # 留时间进行扫码
    # 在Python中，Pickle模块就用来实现数据序列化和反序列化。
    print("login succe")
    cookies = driver.get_cookies()
    # 该方法实现的是将序列化后的对象obj以二进制形式写入文件file中，进行保存

    # https://zhuanlan.zhihu.com/p/271674011
    pickle.dump(cookies, open(cook_path, "wb"))

    jsCookies = json.dumps(cookies)  # 转换成字符串保存
    print("dump cookies succed" + jsCookies)


def loginWithCookies(browser, cookpath, url):
    browser.get(url)
    cookies = pickle.load(open(cookpath, "rb"))
    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        browser.add_cookie(cookie)
    time.sleep(1)
    browser.refresh()
    print("toutiao loginWithCookies")


# 今日头条：格言提醒
def post_maimai_msg(browser, content):
    isEmoji = False
    isPaste = False
    browser.get("https://maimai.cn/web/feed_explore")
    time.sleep(6)

    weitoutiao_content = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".inputPanel")))
    time.sleep(2)
    print("weitoutiao_content.send_keys")
    # JS_ADD_TEXT_TO_INPUT = """
    #   var elm = arguments[0], txt = arguments[1];
    #   elm.value += txt;
    #   elm.dispatchEvent(new Event('change'));
    #   """
    # browser.execute_script(JS_ADD_TEXT_TO_INPUT, weitoutiao_content, content)

    # selenium——鼠标操作ActionChains：点击、滑动、拖动
    # create action chain object
    # https://www.lambdatest.com/blog/handling-keyboard-actions-in-selenium-webdriver/
    # 不支持emoji表情
    if isEmoji:
        weitoutiao_content.send_keys(content)
        weitoutiao_content.send_keys(Keys.ENTER)
    elif isPaste:
        print("this is windows ")
        pyperclip.copy(content)
        action = ActionChains(browser)
        # click the item
        action.click(on_element=weitoutiao_content)
        # send keys
        action.send_keys(Keys.CONTROL, pyperclip.paste())
        # perform the operation
        action.perform()
        time.sleep(2)
    else:
        print("this is centos ")
        JS_ADD_TEXT_TO_INPUT = """
          var elm = arguments[0], txt = arguments[1];
          elm.value = txt;
        """
        elem = browser.find_element(By.CSS_SELECTOR, ".inputPanel")
        # browser.execute_script(JS_ADD_TEXT_TO_INPUT, elem, content)
        # https://blog.csdn.net/weixin_44596902/article/details/116796508
        ActionChains(browser).send_keys_to_element(elem, content).perform()

    print("maimai  write content is ok")
    time.sleep(2)
    weitoutiao_send_btn = browser.find_element(By.CSS_SELECTOR, ".sendBtn")
    time.sleep(2)
    if weitoutiao_send_btn is None:
        print("submit is miss")

    # 模拟鼠标点击动作
    weitoutiao_send_btn.click()
    time.sleep(3)
    print("push toutiao")
    logging.info("push toutiao")


def post_sleep_maimai():
    geup = interface_db.DailyGetUpEvent()
    if len(geup) > 0:
        send_msg_to_maimai(geup)


def send_msg_to_maimai(msg):
    sleeptime = random.randint(0, 5)
    print(sleeptime)
    time.sleep(sleeptime)
    sys = platform.system()
    if sys == "Windows":
        weibo_driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        weibo_coook_path = r"D:\doc\2023\05-third\chromedriver_win32\maimai.pkl"
        liunx_weibo_login = "https://maimai.cn/"
        liunx_weibo = "https://maimai.cn/"
    else:
        weibo_driver_path = r"/root/bin/chromedriver"
        weibo_coook_path = r"/root/bin/maimai.pkl"
        liunx_weibo_login = "https://maimai.cn/"
        liunx_weibo = "https://maimai.cn/"

    try:
        driver = init_browser(weibo_driver_path)
        gen_url_Cookies(driver, weibo_coook_path, liunx_weibo_login)
        loginWithCookies(driver, weibo_coook_path, liunx_weibo)
        post_maimai_msg(driver, msg)
        logging.info(msg)
    except Exception as e:
        print(e)
        traceback.print_exc()
        mymonitor.sendEmail("maimai")
    finally:
        driver.quit()


if __name__ == '__main__':
    msg = interface_db.DailyGetUpEvent()
    if len(msg) > 0:
        send_msg_to_maimai(msg)
