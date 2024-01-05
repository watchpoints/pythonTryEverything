import os
import logging
import platform
import random
import time
import signal
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from putdonwphone import  myshipinhao
from putdonwphone import  ffmeg_to_mp4
from putdonwphone import myxiaohongshu  
from putdonwphone import  englisword
from putdonwphone import  myzhihu
from putdonwphone import  mykuaishou2

LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
def auto_window_task():
    
    file_path, habit_name,habit_detail  = englisword.interface_get_daily_englis_word()
    print(file_path)
    print(habit_name)
    print(habit_detail)
    time.sleep(random.randint(1,50))
    if platform.system() == "Windows":
        OUT_PATH = r"D:\mp4\output"
        BACK_PATH = r"D:\mp4\bak"
    else:
        OUT_PATH = r"/root/mp4/output"
        BACK_PATH = r"/root/mp4/bak"
    try:
        # cookies台容易过去了 因此去掉了
        # time.sleep(random.randint(1,50))
        # myshipinhao.interface_auo_upload_shipinhao("pic",OUT_PATH, BACK_PATH)
        time.sleep(random.randint(1,50))
        myxiaohongshu.interface_auo_upload_myxiaohongshu("pic",file_path,habit_name,habit_detail)
        time.sleep(random.randint(1,50))
        myzhihu.interface_auo_upload_zhihu()
        mykuaishou2.interface_auo_upload_kuaishou2("pic",file_path, habit_name,habit_detail)
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

def my_test():
    """_summary_
    """
    file_path, habit_name,habit_detail  = englisword.interface_get_daily_englis_word()
    print(file_path)
    print(habit_name)
    print(habit_detail)
    mykuaishou2.interface_auo_upload_kuaishou2("pic",file_path, habit_name,habit_detail)
    # myzhihu.interface_auo_upload_zhihu()
    # myxiaohongshu.interface_auo_upload_myxiaohongshu("pic",file_path,habit_name,habit_detail)
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
    my_test()
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
    