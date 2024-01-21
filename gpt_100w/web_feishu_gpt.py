import json
import os
import time
import platform
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page

class CDouBaoQA:
    """
    This class represents a CDouBaoQA.
    """
    def __init__(self,cookies_path: str, login_url:str):
        self.cookies_path = cookies_path
        self.login_url = login_url
        self.ask_url = login_url
        # playwright 部分
        self.browser = None
        self.page = None
        print("create CDouBaoQA")

    def __del__(self):
        print("CBaiduQA is being destroyed")
    def crate_browser_instance(self):
        """
        crate_browser_instance
        https://playwright.dev/python/docs/library
        playwright = sync_playwright().start()
        """
        display_headless = False
        playwright = sync_playwright().start()
        if platform.system() == "Linux":
            display_headless = True
            self.browser = playwright.chromium.launch(headless=display_headless)
        else:
            self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)

        self.page = self.login_or_restore_cookies()

    def login_or_restore_cookies(self) -> Page:
        """
          登录
        """
        userAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.21 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            userAgent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        elif sys == "Darwin":
            #chrome://version/
            userAgent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        context = self.browser.new_context(user_agent=userAgent)
        context.clear_cookies()
        page = context.new_page()
        page.goto(self.login_url)

        if os.path.exists(self.cookies_path):
            print("load cookies >>>>>>>>>>>>>>>>")
            # 从文件中加载 cookies
            with open(self.cookies_path, 'r',encoding='utf-8') as myfile:
                cookies = json.load(myfile)
            print(cookies)
            context.add_cookies(cookies)
            time.sleep(3)
        else:
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            time.sleep(60)
            cookies = page.context.cookies()
            with open(self.cookies_path, 'w',encoding='utf-8') as myfile:
                myfile.write(json.dumps(cookies))
        print("restore_cookies >>>>>>>>>>> ")
        return page

    def yiyan_auto_answer_qa(self, page: Page,msg:str):
        """
        auto_upload_picture
        """
        page.goto(self.ask_url)
        time.sleep(5)
        page.wait_for_url(self.ask_url)
        print(msg)

        page.get_by_role("textbox", name="发消息").fill("你是谁")
        time.sleep(2)
        page.get_by_role("button", name="发送").click()
        time.sleep(10)


        data = page.locator("css=.custom-html").inner_text()
        print(data)
        time.sleep(5)
def ask_test():
    """test"""
    sys = platform.system()
    login_url = "https://www.doubao.com/"
    if sys == "Windows":
        cookies_path = r"D:\mp4\etc\doubao_login.json"
    elif sys == "Darwin":
        cookies_path = r"/Users/wangchuanyi/mp4/etc/doubao_login.json"
    else:
        cookies_path = r"/root/bin/doubao_login.json"
    autoupload = CDouBaoQA(cookies_path, login_ur)
    autoupload.crate_browser_instance()

    for i in range(10):
        time.sleep(i)
        autoupload.yiyan_auto_answer_qa(autoupload.page,"")

if __name__ == '__main__':
    # playwright codegen https://www.doubao.com/
    ask_test()
# pass 被检测到了


