#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author: watchpoints
# FileName:RSS
# DateTime:2024/06/10 17:00
import os
import platform
import logging
from auto.data import myrss
from auto.write.zhihu import auto_ai_zhihu_news
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
################ 全局变量#################
global_count = 30
###############01 获取数据#################
def get_daily_drawing():
    """
      每天一句中国古诗词，生成 AI 图片 Powered by Bing DALL-E-3.
      https://we-drawing.com/
    """
    rss = myrss.PoetryRSS("https://we-drawing.com/rss.xml")
    my_list = rss.get_context()
    global global_count 
    temp = 0
    daily_item = []
    # 每天发布三个记录
    for index, item in enumerate(my_list):
        print(f"索引 {index} 的内容是 {item}")
        if global_count == index:
            global_count+=1
            logging.info("day"+str(global_count))
            temp+=1
            daily_item.append(item)
            # # 打印标题
            # print("诗词标题：", item['art_title'])

            # # 打印链接
            # print("诗词链接：", item['art_link'])

            # # 打印描述
            # print("诗词描述：", item['art_desc'])

            # # 打印更新日期
            # print("更新日期：", item['art_update'])
            # art_link = item['art_link']
        print(global_count)
        if temp == 3:
            break
    if len(daily_item) == 0:
        print("error  get data is null")
        return [];
    sys = platform.system()
    if sys == "Windows":
        picture_path = r"D:\mp4\etc\daily"
    elif sys == "Darwin":
        picture_path = r"/Users/wangchuanyi/mp4/etc/daily"
    else:
        picture_path = r"/root/bin/daily"
    count = 0
    result = []
    for item in daily_item:
        file_path = os.path.join(picture_path, str(count))
        count+=1
        # 输出拼接的路径
        print(file_path)
        # https://we-drawing.com/images/1715122872472/
        # https://daily-poetry-image.vercel.app/images/1715122872472
        # 原始网址
        original_url = item['art_link']
        # 需要替换的部分
        old_part = "https://daily-poetry-image.vercel.app/images/"
        new_part = "https://we-drawing.com/images/"

        # 替换部分
        new_url = original_url.replace(old_part, new_part)

        # 输出替换后的网址
        print(new_url)
        myrss.get_daily_poetry(new_url,file_path)
        data1 = {"art_title": item['art_title'],
                "art_desc": item['art_desc'],
                "art_update": item['art_update'],
                "file_path": file_path,
                }
        result.append(data1)
    return result

###########################02 发布内容#######################
def post_thing_daily_porety_drawing():
    """
    每天一句中国古诗词，生成 AI 图片 Powered by Bing DALL-E-3.
    https://we-drawing.com/images/1715122872472/
    https://daily-poetry-image.vercel.app/images/1715122872472
    
    """
    ## 第一步 诗词作为提示词 绘制图片
    result = get_daily_drawing()
    for item in result:
        print(item)
    ## 第二步：发布想法
    auto_ai_zhihu_news.post_poetry_drawing_to_zhihu_thing(result)
  
if __name__ == '__main__':
    post_thing_daily_porety_drawing()
    job_defaults = {
         'coalesce': False,
         'max_instances': 1
    }
    backsched = BlockingScheduler(job_defaults=job_defaults, timezone='Asia/Shanghai')
    # 汇总 最新资料 每日新闻
    backsched.add_job(post_thing_daily_porety_drawing, CronTrigger.from_crontab("12 0 * * *"))
    backsched.start()

