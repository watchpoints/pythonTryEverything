"""This module provides 视频号助手"""
import time
import json
import os
import logging
import platform
from datetime import datetime
import traceback
import shutil
import requests
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page


class GetupHabit:
    """This class provides a way to do something."""
    def __init__(self, save_picture_path: str, default_picture_path: str, get_up_path:str):
        self.save_picture_path = save_picture_path
        self.default_picture_path = default_picture_path
        self.get_up_path = get_up_path
        print("create GetupHabit")

    def get_weather(self):
        """定义通过城市获取天气信息的函数."""
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
        # date = data_json.get('forecasts')[0].get("casts")[0].get('date')  # 获取日期
        week = data_json.get('forecasts')[0].get("casts")[0].get('week')  # 获取星期几
        dayweather = data_json.get('forecasts')[0].get("casts")[0].get('dayweather')  # 白天天气现象
        #nightweather = data_json.get('forecasts')[0].get("casts")[0].get('nightweather')  # 晚上天气现象
        daytemp = data_json.get('forecasts')[0].get("casts")[0].get('daytemp')  # 白天温度
        nighttemp = data_json.get('forecasts')[0].get("casts")[0].get('nighttemp')  # 晚上温度
        #daywind = data_json.get('forecasts')[0].get("casts")[0].get('daywind')  # 白天风向
        daypower = data_json.get('forecasts')[0].get("casts")[0].get('daypower')  # 白天风力

        weather = ''
        weather +='星期：' + week + "\r\n"
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

        temp_habit_name = "专注学习100天" + "第" + str(difference_in_days) + "天"
        data = self.get_every_word()
        
        title = "#专注学习100天 仅个人学习使用" + "\r\n"
        title = "本视频大纲内容:todo" + "\r\n"
        title = "视频关键时间线：todo" + "\r\n"
        title = "视频核心观点:todo" + "\r\n"
        title = "☔每日一句：" + "\r\n"
        title += data['content'] + "\r\n"
        title += data['note'] + "\r\n"
        print(str(data['fenxiang_img']))
        self.down_picture(data['fenxiang_img'])
        title += datetime.now().strftime('%Y-%m-%d') + "\r\n"
        weather = self.get_weather()
        title += weather + "\r\n"
        # title += "\r\n"
        # title += self.read_get_up_from_txt(self.get_up_path)
        return temp_habit_name,title

 
def interface_get_daily_note():
    """
    获取每日英语单词

    Returns:
        tuple[str, str, Any]: 包含单词、释义和相关图片路径的元组
    Python Return Multiple Values  How to Return a Tuple, List, or Dictionary
    https://www.freecodecamp.org/news/python-returns-multiple-values-how-to-return-a-tuple-list-dictionary/
    """
    sys = platform.system()
    sys = platform.system()  
    if sys == "Windows":
        save_picture_path = r"D:\github\pythonTryEverything\putdonwphone\upload\temp.png"
        default_picture_path = r"D:\github\pythonTryEverything\putdonwphone\upload\ZfCYoSG1BE_small.jpg"
        get_up_path = r"D:\github\pythonTryEverything\config\01_get_up.txt"
    else:
        save_picture_path = r"/root/code/python/putdonwphone/upload/temp.png"
        default_picture_path = r"/root/code/python/putdonwphone/upload/ZfCYoSG1BE_small.jpg"
        get_up_path = '/root/code/python/config/01_get_up.txt'

    getup = GetupHabit(save_picture_path, default_picture_path, get_up_path) 
    temp_habit_name,temp_habit_detail = getup.interface_get_up()
    return getup.save_picture_path, temp_habit_name,temp_habit_detail

########################################################################
class CMyShipinhao:
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

    def upload_picture(self, picture_path: str, habit_name:str, habit_detail:str):
        """
          upload_picture
        """
        with sync_playwright() as playwright:
            display_headless = False
            display_headless = True
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            #self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            self.browser = playwright.chromium.launch(headless=display_headless)
            login_page = self.login_or_restore_cookies()
            print("login_or_restore_cookies")
            self.msg_up_load(login_page, picture_path, habit_name,habit_detail)
            self.browser.close()
    
    def upload_mp4(self, mp4_path: str,habit_name: str,habit_detail: str):
        """
          upload_mp4
        """
        logging.info("upload_mp4 %s",mp4_path)
        with sync_playwright() as playwright:
            display_headless = False
            display_headless = True
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            self.browser = playwright.chromium.launch(headless=display_headless)
            login_page = self.login_or_restore_cookies()
            try:
                self.msg_up_load_mp4(login_page, mp4_path, habit_name, habit_detail)
            except Exception :
                print(traceback.format_exc())
                self.browser.close()
                return False
                
            self.browser.close()
        return True
        
    def login_or_restore_cookies(self) -> Page:
        """
          登录
        """
        userAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.21 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            userAgent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        
        context = self.browser.new_context(user_agent=userAgent)
        context.clear_cookies()
        page = context.new_page()
        page.goto(self.login_url)

        if os.path.exists(self.cookies_path):
            print("load cookies >>>>>>>>>>>>>>>>")
            # 从文件中加载 cookies
            with open(self.cookies_path, 'r',encoding='utf-8') as myfile:
                cookies = json.load(myfile)
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
        print("restore_cookies >>>>>>>>>>> ")
        return page

    def msg_up_load(self, page: Page, picture_path: str,habit_name:str, habit_detail:str):
        """
        msg_up_load
        """
        page.goto(self.upload_picture_url)
        time.sleep(6)
        print(f"open  {self.upload_picture_url}")
        # 从主页进入 headless不行
        page.locator("xpath=//div[contains(text(), '写想法')]").click()
        print("点击 发布图文")
        # time.sleep(3)
        # print(page.content)
        
        # # https://www.zhihu.com/creator
        # page.mouse.click(200,200)
        # dropdown = page.get_by_text("内容创作")
        # dropdown.hover()
        # # dropdown.locator('.dropdown__link >> text=python').click()
        # #dropdown.get_by_role("listitem").filter(has_text="python").click()
        # # 对于ul-li的元素，可以用listitem 的角色定位方式
        # page.locator("a").filter(has_text="发布想法").click()
        
        
        time.sleep(2)
        
        page.get_by_placeholder("请输入标题（选填）").fill(habit_name)
        page.get_by_role("textbox").locator('nth=-1').fill(habit_detail)
        # page.locator(".InputLike").fill(habit_detail)
        time.sleep(3)
        
        print("开始上传图片")
        page.locator(".css-88f71l > button:nth-child(2)").click()
        time.sleep(2)
        print("本地上传")
        with page.expect_file_chooser() as fc_info:
            page.locator(".css-n71hcb").click()
        file_chooser = fc_info.value
        file_chooser.set_files(picture_path)
        time.sleep(5)
        
        page.get_by_role("button", name="插入图片").click()
        time.sleep(5)
        
        print("结束上传图片")
        
        page.get_by_role("button", name="发布").click()
        print("发布")
        time.sleep(5)

    def msg_up_load_mp4(self, page: Page, mp4_path: str,habit_name: str,habit_detail: str):
        """
        msg_up_load_mp4
        """
        page.goto(self.upload_mp4_url)
        print(f"open load {self.upload_mp4_url}")
        time.sleep(15)
        page.wait_for_url(self.upload_mp4_url)
        
       # 请上传2小时以内的视频
       
        print("上传时长2小时内，大小不超过4GB，建议分辨率720p")
        # performs action and waits for a new `FileChooser` to be created
        with page.expect_file_chooser() as fc_info:
            page.locator("xpath=//div[./span[text()='上传时长2小时内，大小不超过4GB，建议分辨率720p及以上，码率10Mbps以内，格式为MP4/H.264格式']]").click()
        print("event expect_file_chooser")
        file_chooser = fc_info.value
        file_chooser.set_files(mp4_path)
        # 预备文件上传时间
        time.sleep(120)
        print(mp4_path)
        page.mouse.down()
        
        # <div contenteditable="" data-placeholder="添加描述" class="input-editor"></div>
        page.locator(".input-editor").fill(habit_detail)
        time.sleep(1)
        
        # <input type="text" name="" placeholder="概括视频主要内容，字数建议6-16个字符" class="weui-desktop-form__input">
        page.get_by_placeholder("概括视频主要内容，字数建议6-16个字符").fill(habit_name)
        time.sleep(1)

        page.get_by_role("button", name="发表").click()
        time.sleep(5)
       
    #################################################################################


def interface_auo_upload_shipinhao(out_path:str, bak_path:str):
    
    """
      对外调用接口
    """
    try:
        sys = platform.system()
        login_url = "https://channels.weixin.qq.com/"
        upload_picture_url = "https://channels.weixin.qq.com/platform/post/create"
        upload_mp4_url = "https://channels.weixin.qq.com/platform/post/create"
        if sys == "Windows":
            cookies_path = r"D:\doc\2023\05-third\chromedriver_win32\shipinhao_xiaohao.json"
        else:
            cookies_path = r"/root/bin/shipinhao_xiaohao.json"

        file_path, habit_name,habit_detail = interface_get_daily_note()
        print(file_path)
        print(habit_name)
        print(habit_detail)
        
        autoupload = CMyShipinhao(cookies_path, login_url, upload_picture_url,upload_mp4_url)
        for root,_,files in os.walk(out_path):
            for file in files:
                # 拼接路径
                mp4_file_path = os.path.join(root,file)
                if file.endswith('.mp4'):
                    if autoupload.upload_mp4(mp4_file_path,habit_name,habit_detail):
                        logging.info("upload_mp4 %s", mp4_file_path)
                        # move file
                        shutil.move(mp4_file_path, bak_path)

                    
                    
        
    except ValueError:
        print("Could not convert data to an integer.")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print(traceback.format_exc())


if __name__ == '__main__':
    # 避免熬夜21点到凌晨3点不工作   每周节省3小时时间
    if platform.system() == "Windows":
        OUT_PATH = r"D:\mp4\output"
        BACK_PATH = r"D:\mp4\back"
    else:
        OUT_PATH = r"/root/mp4/input"
        BACK_PATH = r"/root/mp4/bak"
    interface_auo_upload_shipinhao(OUT_PATH, BACK_PATH)