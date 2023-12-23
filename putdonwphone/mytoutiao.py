"""This module provides mydouyn"""
import time
import json
import os
import platform
from datetime import datetime
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

        temp_habit_name = "挑战早睡早起100天" + "第" + str(difference_in_days) + "天"
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
        return temp_habit_name,title

 
def interface_get_daily_englis_word():
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
class CToutiao:
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
            #display_headless = True
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            #self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            self.browser = playwright.chromium.launch(headless=display_headless)
            login_page = self.login_or_restore_cookies()
            self.msg_up_load(login_page, picture_path, habit_name,habit_detail)
            self.browser.close()
    
    def upload_mp4(self, mp4_path: str, msg: str):
        """
          upload_mp4
        """
        with sync_playwright() as playwright:
            display_headless = False
            # display_headless = True
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
            self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            login_page = self.login_or_restore_cookies()
            self.msg_up_load_mp4(login_page, mp4_path, msg)
            self.browser.close()
        
    def login_or_restore_cookies(self) -> Page:
        """
          登录
        """
        context = self.browser.new_context()
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

    def msg_up_load(self, page: Page, picture_path: str,habit_name:str, habit_detail:str):
        """
         微头条
        """
        page.goto(self.upload_picture_url)
        time.sleep(2)
        print(f"open  {self.upload_picture_url}")
        page.mouse.down()
        page.evaluate("() => window.scrollTo(0,document.body.scrollHeight)")
        page.mouse.click(100,200)

        msg = habit_name + "\r\n"
        msg += habit_detail
        # 使用文本内容定位元素
        page.locator("css=.ProseMirror").fill(msg)
        print("填写标题")
        time.sleep(2)
        page.mouse.down()
        page.evaluate("() => window.scrollTo(0,document.body.scrollHeight)")
        
        
        page.locator("label").filter(has_text="个人观点，仅供参考").locator("div").click()
        print("个人观点，仅供参考")
        
    
        # page.locator("//input[@type='checkbox' and @value='5']").click()
        # page.locator('text="个人观点，仅供参考"').click()
        # page.get_by_label('.byte-checkbox.checkbot-ite').check();
        # page.locator("//label[text()='个人观点，仅供参考']").check();
        # page.locator('css=.syl-toolbar-button').locator('nth=1').click()
        # page.get_by_role("button", name="图片").click()
        # page.getByRole('button', { name: '图片' })
        # page.locator('.byte-checkbox.checkbot-item').locator('nth=1').click()
        # page.get_by_role('checkbox').check()
        
        # with page.expect_file_chooser() as fc_info:
        #     page.locator('//button[contains(text(), "图片")]').click()
        # file_chooser = fc_info.value
        # file_chooser.set_files(picture_path)
         # 使用 page.locator 选择 checkbox
        # checkbox_locator = page.locator('label.byte-checkbox input[type="checkbox"][value="5"]')
        # # 点击 checkbox
        # checkbox_locator.click()
        time.sleep(2)
        print("开始上传图片")
        # page.locator("css=.syl-toolbar-tool.weitoutiao-image-plugin.static").click()
        page.locator("css=.syl-toolbar-tool.weitoutiao-image-plugin.static").click()
        # https://playwright.dev/python/docs/api/class-page#page-get-by-role
        page.get_by_role("button", name="本地上传").get_by_role("textbox").set_input_files(picture_path)
        time.sleep(2)
        page.get_by_role("button", name="确定").click()


        print("结束上传图片")
        
        time.sleep(3)
        print("上传图片")
        page.locator("xpath=//button[./span[text()='发布']]").click()
        print("发布")
        time.sleep(5)

    def msg_up_load_mp4(self, page: Page, mp4_path: str, msg: str):
        """
        msg_up_load_mp4
        """
        page.goto(self.upload_mp4_url)
        time.sleep(3)
        print(f"open  {self.upload_mp4_url}")
        
        # 使用文本内容定位元素
        example_element = page.locator("xpath=//div[contains(text(), '发布视频')]")
        example_element.click()
        print("点击 发布视频")
        time.sleep(3)

        # 使用文本内容定位元素
        
        page.locator(
            "label:has-text(\"点击上传 或直接将视频文件拖入此区域为了更好的观看体验和平台安全，平台将对上传的视频预审。超过40秒的视频建议上传横版视频\")").set_input_files(
            mp4_path)
            
        print("视频文件拖入此区域")
        time.sleep(20)
        # # 点击选择文件，输入文件
        # with page.expect_file_chooser() as fc_info:
        #     # 找到拖拽区域  
        #     page.click("xpath=//button[contains(text(), '上传图片')]")
        #     # 问题 文件弹框后 不自动退出 无法后续自动化操作
        #     file_chooser = fc_info.value
        #     file_chooser.set_files(picture_path)

        # time.sleep(3)
        # page.mouse.down()
        # page.mouse.down()

        # # 填写描述
        # page.locator("css=.iGOvMbhp8tU-").fill(msg)
        # time.sleep(3)
        # # 发布
        # page.locator("xpath=//button[./span[text()='发布']]").click()
        # time.sleep(5)
        print("发布")
        time.sleep(600)
    #################################################################################


def interface_auo_upload_weitoutiao():
    """
      对外调用接口
    """
    sys = platform.system()
    login_url = "https://mp.toutiao.com/profile_v4/weitoutiao/publish"
    upload_picture_url = "https://mp.toutiao.com/profile_v4/weitoutiao/publish"
    upload_mp4_url = "https://mp.toutiao.com/profile_v4/weitoutiao/publish"
    if sys == "Windows":
        cookies_path = r"D:\doc\2023\05-third\chromedriver_win32\toutiao_xiaohao.json"
    else:
        cookies_path = r"/root/bin/toutiao_xiaohao.json"

    file_path, habit_name,habit_detail = interface_get_daily_englis_word()
    print(file_path)
    print(habit_name)
    print(habit_detail)
    
    autoupload = CToutiao(cookies_path, login_url, upload_picture_url,upload_mp4_url)
    autoupload.upload_picture(file_path, habit_name,habit_detail)
    # mp4_path = r"D:\github\pythonTryEverything\putdonwphone\upload\WeChat_20231210084509.mp4"
    # autoupload.upload_mp4(mp4_path, msg)


if __name__ == '__main__':
    interface_auo_upload_weitoutiao()
