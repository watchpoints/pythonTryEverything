"""This module provides 发文助手"""

from auto.write.shipinhao import  myshipinhao_watchpoints

import os
import logging
import platform
import random
import time
import shutil
from apscheduler.schedulers.blocking import BlockingScheduler

from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from putdonwphone import  ffmeg_to_mp4
from putdonwphone import  englisword
from putdonwphone.not_watch_news.zhihu import not_watch_zhihu_news_10_min_small
from putdonwphone import  mykuaishou2

LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
def auto_window_task():
    """headless自动操作"""
    file_path, habit_name,habit_detail  = englisword.interface_get_daily_englis_word()
    time.sleep(random.randint(1,5))
    if platform.system() == "Windows":
        OUT_PATH = r"D:\mp4\output"
        BACK_PATH = r"D:\mp4\bak"
    else:
        OUT_PATH = r"/root/mp4/output"
        BACK_PATH = r"/root/mp4/bak"
    try:
        # cookies台容易过去了 因此去掉了
        time.sleep(random.randint(1,5))
        not_watch_zhihu_news_10_min_small.interface_auo_upload_zhihu_small()
        logging.info("---------------myzhihu-----------------")
        time.sleep(random.randint(1,5))
        mykuaishou2.interface_auo_upload_kuaishou2("pic",file_path, habit_name,habit_detail)
        logging.info("---------------mykuaishou2-----------------")
    finally:
        print("---------------")


def find_mp4_files(directory):
    mp4_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp4'):
                mp4_files.append(os.path.join(root, file))
    return mp4_files

def auto_upload_mp4():
    """_summary_
    """
    if platform.system() == "Windows":
        input_path = r"D:\mp4\auto_write\mp4"
        back_path = r"D:\mp4\bak"
    else:
        input_path = r"/root/mp4/output"
        back_path = r"/root/mp4/bak"
    file_list = find_mp4_files(input_path)
    if len(file_list) == 0:
        logging.info("no task")
        return
    for file in  file_list:
        try:
            print(file)
            myshipinhao_watchpoints.interface_auto_upload_mp4_shipinhao("mp4",file,"","")
        finally:
            print("...")
            # 删除文件
            temp =  os.path.join(back_path, os.path.basename(file))
            if os.path.exists(temp):
                os.remove(file)
            else:
                shutil.move(file, back_path)
                print(file_list)
                print(back_path)
    time.sleep(1)
    # 遍历目录
    for root, __, files in os.walk(input_path):
        for file in files:
            if file.endswith(".mp4"):
                file_path = os.path.join(root, file)
                # 删除文件
                os.remove(file_path)
                print(f"已删除文件: {file_path}")

def change_mp4_to_small():
    """_summary_
    """
    logging.debug("change_mp4_to_small")
    try:
        ffmeg_to_mp4.interface_mp4_to_post()
    except Exception as myunkonw:
        logging.error(f"处理视频文件时出错: {str(myunkonw)}")
#########################
class TimeoutException(Exception):
    pass
def timeout_handler(signum, frame):
    """_summary_
    Args:
        signum (_type_): _description_
        frame (_type_): _description_

    Raises:
        TimeoutException: _description_
    """
    raise TimeoutException("Function execution timed out.")
###########################################################
 
if __name__ == "__main__":
    if platform.system() == "Windows":
        log_path = r"D:\mp4\log\pythonTryEverythingWin.log"
    else:
        log_path = "pythonTryEverythingWin.log"
        
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        filename=log_path
                        )

    logging.info("""
        ┌──────────────────────────────────────────────────────────────────────┐
        │                                                                      │    
        │                      •  Start pythonTryEverythingWin  •                             │
        │                                                                      │
        └──────────────────────────────────────────────────────────────────────┘
    """)

    job_defaults = {
        'coalesce': False,
        'max_instances': 1
    }
    auto_upload_mp4()
    #auto_window_task()
    backsched = BlockingScheduler(job_defaults=job_defaults, timezone='Asia/Shanghai')
    # 习惯养成--早睡早起
    # pip install apscheduler
    #12点:发一个图文
    backsched.add_job(auto_window_task, CronTrigger.from_crontab("0 18 * * *"), id="get_up")
    #1点:开始切换文件
    #backsched.add_job(change_mp4_to_small, CronTrigger.from_crontab("0 1 * * *"), id="cut_big_file")
    #4点:开始上传文件
    backsched.add_job(auto_upload_mp4, CronTrigger.from_crontab("0 6 * * *"), id="put_small_file")
    print("start pythonTryEverythingWin")
    backsched.start()
    