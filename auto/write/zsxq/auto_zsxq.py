

"""This module provides mydouyn"""
import time
import json
import os
import datetime
import platform
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
### 本地目录
from auto.public import mydate
from auto.write.wechat import auto_wechat_api
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
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
        
        time.sleep(10)
        if item_list is None and len(item_list) <1:
            return None
        try:
            with sync_playwright() as playwright:
                self.browser = playwright.chromium.launch(channel="chrome",headless=False)
                login_page = self.login_or_restore_cookies()
                self.send_dest_data(login_page,item_list)
                self.browser.close()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        
        time.sleep(3)

        for item in item_list:
            auto_wechat_api.markdown_to_wechat(item.content)
            time.sleep(60*2)

    
    def login_or_restore_cookies(self) -> Page:
        """
          登录
        """
        userAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            userAgent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        elif sys == "Darwin":
           # chrome://version/
           userAgent='ozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        
        self.context = self.browser.new_context(user_agent=userAgent)
        if os.path.exists(self.cookies_path):
            with open(self.cookies_path, 'r',encoding='utf-8') as f:
                cookies = json.load(f)

            current_time = datetime.datetime.now()
            # 延长1天
            extended_time = current_time + datetime.timedelta(days=1)
            # 获取时间戳（精确到秒）
            timestamp = int(extended_time.timestamp())
            print(timestamp)
            for cookie in cookies:
                 if cookie['name'] == 'abtest_env':
                    cookie['expires'] = timestamp
                 if cookie['name'] == 'zsxq_access_token':
                    cookie['zsxq_access_token'] = timestamp
                    print(cookie)
                 if cookie['name'] == 'sensorsdata2015jssdkcross':
                    cookie['expires'] = timestamp
                    print(cookie)
            self.context.add_cookies(cookies)
            time.sleep(3)
        # 先添加add_cookies
        # 每个浏览器上下文可以承载多个页面
        # Each BrowserContext can have multiple pages. 
        # A Page refers to a single tab or a popup window within a browser context. 
        # It should be used to navigate to URLs and interact with the page content.
        page = self.context.new_page()
        page.goto(self.login_url)

        if os.path.exists(self.cookies_path):
            pass
        else:
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            time.sleep(20)
            cookies = page.context.cookies()
            with open(self.cookies_path, 'w',encoding='utf-8') as f:
                f.write(json.dumps(cookies))
        print("login_or_restore_cookies")
        return page
    # def login_or_restore_cookies(self) -> Page:

    #     """
    #       登录 context-->page
    #     """
    #     print("login_or_restore_cookies")
    #     userAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    #     sys = platform.system()
    #     if sys == "Linux":
    #         userAgent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        
    #     context = self.browser.new_context(user_agent=userAgent)
    #     context.clear_cookies()
    #     page = context.new_page()
    #     page.goto(self.login_url)

    #     if os.path.exists(self.cookies_path):
    #         print("load cookies")
    #         # 从文件中加载 cookies
    #         with open(self.cookies_path, 'r',encoding='utf-8') as f:
    #             cookies = json.load(f)
    #         context.add_cookies(cookies)
    #         time.sleep(3)
    #     else:
    #         # 扫名二维码登录 需要人工处理
    #         # 扫名二维码登录 需要人工处理
    #         # 扫名二维码登录 需要人工处理
    #         time.sleep(30)
    #         cookies = page.context.cookies()
    #         with open(self.cookies_path, 'w',encoding='utf-8') as f:
    #             f.write(json.dumps(cookies))
    #     print("login_or_restore_cookies end") 
    #     return page
    
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
        page.get_by_text("最新", exact=True).click()
        print("点击 最新内容")
        print("点击 精华内容")
        page.wait_for_timeout(1000)
        # page.get_by_role("button", name="去完成").nth(2).click()
        #itemlist = page.locator("xpath=css=.ng-star-inserted")
        itemlist = page.locator("css=.topic-container")
        print(f"文章：  {itemlist.count()}")
        item_index = 1
        # 创建一个空列表来保存Person对象
        itemdetail = []
        while item_index < itemlist.count():
            item = itemlist.nth(item_index)
            item_index =  item_index + 1
            # 作者
            #<div _ngcontent-ng-c1370301819="" class="role owner ng-star-inserted">findyi</div>
            #<div _ngcontent-ng-c1370301819="" class="role member ng-star-inserted">盲而不瞎</div>
            # 日期
            #<div _ngcontent-ng-c1370301819="" class="date"> 2024-09-24 18:00 <!----><!----><!----><!----></div>
            # 内容
            

            #user = item.locator("css=.role.member.ng-star-inserted").inner_text()
            #print(user)
            date = item.locator("css=.date").inner_text()
            # 过滤日期
            if not mydate.check_date_equal(date):
                continue

            content = item.locator("css=.content").inner_text()
            
            # 选择器，查找指定的超级链接
            link_selector = 'a.link-of-topic'  # 替换为您的链接选择器
            if item.locator(link_selector).count() > 0:
                href = item.locator(link_selector).last.get_attribute('href')
                print(href)

            page.wait_for_timeout(200)
            if len(href) > 10:
                content += "请访问：\r\n"
                content += href
                href = ""
            print(content)

            itemdetail.append(Item("",date,content))
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
        for item in itemlist:
            print(item)
            page.locator("xpath=//div[contains(text(),'点击发表主题...')]").click()
            print("点击发表主题...")
            page.wait_for_timeout(2000)
            #<div class="ql-editor ql-blank" contenteditable="true" aria-owns="quill-mention-list" data-placeholder="点击发表主题...">
            # <p><br></p></div>
            page.locator("quill-editor div").nth(1).fill(item.content)
            page.wait_for_timeout(2000)
            #<div _ngcontent-ng-c3190014776="" class="submit-btn">发布</div>
            page.locator("css=.submit-btn").click()
            page.wait_for_timeout(30000) #30秒

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
   
    print("---interface_copy_zsxq---")
    job_defaults = {
         'coalesce': False,
         'max_instances': 1
    }
    backsched = BlockingScheduler(job_defaults=job_defaults, timezone='Asia/Shanghai')
    # 汇总 最新资料 每日新闻
    backsched.add_job(interface_copy_zsxq, CronTrigger.from_crontab("22 50 * * *"))
    backsched.start()
   