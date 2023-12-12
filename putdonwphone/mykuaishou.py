import time
import json
import pickle
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import platform
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import pyautogui
import requests
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
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
    def __init__(self,driver_path:str,cook_path:str,login_url:str, upload_url:str):
         self.chromedriver_path = driver_path
         self.driver = None
         self.cook_path = cook_path
         self.login_url = login_url
         self.upload_url = upload_url
         # playwright 部分
         self.browser = None
         print("creae MyKuaishou")
    def __del__(self):
        if self.driver:
            self.driver.close()
        print("is being destroyed")
         
    def init_browser(self):
        # 采用谷歌浏览器
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')  # 参数是让Chrome在root权限下跑
        chrome_options.add_argument('--disable-gpu')
        # chrome_opt.add_argument('start-maximized')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('window-size=1920x1480')
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

        sys = platform.system()
        print(sys)
        chrome_options.add_argument('--headless')  
        if sys == "Windows":
            print("sys=OS is Windows!!!")
        elif sys == "Linux":
            print("sys=OS is centos!!!")
            chrome_options.add_argument('--headless')  
            # selenium headless 不打开浏览器界面
            chrome_options.add_argument('no-sandbox')
            chrome_options.add_argument('disable-dev-shm-usage')

            # headless将在无头模式下启动Chrome浏览上下文
        # chrome_options.binary_location = chromedriver_path  Chrome has crashed. 不能这样写
        # 创建Chrome浏览器对象
        service_path = Service(self.chromedriver_path)  # 将文件路径作为参数传入Service对象
        driver = webdriver.Chrome(service=service_path, options=chrome_options)
        self.driver = driver
        return driver
    
    def usr_login(self):
        print("gen_url_Cookies begin")
        is_gen_cook = False
        if not os.path.exists(self.cook_path):
            print("cook_path not exists，please login >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            is_gen_cook = True  # 过期
        if not is_gen_cook:
            print(r"the cooks is ok >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            logging.debug(r"cool is is right")
            return  # 没有过期

        # 用法：https://selenium-python.readthedocs.io/getting-started.html
        self.driver.get(self.login_url)
        time.sleep(120)  # 留时间进行扫码
        # 在Python中，Pickle模块就用来实现数据序列化和反序列化。
        print("login succe")
        cookies = self.driver.get_cookies()
        # 该方法实现的是将序列化后的对象obj以二进制形式写入文件file中，进行保存

        # https://zhuanlan.zhihu.com/p/271674011
        pickle.dump(cookies, open(self.cook_path, "wb"))

        jsCookies = json.dumps(cookies)  # 转换成字符串保存
        print("dump cookies succed" + jsCookies)
    # Cookies登录
    def cookieslogin(self):
        print("cookieslogin begin {}".format(self.login_url))
        self.driver.get(self.login_url)
        print("open cook {}".format(self.cook_path))
        cookies = pickle.load(open(self.cook_path, "rb"))
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            self.driver.add_cookie(cookie)
        print("load cook {}".format(self.cook_path))
        time.sleep(1)
        self.driver.refresh()
        print("cookieslogin")
    # 上传图文
    def upload_picture(self, picture_path:str,msg:str):
        self.driver.get(self.upload_url)
        time.sleep(5)
        
        # selenium——鼠标操作ActionChains：点击、滑动、拖动
        # https://selenium-python.readthedocs.io/locating-elements.html
        # How to find elements by CSS selector in Selenium
        # https://scrapfly.io/blog/how-to-find-elements-by-css-selectors-in-selenium/
        # https://selenium-python-zh.readthedocs.io/en/latest/locating-elements.html
        # 通过XPath查找包含特定文本的<div>元素
        element = self.driver.find_element(By.XPATH, '//div[contains(text(), "上传图文")]')
        action = ActionChains(self.driver)
        action.click(element)
        action.perform()
        logging.info("open upload pic ok")
        print("open upload pic ok")
        time.sleep(5)
        
        # 替换 "Click Me" 为实际按钮上显示的文本

        # 找到按钮并执行相应操作
        upload_button = self.driver.find_element(By.XPATH, '//button[contains(text(), "上传图片")]')
        #upload_button.click()
        # 等待一些时间，确保文件上传对话框弹出
        time.sleep(5)
        
        # 使用 pyautogui 模拟键盘输入文件路径
        # pyautogui.write(picture_path)
        # # 模拟按下回车键
        # pyautogui.press("enter")
        # upload_button.send_keys(picture_path)
        # 使用JavaScript设置文件路径
        self.driver.execute_script(f"arguments[0].value='{picture_path}';", upload_button)

        
        time.sleep(10)
        print(f"{picture_path} >>>>>>>>>>>>> upload pic ok")
        # 编辑封面 【无法解决，但是不编辑封面也可以，主要按钮获取不对】
        # https://www.cnblogs.com/miki-peng/p/14509946.html
        # xpath_expression = "//button[./span[text()='编辑封面']]"
        # upload_button = self.driver.find_element(By.XPATH, xpath_expression)
        # upload_button.click()
        # print("编辑封面")
        
        # 等待新页面上的 "确定" 按钮出现
        #https://cloud.tencent.com/developer/article/1908549
        # confirm_button_new_page_xpath = '//*[text()="确定"]'
        # confirm_button_new_page = WebDriverWait(self.driver, 10).until(
        # EC.presence_of_element_located((By.XPATH, confirm_button_new_page_xpath))
        # )
        # # 在新页面上进行其他操作，如点击 "确定" 按钮
        # confirm_button_new_page.click()
        # 等待新窗口出现
        # new_window = WebDriverWait(self.driver, 10).until(EC.new_window_is_opened(self.driver.window_handles))
        # # 切换到新窗口
        # self.driver.switch_to.window(new_window)

        # # 获取新窗口的源码
        # new_page_source = self.driver.page_source

        # # 在这里可以对新页面的源码进行处理，例如打印出来
        # print(new_page_source)
        # 需要人工编译封面
        
        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')   #滑到底部 
                
        #填写描述
        msg_button = self.driver.find_element(By.CSS_SELECTOR,".iGOvMbhp8tU-")
        time.sleep(1)
        msg_button.send_keys(msg)
        msg_button.send_keys(Keys.ENTER)
        time.sleep(2)
        logging.info("write {}".format(msg))
        print("write {}".format(msg))
        
        #发布
        commit_button = self.driver.find_element(By.XPATH, "//button[./span[text()='发布']]")
        commit_button.click()
        time.sleep(5)
        logging.info("commit")
        print("commit")
    
    def login_and_save_cookies():
        
        
#################################################################################
       

def interface_auo_upload_kuaishou():
    
    sys = platform.system()
    if sys == "Windows":
        driver_path = r"D:\doc\2023\05-third\chromedriver_win32\chromedriver.exe"
        coook_path = r"D:\doc\2023\05-third\chromedriver_win32\mykuaishou.pkl"
        login_url = "https://cp.kuaishou.com/profile"
        upload_url = "https://cp.kuaishou.com/article/publish/video"
        save_picture_path = r"D:\github\pythonTryEverything\putdonwphone\upload\temp.png"
        default_picture_path = r"D:\github\pythonTryEverything\putdonwphone\upload\ZfCYoSG1BE_small.jpg"
    else:
        driver_path = r"/root/bin/chromedriver"
        coook_path = r"/root/bin/mykuaishou.pkl"
        login_url = "https://cp.kuaishou.com/profile"
        upload_url = "https://cp.kuaishou.com/article/publish/video"
        save_picture_path = r"/root/code/python/putdonwphone/upload/temp.png"
        default_picture_path = r"/root/code/python/putdonwphone/upload/ZfCYoSG1BE_small.jpg"
    
    getupHaibt = GetupHaibt(save_picture_path,default_picture_path)
    msg = getupHaibt.interface_get_up()
    print(msg)
    file_path = getupHaibt.save_picture_path
    time.sleep(1)
        
    autoupload = MyKuaishou(driver_path,coook_path,login_url,upload_url)
    autoupload.init_browser()
    autoupload.usr_login()
    autoupload.cookieslogin()
    autoupload.upload_picture(file_path,msg)
    
    
    
    

        
if __name__ == '__main__':
    
    interface_auo_upload_kuaishou()
    # scheduler = BlockingScheduler()
    # scheduler.add_job(interface_auo_upload_kuaishou, CronTrigger.from_crontab("26 20 * * *"), id="interface_auo_upload_kuaishou")
    # scheduler.start()
    
# https://www.reddit.com/r/learnpython/comments/kh34f7/selenium_pyautogui_in_background/
# https://github.com/asweigart/pyautogui/issues/87