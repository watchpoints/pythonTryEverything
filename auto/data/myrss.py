#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author:Jruing
# FileName:RSS
# DateTime:2020/5/29 13:59

from xml.dom.minidom import parseString
from datetime import datetime
import platform
import requests
import time
import os
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page


class PoetryRSS():
    """
         https://we-drawing.com/
    """
    def __init__(self, rss_url):
        self.rss_url = rss_url

    def get_context(self):
        response = requests.get(self.rss_url,timeout=20).text
        return self.parse_context(response)

    def parse_context(self, response):
        """
        <item>
            <title>况是青春日将暮，桃花乱落如红雨。</title>
            <link>https://daily-poetry-image.vercel.app/images/1715230672582/</link>
            <guid isPermaLink="true">https://daily-poetry-image.vercel.app/images/1715230672582/</guid>
            <description>今天诗词：况是青春日将暮，桃花乱落如红雨。</description>
            <pubDate>Thu, 09 May 2024 12:57:52 GMT</pubDate>
        </item>
        """
        # 创建解析对象
        domtree = parseString(response)
        collect = domtree.documentElement
        # 根据标签获取诗词名称
        tags = collect.getElementsByTagName('item')
        my_data = []
        # 解析属性信息
        for info in tags:
            art_title = info.getElementsByTagName('title')[0].childNodes[0].data
            art_link = info.getElementsByTagName('link')[0].childNodes[0].data
            art_desc = info.getElementsByTagName('description')[0].childNodes[0].data
            art_update = info.getElementsByTagName('pubDate')[0].childNodes[0].data
            # 将字符串转换为datetime对象
            date_obj = datetime.strptime(art_update, '%a, %d %b %Y %H:%M:%S %Z')
            # 将datetime对象格式化为年月日的字符串
            art_update = date_obj.strftime('%Y-%m-%d')

            data = f"""
            文章作者：{art_title}
            文章地址：{art_link}
            发布时间：{art_desc}
            更新时间：{art_update}
            """
            data = {"art_title": art_title,
                    "art_link": art_link,
                    "art_desc": art_desc,
                    "art_update": art_update}
            #print(data)
            my_data.append(data)
        return my_data
####################################
def down_picture(image_url: str,save_picture_path: str):
    """
    下载图片
    """
    # 发送 GET 请求获取图片内容
    response = requests.get(image_url,timeout=30)
    # 检查请求是否成功
    if response.status_code == 200:
        # 获取图片内容
        image_content = response.content
        # 保存图片到本地
        with open(save_picture_path, "wb") as file:
            file.write(image_content)
            print(f"Image downloaded and saved to {save_picture_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        save_picture_path = ""
    return save_picture_path

def get_daily_poetry(url,picture_path):
    """
      读取诗歌图片
    """
    with sync_playwright() as playwright:
        display_headless = False
        sys = platform.system()
        if sys == "Linux":
            display_headless = True
            browser = playwright.chromium.launch(headless=display_headless)
        else:
            browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
        context = browser.new_context()
        page = context.new_page() # 诗歌内容

        page.goto(url)
        time.sleep(6)
        
        # 查找所有图片元素
        images = page.query_selector_all('img')

        # 输出图片地址
        index = 0
        for image in images:
            img_src =  image.evaluate('(element) => element.src')
            print(">>>>>>>>>"+ img_src)
            index+=1
            save_picture_path = os.path.join(picture_path,str(index) + ".jpg")
            down_picture(img_src, save_picture_path)

#if __name__ == '__main__':