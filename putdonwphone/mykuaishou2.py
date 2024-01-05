import logging
import time
import json
import random
import os
import platform
import requests
from datetime import datetime
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
#from pythonTryEverything.putdonwphone.data import englisword
########################################################################

class MyKuaishou:
    def __init__(self,cookies_path:str,login_url:str, upload_url:str):
         self.driver = None
         self.cookies_path = cookies_path
         self.login_url = login_url
         self.upload_url = upload_url
         # playwright 部分
         self.browser = None
         print("creae MyKuaishou")
    def __del__(self):
        if self.driver:
            self.driver.close()
        print("is being destroyed")
    
    def upload_picture(self,picture_path:str,msg:str):
        """ start instance"""
        with sync_playwright() as playwright:
            #01 启动chomue浏览器
            # playwright执行默认运行的浏览器是chromium！
            #全局代理
            display_headless = False
            if platform.system() == "Linux":
                display_headless = True
                self.browser = playwright.chromium.launch(headless=display_headless)
            else:
                self.browser = playwright.chromium.launch(channel="chrome",
                                                          headless=display_headless)
            login_page = self.login_or_restore_cookies()
            self.msg_up_load(login_page,picture_path,msg)
            self.browser.close()
    # 登录 设置代理
    def login_or_restore_cookies(self)-> Page:
        # 创建一个新的页面
        user_agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.21 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        context = self.browser.new_context(user_agent=user_agent)
        context.clear_cookies()
        page = context.new_page()
        page.goto(self.login_url)
        
        if os.path.exists(self.cookies_path):
            print("cookies is exited load")
            # 从文件中加载 cookies
            with open(self.cookies_path, 'r',encoding='utf-8') as myfile:
                cookies = json.load(myfile)
            # 将 cookies 加载到页面中
            context.add_cookies(cookies)
            time.sleep(3)
        else:
            # 相信第一次接触Playwright的同学，一定会对Browser、 BrowserContext 和Page这三个概念所困
            # https://blog.csdn.net/liwenxiang629/article/details/130810265
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            time.sleep(60)
            # 获取当前页面的 cookies
            cookies = page.context.cookies()
            print(cookies)
            # 保存 cookies 到文件
            with open(self.cookies_path, 'w',encoding='utf-8') as myfile:
                myfile.write(json.dumps(cookies))
        return page

     # 登录
    def msg_up_load(self,page: Page,picture_path:str,msg:str):
        page.goto(self.upload_url)
        time.sleep(3)
        # https://playwright.dev/docs/locators
        # 使用 XPath 表达式定位元素
        xpath_expression = '//div[contains(text(), "上传图文")]'
        example_element = page.locator("xpath=//div[contains(text(), '上传图文')]")
        example_element.click()
        print("进入图文页面")
        time.sleep(2)
        
        # 点击选择文件，输入文件
        with page.expect_file_chooser() as fc_info:
            # 找到拖拽区域  
            page.click("xpath=//button[contains(text(), '上传图片')]")
        file_chooser = fc_info.value
        file_chooser.set_files(picture_path)
        
        time.sleep(3)
        page.mouse.down()
        page.mouse.down()
        
        #填写描述
        page.locator("css=.iGOvMbhp8tU-").fill(msg)
        time.sleep(3)
        print("填写描述")
        
        #添加音乐
        page.get_by_placeholder("搜索音乐、歌手、歌词添加至作品").click()
        time.sleep(5)
        index = random.randint(0, 5)
        page.locator("xpath=//button[./span[text()='添加']]").locator("nth={}".format(index)).click()
        time.sleep(5)

        # 添加地点
        page.mouse.down()
        #发布
        page.locator("xpath=//button[./span[text()='发布']]").click()
        print("发布")
        time.sleep(7)
       # 登录
    def auto_upload_mp4(self,page: Page,mp4_path:str,msg:str):
        """_summary_

        Args:
            page (Page): _description_
            picture_path (str): _description_
            msg (str): _description_
        """
        page.goto(self.upload_url)
        time.sleep(3)
        
        # https://playwright.dev/docs/locators
        # 使用 XPath 表达式定位元素
        page.locator("xpath=//div[contains(text(), '上传视频')]").click()
        print("上传视频")
        time.sleep(3)
        
        # 点击选择文件，输入文件
        with page.expect_file_chooser() as fc_info:
            # 找到拖拽区域
            page.click("xpath=//button[contains(text(), '上传视频')]")
        file_chooser = fc_info.value
        file_chooser.set_files(mp4_path)
        
        time.sleep(300)
        page.mouse.down()
        page.mouse.down()
        
        #填写描述
        page.get_by_placeholder("添加合适的话题和描述，作品能获得更多推荐～").fill(msg)
        time.sleep(3)
        print("填写描述")
        
        #所属领域
        
        #发布
        page.locator("xpath=//button[./span[text()='发布']]").click()
        time.sleep(5)
        print("发布")
        
    def upload_mp4(self,mp4_file_path:str,msg:str):
        ''' 远离手机'''
        with sync_playwright() as playwright:
            #01 启动chomue浏览器
            # playwright执行默认运行的浏览器是chromium！
            #全局代理
            display_headless = False
            #display_headless = True
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            self.browser = playwright.chromium.launch(headless=display_headless)

            # 模拟登录
            login_page = self.login_or_restore_cookies()
            self.auto_upload_mp4(login_page,mp4_file_path,msg)
            self.browser.close()
        
#################################################################################
def interface_auo_upload_kuaishou2(upload_type:str,file_path :str,
                                   habit_name :str,habit_detail :str):
    ''' 远离手机'''
    sys = platform.system()
    if sys == "Windows":
        coook_path = r"D:\mp4\etc\mykuaishou.json"
        login_url = "https://cp.kuaishou.com/profile"
        upload_url = "https://cp.kuaishou.com/article/publish/video"
        out_path = r"D:\mp4\output"
    else:
        coook_path = r"/root/bin/mykuaishou.json"
        login_url = "https://cp.kuaishou.com/profile"
        upload_url = "https://cp.kuaishou.com/article/publish/video"
        out_path = r"/root/mp4/output"

    msg = habit_name + "\r\n"
    msg += habit_detail
    print(msg)
    msg = msg[:407]
    autoupload = MyKuaishou(coook_path,login_url,upload_url)
    if "mp4" == upload_type:
        for root,_,files in os.walk(out_path):
            for file in files:
                # 拼接路径
                mp4_file_path = os.path.join(root,file)
                if file.endswith('.mp4'):
                    file_name = os.path.basename(mp4_file_path)
                    file_name = file_name.split('.')[0]
                    habit_name = "#" + file_name + "\r\n"
                    habit_name += msg
                    print(habit_name)
                    if autoupload.upload_mp4(mp4_file_path,habit_name):
                        logging.info("upload_mp4 %s", mp4_file_path)
    else:
        print("kuaishou pic")
        autoupload.upload_picture(file_path,msg)


if __name__ == '__main__':
    print("test")
    #cur_file_path, cur_habit_name,cur_habit_detail  = englisword.interface_get_daily_englis_word()
    #print(cur_file_path)
    #print(cur_habit_name)
    #print(cur_habit_detail)
    #interface_auo_upload_kuaishou2("pic",cur_file_path, cur_habit_name,cur_habit_detail)
    #interface_auo_upload_kuaishou2("mp4")
