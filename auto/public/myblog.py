import time
import json
import os
import logging
import platform
import random
import subprocess
import sys
import traceback
import threading
import pyperclip
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

class CMyBlog:
    """
    This class represents base
    """
    def __init__(self,cookies_path: str, login_url: str, upload_picture_url: str, upload_mp4_url: str):
        self.cookies_path = cookies_path
        self.login_url = login_url
        self.upload_picture_url = upload_picture_url
        self.upload_mp4_url = upload_mp4_url
        # playwright 部分
        self.browser = None
        # 想法 ---喜欢
        self.user_list = None
        self.context = None
        print("create CMyBlog")
    
    def login_or_restore_cookies(self) -> Page:

        """
          登录
        """
        userAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            userAgent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        
        self.context = self.browser.new_context(user_agent=userAgent)
        self.context.clear_cookies()
        page = self.context.new_page()
        page.goto(self.login_url)

        if os.path.exists(self.cookies_path):
            print("load cookies")
            # 从文件中加载 cookies
            with open(self.cookies_path, 'r',encoding='utf-8') as f:
                cookies = json.load(f)
            self.context.add_cookies(cookies)
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
    #############################
    def post_short_msg(self, page: Page, picture_path_list,habit_name:str, habit_detail:str):
        """
            登录
        """
        print(page)
        print(picture_path_list)
        print(habit_name)
        print(habit_detail)
