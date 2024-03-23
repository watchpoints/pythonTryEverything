"""This module provides 发文助手"""

import os
import logging
import platform
import time
import shutil
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

### 本地目录
from auto.write.shipinhao import  myshipinhao_watchpoints
from auto.write.kuaishou import  auto_post_kuaisou
from auto.write.xiaohongshu import  auto_xiaohongsh_small
from auto.write.zhihu import  auto_write_zhihu_small
from auto.data import  englisword
from auto.write.csdn import auto_write_csdn
from auto.write.douyu import atuo_write_douyu
from auto.write.weibo import auto_write_weibo

LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'



def find_mp4_files(directory):
    """ 获取视频文件"""
    mp4_files = []
    for root, __, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp4'):
                mp4_files.append(os.path.join(root, file))
    return mp4_files

def find_daily_msg(directory_path):
    """ 每日输出内容 和图片内容"""
    pic_list = []
    content = ""
    for root, _, files in os.walk(directory_path):
        # 文件集合
        for file in files:
            if file.endswith(".png") or  file.endswith(".jpg"):
                file_path = os.path.join(root, file)
                pic_list.append(file_path)
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, encoding='UTF-8') as f:
                    print(f"文件 {file_path} 的内容是：")
                    for line in f:
                        #print(line.strip())  # 逐行读取并打印文件内容
                        content += (line.strip()) + "\r\n"
                        print(content)
    print("===================")
    print(content)
    return content,pic_list


def auto_upload_mp4():
    """_summary_
    """
    print("auto_upload_mp4")
    if platform.system() == "Windows":
        input_path = r"D:\mp4\auto_write\mp4"
        back_path = r"D:\mp4\bak"
    else:
        input_path = r"/root/mp4/output"
        back_path = r"/root/mp4/bak"
    file_list = find_mp4_files(input_path)
    if len(file_list) == 0:
        logging.info("no task")
        print("no task")
        return
    for file in  file_list:
        try:
            print(file)
            myshipinhao_watchpoints.interface_auto_upload_mp4_shipinhao("mp4",file,"","")
            print("interface_auto_upload_mp4_shipinhao.....")
            time.sleep(3)
            auto_post_kuaisou.interface_auo_upload_mp4_kuaishou(file)
            print("interface_auo_upload_mp4_kuaishou.....")
            time.sleep(3)
            auto_xiaohongsh_small.interface_auo_upload_mp4_myxiaohongshu(file)
            print("interface_auo_upload_mp4_myxiaohongshu.....")
            time.sleep(3)
            auto_write_zhihu_small.interface_auo_upload_mp4_zhihu(file)
            print("interface_auo_upload_mp4_myxiaohongshu.....")
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




#######################记录每日反思###################################

def auto_upload_thing():
    """
      每天写50字产品理解输出，10行代码
    """
    print("auto_upload_thing")
    
    file_path, habit_name,habit_detail = englisword.interface_get_daily_englis_word_pic()
    
    if platform.system() == "Windows":
        input_path = r"D:\mp4\auto_write"
        back_path = r"D:\mp4\bak"
    else:
        input_path = r"/root/mp4/auto_write"
        back_path = r"/root/mp4/bak"
    print(back_path)
    data,pic_list = find_daily_msg(input_path)
    print(data)
    if len(data) < 10:
        print("NO DATA")
    else:
        # 自己日更 鼓励自己
        habit_name = '日拱一卒'
        habit_detail = data
    if len(pic_list) == 0:
        pic_list = file_path
    else:
        pic_list.append(pic_list)
    
    print(habit_detail)
    print(pic_list)
    try:
        
        time.sleep(3)
        auto_write_zhihu_small.interface_auo_upload_msg_zhihu(pic_list,habit_name,habit_detail)
        print("interface_auo_upload_msg_zhihu.....")

        time.sleep(3)
        auto_write_csdn.interface_auo_upload_mycsdn(pic_list,habit_name,habit_detail)
        print("interface_auo_upload_mycsdn.....")

        time.sleep(3)
        auto_xiaohongsh_small.interface_auo_upload_msg_myxiaohongshu(pic_list,habit_name,habit_detail)
        print("interface_auo_upload_mp4_myxiaohongshu.....")

        time.sleep(3)
        atuo_write_douyu.interface_auto_post_msg_douyu(pic_list, habit_name, habit_detail)
        print("interface_auto_post_msg_douyu.....")

        time.sleep(3)
        auto_write_weibo.interface_auo_upload_msg_weibo(pic_list, habit_name, habit_detail)
        print("interface_auto_post_msg_douyu.....")

    finally:
        print("...")
    time.sleep(1)
    # 遍历目录
    for root, __, files in os.walk(input_path):
        for file in files:
            if file.endswith(".txt") or file.endswith(".jpg") or file.endswith(".png") :
                file_path = os.path.join(root, file)
                # 删除文件
                os.remove(file_path)
                print(f"已删除文件: {file_path}")
###########################################################
 
if __name__ == "__main__":
    if platform.system() == "Windows":
        LOG_PATH = r"D:\mp4\log\write.log"
    else:
        LOG_PATH = "write.log"
        
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        filename=LOG_PATH
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
    auto_upload_thing()
    #auto_window_task()
    backsched = BlockingScheduler(job_defaults=job_defaults, timezone='Asia/Shanghai')
    # 习惯养成--早睡早起
    # pip install apscheduler
    #12点:发一个图文
    backsched.add_job(auto_upload_thing, CronTrigger.from_crontab("0 6 * * *"), id="get_up")

    #4点:开始上传文件
    backsched.add_job(auto_upload_mp4, CronTrigger.from_crontab("0 7 * * *"), id="put_small_file")
    print("start pythonTryEverythingWin")
    backsched.start()
    