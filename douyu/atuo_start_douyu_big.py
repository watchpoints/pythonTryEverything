"""This module provides mydouyn"""
import time
import json
import os
import platform
import random
import subprocess
import shlex
import sys
import traceback
import threading
import pyperclip
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page




########################################################################
class CZTOUYU:
    """
    This class represents a GetupHabit.

    Parameters:
    - save_picture_path (str): The path to save pictures.
    - default_picture_path (str): The default path for pictures.
    """
    def __init__(self,cookies_path: str, login_url: str, zhibo_url: str, watch_room_url: str, mp4_input_directory: str, only_msg):
        self.cookies_path = cookies_path
        self.login_url = login_url
        self.zhibo_url = zhibo_url
        self.watch_room_url = watch_room_url
        # playwright 部分
        self.browser = None
        self.input_directory = mp4_input_directory
        self.only_msg = only_msg
        print("create CMyDouyin")

    def __del__(self):
        print("CMyDouyin is being destroyed")

    def auto_start_zhibo(self, picture_path: str, habit_name:str, habit_detail:str):
        """
          定时直播 不是24小时 推送 很容易断流 被扣分
        """
        with sync_playwright() as playwright:
            display_headless = False
            #display_headless = True
            if platform.system() == "Linux":
                display_headless = True
            if sys == "Linux":
              self.browser = playwright.chromium.launch(headless=display_headless)
            else:
                self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            login_page = self.login_or_restore_cookies()
            self.helper_start_zhibo(login_page, picture_path, habit_name,habit_detail)
            if self.browser.is_connected:
                self.browser.close()
    def auto_stop_zhibo(self):
        """停止直播"""
        with sync_playwright() as playwright:
            display_headless = False
            #display_headless = True
            if platform.system() == "Linux":
                display_headless = True
            if sys == "Linux":
                self.browser = playwright.chromium.launch(headless=display_headless)
            else:
                self.browser = playwright.chromium.launch(channel="chrome",
                                                          headless=display_headless)
            login_page = self.login_or_restore_cookies()
            self.helper_stop_zhibo(login_page)
            if self.browser.is_connected:
                self.browser.close()
    def login_or_restore_cookies(self) -> Page:
        """
          登录
        """
        context = self.browser.new_context()
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
            time.sleep(60)
            cookies = page.context.cookies()
            with open(self.cookies_path, 'w',encoding='utf-8') as f:
                f.write(json.dumps(cookies))
        print("login_or_restore_cookies")
        return page

    def helper_start_zhibo(self, page: Page, picture_path: str,habit_name:str, habit_detail:str):
        """
         解析直播推流地址：防止自动黑屏 断流后 扣费 定时直播2个小时。
        """
        # 只测试留言功能
        if self.only_msg:
            helper_admin_class_rule(page,self.watch_room_url)
            return
            
        page.goto(self.zhibo_url)
        time.sleep(5)
        print(f"open  {self.zhibo_url}")
        page.mouse.down()
        print(picture_path,habit_name,habit_detail)
        
        
        # # 如果一级开始 ，可以关闭
        # print("关闭直播")
        # aa = page.wait_for_timeout(2000).get_by_text("关闭直播")
        # page.get_by_text("关闭直播").click()
        # time.sleep(10)
        # page.get_by_text("直接下播").click()
        
        # Text match
        # https://sqa.stackexchange.com/questions/29079/how-to-access-a-hyper-link-using-xpath
        page.locator("xpath=//a[contains(text(),'开直播')]").click()
        time.sleep(5)
        
        print("开始直播")
        # many span 
        # page.locator("xpath=//div[span[text()='开始直播')]").click()
        # page.locator("css=.start--1NvkXEZ").click()
        page.locator('xpath=//*[@id="root"]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[3]/span[1]').click()
        time.sleep(5)
        # 申请成功，您现在可以直播了
        page.get_by_text("确定").click()
        time.sleep(5)
        print("确定")
        # 从直播房价调回去
        page.goto(self.zhibo_url)
        print(f"reload  {self.zhibo_url}")
        time.sleep(7)
        
        
        # # rtmp地址
        # rtpm_url = page.locator("css=.shark-Input.input--2DEflcU").inputValue()
        # print(rtpm_url)
        
        # #直播码
        # rtpm_code = page.locator("css=.shark-Input.input--2DEflcU").inputValue()
        # print(rtpm_url)
        
        # page.locator("div").filter(has_text="rtmp地址").locator("svg").click()
        # dropdown = page.locator('xpath=//*[@id="root"]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[3]/div[1]/svg')
        dropdown = page.locator("css=.svgIcon--2ypAR1M.svg--2uID9Py").locator("nth=0")
        dropdown.hover()
        time.sleep(1)
        dropdown.click()
        time.sleep(2)
        rtpm_url = pyperclip.paste()
        print(rtpm_url)
        #rtmp://sendtc3.douyu.com/live
    
        
        # page.locator("div").filter(has_text="直播码").locator("svg").click()
        # dropdown1 = page.locator('xpath=//*[@id="root"]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[3]/div[2]/svg')
        # 元素匹配器 - nth
        dropdown1 = page.locator("css=.svgIcon--2ypAR1M.svg--2uID9Py").locator("nth=1")
        dropdown1.hover()
        time.sleep(1)
        dropdown1.click()
        time.sleep(2)
        rtpm_code = pyperclip.paste()
        print("直播码")
        print(rtpm_code)
        time.sleep(2)
        #11975253rWycoTVM?wsSecret=d3f8b9b7cb13599952f8d3e8fae27901&wsTime=65915099&wsSeek=off&wm=0&tw=0&roirecognition=0&record=flv&origin=tct&txHost=sendtc3.douyu.com
        
        rtmp_stream =  rtpm_url + "/" + rtpm_code
        print(rtmp_stream)
        # 开始推流
        # Create a thread with arguments
        my_thread = threading.Thread(target=rtmp_timeout_task, args=(self.input_directory, rtmp_stream))
        # Start the thread
        my_thread.daemon = True
        my_thread.start()
       
        print(self.watch_room_url)
        
        # # Create a thread with arguments
        # my_msg = threading.Thread(target=helper_admin_class_rule, args=page)
        # # Start the thread
        # my_msg.daemon = True
        # my_msg.start()
       
        ## 每天定时直播 3个小时
        #time.sleep(60*60*3)
        # time.sleep(60*60*3)
        helper_admin_class_rule(page,self.watch_room_url)
                
        # 推送直播
        #关闭直播
        # page.locator("css=.close--1RVpTW1").click()
        # page.goto(self.zhibo_url)
        # time.sleep(5)
        # print("关闭直播")
        # page.get_by_text("关闭直播").click()
        # time.sleep(10)
        # page.get_by_text("直接下播").click()
        # time.sleep(10)
        self.auto_stop_zhibo()
        
    def helper_stop_zhibo(self, page: Page):
        """
         自动停直播
        """
        page.goto(self.zhibo_url)
        time.sleep(6)
        page.mouse.down()
        time.sleep(1)
        print("关闭直播")
        page.get_by_text("关闭直播").click()
        time.sleep(5)
        page.get_by_text("直接下播").click()
        time.sleep(5)

def helper_admin_class_rule(page: Page, watch_room_url):
        """
          弹幕提醒：
        """
        page.goto(watch_room_url)
        time.sleep(5)
        page.mouse.down()
        page.mouse.down()
        print("count")
        task = "认真学习使用：今日目标 敢于朗读"
        count = 0
        # 累计3个小时 自动退出
        while True:
            count +=1
            if count > 24:
                return
            page.get_by_placeholder("这里输入聊天内容").fill(task)
            time.sleep(1)
            page.locator("css=.ChatSend-button ").click()
            print(count)
            sleep_time = 300 + random.randint(1,10)
            time.sleep(sleep_time)
    


def interface_auo_start_douyu_zhibo(input_directory, only_msg):
    """
      对外调用接口
    """
    login_url = "https://www.douyu.com/"
    zhibo_url = "https://www.douyu.com/creator/main/live"
    watch_room_url = "https://www.douyu.com/1480416"
    if platform.system() == "Windows":
        cookies_path = r"D:\mp4\etc\zhibodouyu.json"
    else:
        cookies_path = r"/root/bin/zhibodouyu.json"
    
    file_path = ""
    habit_name = ""
    habit_detail =""
    autoupload = CZTOUYU(cookies_path, login_url, zhibo_url,watch_room_url,input_directory,only_msg)
    try:
        autoupload.auto_start_zhibo(file_path, habit_name,habit_detail)
    except Exception as mye:
        print(mye)
        traceback.print_exc()
        autoupload.auto_stop_zhibo()
        

def rtmp_timeout_task(input_directory,output_url):
    """_summary_

    Args:
        input_directory (_type_): _description_
        output_url (_type_): _description_
    """
    try:
        # signal.alarm(7200)   # 设置超时时间为2个小时 3个小时 10800
        while 1:
            local_file_to_rtmp(input_directory,output_url)
    except Exception as mye:
        print(mye)
        traceback.print_exc()
        
        

def local_file_to_rtmp(input_directory,output_url):
    """_summary_
    Args:
         # 本地文件夹路径，包含多个视频文件
         # 输出 URL，可以是 RTMP 服务器地址
    """
    random_file_list = []
    for root,_,files in os.walk(input_directory):
        for file in files:
            # 拼接路径
            file_path = os.path.join(root,file)
            if file_path.endswith('.mp4') or file_path.endswith('.flv'):
                random_file_list.append(file_path)
    print(random_file_list)
    if len(random_file_list) ==0:
        print("empty dir")
        return
    # 随机排序文件列表
    random.shuffle(random_file_list)
    print(random_file_list)
    
    # 遍历文件列表并推流
    for file_name in random_file_list:
        # 构建完整的文件路径
        if file_name.endswith('.mp4') or file_name.endswith('.flv'):
            print(file_name)
            start_live_stream(file_name, output_url)

def start_live_stream(input_file, rtmp_url):
    """_summary_

    Args:
        input_file (_type_): _description_
        output_url (_type_): _description_
    """
    sys.stdout.reconfigure(encoding='utf-8')
    # 构建 FFmpeg 命令行，这里使用 -re 表示以实时速率读取输入文件
    ffmpeg_cmd = f'ffmpeg -re -i {input_file} -vcodec copy -acodec copy  -f flv -y "{rtmp_url}"'
    print(ffmpeg_cmd)
    # cmd = shlex.split(ffmpeg_cmd)
    #https://blog.csdn.net/cnweike/article/details/73620250
    # Execute a child program in a new process.
    # https://docs.python.org/zh-cn/3/library/subprocess.html
    # Python：从subprocess运行的子进程中实时获取输出
    myp = subprocess.Popen(ffmpeg_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,text=True, encoding='utf-8')
    # oll() is None means that the child is still running.
    while myp.poll() is None:
        line = myp.stdout.readline()
        #https://juejin.cn/post/6926442577294000136
        line = line.strip()
        if line:
            print(line)
    #     # 通过循环实时获取输出
    # while True:
    #     # 从管道中读取一行输出
    #     output_line = myp.stdout.readline()

    #     # 判断输出是否为空，为空表示子进程已经结束
    #     if output_line == '' and myp.poll() is not None:
    #         break

    if myp.returncode == 0:
        print('Subprogram success')
    else:
        print('Subprogram failed')
        
    print(ffmpeg_cmd)
    # https://www.cnblogs.com/suwings/p/6216279.html
    result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,check=False, encoding='utf-8')
    # 获取命令执行结果
    output = result.stdout
    error = result.stderr

    # 打印输出结果
    print(output)
    # 打印错误结果
    print(error)

if __name__ == '__main__':
    # playwright codegen https://www.douyu.com/creator/main/live
    MP4_DIR = r"D:\mp4\speak"
    ## false 直播 --留言  true 只有留言
    ONLIY_MSG = False
    interface_auo_start_douyu_zhibo(MP4_DIR,ONLIY_MSG)
