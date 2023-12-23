import logging
import time
import json
import random
import os
import platform
import requests
from datetime import datetime
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page

class GetupHaibt:
    def __init__(self,save_picture_path:str, default_picture_path:str):
        self.save_picture_path = save_picture_path
        self.default_picture_path = default_picture_path
        print("creae GetupHaibt")
    # 定义通过城市获取天气信息的函数
    def get_weather(self):
        url = 'https://restapi.amap.com/v3/weather/weatherInfo?parameters'
        params_estimate = {
            'key': '0a0bb34d7214a2caebb4cb2fe6471f9f',
            'city': '110105',
            'extensions': 'all'  # 获取预报天气
        }

        res = requests.get(url=url, params=params_estimate)  # 预报天气
        # res2 = requests.get(url=url,params=params_realtime) # 实时天气
        tianqi = res.json()
        province = tianqi['forecasts'][0]["province"]  # 获取省份
        city = tianqi.get('forecasts')[0].get("city")  # 获取城市
        adcode = tianqi.get('forecasts')[0].get("adcode")  # 获取城市编码
        reporttime = tianqi.get('forecasts')[0].get("reporttime")  # 获取发布数据时间
        date = tianqi.get('forecasts')[0].get("casts")[0].get('date')  # 获取日期
        week = tianqi.get('forecasts')[0].get("casts")[0].get('week')  # 获取星期几
        dayweather = tianqi.get('forecasts')[0].get("casts")[0].get('dayweather')  # 白天天气现象
        nightweather = tianqi.get('forecasts')[0].get("casts")[0].get('nightweather')  # 晚上天气现象
        daytemp = tianqi.get('forecasts')[0].get("casts")[0].get('daytemp')  # 白天温度
        nighttemp = tianqi.get('forecasts')[0].get("casts")[0].get('nighttemp')  # 晚上温度
        daywind = tianqi.get('forecasts')[0].get("casts")[0].get('daywind')  # 白天风向
        nightwind = tianqi.get('forecasts')[0].get("casts")[0].get('nightwind')  # 晚上风向
        daypower = tianqi.get('forecasts')[0].get("casts")[0].get('daypower')  # 白天风力
        nightpower = tianqi.get('forecasts')[0].get("casts")[0].get('nightpower')  # 晚上风力

        # print("省份:",province)
        # print("城市:",city)
        # print("城市编码:",adcode)
        # print("发布数据时间:",reporttime)
        # print("日期:",reporttime)
        # print("星期:",week)
        # print("白天天气现象:",dayweather)
        # print("晚上天气现象:",nightweather)
        # print("白天温度:",daytemp)
        # print("晚上温度:",nighttemp)
        # print("白天风向:",daywind)
        # print("晚上风向:",nightwind)
        # print("白天风力:",daypower)
        # print("晚上风力:",nightpower)

        weather = ''
        weather += '✅ 天气:' + dayweather + "\r\n"
        weather += '✅  温度:' + "低温 " + nighttemp + "℃ ~高温 " + daytemp + " ℃\r\n"
        weather += '✅ 风力:' + daypower + "级\r"
        return weather
    # 获取金山词霸每日一句
    def get_every_word(self):
        url = "http://open.iciba.com/dsapi/"
        r = requests.get(url)
        # content = ''
        # #英文内容
        # day1 = r.json()['content']
        # #中文内容
        # day2 = r.json()['note']
        # picture2 = r.json()['picture2'] 
        # print(picture)
        # print(picture2)
        # content += day2
        # content += "\r\n"

        # content += day1
        # content += "\r\n"
        return r.json()
    # 图片 URL
    def down_picture(self,image_url:str):
        # 发送 GET 请求获取图片内容
        response = requests.get(image_url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 获取图片内容
            image_content = response.content
            # 保存图片到本地
            with open(self.save_picture_path, "wb") as file:
                file.write(image_content)
                print(f"Image downloaded and saved to {self.save_picture_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            self.save_picture_path = self.default_picture_path
        
    def interface_get_up(self):
        # Current date
        current_date = datetime.now()
        # Specific date (2023-12-10)
        target_date = datetime(2023, 12, 1)
        # Calculate the difference in days
        difference_in_days = (current_date - target_date).days
        
        title = "#挑战早睡早起100天" + "\r\n"
        
        title += "第" + str(difference_in_days) + "天" + "\r\n"
        data = self.get_every_word()
        title += data['content'] + "\r\n"
        title += data['note'] + "\r\n"
        print(str(data['fenxiang_img']))
        self.down_picture(data['fenxiang_img'])
        title += datetime.now().strftime('%Y-%m-%d') + "\r\n"
        weather = self.get_weather()
        title += weather + "\r\n"
        title += "\r\n"
        return title

########################################################################
class MyKuaishou:
    def __init__(self,driver_path:str,cookies_path:str,login_url:str, upload_url:str):
         self.chromedriver_path = driver_path
         self.driver = None
         self.cookies_path = cookies_path
         self.login_url = login_url
         self.upload_url = upload_url
         # playwright 部分
         self.browser = None
         print("creae MyKuaishou")
    def __del__(self):
        if self.driver:
            self.driver.close()
        print("is being destroyed")
    
    def upload_picture(self,picture_path:str,msg:str):
        """_summary_

        Args:
            picture_path (str): _description_
            msg (str): _description_
        """
        with sync_playwright() as playwright:
            #01 启动chomue浏览器
            # playwright执行默认运行的浏览器是chromium！
            #全局代理
            display_headless = False
            #display_headless = True
            if platform.system() == "Linux":
                display_headless = True
            # https://github.com/microsoft/playwright-python?tab=readme-ov-file
            # self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            self.browser = playwright.chromium.launch(headless=display_headless)
            # 模拟登录
            login_page = self.login_or_restore_cookies()
            self.msg_up_load(login_page,picture_path,msg)
            # https://www.programsbuzz.com/article/playwright-xpath-selectors
            self.browser.close()
            
    # 登录
    def login_or_restore_cookies(self)-> Page:
        # 创建一个新的页面
        user_agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.21 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        
        context = self.browser.new_context(user_agent=user_agent)
        context.clear_cookies()
        page = context.new_page()
        page.goto(self.login_url) 
        
        if os.path.exists(self.cookies_path):
            print("cookies is exited load")
            # 从文件中加载 cookies
            with open(self.cookies_path, 'r',encoding='utf-8') as myfile:
                cookies = json.load(myfile)
            # 将 cookies 加载到页面中
            context.add_cookies(cookies)
            time.sleep(3)
        else:
            # 相信第一次接触Playwright的同学，一定会对Browser、 BrowserContext 和Page这三个概念所困
            # https://blog.csdn.net/liwenxiang629/article/details/130810265
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            time.sleep(60)
            # 获取当前页面的 cookies
            cookies = page.context.cookies()
            print(cookies)
            # 保存 cookies 到文件
            with open(self.cookies_path, 'w',encoding='utf-8') as myfile:
                myfile.write(json.dumps(cookies))
        return page

     # 登录
    def msg_up_load(self,page: Page,picture_path:str,msg:str):
        page.goto(self.upload_url)
        time.sleep(3)
        # https://playwright.dev/docs/locators
        # 使用 XPath 表达式定位元素
        xpath_expression = '//div[contains(text(), "上传图文")]'
        example_element = page.locator("xpath=//div[contains(text(), '上传图文')]")
        example_element.click()
        print("进入图文页面")
        time.sleep(2)
        # https://github.com/Superheroff/douyin_uplod/blob/main/main.py
    
        #  # 找到拖拽区域  
        upload_button  = page.locator("xpath=//button[contains(text(), '上传图片')]")
        # # 模拟拖拽文件到拖拽区域
        upload_button.click()
        print("上传图片")
        time.sleep(3)
        # 点击选择文件，输入文件
        with page.expect_file_chooser() as fc_info:
            # 找到拖拽区域  
            page.click("xpath=//button[contains(text(), '上传图片')]") 
            # 问题 文件弹框后 不自动退出 无法后续自动化操作
            file_chooser = fc_info.value
            file_chooser.set_files(picture_path)
        
        time.sleep(3)
        page.mouse.down()
        page.mouse.down()
        
        #填写描述
        page.locator("css=.iGOvMbhp8tU-").fill(msg)
        time.sleep(3)
        print("填写描述")
        
        #添加音乐
        page.get_by_placeholder("搜索音乐、歌手、歌词添加至作品").click()
        time.sleep(5)
        index = random.randint(0, 5)
        page.locator("xpath=//button[./span[text()='添加']]").locator("nth={}".format(index)).click()
        time.sleep(5)

        # 添加地点
        
        #发布
        page.locator("xpath=//button[./span[text()='发布']]").click()
        time.sleep(5)
        print("发布")
       # 登录
    def auto_upload_mp4(self,page: Page,mp4_path:str,msg:str):
        """_summary_

        Args:
            page (Page): _description_
            picture_path (str): _description_
            msg (str): _description_
        """
        page.goto(self.upload_url)
        time.sleep(3)
        
        # https://playwright.dev/docs/locators
        # 使用 XPath 表达式定位元素
        page.locator("xpath=//div[contains(text(), '上传视频')]").click()
        print("上传视频")
        time.sleep(3)
        
        # 点击选择文件，输入文件
        with page.expect_file_chooser() as fc_info:
            # 找到拖拽区域
            page.click("xpath=//button[contains(text(), '上传视频')]")
        file_chooser = fc_info.value
        file_chooser.set_files(mp4_path)
        
        time.sleep(300)
        page.mouse.down()
        page.mouse.down()
        
        #填写描述
        page.get_by_placeholder("添加合适的话题和描述，作品能获得更多推荐～").fill(msg)
        time.sleep(3)
        print("填写描述")
        
        #所属领域
        
        #发布
        page.locator("xpath=//button[./span[text()='发布']]").click()
        time.sleep(5)
        print("发布")
        
    def upload_mp4(self,mp4_file_path:str,msg:str):
        ''' 远离手机'''
        with sync_playwright() as playwright:
            #01 启动chomue浏览器
            # playwright执行默认运行的浏览器是chromium！
            #全局代理
            display_headless = False
            #display_headless = True
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            self.browser = playwright.chromium.launch(headless=display_headless)

            # 模拟登录
            login_page = self.login_or_restore_cookies()
            self.auto_upload_mp4(login_page,mp4_file_path,msg)
            self.browser.close()
        
#################################################################################
       

def interface_auo_upload_kuaishou2(upload_type:str):
    ''' 远离手机'''
    sys = platform.system()
    if sys == "Windows":
        driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        coook_path = r"D:\doc\2023\05-third\chromedriver_win32\mykuaishou.json"
        login_url = "https://cp.kuaishou.com/profile"
        upload_url = "https://cp.kuaishou.com/article/publish/video"
        save_picture_path = r"D:\github\pythonTryEverything\putdonwphone\upload\temp.png"
        default_picture_path = r"D:\github\pythonTryEverything\putdonwphone\upload\ZfCYoSG1BE_small.jpg"
        out_path = r"D:\mp4\output"
        # BACK_PATH = r"D:\mp4\bak"
    else:
        driver_path = r"/root/bin/chromedriver"
        coook_path = r"/root/bin/mykuaishou.json"
        login_url = "https://cp.kuaishou.com/profile"
        upload_url = "https://cp.kuaishou.com/article/publish/video"
        save_picture_path = r"/root/code/python/putdonwphone/upload/temp.png"
        default_picture_path = r"/root/code/python/putdonwphone/upload/ZfCYoSG1BE_small.jpg"
        out_path = r"/root/mp4/output"
        # BACK_PATH = r"/root/mp4/bak"
    
    getup_haibt = GetupHaibt(save_picture_path,default_picture_path)
    msg = getup_haibt.interface_get_up()
    print(msg)
    file_path = getup_haibt.save_picture_path
    time.sleep(1)
        
    autoupload = MyKuaishou(driver_path,coook_path,login_url,upload_url)
    if "mp4" == upload_type:
        for root,_,files in os.walk(out_path):
            for file in files:
                # 拼接路径
                mp4_file_path = os.path.join(root,file)
                if file.endswith('.mp4'):
                    file_name = os.path.basename(mp4_file_path)
                    file_name = file_name.split('.')[0]
                    habit_name = "#" + file_name + "\r\n"
                    habit_name += msg
                    print(habit_name)
                    if autoupload.upload_mp4(mp4_file_path,habit_name):
                        logging.info("upload_mp4 %s", mp4_file_path)
    else:
        autoupload.upload_picture(file_path,msg)


if __name__ == '__main__':
    
    #interface_auo_upload_kuaishou2("pic")
    interface_auo_upload_kuaishou2("mp4")
