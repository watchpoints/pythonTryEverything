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
from kernel import interface_db
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
    try:
        for cookie in cookies:
            print(cookie)
            if 'expiry' in cookie:
                cookie['expiry'] = int(cookie['expiry'])
            browser.add_cookie(cookie)
    except Exception as e:
     print(e)

    
    time.sleep(3)
    browser.refresh()
    print("toutiao loginWithCookies")


# https://yuba.douyu.com/homepage/main 新鲜事
def post_douyu_msg(browser, coook_path, content):

    print("post_douyu_msg begin 1111111111111111111")

    browser.get("https://yuba.douyu.com")  # # Add driver.get() before set cookie 
    print("post_douyu_msg begin222222222222222222")
    time.sleep(6) 
    print("post_douyu_msg begin333333333333")
    
    cookies = pickle.load(open(coook_path, "rb"))
    print(cookies)
    print("post_douyu_msg begin44444")
    for cookie in cookies:
        print(cookie)
        # if 'domain' in cookie:
        #    cookie['domain']='www.douyu.com'
            
        browser.add_cookie(cookie)
        
    browser.refresh()
    browser.get("https://yuba.douyu.com/homepage/main")
    browser.refresh()
    time.sleep(5)
    
    last = len(content)
    if len(content) - 100 > 0:
        last = len(content) - 125

    sendContent = content[0:last]  # 长度有限制
    print(sendContent)
    weitoutiao_content = WebDriverWait(browser, 15).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".common-editorText-ZGMmg")))
    time.sleep(1)
    weitoutiao_content.send_keys(sendContent)
    time.sleep(2)
    # https://blog.csdn.net/weixin_44065501/article/details/89314538
    weitoutiao_content.send_keys(Keys.ENTER)

    # elem = browser.find_element(By.CSS_SELECTOR, "common-editorText-ZGMmg")
    # ActionChains(browser).send_keys_to_element(elem, content).perform()

    time.sleep(5)

    # 模拟发布按钮
    weitoutiao_send_btn = browser.find_element(By.CSS_SELECTOR, ".common-editorPostBtn-EDyd1")
    time.sleep(3)
    ActionChains(browser).move_to_element(weitoutiao_send_btn).perform()
    time.sleep(1)
    ActionChains(browser).click(weitoutiao_send_btn).perform()
    # https://blog.csdn.net/a12355556/article/details/111772547

    # https://blog.csdn.net/a12355556/article/details/111772547
    time.sleep(3)
    print("push  douyu")
    logging.info(r"push douyu{content}")


def post_mp4_to_shipinhao(mp4_path):
    sys = platform.system()
    if sys == "Windows":
        weibo_driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        weibo_coook_path = r"D:\doc\2023\05-third\chromedriver_win32\douyu.pkl"
        liunx_weibo_login = "https://channels.weixin.qq.com/platform/post/create"
        liunx_weibo = "https://channels.weixin.qq.com/platform/post/create"
    else:
        weibo_driver_path = r"/root/bin/chromedriver"
        weibo_coook_path = r"/root/bin/douyu.pkl"
        liunx_weibo_login = "https://channels.weixin.qq.com/platform/post/create"
        liunx_weibo = "https://channels.weixin.qq.com/platform/post/create"

    try:
        driver = init_browser(weibo_driver_path)
        gen_url_Cookies(driver, weibo_coook_path, liunx_weibo_login)
        # loginWithCookies(driver, weibo_coook_path, liunx_weibo)
        post_douyu_msg(driver, weibo_coook_path, msg)

        driver.quit()

        logging.info(msg)
    except Exception as e:
        print(e)
        driver.quit()
        traceback.print_exc()
        mymonitor.sendEmail("post DailyGetUpEvent to douyu failed")
        return False
    return True


if __name__ == '__main__':
    mp4_path = ""
    post_mp4_to_shipinhao(mp4_path)
