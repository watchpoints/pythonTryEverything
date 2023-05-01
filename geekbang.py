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


# 格言提醒
def postJike(browser, post_url, content):
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


def send_msg_to_jike(msg):
    sleeptime = random.randint(0, 5)
    print(sleeptime)
    time.sleep(sleeptime)
    sys = platform.system()
    log_url = "https://horde.geekbang.org/home"
    post_url = "https://horde.geekbang.org/home"
    if sys == "Windows":
        weibo_driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        weibo_coook_path = r"D:\doc\2023\05-third\chromedriver_win32\jike.pkl"
    else:
        weibo_driver_path = r"/root/bin/chromedriver"
        weibo_coook_path = r"/root/bin/jike.pkl"
    try:
        driver = myblog.init_browser(weibo_driver_path)
        myblog.gen_url_Cookies(driver, weibo_coook_path, log_url)
        myblog.loginWithCookies(driver, weibo_coook_path, log_url)
        postJike(driver, post_url, msg)
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
    send_msg_to_jike(myblog.query_sleep_content())
