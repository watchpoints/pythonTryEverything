"""This module provides mydouyn"""
import time
import json
import os
import platform
import logging
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
#from pythonTryEverything.putdonwphone.data import englisword
#from putdonwphone.data import englisword
class CMyRedBook:
    """
    This class represents a GetupHabit.

    Parameters:
    - save_picture_path (str): The path to save pictures.
    - default_picture_path (str): The default path for pictures.
    """
    def __init__(self,cookies_path: str, login_url: str, 
                      upload_picture_url: str, upload_mp4_url: str):
        self.cookies_path = cookies_path
        self.login_url = login_url
        self.upload_picture_url = upload_picture_url
        self.upload_mp4_url = upload_mp4_url
        # playwright 部分
        self.browser = None
        self.page = None
        print("create CMyDouyin")

    def __del__(self):
        if self.browser:
            self.browser.close()
        print("CMyDouyin is being destroyed")

    def upload_picture(self, picture_path: str, habit_name: str, habit_detail:str):
        """
          upload_picture
        """
        with sync_playwright() as playwright:
            display_headless = False
            #display_headless = True
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            if sys == "Linux":
              self.browser = playwright.chromium.launch(headless=display_headless)
            else:
                self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            login_page = self.login_or_restore_cookies()
            self.msg_up_load(login_page, picture_path, habit_name, habit_detail)
            self.browser.close()

    def login_or_restore_cookies(self) -> Page:
        """
          登录
        """
        user_agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.21 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        
        context = self.browser.new_context(user_agent=user_agent)
        context.clear_cookies()
        page = context.new_page()
        page.goto(self.login_url)

        if os.path.exists(self.cookies_path):
            print("load cookies--------------------")
            # 从文件中加载 cookies
            with open(self.cookies_path, 'r',encoding='utf-8') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            time.sleep(3)
        else:
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            print("扫名二维码登录 需要人工处理--------------------")
            time.sleep(60)
            cookies = page.context.cookies()
            with open(self.cookies_path, 'w',encoding='utf-8') as f:
                f.write(json.dumps(cookies))
        print("login_or_restore_cookies")
        return page

    def msg_up_load(self, page: Page, picture_path: str, habit_name: str, habit_detail:str):
        """
        上传图文
        """
        page.goto(self.upload_picture_url)
        time.sleep(3)
        print(f"open  {self.upload_picture_url}")
        # 使用文本内容定位元素
        example_element = page.locator("xpath=//span[contains(text(), '上传图文')]")
        example_element.click()
        print("点击 发布图文")
        time.sleep(4)
        
        
        # # page.locator('.drag-over').locator('nth=0').click()
        # page.locator('.drag-over').locator('nth=0').set_input_files()
        # # page.locator(
        # #     ":has-text(\"最多支持上传18张\")").locator('nth=1').set_input_files(
        # #     picture_path)
            
    
        # 点击选择文件，输入文件
        with page.expect_file_chooser() as fc_info:
            # 找到拖拽区域  
            page.locator('.drag-over').locator('nth=0').click()
            # 问题 文件弹框后 不自动退出 无法后续自动化操作
            file_chooser = fc_info.value
            file_chooser.set_files(picture_path)

        time.sleep(4)
        print("上传图片")
        #填写标题，可能会有更多赞哦～
        page.locator("css=.c-input_inner").fill(habit_name)
        time.sleep(3)
        #填写更全面的描述信息，让更多的人看到你吧！
        page.locator("css=.post-content").fill(habit_detail)
        time.sleep(3)
        page.mouse.down()
        page.mouse.down()
        time.sleep(1)
        # 发布
        page.locator("xpath=//button[./span[text()='发布']]").click()
        print("发布")
        time.sleep(8)
    
    def upload_mp4(self, mp4_file_path: str, habit_name: str, habit_detail:str):
        """
          upload_picture
        """
        with sync_playwright() as playwright:
            display_headless = False
            #display_headless = True
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            #self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            self.browser = playwright.chromium.launch(headless=display_headless)
            login_page = self.login_or_restore_cookies()
            self.auto_up_mp4(login_page, mp4_file_path, habit_name, habit_detail)
            self.browser.close()

    def auto_up_mp4(self, page: Page, mp4_file_path: str, habit_name: str, habit_detail:str):
        """
        上传视频
        """
        page.goto(self.upload_picture_url)
        time.sleep(3)
        print(f"open  {self.upload_picture_url}")
        # 使用文本内容定位元素
        example_element = page.locator("xpath=//span[contains(text(), '上传视频')]")
        example_element.click()
        print("点击 上传视频")
        time.sleep(4)
        
        # 点击选择文件，输入文件
        with page.expect_file_chooser() as fc_info:
            page.locator('.drag-over').locator('nth=0').click()
        file_chooser = fc_info.value
        file_chooser.set_files(mp4_file_path)

        time.sleep(180)
        print("上传视频")
        #填写标题，可能会有更多赞哦～
        page.locator("css=.c-input_inner").fill(habit_name)
        time.sleep(3)
        #填写更全面的描述信息，让更多的人看到你吧！
        page.locator("css=.post-content").fill(habit_detail)
        time.sleep(3)
        page.mouse.down()
        page.mouse.down()
        time.sleep(1)
        # 发布
        page.locator("xpath=//button[./span[text()='发布']]").click()
        print("发布")
        time.sleep(8)
    #################################################################################
        
    def crate_browser_instance(self):
        """
        crate_browser_instance
        https://playwright.dev/python/docs/library
        playwright = sync_playwright().start()
        """
        display_headless = False
        playwright = sync_playwright().start()
        if platform.system() == "Linux":
            display_headless = True
            self.browser = playwright.chromium.launch(headless=display_headless)
        else:
            self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)

        self.page = self.login_or_restore_cookies()
        #self.msg_up_load(login_page, picture_path, habit_name, habit_detail)
               



def interface_auo_upload_myxiaohongshu(file_type,file_path,habit_name,habit_detail):
    """
      对外调用接口
    """
    sys = platform.system()
    login_url = "https://creator.xiaohongshu.com/login?source=official"
    upload_picture_url = "https://creator.xiaohongshu.com/publish/publish?source=official"
    upload_mp4_url = "https://creator.xiaohongshu.com/publish/publish?source=official"
    sys = platform.system()
    if sys == "Windows":
        cookies_path = r"D:\mp4\etc\xiaohongshu.json"
        save_picture_path = r"D:\mp4\etc\temp.png"
        default_picture_path = r"D:\mp4\etc\ZfCYoSG1BE_small.jpg"
        get_up_path = r"D:\mp4\etc\01_get_up.txt"
        out_path = r"D:\mp4\output"
        # BACK_PATH = r"D:\mp4\bak"
    elif sys == "Darwin":
        cookies_path = r"/Users/wangchuanyi/etcxiaohongshu.json"
        save_picture_path = r"/Users/wangchuanyi/etc/temp.png"
        default_picture_path = r"/Users/wangchuanyi/etc/ZfCYoSG1BE_small.jpg"
        get_up_path = '/Users/wangchuanyi/etc/01_get_up.txt'
    else:
        cookies_path = r"/root/bin/xiaohongshu.json"
        save_picture_path = r"/root/code/python/putdonwphone/upload/temp.png"
        default_picture_path = r"/root/code/python/putdonwphone/upload/ZfCYoSG1BE_small.jpg"
        get_up_path = '/root/code/python/config/01_get_up.txt'
        out_path = r"/root/mp4/output"
        # BACK_PATH = r"/root/mp4/bak"

    autoupload = CMyRedBook(cookies_path, login_url, upload_picture_url,upload_mp4_url)
    if file_type == "pic":
        print("this is pic")
        autoupload.upload_picture(file_path, habit_name, habit_detail)
    else:
        for root,_,files in os.walk(out_path):
            for file in files:
                # 拼接路径
                mp4_file_path = os.path.join(root,file)
                if file.endswith('.mp4'):
                    file_name = os.path.basename(mp4_file_path)
                    file_name = file_name.split('.')[0]
                    msg = "#" + file_name + "\r\n"
                    msg += habit_detail
                    print(habit_name)
                    if autoupload.upload_mp4(mp4_file_path,habit_name,msg):
                        logging.info("upload_mp4 %s", mp4_file_path)

def interface_not_quit_red_tool(file_type):
    """
      start 
    """
    file_path, habit_name,habit_detail  = englisword.interface_get_daily_englis_word()
    sys = platform.system()
    login_url = "https://creator.xiaohongshu.com/login?source=official"
    upload_picture_url = "https://creator.xiaohongshu.com/publish/publish?source=official"
    upload_mp4_url = "https://creator.xiaohongshu.com/publish/publish?source=official"
    sys = platform.system()
    if sys == "Windows":
        cookies_path = r"D:\mp4\etc\xiaohongshu.json"
        save_picture_path = r"D:\mp4\etc\temp.png"
        default_picture_path = r"D:\mp4\etc\ZfCYoSG1BE_small.jpg"
        get_up_path = r"D:\mp4\etc\01_get_up.txt"
        out_path = r"D:\mp4\output"
        # BACK_PATH = r"D:\mp4\bak"
    elif sys == "Darwin":
        cookies_path = r"/Users/wangchuanyi/mp4/etc/xiaohongshu.json"
        save_picture_path = r"/Users/wangchuanyi/mp4/etc/temp.png"
        default_picture_path = r"/Users/wangchuanyi/mp4/etc/ZfCYoSG1BE_small.jpg"
        get_up_path = '/Users/wangchuanyi/etc/01_get_up.txt'
    else:
        cookies_path = r"/root/bin/xiaohongshu.json"
        save_picture_path = r"/root/code/python/putdonwphone/upload/temp.png"
        default_picture_path = r"/root/code/python/putdonwphone/upload/ZfCYoSG1BE_small.jpg"
        get_up_path = '/root/code/python/config/01_get_up.txt'
        out_path = r"/root/mp4/output"
        # BACK_PATH = r"/root/mp4/bak"
   
    try:
            
        autoupload = CMyRedBook(cookies_path, login_url, upload_picture_url,upload_mp4_url)
        autoupload.crate_browser_instance()
        if file_type == "pic":
            print("this is pic")
            #autoupload.msg_up_load(autoupload.page,file_path, habit_name, habit_detail)
        else:
            print("mp4")

        # job_defaults = {
        #     'coalesce': False,
        #     'max_instances': 1
        # }
        # backsched = BlockingScheduler(job_defaults=job_defaults, timezone='Asia/Shanghai')
        # # self.msg_up_load(login_page, picture_path, habit_name, habit_detail)
        # backsched.add_job(autoupload.msg_up_load,
        #                   CronTrigger.from_crontab("52 22 * * *"),
        #                   args=[autoupload.page,file_path, habit_name,habit_detail])
        while True:
            autoupload.msg_up_load(autoupload.page,file_path, habit_name,habit_detail)
            steps = 12*60*60
            time.sleep(steps)
            print("start xiaohongshu")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        autoupload.browser.close()

####################################
def interface_auo_upload_mp4_myxiaohongshu(mp4_file_path):
    """
      对外调用接口
    """
    sys = platform.system()
    login_url = "https://creator.xiaohongshu.com/login?source=official"
    upload_picture_url = "https://creator.xiaohongshu.com/publish/publish?source=official"
    upload_mp4_url = "https://creator.xiaohongshu.com/publish/publish?source=official"
    sys = platform.system()
    if sys == "Windows":
        cookies_path = r"D:\mp4\etc\xiaohongshu_small.json"
        save_picture_path = r"D:\mp4\etc\temp.png"
        default_picture_path = r"D:\mp4\etc\ZfCYoSG1BE_small.jpg"
        get_up_path = r"D:\mp4\etc\01_get_up.txt"
        out_path = r"D:\mp4\output"
        # BACK_PATH = r"D:\mp4\bak"
    elif sys == "Darwin":
        cookies_path = r"/Users/wangchuanyi/xiaohongshu_small.json"
        save_picture_path = r"/Users/wangchuanyi/etc/temp.png"
        default_picture_path = r"/Users/wangchuanyi/etc/ZfCYoSG1BE_small.jpg"
        get_up_path = '/Users/wangchuanyi/etc/01_get_up.txt'
    else:
        cookies_path = r"/root/bin/xiaohongshu_small.json"
        save_picture_path = r"/root/code/python/putdonwphone/upload/temp.png"
        default_picture_path = r"/root/code/python/putdonwphone/upload/ZfCYoSG1BE_small.jpg"
        get_up_path = '/root/code/python/config/01_get_up.txt'
        out_path = r"/root/mp4/output"
        # BACK_PATH = r"/root/mp4/bak"

    autoupload = CMyRedBook(cookies_path, login_url, upload_picture_url,upload_mp4_url)
    file_name = os.path.basename(mp4_file_path)
    file_name = file_name.split('.')[0]
    habit_name = "#" + file_name + "\r\n"
    habit_name += " 日拱一卒无有尽，功不唐捐终入海" + "\r\n"
    print(habit_name)
    print(habit_name)
    if autoupload.upload_mp4(mp4_file_path,file_name,habit_name):
        logging.info("upload_mp4 %s", mp4_file_path)
# export PYTHONPATH="${PYTHONPATH}:/Users/wangchuanyi/python"
# cp __init__.py ../
if __name__ == '__main__':
    #interface_not_quit_red_tool("pic")
    interface_auo_upload_mp4_myxiaohongshu("")