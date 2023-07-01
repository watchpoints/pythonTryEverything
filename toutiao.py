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
import mail_msg

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
    print("dump cookies succed" + jsCookies)


def loginWithCookies(browser, cookpath, url):
    browser.get(url)
    cookies = pickle.load(open(cookpath, "rb"))
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        browser.add_cookie(cookie)
    time.sleep(1)
    browser.refresh()
    print("toutiao loginWithCookies")


# 今日头条：格言提醒
def postWeiToutiao(browser, content):
    print("postWeiToutiao begin")
    # load
    browser.get("https://mp.toutiao.com/profile_v4/weitoutiao/publish")
    time.sleep(8)

    # selenium控制鼠标下滑
    # 一共下滑十次，下滑一次停顿0.5s
    for i in range(3):
        browser.execute_script('window.scrollTo(0,-document.body.scrollHeight)')
        time.sleep(0.5)

    # 填写内容
    weitoutiao_content = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".ProseMirror")))
    time.sleep(2)
    # weitoutiao_content = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
    #     (By.CSS_SELECTOR, ".ProseMirror")))
    # CSS选择器 https://www.w3school.com.cn/cssref/css_selectors.asp
    # https://github.com/seleniumhq/selenium/issues/1480
    # div CLASS .intro id .
    weitoutiao_content.send_keys(content)
    time.sleep(2)
    # https://blog.csdn.net/weixin_44065501/article/details/89314538
    weitoutiao_content.send_keys(Keys.ENTER)
    time.sleep(2)
    # selenium——鼠标操作ActionChains：点击、滑动、拖动
    # 第一步：创建一个鼠标操作的对象
    action = ActionChains(browser)
    # 第二步：进行点击动作（事实上不会进行操作，只是添加一个点击的动作）
    action.click(weitoutiao_content)
    # 第三步：执行动作
    action.perform()
    time.sleep(2)
    # https://blog.csdn.net/MarkAdc/article/details/107204126
    # https://www.cnblogs.com/jasmine0627/p/13094288.html

    # 模拟发布按钮
    # https://selenium-python.readthedocs.io/locating-elements.html

    # class ="byte-btn byte-btn-primary byte-btn-size-default byte-btn-shape-square publish-content" type="button" > < span > 发布 < / span > < / button >
    weitoutiao_send_btn = browser.find_element(By.CSS_SELECTOR,
                                               ".byte-btn.byte-btn-primary.byte-btn-size-default.byte-btn-shape-square.publish-content")
    time.sleep(2)
    if weitoutiao_send_btn is None:
        print("submit is miss")
    # 模拟鼠标点击动作
    # https://juejin.cn/post/7119756252850159647
    # weitoutiao_send_btn.send_keys(Keys.SPACE)
    weitoutiao_send_btn.click()
    time.sleep(3)
    print("push toutiao")
    logging.info("push toutiao")


def post_sleep_toutiao():
    sleeptime = random.randint(0, 5)
    print(sleeptime)
    time.sleep(sleeptime)
    sys = platform.system()
    if sys == "Windows":
        weibo_driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        weibo_coook_path = r"D:\doc\2023\05-third\chromedriver_win32\toutiao.pkl"
        liunx_weibo_login = "https://mp.toutiao.com"
        liunx_weibo = "https://mp.toutiao.com"
    else:
        weibo_driver_path = r"/root/bin/chromedriver"
        weibo_coook_path = r"/root/bin/toutiao.pkl"
        # weibo_coook_txt = r"/root/bin/toutiao.txt"
        liunx_weibo_login = "https://mp.toutiao.com"
        liunx_weibo = "https://mp.toutiao.com"

    liunx_msg = query_sleep_content()

    try:
        driver = init_browser(weibo_driver_path)
        gen_url_Cookies(driver, weibo_coook_path, liunx_weibo_login)
        loginWithCookies(driver, weibo_coook_path, liunx_weibo)
        postWeiToutiao(driver, liunx_msg)
        # 脚本退出时，一定要主动调用 driver.quit !!!
        # https://cloud.tencent.com/developer/article/1404558
        driver.quit()

        logging.info(liunx_msg)
    except Exception as e:
        print(e)
        driver.quit()
        traceback.print_exc()
        mail_msg.sendEmail("toutiao")

def send_msg_to_toutiao(msg):
    sleeptime = random.randint(0, 5)
    print(sleeptime)
    time.sleep(sleeptime)
    sys = platform.system()
    if sys == "Windows":
        weibo_driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        weibo_coook_path = r"D:\doc\2023\05-third\chromedriver_win32\toutiao.pkl"
        liunx_weibo_login = "https://mp.toutiao.com"
        liunx_weibo = "https://mp.toutiao.com"
    else:
        weibo_driver_path = r"/root/bin/chromedriver"
        weibo_coook_path = r"/root/bin/toutiao.pkl"
        # weibo_coook_txt = r"/root/bin/toutiao.txt"
        liunx_weibo_login = "https://mp.toutiao.com"
        liunx_weibo = "https://mp.toutiao.com"

    try:
        driver = init_browser(weibo_driver_path)
        gen_url_Cookies(driver, weibo_coook_path, liunx_weibo_login)
        loginWithCookies(driver, weibo_coook_path, liunx_weibo)
        postWeiToutiao(driver, msg)
        # 脚本退出时，一定要主动调用 driver.quit !!!
        # https://cloud.tencent.com/developer/article/1404558
        driver.quit()
    except Exception as e:
        print(e)
        driver.quit()
        traceback.print_exc()
        return False
    return True

if __name__ == '__main__':
    send_msg_to_toutiao(query_sleep_content())
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
