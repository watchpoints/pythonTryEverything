#!/usr/bin/python
# -*-coding:utf-8 -*-
import logging
import pickle
import platform
import random
import time
import traceback
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import myblog


# 格言提醒
# """
#  调用公共接口
# """
# myblog.InterfaceSendToBlog(driver, post_url, ".editor-content.rich-editor.iget-common-f4",
#                            ".ubmit.iget-common-c9.iget-common-b10.activeSubmit.pointer", msg)
def post_send_msg_to_zhishi(browser, coook_path, content, post_url):
    # load
    browser.get(post_url)
    browser.maximize_window()
    browser.refresh()
    time.sleep(3)

    # 点击--弹出一筐
    # https://blog.csdn.net/AI_Green/article/details/120911847
    client_post = browser.find_element(By.CSS_SELECTOR, ".post-topic-head")
    print("client_post: ", client_post)

    # selenium  模拟鼠标操作
    actions = ActionChains(browser)
    # 鼠标移动到某个元素
    actions.move_to_element(client_post)
    actions.perform()
    # 双击鼠标左键
    actions.double_click(client_post)
    actions.perform()
    # selenium中的三种切换：Windows窗口，iframe，alert弹窗
    # https://blog.csdn.net/c_xiazai12345/article/details/120654809
    # 切换到alert
    # 原生CSS，实现点击按钮出现交互弹窗【新手扫盲】
    # https://blog.csdn.net/xia_yanbing/article/details/104508019
    # WebDriverWait(browser, 5).until(EC.alert_is_present())  # 等待弹出窗口出现
    # alert = browser.switch_to.alert
    # print(alert.text)

    time.sleep(2)
    weitoutiao_content = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".ql-editor")))
    time.sleep(1)
    weitoutiao_content.send_keys(content)
    weitoutiao_content.send_keys(Keys.ENTER)

    btn = browser.find_element(By.CSS_SELECTOR, ".submit-btn")
    time.sleep(1)
    btn.click()
    time.sleep(4)


def send_msg_to_zhishi(msg):
    sys = platform.system()
    log_url = "https://wx.zsxq.com/dweb2/index/group/552812528214"
    post_url = "https://wx.zsxq.com/dweb2/index/group/552812528214"
    if sys == "Windows":
        weibo_driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        weibo_coook_path = r"D:\doc\2023\05-third\chromedriver_win32\zhishi.pkl"
    else:
        weibo_driver_path = r"/root/bin/chromedriver"
        weibo_coook_path = r"/root/bin/zhishi.pkl"
    try:
        driver = myblog.init_browser(weibo_driver_path)
        myblog.gen_url_Cookies(driver, weibo_coook_path, log_url)
        myblog.loginWithCookies(driver, weibo_coook_path, post_url)
        post_send_msg_to_zhishi(driver, weibo_coook_path, msg, post_url)
    except Exception as e:
        print(e)
        traceback.print_exc()
        return False
    finally:
        driver.quit()
    return True


if __name__ == '__main__':
    send_msg_to_zhishi(myblog.query_sleep_content())
