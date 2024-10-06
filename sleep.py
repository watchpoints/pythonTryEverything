"""This module provides 统一调度模块"""
import os
import logging
import signal
import platform
import shutil
import random
import time
import toutiao
import maimai
import douyu
import myblog
import mycsdn
import dedao
import zhishi
from kernel import interface_db
from third import mainWechatDaily
from putdonwphone import mykuaishou2
from putdonwphone import mydouyin
from putdonwphone import mytoutiao
from auto.zsxq import myzhihu
from putdonwphone import  mycsdn
from putdonwphone import  englisword

def get_up_tuwen():
    """
      早睡早起图文模式
    """
    try:
        file_path, habit_name,habit_detail  = englisword.interface_get_daily_englis_word()
        mykuaishou2.interface_auo_upload_kuaishou2("pic",file_path,habit_name,habit_detail)
        time.sleep(random.randint(1,10))
        myxiaohongshu.interface_auo_upload_myxiaohongshu("pic")
        time.sleep(random.randint(1,10))
        mydouyin.interface_auo_upload_mydouyin()
        time.sleep(random.randint(1,10))
        mytoutiao.interface_auo_upload_weitoutiao()
        time.sleep(random.randint(1,10))
        myzhihu.interface_auo_upload_zhihu()
        time.sleep(random.randint(1,10))
        mycsdn.interface_auo_upload_mycsdn(file_path,habit_name,habit_detail)
    finally:
        print("end")

def show_sleep():
    """
       起床打卡
    """
    try:
        get_up_tuwen()
        msgGetUp = interface_db.DailyGetUpEvent()
        if len(msgGetUp) == 0:
            logging.error("the DailyGetUpEvent is null")
            return
        try:
            # 微博发表完成
            myblog.KillChromebeta()
            # weibo.send_msg_to_weibo(msgGetUp)

            # 今日头条发表完成
            myblog.KillChromebeta()
            toutiao.post_sleep_toutiao()  # easy sleep

            # 斗鱼发表完成
            myblog.KillChromebeta()
            douyu.send_msg_to_douyu(msgGetUp)

            # 脉脉提醒 发表完成
            myblog.KillChromebeta()
            maimai.post_sleep_maimai()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            
        try:
            # csdn is ok
            myblog.KillChromebeta()
            mycsdn.send_msg_to_csdn(msgGetUp)

            # 得到定时提醒
            myblog.KillChromebeta()
            dedao.send_msg_to_dedao(msgGetUp)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        try:
            # 知识星球定时提醒
            # myblog.KillChromebeta()
            zhishi.send_msg_to_zhishi(msgGetUp)
            # whchat 
            mainWechatDaily.wechat_every_daily()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        
    finally:
        print("end")


# 起床打卡
def show_sleepForTest():
    """_summary_
    """
    show_sleep()


def send_msg_to_blog(wechat_txt: str):
    """_summary_

    Args:
        wechat_txt (str): _description_
    """
    try:
        myblog.KillChromebeta()
        # if not toutiao.send_msg_to_toutiao(wechat_txt):
        #     logging.error("post toutiao failed")
        # print("post send_msg_to_douyu")
        myblog.KillChromebeta()
        if not douyu.send_msg_to_douyu(wechat_txt):
            logging.error("post douyu failed")
        print("post send_msg_to_maimai")
        myblog.KillChromebeta()
        if not maimai.send_msg_to_maimai(wechat_txt):
            logging.error("post maimai failed")

        myblog.KillChromebeta()
        if not mycsdn.send_msg_to_csdn(wechat_txt):
            logging.error("post mycsdn failed")

        myblog.KillChromebeta()
        if not dedao.send_msg_to_dedao(wechat_txt):
            logging.error("post dedao failed")

        myblog.KillChromebeta()
        if not zhishi.send_msg_to_zhishi(wechat_txt):
            logging.error("post send_msg_to_zhishi failed")

    finally:
        signal.alarm(0)  # 成功完成任务，取消超时信号
        print("end")

def auto_upload_mp4():
    """ call """
    if platform.system() == "Windows":
        OUT_PATH = r"D:\mp4\output"
        BACK_PATH = r"D:\mp4\bak"
    else:
        OUT_PATH = r"/root/mp4/output"
        BACK_PATH = r"/root/mp4/bak"
    try:
        print("")
        #myshipinhao.interface_auo_upload_shipinhao(OUT_PATH, BACK_PATH)
    finally:
        print("interface_auo_upload_shipinhao")
    try:
        mykuaishou2.interface_auo_upload_kuaishou2("mp4")
    finally:
        print("interface_auo_upload_kuaishou2")
    try:
        myxiaohongshu.interface_auo_upload_myxiaohongshu("mp4")
    finally:
        print("interface_auo_upload_myxiaohongshu")

    # 上传完毕 移动到临时目录
    for root,_,files in os.walk(OUT_PATH):
        for file in files:
            file_path = os.path.join(root,file)
            if file.endswith('.mp4'):
                print(file_path)
                shutil.move(file_path, BACK_PATH)


############################
def auto_window_task():
    if platform.system() == "Windows":
        OUT_PATH = r"D:\mp4\output"
        BACK_PATH = r"D:\mp4\bak"
    else:
        OUT_PATH = r"/root/mp4/output"
        BACK_PATH = r"/root/mp4/bak"
    try:
        #myshipinhao.interface_auo_upload_shipinhao("pic",OUT_PATH, BACK_PATH)
        print("")
    finally:
        print("interface_auo_upload_shipinhao")

def my_test():
    """_summary_
    """
    file_path, habit_name,habit_detail  = englisword.interface_get_daily_englis_word()
    print(file_path)
    print(habit_name)
    print(habit_detail)
    mykuaishou2.interface_auo_upload_kuaishou2("pic",file_path,habit_name,habit_detail)
    #mycsdn.interface_auo_upload_mycsdn(file_path,habit_name,habit_detail)
if __name__ == '__main__':
    #auto_upload_mp4()
    #get_up_tuwen()
    #msg = interface_db.DailyGetUpEvent()
    #baidubaijia.send_msg_to_baidubaijia(msg)
    #mykuaishou2.interface_auo_upload_kuaishou2()
    # myxiaohongshu.interface_auo_upload_myxiaohongshu()
    # mydouyin.interface_auo_upload_mydouyin()
    # mytoutiao.interface_auo_upload_weitoutiao()
    # myzhihu.interface_auo_upload_zhihu()
    my_test()
