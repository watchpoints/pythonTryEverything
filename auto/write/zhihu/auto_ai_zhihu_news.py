"""This module provides zhuhu small"""
import json
import os
import time
import datetime
import platform
import requests
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
    ####################################################
    def push_msg_to_article (self, page: Page, article_title: str, article_msg: str, article_picture_path:str):
        """
        发布文章
        """
        page.goto("https://zhuanlan.zhihu.com/write")
        time.sleep(3)

        page.locator("css=.Input.i7cW1UcwT6ThdhTakqFm").fill(article_title)
        time.sleep(1)
        # playwright codegen https://zhuanlan.zhihu.com/write
        # 填写内容
        page.locator(".DraftEditor-root").click()
        page.get_by_role("textbox").nth(1).fill(article_msg)
        time.sleep(3)
        
        page.mouse.down()
        page.mouse.down()
        
        with page.expect_file_chooser() as fc_info:
            page.get_by_text("添加文章封面").click()
        file_chooser = fc_info.value
        file_chooser.set_files(article_picture_path)
        time.sleep(5)

        page.get_by_text("无声明").click()
        time.sleep(3)
        page.get_by_role("option", name="包含 AI 辅助创作").click()
        time.sleep(3)
        # element = page.locator("xpath=//button[contains(text(),'赞同')]").locator('nth={}'.format(index))
        # time.sleep(1)
        # print(element.all_inner_texts())

        button1 = page.query_selector('css=.css-1gtqxw0')
        print(button1.inner_html())
        print(button1.inner_text())
        button1.hover()
        time.sleep(3)
        button1.click()

        page.get_by_placeholder("搜索话题").fill("打工人")
        time.sleep(3)
        page.get_by_placeholder("搜索话题").press("Enter")
        time.sleep(3)
        page.get_by_role("button", name="打工人", exact=True).click()
        time.sleep(3)

        page.locator("css=.Button.css-d0uhtl.FEfUrdfMIKpQDJDqkjte.Button--primary.Button--blue.epMJl0lFQuYbC7jrwr_o.JmYzaky7MEPMFcJDLNMG").click()
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
        autoupload.zhihu_auto_guanzhu(login_page)

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
#############################

def push_msg_zhihu_article(artilce_title:str, artilce_msg:str, save_picture_path:str):
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
            # 发布文章
            autoupload.push_msg_to_article(login_page, artilce_title, artilce_msg,save_picture_path)
            # 赞同
            #autoupload.zhihu_auto_agree(login_page)
            
            # 推荐关注
            # playwright codegen https://www.zhihu.com/creator
            #autoupload.zhihu_auto_guanzhu(login_page)

        
            autoupload.browser.close()
    except Exception as mye:
        print(mye)
##############################
def down_picture(image_url: str,save_picture_path: str):
    """
    下载图片
    """
    # 发送 GET 请求获取图片内容
    response = requests.get(image_url,timeout=30)
    # 检查请求是否成功
    if response.status_code == 200:
        # 获取图片内容
        image_content = response.content
        # 保存图片到本地
        with open(save_picture_path, "wb") as file:
            file.write(image_content)
            print(f"Image downloaded and saved to {save_picture_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        save_picture_path = ""
    return save_picture_path

def get_url_content(url, file_path, save_picture_path):
    """
      读取文章内容 
    """
    with sync_playwright() as playwright:
        display_headless = False
        sys = platform.system()
        if sys == "Linux":
            display_headless = True
            browser = playwright.chromium.launch(headless=display_headless)
        else:
            browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
        context = browser.new_context()
        page = context.new_page() # 我要获取整个文章内容

        page.goto(url)
        time.sleep(3)
        ## print(page.content()) # 我要获取整个文章内容 html不

        title = page.title() #2024-05-13 打工人日报 - 博客 - 打工人日志
        print("网页标题:", title)
        # 获取当前日期（假设今天是 2024 年 6 月 9 日）
        current_date = datetime.datetime.now()
        current_format = current_date.strftime('%Y-%m-%d')
        # 获取本年的第几周
        week_number = current_date.strftime("%U")
        # 计算过去多少时间
        days_passed = current_date.timetuple().tm_yday
        # 将信息拼接成一个字符串

        data_output_string = f"当前日期是 {current_format}, 本年的第 {int(week_number)+1} 周，本年已经过去 {days_passed} 天。"
        print(data_output_string)

        english_words_txt = requests.get("https://open.iciba.com/dsapi/",timeout=10).json()
        data_output_string += "\r\n"
        data_output_string += english_words_txt['content'] + "\r\n"
        data_output_string += english_words_txt['note'] + "\r\n"

        # 获取包含图片的 <img> 元素
        img_element = page.query_selector('img.hb-featured-img')
        # 获取图片地址
        img_src = img_element.get_attribute('src')
        print("Picture URL:", img_src)
        save_picture_path = down_picture(img_src, save_picture_path)


        new_blog=page.locator(".hb-blog-post-content.hb-module")
        # https://brightdata.com/blog/how-tos/playwright-web-scraping
        print('-------------小王同学提效----------------------')
        new_blog_text = new_blog.inner_text()
        # 数据分析

        # 定义关键字
        keyword = "福利分享"

        # 查找关键字在字符串中的位置
        index = new_blog_text.find(keyword)

        if index != -1:  # 如果关键字存在于字符串中
            # 通过关键字位置进行切片取出福利分享之前的内容
            content_before_keyword = new_blog_text[:index]
            new_blog_text =  content_before_keyword
        else:
            print("字符串中不包含关键字:", keyword)

        # 组装结果
        all_msg = data_output_string
        all_msg += "\r\n"
        all_msg += "来源：打工人日志 来源 网络，不代表个人观点 侵删"
        all_msg += new_blog_text + "\r\n"

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(all_msg)
        browser.close()
        return save_picture_path,all_msg

def auto_ai_tools_zhihu():
    """
      读取文章内容 
    """
    # 获取当前日期
    current_date = datetime.datetime.now()
    # 减去三天
    three_days_ago = current_date - datetime.timedelta(days=3)
    # 格式化当前日期和三天前的日期为 "YYYY-MM-DD" 格式
    current_date_str = current_date.strftime('%Y-%m-%d')
    three_days_ago_str = three_days_ago.strftime('%Y-%m-%d')

    print("当前日期:", current_date_str)
    print("三天前的日期:", three_days_ago_str)
    current_date_str = three_days_ago_str
    ## 01
    sys = platform.system()
    if sys == "Windows":
        save_picture_path = r"D:\mp4\etc\temp.png"
    elif sys == "Darwin":
        save_picture_path = r"/Users/wangchuanyi/mp4/etc/temp.png"
    else:
        save_picture_path = r"/root/code/python/putdonwphone/upload/temp.png"
    web_url = "https://jobcher.github.io/github_trending_" + current_date_str
    save_file_path = "/Users/wangchuanyi/temp/" + current_date_str + ".txt"
    article_title = "打工人日报:" + current_date_str
    save_picture_path,article_msg = get_url_content(web_url, save_file_path,save_picture_path)
    push_msg_zhihu_article(article_title, article_msg,save_picture_path)
    

if __name__ == '__main__':

    #auto_ai_tools_zhihu()
   
    print("---interface_auo_upload_zhihu---")
    job_defaults = {
         'coalesce': False,
         'max_instances': 1
    }
    backsched = BlockingScheduler(job_defaults=job_defaults, timezone='Asia/Shanghai')
    # 汇总 最新资料 每日新闻
    backsched.add_job(auto_ai_tools_zhihu, CronTrigger.from_crontab("0 20 * * *"))
    backsched.start()