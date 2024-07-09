"""This module provides zhuhu small"""
import json
import os
import time
import platform
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
#from pythonTryEverything.putdonwphone.data import englisword
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from learn import learn_english_speak
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
    
    def upload_mp4(self, mp4_path: str, msg: str):
        """
          upload_mp4
        """
        with sync_playwright() as playwright:
            display_headless = False
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
        userAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        sys = platform.system()
        if sys == "Linux":
            userAgent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        
        self.context = self.browser.new_context(user_agent=userAgent)
        self.context.clear_cookies()
        page = self.context.new_page()
        page.goto(self.login_url)

        if os.path.exists(self.cookies_path):
            print("load cookies")
            # 从文件中加载 cookies
            with open(self.cookies_path, 'r',encoding='utf-8') as f:
                cookies = json.load(f)
            self.context.add_cookies(cookies)
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

    def msg_up_load(self, page: Page, picture_path_list,habit_name:str, habit_detail:str):
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
        # page.get_by_placeholder("请输入标题（选填）").fill(habit_name)
        msg = habit_name + "\r\n"
        msg += habit_detail
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
        for index in [2,3,4,5]:
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

    ###########################################################################  
    def zhihu_auto_answer(self, page: Page):
        """
        回答问题 playwright codegen https://www.zhihu.com/creator/featured-question/recommend
        """
        page.goto("https://www.zhihu.com/creator/featured-question/recommend")
        time.sleep(3)
        print("https://www.zhihu.com/creator/featured-question/recommend")
        page.get_by_role("link", name="为你推荐").click()
        print("为你推荐,这个时间设置5秒，太短，改为10秒")
        time.sleep(10)
        
        # man question 第二个问题 下表是3
        with self.context.expect_page(timeout=20000) as new_page_info:
            #page.locator("xpath=//*[contains(text(),'写回答')]").locator("nth=1")
            page.locator("div:nth-child(3) > .css-n9ov20 > .css-wfj162 > .css-nyeu1f > div > .Button").click(timeout=20000)
            
        time.sleep(5)
        question_page = new_page_info.value
        question_page.wait_for_load_state()

        question_title = question_page.locator("h1.QuestionHeader-title").locator("nth=1").text_content()
        print(question_title)
        # #question_example = question_page.locator("css=.RichText.ztext.css-jflero").locator("nth=0").text_content()
        # question_example = question_page.locator("css=.RichText.ztext.css-jflero:first-child").text_content()
        # if len(question_example) ==0:
        #     question_example =None
        # print(question_example)
        time.sleep(2)
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

        #question_page.get_by_role("textbox").fill(question_title)
        page_answer.locator("css=.notranslate.public-DraftEditor-content").fill(question_title)
        page_answer.mouse.down()
        page_answer.mouse.down()
        page_answer.mouse.down()
        page_answer.get_by_text("无声明").click()
        time.sleep(3)
        page_answer.get_by_role("option", name="包含 AI 辅助创作").click()
        time.sleep(3)

        page_answer.get_by_text("允许规范转载").click()
        page_answer.get_by_role("option", name="禁止转载").click()
        time.sleep(1)

        page_answer.get_by_role("button", name="发布回答").click()
        time.sleep(30)
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
    def msg_up_load_mp4(self, page: Page, mp4_file_path: str, msg: str):
        """
        msg_up_load_mp4
        """
        page.goto(self.upload_mp4_url)
        time.sleep(5)
        print(f"open  {self.upload_mp4_url}")
        
         # 点击选择文件，输入文件
        with page.expect_file_chooser() as fc_info:
            page.locator("xpath=//button[contains(text(), '上传视频')]").click()
        file_chooser = fc_info.value
        file_chooser.set_files(mp4_file_path)
        time.sleep(120)
        print("上传视频完成")
        ## https://www.zhihu.com/zvideo/upload-video

      
        page.mouse.down()
        page.get_by_placeholder("填写视频简介，让更多人找到你的视频").fill(msg)
        time.sleep(3)
        
        page.mouse.down()
        page.locator("css=.RadioButton.VideoUploadForm-radio.css-1u1atbi").locator('nth=0').click()
        time.sleep(6)
        # # 发布
        page.get_by_role("button", name="发布视频").click()
        print("发布")
        time.sleep(8)
        
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

    #################################################################################
    def zhihu_auto_guanzhu(self, page: Page):
        """
         赞同 三个积分 playwright codegen https://www.zhihu.com/creator
         follow ---
        """
        try:
            page.goto("https://www.zhihu.com/creator")
            time.sleep(5)
            page.mouse.down()
            page.get_by_role("button", name="去完成").nth(2).click()
            time.sleep(4)
            page.locator(".css-yxuzwv").first.click()
            page.mouse.down()
        finally:
            print("-----")
    ###############################


def interface_auo_upload_zhihu_small():
    """
      对外调用接口
    """
    print("interface_auo_upload_zhihu_small")
    
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
    file_path_list, habit_name,habit_detail = learn_english_speak.interface_get_daily_englis_word_big()

    autoupload = CMyZhiHu(cookies_path, login_url, upload_picture_url,upload_mp4_url)
    # mp4_path = r"D:\github\pythonTryEverything\putdonwphone\upload\WeChat_20231210084509.mp4"
    # autoupload.upload_mp4(mp4_path, msg)
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

####################################################

def interface_auo_upload_mp4_zhihu(mp4_file_path):
    """
      对外调用接口
    """
    print("interface_auo_upload_zhihu_small")
    
    sys = platform.system()
    login_url = "https://www.zhihu.com/"
    upload_picture_url = "https://www.zhihu.com/"
    upload_mp4_url = "https://www.zhihu.com/zvideo/upload-video"
    if sys == "Windows":
        cookies_path = r"D:\mp4\etc\zhihu_small.json"
    elif sys == "Darwin":
        cookies_path = r"/Users/wangchuanyi/mp4/etc/zhihu_small.json"
    else:
        cookies_path = r"/root/bin/zhihu_small.json"
    #file_path_list, habit_name,habit_detail = learn_english_speak.interface_get_daily_englis_word_big()

    autoupload = CMyZhiHu(cookies_path, login_url, upload_picture_url,upload_mp4_url)
    # mp4_path = r"D:\github\pythonTryEverything\putdonwphone\upload\WeChat_20231210084509.mp4"
    file_name = os.path.basename(mp4_file_path)
    file_name = file_name.split('.')[0]
    habit_name = "#" + file_name + "\r\n"
    habit_name += " 日拱一卒无有尽，功不唐捐终入海" + "\r\n"
    autoupload.upload_mp4(mp4_file_path, habit_name)
###############################################################

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
        