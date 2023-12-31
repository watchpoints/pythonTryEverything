"""This module provides mydouyn"""
import time
import json
import os
import platform
import logging
import requests
from datetime import datetime
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page


class GetupHabit:
    def __init__(self, save_picture_path: str, default_picture_path: str, get_up_path:str):
        self.save_picture_path = save_picture_path
        self.default_picture_path = default_picture_path
        self.get_up_path = get_up_path
        print("create GetupHabit")

    # 定义通过城市获取天气信息的函数
    def get_weather(self):
        print(self.save_picture_path)
        url: str = 'https://restapi.amap.com/v3/weather/weatherInfo?parameters'
        params_estimate1 = {
            'key': '0a0bb34d7214a2caebb4cb2fe6471f9f',
            'city': '110105',
            'extensions': 'all'  # 获取预报天气
        }

        res = requests.get(url=url, params=params_estimate1)  # 预报天气
        # res2 = requests.get(url=url,params=params_realtime) # 实时天气
        data_json = res.json()
        province = data_json['forecasts'][0]["province"]  # 获取省份
        city = data_json.get('forecasts')[0].get("city")  # 获取城市
        adcode = data_json.get('forecasts')[0].get("adcode")  # 获取城市编码
        reporttime = data_json.get('forecasts')[0].get("reporttime")  # 获取发布数据时间
        date = data_json.get('forecasts')[0].get("casts")[0].get('date')  # 获取日期
        week = data_json.get('forecasts')[0].get("casts")[0].get('week')  # 获取星期几
        dayweather = data_json.get('forecasts')[0].get("casts")[0].get('dayweather')  # 白天天气现象
        nightweather = data_json.get('forecasts')[0].get("casts")[0].get('nightweather')  # 晚上天气现象
        daytemp = data_json.get('forecasts')[0].get("casts")[0].get('daytemp')  # 白天温度
        nighttemp = data_json.get('forecasts')[0].get("casts")[0].get('nighttemp')  # 晚上温度
        daywind = data_json.get('forecasts')[0].get("casts")[0].get('daywind')  # 白天风向
        nightwind = data_json.get('forecasts')[0].get("casts")[0].get('nightwind')  # 晚上风向
        daypower = data_json.get('forecasts')[0].get("casts")[0].get('daypower')  # 白天风力
        nightpower = data_json.get('forecasts')[0].get("casts")[0].get('nightpower')  # 晚上风力

        weather = ''
        weather += '✅ 天气:' + dayweather + "\r\n"
        weather += '✅  温度:' + "低温 " + nighttemp + "℃ ~高温 " + daytemp + " ℃\r\n"
        weather += '✅ 风力:' + daypower + "级\r"
        return weather
    # 获取金山词霸每日一句
    def get_every_word(self):
        """
        目标养成计划
        """
        print(self.save_picture_path)
        return requests.get("https://open.iciba.com/dsapi/").json()

    def read_get_up_from_txt(self,path: str):
        """
        目标养成计划 emoji 表情作为目标的例子：

        """
        content = ""
        with open(path, encoding='UTF-8') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if len(line.strip()) == 0:
                    continue
                if i % 3 == 0:
                    # content += (line.strip() + " 😊") + "\r\n"
                    content += (line.strip()) + "\r\n"
                elif i % 3 == 1:
                    content += (line.strip()) + "\r\n"
                else:
                    content += (line.strip()) + "\r\n"
        content += "🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉" + "\r\n"
        return content

    def down_picture(self, image_url: str):
        """
        目标养成计划
        """
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
        """
        目标养成计划
        """
        # Current date
        current_date = datetime.now()
        # Specific date (2023-12-10)
        target_date = datetime(2023, 12, 1)
        # Calculate the difference in days
        difference_in_days = (current_date - target_date).days

        habit_name = "挑战早睡早起100天" + "第" + str(difference_in_days) + "天"
        data = self.get_every_word()
        title = "#挑战早睡早起100天" + "\r\n"
        title += data['content'] + "\r\n"
        title += data['note'] + "\r\n"
        print(str(data['fenxiang_img']))
        self.down_picture(data['fenxiang_img'])
        title += datetime.now().strftime('%Y-%m-%d') + "\r\n"
        weather = self.get_weather()
        title += weather + "\r\n"
        title += "\r\n"
        title += self.read_get_up_from_txt(self.get_up_path)
        return habit_name,title


########################################################################
class CMyRedBook:
    """
    This class represents a GetupHabit.

    Parameters:
    - save_picture_path (str): The path to save pictures.
    - default_picture_path (str): The default path for pictures.
    """
    def __init__(self,cookies_path: str, login_url: str, upload_picture_url: str, upload_mp4_url: str):
        self.cookies_path = cookies_path
        self.login_url = login_url
        self.upload_picture_url = upload_picture_url
        self.upload_mp4_url = upload_mp4_url
        # playwright 部分
        self.browser = None
        print("create CMyDouyin")

    def __del__(self):
        print("CMyDouyin is being destroyed")

    def upload_picture(self, picture_path: str, habit_name: str, habit_detail:str):
        """
          upload_picture
        """
        with sync_playwright() as playwright:
            display_headless = False
            #display_headless = True
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            #self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            self.browser = playwright.chromium.launch(headless=display_headless)
            login_page = self.login_or_restore_cookies()
            self.msg_up_load(login_page, picture_path, habit_name, habit_detail)
            self.browser.close()
    
        
    def login_or_restore_cookies(self) -> Page:
        """
          登录
        """
        user_agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.21 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        
        context = self.browser.new_context(user_agent=user_agent)
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
            time.sleep(60)
            cookies = page.context.cookies()
            with open(self.cookies_path, 'w',encoding='utf-8') as f:
                f.write(json.dumps(cookies))
        print("login_or_restore_cookies")
        return page

    def msg_up_load(self, page: Page, picture_path: str, habit_name: str, habit_detail:str):
        """
        上传图文
        """
        page.goto(self.upload_picture_url)
        time.sleep(3)
        print(f"open  {self.upload_picture_url}")
        # 使用文本内容定位元素
        example_element = page.locator("xpath=//span[contains(text(), '上传图文')]")
        example_element.click()
        print("点击 发布图文")
        time.sleep(4)
        
        
        # # page.locator('.drag-over').locator('nth=0').click()
        # page.locator('.drag-over').locator('nth=0').set_input_files()
        # # page.locator(
        # #     ":has-text(\"最多支持上传18张\")").locator('nth=1').set_input_files(
        # #     picture_path)
            
    
        # 点击选择文件，输入文件
        with page.expect_file_chooser() as fc_info:
            # 找到拖拽区域  
            page.locator('.drag-over').locator('nth=0').click()
            # 问题 文件弹框后 不自动退出 无法后续自动化操作
            file_chooser = fc_info.value
            file_chooser.set_files(picture_path)

        time.sleep(4)
        print("上传图片")
        #填写标题，可能会有更多赞哦～
        page.locator("css=.c-input_inner").fill(habit_name)
        time.sleep(3)
        #填写更全面的描述信息，让更多的人看到你吧！
        page.locator("css=.post-content").fill(habit_detail)
        time.sleep(3)
        page.mouse.down()
        page.mouse.down()
        time.sleep(1)
        # 发布
        page.locator("xpath=//button[./span[text()='发布']]").click()
        print("发布")
        time.sleep(5)
    
    def upload_mp4(self, mp4_file_path: str, habit_name: str, habit_detail:str):
        """
          upload_picture
        """
        with sync_playwright() as playwright:
            display_headless = False
            #display_headless = True
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            #self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            self.browser = playwright.chromium.launch(headless=display_headless)
            login_page = self.login_or_restore_cookies()
            self.auto_up_mp4(login_page, mp4_file_path, habit_name, habit_detail)
            self.browser.close()

    def auto_up_mp4(self, page: Page, mp4_file_path: str, habit_name: str, habit_detail:str):
        """
        上传视频
        """
        page.goto(self.upload_picture_url)
        time.sleep(3)
        print(f"open  {self.upload_picture_url}")
        # 使用文本内容定位元素
        example_element = page.locator("xpath=//span[contains(text(), '上传视频')]")
        example_element.click()
        print("点击 上传视频")
        time.sleep(4)
        
        # 点击选择文件，输入文件
        with page.expect_file_chooser() as fc_info:
            page.locator('.drag-over').locator('nth=0').click()
        file_chooser = fc_info.value
        file_chooser.set_files(mp4_file_path)

        time.sleep(300)
        print("上传视频")
        #填写标题，可能会有更多赞哦～
        page.locator("css=.c-input_inner").fill(habit_name)
        time.sleep(3)
        #填写更全面的描述信息，让更多的人看到你吧！
        page.locator("css=.post-content").fill(habit_detail)
        time.sleep(3)
        page.mouse.down()
        page.mouse.down()
        time.sleep(1)
        # 发布
        page.locator("xpath=//button[./span[text()='发布']]").click()
        print("发布")
        time.sleep(5)
    #################################################################################


def interface_auo_upload_myxiaohongshu(file_type="pic"):
    """
      对外调用接口
    """
    sys = platform.system()
    login_url = "https://creator.xiaohongshu.com/login?source=official"
    upload_picture_url = "https://creator.xiaohongshu.com/publish/publish?source=official"
    upload_mp4_url = "https://creator.xiaohongshu.com/publish/publish?source=official"
    sys = platform.system()
    if sys == "Windows":
        cookies_path = r"D:\mp4\etc\xiaohongshu.json"
        save_picture_path = r"D:\mp4\etc\temp.png"
        default_picture_path = r"D:\mp4\etc\ZfCYoSG1BE_small.jpg"
        get_up_path = r"D:\mp4\etc\01_get_up.txt"
        out_path = r"D:\mp4\output"
        # BACK_PATH = r"D:\mp4\bak"
    elif sys == "Darwin":
        cookies_path = r"/Users/wangchuanyi/etcxiaohongshu.json"
        save_picture_path = r"/Users/wangchuanyi/etc/temp.png"
        default_picture_path = r"/Users/wangchuanyi/etc/ZfCYoSG1BE_small.jpg"
        get_up_path = '/Users/wangchuanyi/etc/01_get_up.txt'
    else:
        cookies_path = r"/root/bin/xiaohongshu.json"
        save_picture_path = r"/root/code/python/putdonwphone/upload/temp.png"
        default_picture_path = r"/root/code/python/putdonwphone/upload/ZfCYoSG1BE_small.jpg"
        get_up_path = '/root/code/python/config/01_get_up.txt'
        out_path = r"/root/mp4/output"
        # BACK_PATH = r"/root/mp4/bak"

    getup = GetupHabit(save_picture_path, default_picture_path, get_up_path)
    habit_name,habit_detail = getup.interface_get_up()
    print(habit_name)
    print(habit_detail)
    file_path = getup.save_picture_path
    time.sleep(1)

    autoupload = CMyRedBook(cookies_path, login_url, upload_picture_url,upload_mp4_url)
    if file_type == "pic":
        autoupload.upload_picture(file_path, habit_name, habit_detail)
    else:
        for root,_,files in os.walk(out_path):
            for file in files:
                # 拼接路径
                mp4_file_path = os.path.join(root,file)
                if file.endswith('.mp4'):
                    file_name = os.path.basename(mp4_file_path)
                    file_name = file_name.split('.')[0]
                    msg = "#" + file_name + "\r\n"
                    msg += habit_detail
                    print(habit_name)
                    if autoupload.upload_mp4(mp4_file_path,habit_name,msg):
                        logging.info("upload_mp4 %s", mp4_file_path)



if __name__ == '__main__':
    interface_auo_upload_myxiaohongshu("mp4")
