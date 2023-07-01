#!/usr/bin/python
# -*-coding:utf-8 -*-
import logging
import platform
import random
import time
import traceback

from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import myblog
import mail_msg


# 格言提醒
def post_send_msg_to_csdn(browser, content):
    print("send_msg_to_csdn begin")
    # load
    browser.get("https://blink.csdn.net/?spm=1035.2022.3001.5353")
    browser.implicitly_wait(4)
    print(r"get https://blink.csdn.net/?spm=1035.2022.3001.5353 is ok")

    weitoutiao_content = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".comment-area")))
    time.sleep(2)
    weitoutiao_content.send_keys(content)
    weitoutiao_content.send_keys(Keys.ENTER)
    time.sleep(3)

    # css class 填写内容 和不填写内容会发生变化。
    weitoutiao_send_btn = browser.find_element(By.CSS_SELECTOR,
                                               ".reply-btn.send-btn-b.clearTpaErr.active")  # 双击按钮
    time.sleep(2)
    weitoutiao_send_btn.click()
    time.sleep(10)
    print(r'push {content} succed')


def send_msg_to_csdn(msg):
    sleeptime = random.randint(0, 8)
    print(sleeptime)
    time.sleep(sleeptime)
    sys = platform.system()
    log_url = "https://blink.csdn.net/?spm=1035.2022.3001.5353"
    post_url = "https://blink.csdn.net/?spm=1035.2022.3001.5353"
    if sys == "Windows":
        weibo_driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        weibo_coook_path = r"D:\doc\2023\05-third\chromedriver_win32\csdn.pkl"
    else:
        weibo_driver_path = r"/root/bin/chromedriver"
        weibo_coook_path = r"/root/bin/csdn.pkl"
    try:
        driver = myblog.init_browser(weibo_driver_path)
        myblog.gen_url_Cookies(driver, weibo_coook_path, log_url)
        myblog.loginWithCookies(driver, weibo_coook_path, log_url)
        post_send_msg_to_csdn(driver, msg)
        """
           博客发表接口
           class="comment-area"
           "reply-btn send-btn-b clearTpaErr
        """
        # myblog.InterfaceSendToBlog(driver, post_url, ".comment-area",
        #                            ".eply-btn.send-btn-b.clearTpaErr", msg)
    except Exception as e:
        print(e)
        traceback.print_exc()
        mail_msg.sendEmail("csdn")
        return False
    finally:
        driver.quit()
    return True


if __name__ == '__main__':
    send_msg_to_csdn(myblog.query_sleep_content())
