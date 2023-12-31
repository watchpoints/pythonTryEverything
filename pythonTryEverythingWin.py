import os
import logging
import platform
import random
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from putdonwphone import  myshipinhao
from putdonwphone import  ffmeg_to_mp4
from putdonwphone import myxiaohongshu

LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
def auto_window_task():
    
    time.sleep(random.randint(1,50))
    if platform.system() == "Windows":
        OUT_PATH = r"D:\mp4\output"
        BACK_PATH = r"D:\mp4\bak"
    else:
        OUT_PATH = r"/root/mp4/output"
        BACK_PATH = r"/root/mp4/bak"
    try:
        myshipinhao.interface_auo_upload_shipinhao("pic",OUT_PATH, BACK_PATH)
        myxiaohongshu.interface_auo_upload_myxiaohongshu("pic")
    finally:
        print("interface_auo_upload_shipinhao")

def auto_upload_mp4():
    
    time.sleep(random.randint(1,10))
    if platform.system() == "Windows":
        OUT_PATH = r"D:\mp4\output"
        BACK_PATH = r"D:\mp4\bak"
    else:
        OUT_PATH = r"/root/mp4/output"
        BACK_PATH = r"/root/mp4/bak"
    try:
        myshipinhao.interface_auo_upload_shipinhao("mp4",OUT_PATH, BACK_PATH)
    finally:
        print("interface_auo_upload_shipinhao")
        
def change_mp4_to_small():
    logging.debug("change_mp4_to_small")
    try:
        ffmeg_to_mp4.interface_mp4_to_post()
    except Exception as myunkonw:
        logging.error(f"处理视频文件时出错: {str(myunkonw)}")
    

if __name__ == "__main__":
    if platform.system() == "Windows":
        log_path = r"D:\mp4\bak\pythonTryEverythingWin.log"
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
    backsched = BlockingScheduler(job_defaults=job_defaults, timezone='Asia/Shanghai')
    # 习惯养成--早睡早起
    # pip install apscheduler
    #12点:发一个图文
    backsched.add_job(auto_window_task, CronTrigger.from_crontab("0 0 * * *"), id="get_up")
    #1点:开始切换文件
    backsched.add_job(change_mp4_to_small, CronTrigger.from_crontab("0 1 * * *"), id="cut_big_file")
    #4点:开始上传文件
    backsched.add_job(auto_upload_mp4, CronTrigger.from_crontab("0 2 * * *"), id="put_small_file")
    print("start pythonTryEverythingWin")
    backsched.start()
    