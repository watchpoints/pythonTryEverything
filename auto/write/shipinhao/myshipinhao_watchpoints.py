"""This module provides 视频号助手"""
import time
import json
import os
import logging
import platform
import traceback
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from moviepy.editor import VideoFileClip,TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

#from pythonTryEverything.putdonwphone.data import englisword

########################################################################
class CMyShipinhao:
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
        self.page = None
        print("create CMyShipinhao")

    def __del__(self):
        print("CMyShipinhao is being destroyed")
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

    def upload_picture(self, picture_path: str, habit_name:str, habit_detail:str):
        """
          upload_picture
        """
        with sync_playwright() as playwright:
            display_headless = False
            #display_headless = True
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            sys = platform.system()
            if sys == "Linux":
              self.browser = playwright.chromium.launch(headless=display_headless)
            else:
                self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            #self.browser = playwright.chromium.launch(headless=display_headless)
            login_page = self.login_or_restore_cookies()
            print("login_or_restore_cookies")
            self.auto_upload_picture(login_page, picture_path, habit_name,habit_detail)
            self.browser.close()
    
    def get_video_properties(self,video_path):
        """
            功能：
            输出：
            输出：
        """
        try:
            clip = VideoFileClip(video_path)
            duration = clip.duration
            file_size = os.path.getsize(video_path)
            print(f"视频文件的时长为 {duration} 秒")
            print(f"视频文件的大小为 {file_size/1024/1204} M")
            return duration, file_size
        except Exception as myunkonw:
           print(f"发生异常：{myunkonw}")
     
    def upload_mp4(self, mp4_path: str,habit_name: str,habit_detail: str):
        """
          upload_mp4
        """
        logging.info("upload_mp4 %s",mp4_path)
        with sync_playwright() as playwright:
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
                self.browser = playwright.chromium.launch(headless=display_headless)
            else:
                display_headless = False
                self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            login_page = self.login_or_restore_cookies()
            try:
                self.msg_up_load_mp4(login_page, mp4_path, habit_name, habit_detail)
            except Exception :
                print(traceback.format_exc())
                self.browser.close()
                return False
                
            self.browser.close()
        return True
        
    def login_or_restore_cookies(self) -> Page:
        """
          登录
        """
        userAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.21 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            userAgent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        
        context = self.browser.new_context(user_agent=userAgent)
        context.clear_cookies()
        page = context.new_page()
        page.goto(self.login_url)

        if os.path.exists(self.cookies_path):
            print("load cookies >>>>>>>>>>>>>>>>")
            # 从文件中加载 cookies
            with open(self.cookies_path, 'r',encoding='utf-8') as myfile:
                cookies = json.load(myfile)
            print(cookies)
            context.add_cookies(cookies)
            time.sleep(3)
        else:
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            time.sleep(60)
            cookies = page.context.cookies()
            with open(self.cookies_path, 'w',encoding='utf-8') as myfile:
                myfile.write(json.dumps(cookies))
        print("restore_cookies >>>>>>>>>>> ")
        return page

    def auto_upload_picture(self, page: Page, picture_path: str,habit_name:str, habit_detail:str):
        """
        auto_upload_picture
        """
        page.goto(self.upload_mp4_url)
        print(f"open load {self.upload_mp4_url}")
        time.sleep(15)
        page.wait_for_url(self.upload_mp4_url)
        
        # 请上传2小时以内的视频
        #print("上传时长2小时内，大小不超过4GB，建议分辨率720p")
        # performs action and waits for a new `FileChooser` to be created
        with page.expect_file_chooser() as fc_info:
            page.locator("xpath=//div[./span[text()='上传时长2小时内，大小不超过4GB，建议分辨率720p及以上，码率10Mbps以内，格式为MP4/H.264格式']]").click()
        print("upload file begin")
        file_chooser = fc_info.value
        file_chooser.set_files(picture_path)
        # 预备文件上传时间
        time.sleep(20)
        print(picture_path)
        page.mouse.down()
        
        # <div contenteditable="" data-placeholder="添加描述" class="input-editor"></div>
        page.locator(".input-editor").fill(habit_detail)
        time.sleep(1)
        
        # <input type="text" name="" placeholder="概括视频主要内容，字数建议6-16个字符" class="weui-desktop-form__input">
        page.get_by_placeholder("概括视频主要内容，字数建议6-16个字符").fill(habit_name)
        time.sleep(1)
        #print(habit_name)
        page.get_by_role("button", name="发表").click()
        #print("发表")
        time.sleep(3)
        cookies = page.context.cookies()
        with open(self.cookies_path, 'w',encoding='utf-8') as myfile:
            myfile.write(json.dumps(cookies))
        time.sleep(5)

    def msg_up_load_mp4(self, page: Page, mp4_path: str,habit_name: str,habit_detail: str):
        """
        msg_up_load_mp4
        """
        print("msg_up_load_mp4")
        page.goto(self.upload_mp4_url)
        print(f"open load {self.upload_mp4_url}")
        time.sleep(15)
        page.wait_for_url(self.upload_mp4_url)
        
       # 请上传2小时以内的视频
        print("msg_up_load_mp4")
        # performs action and waits for a new `FileChooser` to be created
        with page.expect_file_chooser() as fc_info:
            page.locator("xpath=//div[./span[text()='上传时长2小时内，大小不超过4GB，建议分辨率720p及以上，码率10Mbps以内，格式为MP4/H.264格式']]").click()
        print("upload file begin")
        file_chooser = fc_info.value
        file_chooser.set_files(mp4_path)
        # 预备文件上传时间
        time.sleep(180)
        print(mp4_path)
        page.mouse.down()
        
        # <div contenteditable="" data-placeholder="添加描述" class="input-editor"></div>
        page.locator(".input-editor").fill(habit_detail)
        time.sleep(8)
        
        # <input type="text" name="" placeholder="概括视频主要内容，字数建议6-16个字符" class="weui-desktop-form__input">
        page.get_by_placeholder("概括视频主要内容，字数建议6-16个字符").fill(habit_name)
        time.sleep(8)
        print(habit_name)
        page.mouse.down()
        page.mouse.down()
        time.sleep(3)
        page.get_by_role("button", name="发表").click()
        #print("发表")
        time.sleep(5)
       
    #################################################################################


def interface_auo_upload_shipinhao(upload_type:str,out_path:str, bak_path:str):
    """
      对外调用接口
    """
    try:
        sys = platform.system()
        login_url = "https://channels.weixin.qq.com/"
        upload_picture_url = "https://channels.weixin.qq.com/platform/post/create"
        upload_mp4_url = "https://channels.weixin.qq.com/platform/post/create"
        if sys == "Windows":
            cookies_path = r"D:\mp4\etc\shipinhao_xiaohao.json"
        elif sys == "Darwin":
             cookies_path = r"/Users/wangchuanyi/etc/shipinhao_xiaohao.json"
        else:
            cookies_path = r"/root/bin/shipinhao_xiaohao.json"

        file_path, habit_name,habit_detail = englisword.interface_get_daily_englis_word_pic()
        
        
        autoupload = CMyShipinhao(cookies_path, login_url, upload_picture_url,upload_mp4_url)
        if upload_type == "pic":
            autoupload.upload_picture(file_path,habit_name,habit_detail)
            return
        for root,_,files in os.walk(out_path):
            for file in files:
                # 拼接路径
                time.sleep(5)
                mp4_file_path = os.path.join(root,file)
                print(mp4_file_path)
                duration, file_size = autoupload.get_video_properties(mp4_file_path)
                if  duration > 60*5 or  file_size /1024/1024  > 80:
                    print("超过80M和 5分钟")
                    continue
                    
                if file.endswith('.mp4') or file.endswith('.flv'):
                    file_name = os.path.basename(mp4_file_path)
                    bak_file_name_path =os.path.join(bak_path, file_name)
                    print(file_name)
                    print(bak_file_name_path)
                    file_name = os.path.splitext(os.path.basename(mp4_file_path))[0]
                    msg = "#" + file_name + "\r\n"
                    msg += "#正能量" + "\r\n"
                    msg += "#关注我,每天持续更新" + "\r\n"
                    msg += "直播精彩回放" + "\r\n"
                    msg += habit_detail
                    print(msg)
                    if autoupload.upload_mp4(mp4_file_path,habit_name,msg):
                        print("autoupload.upload_mp4 is ok ")
                        logging.info("upload_mp4 %s", mp4_file_path)
                        # 用完删除，我是最后一个使用的 我需要删除
                        if os.path.exists(mp4_file_path):
                            os.remove(mp4_file_path)
        print("mp4 done")
    except ValueError:
        print("Could not convert data to an integer.")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print(traceback.format_exc())
##################################################

def interface_not_quit_auto_shipinhao_window():
    """
      视频号 有窗口 window常驻定时发送
    """
    file_path, habit_name,habit_detail  = englisword.interface_get_daily_englis_word_pic()
    sys = platform.system()
    login_url = "https://channels.weixin.qq.com/"
    upload_picture_url = "https://channels.weixin.qq.com/platform/post/create"
    upload_mp4_url = "https://channels.weixin.qq.com/platform/post/create"
    sys = platform.system()
    if sys == "Windows":
        cookies_path = r"D:\mp4\etc\shipinhao_xiaohao.json"
    elif sys == "Darwin":
        cookies_path = r"/Users/wangchuanyi/mp4/etc/xiaohongshu.json"
    else:
        cookies_path = r"/root/bin/xiaohongshu.json"
    try:
        autoupload = CMyShipinhao(cookies_path, login_url, upload_picture_url,upload_mp4_url)
        autoupload.crate_browser_instance()
        while True:
            # 发布图文
            autoupload.auto_upload_picture(autoupload.page,file_path, habit_name,habit_detail)
            # 发布视频
            steps = 12*60*60
            time.sleep(steps)
            print("--------------start xiaohongshu----------------")
    finally:
        autoupload.browser.close()
############################################################################

def interface_auto_upload_mp4_shipinhao(upload_type:str,mp4_file_path:str,head:str,body:str):
    """
      对外调用接口
    """
    try:
        sys = platform.system()
        login_url = "https://channels.weixin.qq.com/"
        upload_picture_url = "https://channels.weixin.qq.com/platform/post/create"
        upload_mp4_url = "https://channels.weixin.qq.com/platform/post/create"
        if sys == "Windows":
            cookies_path = r"D:\mp4\etc\shipinhao_watchpoint.json"
        elif sys == "Darwin":
             cookies_path = r"/Users/wangchuanyi/etc/shipinhao_watchpoint.json"
        else:
            cookies_path = r"/root/bin/shipinhao_watchpoint.json"

        #file_path, habit_name,habit_detail = englisword.interface_get_daily_englis_word_pic()
        
        
        autoupload = CMyShipinhao(cookies_path, login_url, upload_picture_url,upload_mp4_url)
        if upload_type == "pic":
            print("pic")
            #autoupload.upload_picture(file_path,habit_name,habit_detail)
            return
        
        duration, file_size = autoupload.get_video_properties(mp4_file_path)
        if  duration > 60*15 or  file_size /1024/1024  > 300:
            #print("超过80M和 15分钟")
            print("超过300M和 15分钟")
            return
        file_name = os.path.splitext(os.path.basename(mp4_file_path))[0]
        habit_name = file_name
        msg = "#" + file_name + "\r\n"
        msg += "日拱一卒无有尽，功不唐捐终入海" + "\r\n"
        print(msg)
        if autoupload.upload_mp4(mp4_file_path,habit_name,msg):  
            print("mp4 done")
    except ValueError:
        print("Could not convert data to an integer.")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print(traceback.format_exc())
if __name__ == '__main__':
    #interface_not_quit_auto_shipinhao_window()
    print("11")
