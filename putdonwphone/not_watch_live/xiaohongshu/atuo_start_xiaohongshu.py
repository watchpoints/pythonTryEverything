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

def rtmp_timeout_task(input_directory,output_url):
    """_summary_

    Args:
        input_directory (_type_): _description_
        output_url (_type_): _description_
    """
    try:
        # 设置超时时间为3个小时
        timestamp1 = time.time()
        while True:
            local_file_to_rtmp(input_directory,output_url)
            timestamp2 = time.time()
            time_difference = timestamp2 - timestamp1
            if int(time_difference) > 3*60*60:
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
    ffmpeg_cmd = f'ffmpeg -re -i {input_file} -c:v libx264 -preset veryfast -maxrate 300k -bufsize 600k -pix_fmt yuv420p -c:a aac -b:a 128k  -f flv -y "{rtmp_url}"'
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

def start_live_stream1(input_file, rtmp_url):
    """_summary_

    Args:
        input_file (_type_): _description_
        output_url (_type_): _description_
    """
    sys.stdout.reconfigure(encoding='utf-8')
    # 构建 FFmpeg 命令行，这里使用 -re 表示以实时速率读取输入文件
    ffmpeg_cmd = f'ffmpeg -re -i {input_file} -vcodec copy -acodec copy  -f flv -y "{rtmp_url}"'
    print(ffmpeg_cmd)
    logging.info(ffmpeg_cmd)
    
    result = subprocess.run(ffmpeg_cmd, shell=True,capture_output=True, text=True,check=False, encoding='utf-8',timeout=10800)

    # 获取命令执行结果
    output = result.stdout
    error = result.stderr

    # 打印输出结果
    print(output)
    # 打印错误结果
    print(error)


def interface_auo_start_xiaohongshu_zhibo(path,rtmp_url):
    """test"""
    rtmp_timeout_task(path,rtmp_url)

# playwright codegen https://link.bilibili.com/p/center/index#/my-room/start-live
if __name__ == '__main__':
    if platform.system() == "Windows":
        LOG_PATH = r"D:\mp4\log\xiaohongshu.log"
        MP4_DIR = r"D:\mp4\heng_sleep"
    if platform.system() == "Darwin":
        LOG_PATH = r"/Users/wangchuanyi/mp4/log/bibi.log"
        MP4_DIR = r"/Users/wangchuanyi/mp4/zhibo"
    else:
        LOG_PATH = "xiaohongshu.log"
        MP4_DIR = r"D:\mp4\heng_sleep"
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        filename=LOG_PATH
                        )

    job_defaults = {
        'coalesce': False,
        'max_instances': 1
    }
    # https://www.xiao hongshu.com/zhibo/obs
    RTMP_URl = "rtmp://live-push.xhscdn.com/live/"
    RTMP_URl += '569075723911978853?txSecret=cf816da64133cf4ce5a7ae0dfc9e3424&txTime=65C4ACA2&txDelayTime=0'

    interface_auo_start_xiaohongshu_zhibo(MP4_DIR,RTMP_URl)
  
