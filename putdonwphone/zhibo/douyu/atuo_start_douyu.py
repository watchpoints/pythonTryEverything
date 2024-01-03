"""This module provides mydouyn"""
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

######################global########################
LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
TOTAL_WORK_TIME = 180
TOTAL_COUNT= 0
one_work_time =30
#STEPS = 10
STEPS = 10
TOTAL_WORK_TIME_COUNT = 0
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
                self.browser = playwright.chromium.launch(channel="chrome",
                                                          headless=display_headless)
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
        if self.only_msg == 1:
            helper_admin_class_rule(page,self.watch_room_url,self.only_msg)
            return
        page.goto(self.zhibo_url)
        time.sleep(5)
        print(f"open  {self.zhibo_url}")
        page.mouse.down()
        print(picture_path,habit_name,habit_detail)
        
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
        time.sleep(1)
        print(rtpm_url)
        #rtmp://sendtc3.douyu.com/live
    
        
        # page.locator("div").filter(has_text="直播码").locator("svg").click()
        # dropdown1 = page.locator('xpath=//*[@id="root"]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[3]/div[2]/svg')
        # 元素匹配器 - nth
        dropdown1 = page.locator("css=.svgIcon--2ypAR1M.svg--2uID9Py").locator("nth=1")
        dropdown1.hover()
        time.sleep(1)
        dropdown1.click()
        # 等待2秒获取黏贴内容
        time.sleep(2)
        rtpm_code = pyperclip.paste()
        print("直播码")
        time.sleep(1)
        print(rtpm_code)
        logging.debug(rtpm_code)
        #11975253rWycoTVM?wsSecret=d3f8b9b7cb13599952f8d3e8fae27901&wsTime=65915099&wsSeek=off&wm=0&tw=0&roirecognition=0&record=flv&origin=tct&txHost=sendtc3.douyu.com
        
        rtmp_stream =  rtpm_url + "/" + rtpm_code
        logging.debug(rtpm_code)
        print(rtmp_stream)
        # 开始推流
        # Create a thread with arguments
        my_thread = threading.Thread(target=rtmp_timeout_task, args=(self.input_directory, rtmp_stream))
        #Start the thread
        my_thread.daemon = True
        my_thread.start()
        time.sleep(1)
        #rtmp_timeout_task(self.input_directory,rtmp_stream)
        print(self.watch_room_url)
        
        helper_admin_class_rule(page,self.watch_room_url,self.only_msg)
                
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
        time.sleep(10)
        page.get_by_text("直接下播").click()
        time.sleep(10)

def helper_admin_class_rule(page: Page, watch_room_url, only_msg):
    """弹幕提醒"""
    global TOTAL_COUNT
    page.goto(watch_room_url)
    time.sleep(5)
    page.mouse.down()
    page.mouse.down()
    print("count")
    count = 0
    # 累计3个小时 自动退出
    while True:
        
        if count > 24 or page.is_closed() :
            return
        if only_msg ==1 or only_msg ==3:
            task = get_task_msg()
            print(task)
            page.get_by_placeholder("这里输入聊天内容").fill(task)
            time.sleep(1)
            page.locator("css=.ChatSend-button ").click()
        print(count)
        sleep_time = STEPS*60 + random.randint(1,10)
        TOTAL_COUNT += 1
        count +=1
        time.sleep(sleep_time)
def get_task_msg():
    """ task"""
    global TOTAL_COUNT
    global TOTAL_WORK_TIME_COUNT
    get_work_time =  STEPS*TOTAL_COUNT
    TOTAL_WORK_TIME_COUNT +=STEPS
    print(get_work_time)
    get_off_work_time = TOTAL_WORK_TIME - get_work_time
    get_rest_time  = one_work_time - get_work_time
    print(get_rest_time)

    if get_off_work_time <= 0 or  get_rest_time <= 0:
        get_off_work_time = 0
        get_rest_time = 0
        TOTAL_COUNT = 0

    # task =" 专注番茄时间 30分钟工作 5分钟休息" + "\r\n"
    task = "累计学习：" + str(TOTAL_WORK_TIME_COUNT) + "分钟"
    task +=" 距离下播" + str(get_off_work_time) + "分钟"
    # task += "距离下次休息：" + "\r\n"
    if 30 == get_rest_time:
        task += "倒计时30分钟，别急，先给自己一个微笑，休息马上来了:" + "\r\n"
    elif 20 == get_rest_time:
        task += "20分钟倒计时，是不是感觉到了一阵小激动？预热一下休息模式吧:" + "\r\n"
    elif 10 == get_rest_time:
        task += "咦，倒计时10分钟啦！是不是感觉到一阵轻松的氛围？:" + "\r\n"
    elif 0 == get_rest_time:
        task += "倒计时结束！是不是期待已久的休息时间？把握住，开启属于你的放松时刻吧:" + "\r\n"
    return task
def interface_auo_start_douyu_zhibo(input_directory, only_msg):
    """
      对外调用接口
    """
    login_url = "https://www.douyu.com/"
    zhibo_url = "https://www.douyu.com/creator/main/live"
    watch_room_url = "https://www.douyu.com/11975253"
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
        timestamp1 = time.time()
        while True:
            local_file_to_rtmp(input_directory,output_url)
            timestamp2 = time.time()
            time_difference = timestamp2 - timestamp1
            if int(time_difference) > 10800:
                logging.info("timeout")
                break
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
    
    result = subprocess.run(ffmpeg_cmd, shell=True,capture_output=True, text=True,check=False, encoding='utf-8',timeout=10800)

    # 获取命令执行结果
    output = result.stdout
    error = result.stderr

    # 打印输出结果
    print(output)
    # 打印错误结果
    print(error)



if __name__ == '__main__':
    if platform.system() == "Windows":
        LOG_PATH = r"D:\mp4\log\douyu.log"
    else:
        LOG_PATH = "douyu.log"
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        filename=LOG_PATH
                        )

    job_defaults = {
        'coalesce': False,
        'max_instances': 1
    }
    MP4_DIR = r"D:\mp4\speak"
    # 1.  只留言 2   只直播 3. 留言和和直播一块不支持。
    ONLIY_MSG = 2
    # interface_auo_start_douyu_zhibo(MP4_DIR,ONLIY_MSG)
    backsched = BlockingScheduler(job_defaults=job_defaults, timezone='Asia/Shanghai')
    # 习惯养成--早睡早起
    # pip install apscheduler
    #12点:发一个图文
    backsched.add_job(interface_auo_start_douyu_zhibo,
                     CronTrigger.from_crontab("30 6 * * *"), args=[MP4_DIR,ONLIY_MSG],id="get_up")

    backsched.add_job(interface_auo_start_douyu_zhibo,
                     CronTrigger.from_crontab("0 12 * * *"), args=[MP4_DIR,ONLIY_MSG],id="get_mid")
    
    backsched.add_job(interface_auo_start_douyu_zhibo,
                      CronTrigger.from_crontab("30 17 * * *"), args=[MP4_DIR,ONLIY_MSG],id="get_sleep")
    backsched.start()
    # playwright codegen https://www.douyu.com/creator/main/live
