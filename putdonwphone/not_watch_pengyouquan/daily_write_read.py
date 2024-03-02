import os
import logging
import platform
import random
import time
import signal
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
    if platform.system() == "Windows":
        input_path = r"D:\mp4\dail_note"
        back_path = r"D:\mp4\bak"
    else:
        input_path = r"/root/mp4/output"
        back_path = r"/root/mp4/bak"

    #01 获取资源
    file_path, habit_name,habit_detail  = englisword.interface_get_daily_englis_word()
    time.sleep(random.randint(1,5))
    
    #02 发表内容
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
    #03  删除资源


def auto_upload_mp4():
    
    time.sleep(random.randint(1,5))
    if platform.system() == "Windows":
        OUT_PATH = r"D:\mp4\output"
        BACK_PATH = r"D:\mp4\bak"
    else:
        OUT_PATH = r"/root/mp4/output"
        BACK_PATH = r"/root/mp4/bak"
    try:
        print("")
    finally:
        print("...")
        
def change_mp4_to_small():
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
    auto_window_task()
    backsched = BlockingScheduler(job_defaults=job_defaults, timezone='Asia/Shanghai')
    # 习惯养成--早睡早起
    # pip install apscheduler
    #12点:发一个图文
    backsched.add_job(auto_window_task, CronTrigger.from_crontab("0 8 * * *"))
    backsched.add_job(auto_window_task, CronTrigger.from_crontab("0 12 * * *"))
    backsched.add_job(auto_window_task, CronTrigger.from_crontab("0 18 * * *"))
    #1点:开始切换文件
    #backsched.add_job(change_mp4_to_small, CronTrigger.from_crontab("0 1 * * *"), id="cut_big_file")
    #4点:开始上传文件
    #backsched.add_job(auto_upload_mp4, CronTrigger.from_crontab("0 2 * * *"), id="put_small_file")
    print("start pythonTryEverythingWin")
    backsched.start()
    