""" ai"""
import time,sys,signal
import platform
import json
import os
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from zhipuai import ZhipuAI

def QuitAndSave(signum, frame):#监听退出信号
    print ('catched singal: %d' % signum)
    sys.exit(0)

class CDouYulive():
    def __init__(self):
        self.login_url = None
        self.cookies_path = None
        self.room_id = None
        self.context = None
        self.browser = None
        print("create")
    def login_or_restore_cookies(self) -> Page:
        """
          登录
        """
        userAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            userAgent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        
        self.context = self.browser.new_context(user_agent=userAgent)
        self.context.clear_cookies()
        page = self.context.new_page()
        page.goto(self.login_url)
    
        if os.path.exists(self.cookies_path):
            print("cookies is exited load")
            # 从文件中加载 cookies
            with open(self.cookies_path, 'r',encoding='utf-8') as myfile:
                cookies = json.load(myfile)
            # 将 cookies 加载到页面中
            self.context.add_cookies(cookies)
            time.sleep(3)
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
    
    def listen_msg(self, page: Page):
        """
         弹幕播放
        """
        print(self.room_id)
        page.goto(self.room_id)
        time.sleep(15)
        page.mouse.down()
        #https://www.cnblogs.com/yoyoketang/p/17642763.html
        page.wait_for_selector("xpath=//*[@class='Barrage-container']", state='attached')
        print("login is ok")
        
        last_count = 0
        last_barrage = None
        

        while True:  # 无限循环，伪监听
            time.sleep(15)  # 等待1秒加载
            # class="vue-recycle-scroller__item-view"
            # chat_room_list = page.locator("xpath=//*[@class='vue-recycle-scroller__item-wrapper']")
            chat_msgs_list = page.locator("xpath=//*[@class='Barrage-listItem']")
            cur_count = chat_msgs_list.count()
            print(cur_count)
            # https://www.cnblogs.com/yoyoketang/p/17198224.html
            # https://playwright.dev/python/docs/api/class-locator#locator-count
            if  last_count == cur_count :
                print("have no new msg ")
            else:
                #last_count = cur_count
                print(" new msg ")
                # https://github.com/microsoft/playwright/issues/11909
                # for msg in chat_msgs_list:
                #     # https://www.yisu.com/zixun/47149.html
                #     print(msg)
                last_data_id = last_count
                while  last_data_id < chat_msgs_list.count():
                    item = chat_msgs_list.nth(last_data_id)
                    print(item)
                    list_value = item.locator("css=.Barrage-notice--normalBarrage")
                    print(list_value)
                    # user = list_value.get_by_role("span").locator('nth=1').inner_text()
                    # msg = list_value.get_by_role("span").locator('nth=2').inner_text()
                    # user = item.locator("css=.Barrage-nickName.Barrage-nickName--blue.is-self.js-nick ").inner_text()
                    # msg = item.locator("css=.message-content").inner_text()
                    # print(user)
                    # print(msg)
                    last_data_id =  last_data_id + 1
    def Connect(self):
        """
         获取弹幕
        """
        print("login")
        self.login_url = "https://www.douyu.com/"
        self.room_id = "https://www.douyu.com/11975253"
        # 说明：视频号 cookies很容易失效 第三天可能实现 todo
        if platform.system() == "Windows":
            self.cookies_path = r"D:\mp4\etc\douyu_big.json"
        elif platform.system() == "Darwin":
            self.cookies_path = r"/Users/wangchuanyi/mp4/etc/douyu_big.json"
        else:
           self.cookies_path = r"/root/bin/douyu_big.json"
        # 打开
        with sync_playwright() as playwright:
            display_headless = False
            if sys == "Linux":
                display_headless = True
                self.browser = playwright.chromium.launch(headless=display_headless)
            else:
                self.browser = playwright.chromium.launch(channel="chrome",
                                                          headless=display_headless)
            login_page = self.login_or_restore_cookies()
            self.listen_msg(login_page)
            if self.browser.is_connected:
                self.browser.close()

def zhipu_ai():
    """
     ai
    """
    client = ZhipuAI(api_key="de143fda204456eaf43e834b0f3b6be8.GvP7iMxkqBPnElaM") # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": "讲个笑话"}
        ],
    )
    print(response.choices[0].message)

if __name__ == '__main__':#执行层
    #zhipu_ai()
    #信号监听
    signal.signal(signal.SIGTERM, QuitAndSave)
    signal.signal(signal.SIGINT, QuitAndSave)
    duyuobj = CDouYulive()
    duyuobj.Connect()