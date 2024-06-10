from auto.data import myrss
import platform
# from playwright.sync_api import sync_playwright
# from playwright.sync_api import Page
# from auto.write.zhihu import auto_ai_zhihu_news

# def test_zhuhu_small():
#     try:
#         sys = platform.system()
#         login_url = "https://www.zhihu.com/"
#         upload_picture_url = "https://www.zhihu.com/"
#         upload_mp4_url = "https://www.zhihu.com/"
#         if sys == "Windows":
#             cookies_path = r"D:\mp4\etc\zhihu_small.json"
#         elif sys == "Darwin":
#             cookies_path = r"/Users/wangchuanyi/mp4/etc/zhihu_small.json"
#         else:
#             cookies_path = r"/root/bin/zhihu_small.json"
#         autoupload = auto_ai_zhihu_news.CMyZhiHu(cookies_path, login_url, upload_picture_url,upload_mp4_url)
#         with sync_playwright() as playwright:
#             display_headless = False
#             sys = platform.system()
#             if sys == "Linux":
#                 display_headless = True
#                 browser = playwright.chromium.launch(headless=display_headless)
#             else:
#                 browser = playwright.chromium.launch(channel="chrome",headless=display_headless)
#             autoupload.browser = browser
#             login_page = autoupload.login_or_restore_cookies()
#             # 发布文章
#             autoupload.push_msg_to_article(login_page, artilce_title, artilce_msg,save_picture_path)
          
#             autoupload.browser.close()
#     except Exception as mye:
#         print(mye)
def push_daily_drawing():
    sys = platform.system()
    if sys == "Windows":
        picture_path = r"D:\mp4\etc\daily"
    elif sys == "Darwin":
        picture_path = r"/Users/wangchuanyi/mp4/etc/daily"
    else:
        picture_path = r"/root/bin/daily"
    daily_item = myrss.get_daily_drawing()
    
    for item in daily_item:
            # # 打印标题
            # print("诗词标题：", item['art_title'])

            # # 打印链接
            # print("诗词链接：", item['art_link'])

            # # 打印描述
            # print("诗词描述：", item['art_desc'])

            # # 打印更新日期
            # print("更新日期：", item['art_update'])
            myrss.get_daily_poetry(item['art_link'],picture_path)

            data = {"art_title": art_title,
                    "art_link": art_link,
                    "art_desc": art_desc,
                    "art_update": art_update}


if __name__ == '__main__':
 

