

"""This module provides mydouyn"""
import time
import json
import os
import platform
from datetime import datetime
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page


class Item:
    def __init__(self, name, date,content):
        self.name = name  # 保存名称
        self.date = date  # 保存地址
        self.content = content  # 保存地址
########################################################################
class CZSxq:
    """
    This class represents a GetupHabit.

    Parameters:
    - save_picture_path (str): The path to save pictures.
    - default_picture_path (str): The default path for pictures.
    """
    def __init__(self,cookies_path: str, login_url: str,from_url: str, dest_url: str):
        self.cookies_path = cookies_path
        self.login_url = login_url
        self.from_url = from_url
        self.dest_url = dest_url
        # playwright 部分
        self.browser = None
        print("create CZSxq")

    def __del__(self):
        print("CZSxq is being destroyed")

    def get_from_page(self):
        """
          根据日期获取内容
        """
        item_list = None
        with sync_playwright() as playwright:
            self.browser = playwright.chromium.launch(channel="chrome",headless=False)
            login_page = self.login_or_restore_cookies()
            item_list = self.read_from_data(login_page)
            self.browser.close()
        
        time.sleep(3)
        if item_list is None and len(item_list) <1:
            return None
        
        with sync_playwright() as playwright:
            self.browser = playwright.chromium.launch(channel="chrome",headless=False)
            login_page = self.login_or_restore_cookies()
            item_list = self.send_dest_data(login_page,item_list)
            self.browser.close()

    
        
    def login_or_restore_cookies(self) -> Page:

        """
          登录 context-->page
        """
        print("login_or_restore_cookies")
        userAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            userAgent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        
        context = self.browser.new_context(user_agent=userAgent)
        context.clear_cookies()
        page = context.new_page()
        page.goto(self.login_url)

        if os.path.exists(self.cookies_path):
            print("load cookies")
            # 从文件中加载 cookies
            with open(self.cookies_path, 'r',encoding='utf-8') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            time.sleep(3)
        else:
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            time.sleep(30)
            cookies = page.context.cookies()
            with open(self.cookies_path, 'w',encoding='utf-8') as f:
                f.write(json.dumps(cookies))
        print("login_or_restore_cookies end") 
        return page
    
    def read_from_data(self, page: Page):
        """
        read_from_data
        """
        page.goto(self.from_url)
        page.wait_for_timeout(1000)
        print(f"open  {self.from_url}")
        page.mouse.down()
        page.mouse.down()
        page.mouse.down()
        page.wait_for_timeout(1000)


        #page.locator("xpath=//div[@class='item ng-star-inserted' and contains(text(),'最新')]").click()
        #page.locator("xpath=//div[contains(text(),'最新')]").click()
        # newbuttion = page.locator("xpath=//div[@class='item ng-star-inserted']").nth(0)
        # newbuttion.hover()
        # page.wait_for_timeout(1000)
        # newbuttion.click()
        # newbuttion.click()
        # page.wait_for_timeout(10000)
        print("点击 最新内容")
        print("点击 精华内容")
        page.wait_for_timeout(1000)
        # page.get_by_role("button", name="去完成").nth(2).click()
        #itemlist = page.locator("xpath=css=.ng-star-inserted")
        itemlist = page.locator("css=.topic-container")
        print(f"文章：  {itemlist.count()}")
        item_index = 2
        # 创建一个空列表来保存Person对象
        itemdetail = []
        while item_index < itemlist.count():
            item = itemlist.nth(item_index)
            # 作者
            #<div _ngcontent-ng-c1370301819="" class="role owner ng-star-inserted">findyi</div>
            #<div _ngcontent-ng-c1370301819="" class="role member ng-star-inserted">盲而不瞎</div>
            # 日期
            #<div _ngcontent-ng-c1370301819="" class="date"> 2024-09-24 18:00 <!----><!----><!----><!----></div>
            # 内容
            

            #user = item.locator("css=.role.member.ng-star-inserted").inner_text()
            #print(user)
            date = item.locator("css=.date").inner_text()
            print(date)
            content = item.locator("css=.content").inner_text()
            print(content)
            page.wait_for_timeout(2000)
            itemdetail.append(Item("",date,content))
            item_index =  item_index + 1
        return itemdetail  
       
    def send_dest_data(self, page: Page, itemlist):
        """
        send_dest_data
        """
        page.goto(self.dest_url)
        page.wait_for_timeout(1000)
        print(f"open  {self.from_url}")
        page.mouse.down()
        page.mouse.down()
        page.wait_for_timeout(1000)
        #  <div _ngcontent-ng-c2012982032="" class="tip">点击发表主题...</div>

        page.locator("xpath=//div[contains(text(),'点击发表主题...')]").click()
        
        print("点击发表主题...")
        page.wait_for_timeout(1000)
        # page.get_by_role("button", name="去完成").nth(2).click()
        #itemlist = page.locator("xpath=css=.ng-star-inserted")
        itemlist = page.locator("css=.topic-container")
        print(f"文章：  {itemlist.count()}")
        item_index = 2
        # 创建一个空列表来保存Person对象
        itemdetail = []
        while item_index < itemlist.count():
            item = itemlist.nth(item_index)
            # 作者
            #<div _ngcontent-ng-c1370301819="" class="role owner ng-star-inserted">findyi</div>
            #<div _ngcontent-ng-c1370301819="" class="role member ng-star-inserted">盲而不瞎</div>
            # 日期
            #<div _ngcontent-ng-c1370301819="" class="date"> 2024-09-24 18:00 <!----><!----><!----><!----></div>
            # 内容
            

            #user = item.locator("css=.role.member.ng-star-inserted").inner_text()
            #print(user)
            date = item.locator("css=.date").inner_text()
            print(date)
            content = item.locator("css=.content").inner_text()
            print(content)
            page.wait_for_timeout(2000)
            itemdetail.append(Item("",date,content))
            item_index =  item_index + 1
        return itemdetail


###################################
def interface_copy_zsxq():
    """
     项目需求：将知识星球精彩内容，同步到其他平台
    """
    sys = platform.system()
    login_url = "https://wx.zsxq.com/login"
    from_url = "https://wx.zsxq.com/group/15552545485212"
    dest_url = "https://wx.zsxq.com/group/552812528214"
    try:
        sys = platform.system()
        if sys == "Windows":
            cookies_path = r"D:\mp4\etc\zsxq.json"
        elif sys == "Darwin":
             cookies_path = r"/Users/wangchuanyi/mp4/etc/zsxq.json"
        else:
            cookies_path = r"/root/bin/zsxq.json"

        autoupload = CZSxq(cookies_path, login_url,from_url, dest_url)
        autoupload.get_from_page()

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


if __name__ == '__main__':
    interface_copy_zsxq()
    # playwright codegen https://wx.zsxq.com/group/15552545485212
   