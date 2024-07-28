"""This module provides zhuhu small"""
import json
import os
import time
import random
import platform
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
#from pythonTryEverything.putdonwphone.data import englisword
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from auto.write.util import bingpic
from learn import learn_english_speak
from selenium import webdriver
from auto.write.zhihu import mykimi
########################################################################
class CMyZhiHu:
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
        # 想法 ---喜欢
        self.user_list = None
        self.context = None
        self.zse_ck = None
        self.pic_path = None
        print("create CMyZhiHu")

    def __del__(self):
        print("CMyZhiHu is being destroyed")

    def upload_picture(self, picture_path_list: str, habit_name:str, habit_detail:str):
        """
          upload_picture
        """
        with sync_playwright() as playwright:
            display_headless = False
            sys = platform.system()
            if sys == "Linux":
              display_headless = True
              self.browser = playwright.chromium.launch(headless=display_headless)
            else:
                self.browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            login_page = self.login_or_restore_cookies()
            print("login_or_restore_cookies")
            self.msg_up_load(login_page, picture_path_list, habit_name,habit_detail)
            self.browser.close()
    
    ##############################
    def get_signed_header(self)-> str:
        """
          害怕自己的内容被第三方拿去训练大模型 乱码
        """
        # 启动浏览器
        driver = webdriver.Chrome()

        # 打开知乎页面
        driver.get("https://www.zhihu.com/question/660773601")

        # 等待页面加载
        time.sleep(5)

        # 获取所有cookie
        cookies = driver.get_cookies()

        # 查找包含__zse_ck参数的cookie值
        zse_ck = None
        for cookie in cookies:
            if '__zse_ck' in cookie['name']:
                zse_ck = cookie['value']
                break

        # 打印获取到的__zse_ck参数值
        if zse_ck:
            print("获取到的__zse_ck值为:", zse_ck)
        else:
            print("未找到包含__zse_ck参数的cookie")
        # 关闭浏览器
        driver.quit()
        return zse_ck
    
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
        self.context.clear_cookies()
        page = self.context.new_page()
        page.goto(self.login_url)

        if os.path.exists(self.cookies_path):
            print("load cookies")
            # 从文件中加载 cookies
            with open(self.cookies_path, 'r',encoding='utf-8') as f:
                cookies = json.load(f)
                print(cookies)
            self.context.add_cookies(cookies)
            self.context.add_cookies([
                         {"name": "__zse_ck", "value": "001_2NzwjJPAHL=5po/JQ2N8cxTB+cA+56jPH3pt5SxdE7uYZHSo+XcH/sc=IMo6WrWS9CFziCu8akMtctM+qXfHQsx1ewSq5aQfpj484G9R5/Kyqk64cDPk5iplyCr+T4xG", "domain": ".zhihu.com", "path": "/", "expires": int(time.time()) + 5000}
                         ])
            time.sleep(3)
        else:
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            # 扫名二维码登录 需要人工处理
            time.sleep(60)
            cookies = page.context.cookies()
            zse_ck = None
            for cookie in cookies:
                if '__zse_ck' in cookie['name']:
                    zse_ck = cookie['value']
                    break

            # 打印获取到的__zse_ck参数值
            if zse_ck:
                print("获取到的__zse_ck值为:", zse_ck)
            else:
                print("未找到包含__zse_ck参数的cookie")

            with open(self.cookies_path, 'w',encoding='utf-8') as f:
                f.write(json.dumps(cookies))
        print("login_or_restore_cookies")
        return page


    #######################自动点赞#########################################
    def zhihu_auto_agree(self, page: Page):
        """
         赞同 三个积分 playwright codegen https://www.zhihu.com/
         follow ---
        """
        page.goto("https://www.zhihu.com/follow")
        time.sleep(6)
        print("https://www.zhihu.com/follow")
        # page.locator("xpath=//a[text()='推荐']").click()
        #page.locator("xpath=//a[contains(text(),'推荐']").click()
        page.get_by_role("main").get_by_role("link", name="推荐", exact=True).click()
        time.sleep(4)
        page.mouse.down()
        print("推荐")
        ## Child
        for index in [2,3,4]:
            page.mouse.down()
            page.mouse.down()
            time.sleep(1)
            page.mouse.down()
            page.mouse.down()
            time.sleep(1)
            element = page.locator("xpath=//button[contains(text(),'赞同')]").locator('nth={}'.format(index))
            time.sleep(1)
            print(element.all_inner_texts())
            element.hover()
            time.sleep(3)
            element.click()
            print("赞同完成")
            time.sleep(3)
        print("---------zhihu_auto_agree---------")
    ##################################自动回答#########################################   
    def zhihu_auto_answer(self, page: Page):
        """
        回答问题 playwright codegen https://www.zhihu.com/creator/featured-question/goodat-topic/all
        方向：职场
        """
        page.goto("https://www.zhihu.com/creator/featured-question/goodat-topic/all")
        time.sleep(5)
        page.get_by_role("link", name="擅长话题").click()
        print("为你推荐,这个时间设置5秒，太短，改为10秒")
        time.sleep(20)
        # man question 第二个问题 下标是3
        with self.context.expect_page(timeout=20000) as new_page_info:
            #page.locator("xpath=//*[contains(text(),'写回答')]").locator("nth=1")
            #CSS选择器
            page.locator("div:nth-child(4) > .css-1hbj689 > .css-ra7giy > div > .Button").click(timeout=20000)
        time.sleep(5)
        question_page = new_page_info.value
        question_page.wait_for_load_state()

        question_title = question_page.locator("h1.QuestionHeader-title").locator("nth=1").text_content()
        print(question_title)
        
        time.sleep(3)
        resulut = mykimi.Get_msg_by_kimi(question_title)
        if len(resulut) == 0:
            return None
        resulut = resulut.replace("**", "")
        resulut = resulut.replace("#", "")
        #去掉字符串中的所有 **（双星号)
        print("---写回答-----")
        #写回答
        #question_page.get_by_role("main").get_by_role("button", name="​写回答").click()
        #page.locator("xpath=//button[./span[text()='发布']]").click()
        question_page.locator("xpath=//button[contains(text(),'写回答')]").locator("nth=0").click()
        time.sleep(5)
        
        with self.context.expect_page(timeout=20000) as page_answer1:
            #page.locator("xpath=//*[contains(text(),'写回答')]").locator("nth=1")
            #question_page.locator(".css-1codfpf").click(timeout=20000)
            question_page.get_by_text("全屏编辑").click()
        time.sleep(5)
        page_answer = page_answer1.value
        page_answer.wait_for_load_state()

       
        # 自动发布---填写回答内容
        print("begin answer")
        page_answer.locator("css=.notranslate.public-DraftEditor-content").fill(resulut)
        time.sleep(5)
        
        picture_path_list = bingpic.get_random_jpg_files(self.pic_path)
        print(picture_path_list)
        if len(picture_path_list) > 0:
            print("开始上传图片")
            page_answer.get_by_role("button", name="图片").click()
            time.sleep(3)
            print("本地上传")
            with page_answer.expect_file_chooser() as fc_info:
                page_answer.locator(".css-n71hcb").click()
            file_chooser = fc_info.value
            file_chooser.set_files(picture_path_list)
            time.sleep(180) # 防止图片过大 来不及上传,3miniute
            page_answer.get_by_role("button", name="插入图片").click()
            print("insert the pic")
            time.sleep(5)
        
        page_answer.mouse.down()
        page_answer.mouse.down()
        page_answer.mouse.down()
        page_answer.get_by_text("无声明").click()
        time.sleep(3)
        page_answer.get_by_role("option", name="包含 AI 辅助创作").click()
        time.sleep(3)

        # page_answer.get_by_text("允许规范转载").click()
        # page_answer.get_by_role("option", name="禁止转载").click()
        # time.sleep(10)
        page_answer.get_by_role("button", name="发布回答").click()
        time.sleep(10)
        page_answer.close()
    ###################################################
    # def like_other_things(self, page: Page, user_list):
    #     """
    #     喜欢 playwright codegen https://www.zhihu.com/
    #     """
    #     for  cur_url in user_list:
    #         page.goto(cur_url)
    #         time.sleep(6)
    #         print(f"open  {cur_url}")
    #         # 从主页进入 headless不行
    #         page.locator("xpath=//div[contains(text(), '写想法')]").click()
    #         print("点击 发布图文")
            
            
    #         time.sleep(2)
            
    #         page.get_by_placeholder("请输入标题（选填）").fill(habit_name)
    #         page.get_by_role("textbox").locator('nth=-1').fill(habit_detail)
    #         # page.locator(".InputLike").fill(habit_detail)
    #         time.sleep(3)
            
    #         print("开始上传图片")
    #         page.locator(".css-88f71l > button:nth-child(2)").click()
    #         time.sleep(2)
    #         print("本地上传")
    #         with page.expect_file_chooser() as fc_info:
    #             page.locator(".css-n71hcb").click()
    #         file_chooser = fc_info.value
    #         file_chooser.set_files(picture_path_list)
    #         time.sleep(5)
     ################################################################################
        
    def auto_help_answer(self, page: Page, picture_path_list,habit_name:str, habit_detail:str):
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
        file_chooser.set_files(picture_path_list)
        time.sleep(5)
       
        
        page.get_by_role("button", name="插入图片").click()
        time.sleep(5)
        
        print("结束上传图片")
        
        page.get_by_role("button", name="发布").click()
        print("发布")
        time.sleep(5)

def help_ohter_by_qa():
    """
     成为技术大牛，成为专业人士
    """
    sys = platform.system()
    # 参数设置
    login_url = "https://www.zhihu.com/"
    upload_picture_url = "https://www.zhihu.com/"
    upload_mp4_url = "https://www.zhihu.com/"
    if sys == "Windows":
        cookies_path = r"D:\mp4\etc\zhihu_qa.json"
        pic_path = r"D:\mp4\wallpapers\2024\02"
    elif sys == "Darwin":
        cookies_path = r"/Users/wangchuanyi/mp4/etc/zhihu_qa.json"
        pic_path = r"/Users/wangchuanyi/mp4/pic"
    else:
        cookies_path = r"/root/bin/zhihu_qa.json"
    autoupload = CMyZhiHu(cookies_path, login_url, upload_picture_url,upload_mp4_url)
    autoupload.pic_path = pic_path
    #zse_ck = au
    with sync_playwright() as playwright:
        display_headless = False
        sys = platform.system()
        if sys == "Linux":
            display_headless = True
            browser = playwright.chromium.launch(headless=display_headless)
        else:
            browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
        autoupload.browser = browser
        login_page = autoupload.login_or_restore_cookies()

        # 回答问题
        time.sleep(random.randint(0, 20))
        # 连续回答三个问题 这个做法不如 一次获取三个问题，每个问题继续回答
        count = 1
        while(count < 3):
            try:
                autoupload.zhihu_auto_answer(login_page)
                time.sleep(random.randint(0, 30))
            except Exception as mye:
                print(mye)
            count = count + 1
        autoupload.zhihu_auto_agree(login_page)
        # 关闭浏览器
        autoupload.browser.close()
        print("--------small---------")

####################################################

def interface_auo_upload_msg_zhihu(file_path_list:str,habit_name :str,habit_detail :str):
    """
      对外调用接口
    """
    print("interface_auo_upload_zhihu_small")
    try:
        sys = platform.system()
        login_url = "https://www.zhihu.com/"
        upload_picture_url = "https://www.zhihu.com/"
        upload_mp4_url = "https://www.zhihu.com/"
        if sys == "Windows":
            cookies_path = r"D:\mp4\etc\zhihu_small.json"
        elif sys == "Darwin":
            cookies_path = r"/Users/wangchuanyi/mp4/etc/zhihu_small.json"
        else:
            cookies_path = r"/root/bin/zhihu_small.json"
        autoupload = CMyZhiHu(cookies_path, login_url, upload_picture_url,upload_mp4_url)
        with sync_playwright() as playwright:
            display_headless = False
            sys = platform.system()
            if sys == "Linux":
                display_headless = True
                browser = playwright.chromium.launch(headless=display_headless)
            else:
                browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
            autoupload.browser = browser
            login_page = autoupload.login_or_restore_cookies()
            # 发布想法
            autoupload.msg_up_load(login_page, file_path_list, habit_name,habit_detail)
            # 赞同
            autoupload.zhihu_auto_agree(login_page)
            
            # 推荐关注
            # playwright codegen https://www.zhihu.com/creator
            #autoupload.zhihu_auto_guanzhu(login_page)
           # 回答问题
        #autoupload.zhihu_auto_answer(login_page)
        # 关闭浏览器
        autoupload.browser.close() 
    except Exception as mye:
        print(mye)
        
if __name__ == '__main__':
    help_ohter_by_qa()
    job_defaults = {
         'coalesce': False,
         'max_instances': 1
    }
    backsched = BlockingScheduler(job_defaults=job_defaults, timezone='Asia/Shanghai')
    backsched.add_job(help_ohter_by_qa, CronTrigger.from_crontab("30 0 * * *"))
    backsched.start()