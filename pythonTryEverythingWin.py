import os
import logging
import platform
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from putdonwphone import  myshipinhao
import random
import time


LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
def auto_window_task():
    
    time.sleep(random.randint(10,300))
    if platform.system() == "Windows":
        OUT_PATH = r"D:\mp4\output"
        BACK_PATH = r"D:\mp4\bak"
    else:
        OUT_PATH = r"/root/mp4/output"
        BACK_PATH = r"/root/mp4/bak"
    try:
        myshipinhao.interface_auo_upload_shipinhao("pic",OUT_PATH, BACK_PATH)
    finally:
        print("interface_auo_upload_shipinhao")
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        filename="./pythonTryEverythingWin.log"
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
    #backsched.add_job(EeasyHabitSleep, CronTrigger.from_crontab("30 2 * * *"), id="get_up")
    backsched.add_job(auto_window_task, CronTrigger.from_crontab("30 0 * * *"), id="get_up")
    print("start pythonTryEverythingWin")
    backsched.start()
    