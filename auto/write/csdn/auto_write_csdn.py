"""This module provides mydouyn"""
import time
import json
import os
import platform
from datetime import datetime
import requests
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page

########################################################################
class CMyCsdn:
    """
    This class represents a GetupHabit.

    Parameters:
    - save_picture_path (str): The path to save pictures.
    - default_picture_path (str): The default path for pictures.
    """
    def __init__(self,cookies_path: str, login_url: str, upload_picture_url: str, upload_mp4_url: str):
        self.cookies_path = cookies_path
        self.login_url = login_url
        self.upload_picture_url = upload_picture_url
        self.upload_mp4_url = upload_mp4_url
        # playwright 部分
        self.browser = None
        print("create CMyCsdn")

    def __del__(self):
        print("CMyCsdn is being destroyed")

    def upload_msg_with_picture(self, picture_path: str, habit_name:str, habit_detail:str):
        """
          upload_picture
        """
        with sync_playwright() as playwright:
            display_headless = False
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            #self.browser = playwright.chromium.launch(headless=display_headless)
            login_page = self.login_or_restore_cookies()
            self.msg_up_load(login_page, picture_path, habit_name,habit_detail)
            self.browser.close()
    
    def upload_mp4(self, mp4_path: str, msg: str):
        """
          upload_mp4
        """
        with sync_playwright() as playwright:
            display_headless = False
            # display_headless = True
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            login_page = self.login_or_restore_cookies()
            self.msg_up_load_mp4(login_page, mp4_path, msg)
            self.browser.close()
        
    def login_or_restore_cookies(self) -> Page:

        """
          登录 context-->page
        """
        userAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            userAgent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        
        context = self.browser.new_context(user_agent=userAgent)
        context.clear_cookies()
        page = context.new_page()
        page.goto(self.login_url)

        if os.path.exists(self.cookies_path):
            print("load cookies")
            # 从文件中加载 cookies
            with open(self.cookies_path, 'r',encoding='utf-8') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            time.sleep(3)
        else:
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            time.sleep(80)
            cookies = page.context.cookies()
            with open(self.cookies_path, 'w',encoding='utf-8') as f:
                f.write(json.dumps(cookies))
        print("login_or_restore_cookies")
        return page

    def msg_up_load(self, page: Page, picture_path: str,habit_name:str, habit_detail:str):
        """
        msg_up_load
        """
        page.goto(self.upload_picture_url)
        time.sleep(3)
        print(f"open  {self.upload_picture_url}")
        
        msg = habit_name + "\r\n"
        msg += habit_detail
        # 博客内容
        ##  playwright codegen https://blink.csdn.net/?spm=1010.2135.3001.5353
        page.get_by_placeholder("有什么新的观点，快来说说看～").fill(msg)
        print("什么新的观点，快来说说看～")
        time.sleep(6)
        for onefile in picture_path:
            with page.expect_file_chooser() as fc_info:
                page.locator(".emoticon").first.click()
            file_chooser = fc_info.value
            file_chooser.set_files(onefile)
            time.sleep(6)
        print("图片")
        page.get_by_role("contentinfo").get_by_text("发布", exact=True).click()
        print("发布")
        time.sleep(6)

    def msg_up_load_mp4(self, page: Page, mp4_path: str, msg: str):
        """
        msg_up_load_mp4
        """
        page.goto(self.upload_mp4_url)
        time.sleep(3)
        print(f"open  {self.upload_mp4_url}")
        
        # 使用文本内容定位元素
        example_element = page.locator("xpath=//div[contains(text(), '发布视频')]")
        example_element.click()
        print("点击 发布视频")
        time.sleep(3)

        # 使用文本内容定位元素
        
        page.locator(
            "label:has-text(\"点击上传 或直接将视频文件拖入此区域为了更好的观看体验和平台安全，平台将对上传的视频预审。超过40秒的视频建议上传横版视频\")").set_input_files(
            mp4_path)
            
        print("视频文件拖入此区域")
        time.sleep(20)
        # # 点击选择文件，输入文件
        # with page.expect_file_chooser() as fc_info:
        #     # 找到拖拽区域
        #     page.click("xpath=//button[contains(text(), '上传图片')]")
        #     # 问题 文件弹框后 不自动退出 无法后续自动化操作
        #     file_chooser = fc_info.value
        #     file_chooser.set_files(picture_path)


        # # 填写描述
        # page.locator("css=.iGOvMbhp8tU-").fill(msg)
        # time.sleep(3)
        # # 发布
        # page.locator("xpath=//button[./span[text()='发布']]").click()
        # time.sleep(5)
        print("发布")
        time.sleep(600)
    #################################################################################


def interface_auo_upload_mycsdn(file_path,habit_name,habit_detail):
    """
      对外调用接口
    """
    try:
        sys = platform.system()
        login_url = "https://www.csdn.net/"
        upload_picture_url = "https://blink.csdn.net/?spm=1020.2143.3001.5353"
        upload_mp4_url = "https://blink.csdn.net/?spm=1020.2143.3001.5353"
        if sys == "Windows":
            cookies_path = r"D:\mp4\etc\mycsdn_small.json"
        elif sys == "Darwin":
             cookies_path = r"/Users/wangchuanyi/mp4/etc/mycsdn_small.json"
        else:
            cookies_path = r"/root/bin/mycsdn_small.json"

        autoupload = CMyCsdn(cookies_path, login_url, upload_picture_url,upload_mp4_url)
        autoupload.upload_msg_with_picture(file_path, habit_name,habit_detail)
       

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

if __name__ == '__main__':
    print("test")
    # playwright codegen https://blink.csdn.net/?spm=1010.2135.3001.5353
