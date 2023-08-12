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
from kernel import mymonitor


# 格言提醒
def post_send_msg_to_dedao(browser, coook_path, content, post_url):
    print("post_send_msg_to_dedao begin")
    browser.get(post_url)  # 这句话必须添加
    cookies = pickle.load(open(coook_path, "rb"))
    # print(cookies)
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        browser.add_cookie(cookie)
    browser.refresh()  # 刷新网页,cookies才成功
    time.sleep(2)

    # load
    browser.get(post_url)
    browser.refresh()
    time.sleep(5)
    print("load .。。。。。。。。。。。。。。。。。。")
    try:
        # 获取不到报错 is not clickable at point (460, 286). Other element would receive the click:
        # weitoutiao_content = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
        #     (By.CSS_SELECTOR, ".editor-content.rich-editor.iget-common-f4")))

        weitoutiao_content = WebDriverWait(browser, 35).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".editor-content.rich-editor.iget-common-f4")))
        print("weitoutiao_content: ", weitoutiao_content)
        weitoutiao_content.send_keys(content)
        weitoutiao_content.send_keys(Keys.ENTER)
        time.sleep(15)

    except Exception as e:
        print(e)
        time.sleep(5)
        print("send_keys  error.。。。。。。。。。。。。。。。。。。")
    print("send_keys .。。。。。。。。。。。。。。。。。。")

    # css class 填写内容 和不填写内容会发生变化。
    # https://www.geeksforgeeks.org/find_element_by_xpath-driver-method-selenium-python/
    # weitoutiao_send_btn = browser.find_element(By.CSS_SELECTOR, '//*[@id="knowledgeLeft"]/div/div[1]/section/div[2]/p[2]/span[2]/span[1]')
    try:

        # weitoutiao_send_btn = WebDriverWait(browser, 35).until(EC.presence_of_element_located(
        #     (By.CSS_SELECTOR, ".submit.iget-common-c9.iget-common-b10.activeSubmit.pointer")))
        # print("weitoutiao_send_btn: ", weitoutiao_send_btn)
        time.sleep(10)
        element = browser.find_element(By.CSS_SELECTOR, ".submit.iget-common-c9.iget-common-b10.activeSubmit.pointer")
        print("click: ", element)
        time.sleep(2)
        # ActionChains(browser).moveToElement(element).click().perform()
        a = browser.find_element(By.CSS_SELECTOR, '.submit.iget-common-c9.iget-common-b10.activeSubmit.pointer')
        browser.execute_script("arguments[0].click();", a)
        print("click .。。。。。。。。。。。。。。。。。。")
        time.sleep(3)
    except Exception as e:
        print(e)
        weitoutiao_send_btn = browser.find_element(By.CSS_SELECTOR,
                                                   ".submit.iget-common-c9.iget-common-b10.activeSubmit.pointer")
        time.sleep(2)
        weitoutiao_send_btn.click()
        time.sleep(2)
        mymonitor.sendEmail("post DailyGetUpEvent to Dedao failed")


def send_msg_to_dedao(msg):
    sys = platform.system()
    log_url = "https://www.dedao.cn/knowledge/home"
    post_url = "https://www.dedao.cn/knowledge/home"
    if sys == "Windows":
        weibo_driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        weibo_coook_path = r"D:\doc\2023\05-third\chromedriver_win32\dedao.pkl"
    else:
        weibo_driver_path = r"/root/bin/chromedriver"
        weibo_coook_path = r"/root/bin/dedao.pkl"
    try:
        driver = myblog.init_browser(weibo_driver_path)
        myblog.gen_url_Cookies(driver, weibo_coook_path, log_url)
        # myblog.loginWithCookies(driver, weibo_coook_path, post_url)
        post_send_msg_to_dedao(driver, weibo_coook_path, msg, post_url)
    except Exception as e:
        print(e)
        traceback.print_exc()
        return False
    finally:
        driver.quit()
    return True


if __name__ == '__main__':
    send_msg_to_dedao(myblog.query_sleep_content())
