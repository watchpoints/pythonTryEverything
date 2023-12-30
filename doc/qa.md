
### 微信上传慢 点击发布 没有发布视频

1. 2g上传直接卡死
2. 发布没有起作用


## 当天问题当天解决

python+playwright 学习-03  input文件上传控件display: none

很多人遇到同样问题

<input type="file" accept="video/mp4,video/x-m4v,video/*,image/*" multiple="multiple" style="display: none;">


[Question] How to click hidden elements? 
- https://stackoverflow.com/questions/69001691/selector-resolved-to-hidden-playwright-and-input-with-display-none-can-any
- https://github.com/microsoft/playwright/issues/12267
- https://www.cnblogs.com/yoyoketang/p/17175183.html
- https://github.com/cypress-io/cypress/issues/19763
- 


尝试方法1: 如果不是input输入框，必须点开文件框的情况（selenium上没法实现的操作
  performs action and waits for a new `FileChooser` to be created
  with page.expect_file_chooser() as fc_info:
      page.locator("xpath=//div[./span[text()='上传时长2小时内，大小不超过4GB，建议分辨率720p及以上，码率10Mbps以内，格式为MP4/H.264格式']]").click()
  print("event expect_file_chooser")
  file_chooser = fc_info.value
  file_chooser.set_files(mp4_path)

 默认上传1分钟的文件


How to determine video stream size



----------------------------------------------------------------------------------------------
python+playwright 学习-02 HTTP请求头之User-Agent

1. User agent 用户代理 chrome://version/
   window:
   Linux
   user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
   自定义UA代理池 



2. [Question] 反爬虫

https://github.com/microsoft/playwright-python/issues/2120
https://github.com/microsoft/playwright-python/issues/1793


https://blog.csdn.net/LIFENG0402/article/details/120832220

https://www.zenrows.com/blog/playwright-user-agent#use-a-random-user-agent





--------------------------------------------------------

## 实现思路 





- https://www.programsbuzz.com/article/playwright-nth-element-selector

  1) <textarea class="css-27pm8q" placeholder="请输入标题（选填）"></textarea> aka get_by_placeholder("请输入标题（选填）")
   2) <div tabindex="0" role="textbox" spellcheck="true" co…>…</div> aka locator("div").filter(has_text="分享你此刻的想法，亿万知友为 你鼓掌0").get_by_role("textbox")


 -   有弹框 看不到源码怎么办？ 
  

 Allows locating elements by their ARIA role, ARIA attributes and accessible name.



 https://playwright.dev/python/docs/api/class-page#page-get-by-role
        page.get_by_role("button", name="本地上传").get_by_role("textbox").set_input_files(picture_path)
python+playwright 学习-01 鼠标悬停 hover() 和listitem 定位
- https://zhuanlan.zhihu.com/p/632612838
- https://www.cnblogs.com/yoyoketang/p/17198000.html
- 
- 根据文本内容 和标签来完成

page.locator("label").filter(has_text="个人观点，仅供参考").locator("div").click()

<label class="byte-checkbox checkbot-item"><input type="checkbox" value="5"><span class="byte-checkbox-wrapper" data-immersive-translate-effect="1" data-immersive_translate_walked="09f2a076-4c93-439f-8ea8-c8fc82bcd126"><div class="byte-checkbox-mask" data-immersive-translate-effect="1" data-immersive_translate_walked="09f2a076-4c93-439f-8ea8-c8fc82bcd126"></div><span class="byte-checkbox-inner-text" data-immersive-translate-effect="1" data-immersive_translate_walked="09f2a076-4c93-439f-8ea8-c8fc82bcd126">个人观点，仅供参考</span></span></label>

page.locator("label").filter(has_text="个人观点，仅供参考").locator("div").click()

<label class="byte-checkbox checkbot-item"><input type="checkbox" value="5"><span class="byte-checkbox-wrapper" data-immersive-translate-effect="1" data-immersive_translate_walked="09f2a076-4c93-439f-8ea8-c8fc82bcd126"><div class="byte-checkbox-mask" data-immersive-translate-effect="1" data-immersive_translate_walked="09f2a076-4c93-439f-8ea8-c8fc82bcd126"></div><span class="byte-checkbox-inner-text" data-immersive-translate-effect="1" data-immersive_translate_walked="09f2a076-4c93-439f-8ea8-c8fc82bcd126">个人观点，仅供参考</span></span></label>



- 文件上传：点击整个区域代替 里面部分元素

intput:<div class="syl-toolbar-tool weitoutiao-image-plugin static"> xxxx 很多内容
ouput:page.locator("css=.syl-toolbar-tool.weitoutiao-image-plugin.static").click()


- lable 标签
<label class="upload-btn--9eZLd button--1pFK2">
  <input class="upload-btn-input--1NeEX" type="file" name="upload-btn" accept="video/mp4,video/x-m4v,video/*">
  </path></svg><div class="desc--1V2R7"><span class="btn--3RthP">点击上传 </span>或直接将视频文件拖入此区域</div><div class="desc--1V2R7"><span class="btn--3RthP">点击上传 </span>或直接将视频文件拖入此区域</div><div class="info-desc--3I4Id">为了更好的观看体验和平台安全，平台将对上传的视频预审。超过40秒的视频建议上传横版视频</div></div>
</label>

-  span
<span class="title" data-v-2e9dc210="">上传图文</span>

xpath=//span[contains(text(),'上传图文')]


- page.locator("xpath=//button[./span[text()='发布']]").click()

<button class="css-k3hpu2 css-osq2ks dyn publishBtn red" data-v-204325b9="">
<!----><!----><span class="btn-content">发布</span><!----></button

 ---drag-over多个匹配标签 不行
<div class="drag-over" data-v-3bc8d9fd="" data-v-6c433b79=""
<input class="upload-input" type="file" multiple="" accept=".jpg,.jpeg,.png,.webp" data-v-6c433b79="" data-v-3bc8d9fd-s="">
<div class="wrapper" data-v-6c433b79="" data-v-3bc8d9fd-s=""><span class="icon" data-v-6c433b79="" data-v-3bc8d9fd-s="">
</span><p data-v-6c433b79="" data-v-3bc8d9fd-s="">拖拽图片到此或点击上传</p>
<p class="info" data-v-6c433b79="" data-v-3bc8d9fd-s="">（最多支持上传18张）</p>
<div class="btn red" data-v-6c433b79="" data-v-3bc8d9fd-s="">上传图片</div>
</div>
</div>

    1) <div class="drag-over" data-v-3bc8d9fd="" data-v-6c43…>…</div> aka locator("div").filter(has_text="拖拽图片到此或点击上传（最多 支持上传18张）上传图片").nth(1)
    2) <div class="drag-over" data-v-3bc8d9fd="" data-v-0796…>…</div> aka locator("div").filter(has_text="拖拽图片到此或点击上传上传图 片").nth(1)
  
 page.locator('.drag-over').locator('nth=0').click()

4. 里面内容获取不到 到文件上传拖拽整个区域
   page.locator("css=.container--157qa").click()
    with page.expect_file_chooser() as fc_info:
            page.locator("css=.container--157qa").click()
            file_chooser = fc_info.value
            file_chooser.set_files(picture_path)

5. 无法通过文本，属性获取 通过xpath位置获取 

<div class="zone-container editor-kit-container editor editor-comp-publish notranslate chrome window chrome88" data-zone-id="0" data-zone-container="*" data-slate-editor="true" contenteditable="true" spellcheck="false" style="height: 97px;" data-placeholder="添加作品描述...">

//*[@id="root"]/div/div/div/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div/div/div[2]/div





### 002 
python+Selenium模拟登录报错:`InvalidCookieDomainException`



 selenium ertV- ERROR: Time is after notAfter
https://blog.csdn.net/qq_42236551/article/details/129050032


### 001 
Message: session not created: This version of ChromeDriver only supports Chrome version 114

chrome://version/
Google Chrome	116.0.5845.188 (正式版本)

https://chromedriver.chromium.org/downloads(no)

https://googlechromelabs.github.io/chrome-for-testing/#stable

### 0813

1. 测试整个项目 是否运行成功。如果 ok 说明ok了，如果不行 看看是是单独测试是可以 如果可以的。需要调整整个项目了 ok
2， main启动测试



### mac如何下载：

chrome://version/
Google Chrome	114.0.5735.198 (正式版本) (x86_64)

https://chromedriver.chromium.org/downloads

mac 非arm架构的

无法打开“chromedriver”，因为无法验证开发者。



### 提问13：Python实现将爱词霸每日一句定时推送至微信

https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login

https://www.cnblogs.com/connect/p/python-wechat-iciba.html
https://github.com/varlemon/wechat-iciba-everyday
https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html

{{content.DATA}}
{{note.DATA}}
{{translation.DATA}}

sys.path.append("../kernel")
from kernel import interface_db


### 提问12
https://github.com/littlecodersh/ItChat/issues/943
现在永的是Windows下的hook机制

### 提问11

    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.ElementClickInterceptedException: 
Message: element click intercepted: 
Element <span class="submit iget-common-c9  iget-common-b10 activeSubmit pointer">...</span> is not clickable at point (1089, 462). Other element would receive the click: <div class="yidun_popup__mask" style="opacity: 0.3;"></div>

selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element <span class="submit iget-common-c9  iget-common-b10 activeSubmit pointer">...</span> is not clickable at point (1089, 462). Other element would receive the click: <div class="yidun_popup__mask" style="opacity: 0.3;"></div>


https://blog.csdn.net/qq_43572758/article/details/104077186

解决方法：
 a = browser.find_element(By.CSS_SELECTOR, '.submit.iget-common-c9.iget-common-b10.activeSubmit.pointer')
browser.execute_script("arguments[0].click();", a)

### 提问10：
为什么python在urlencode空格的时候会被编码成“20”而不是“+”？


### css 知识 wanc 

<button type="button" data-disab="0" class="common-editorPostBtn-EDyd1">发布</button>

<button type="button" data-disab="0" class="common-editorPostBtn-EDyd1">发布</button>

### 了解想打包


三、安装依赖文件命令
pip install -r requirements.txt
pip freeze > requirements.txt

what：
Exception: You must install either cryptography or pycryptodome

pip install pycryptodome

https://pypi.org/project/pycryptodome/

### 掌握Selenium ActionChains用法 DONE
- https://www.cnblogs.com/yoyoketang/p/14124336.html
- js
- jquery
How Can We Type In Selenium Without Using sendKeys?
Using Javascript Executor

### done

what：
 Pyperclip could not find a copy/paste mechanism for your system.
 For more information, please visit https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error
 Connection unexpectedly closed: timed out

how：
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome('D:\\chromedriver.exe')
driver.get("http://www.example.com")
elem = driver.find_element_by_name('email')
ActionChains(driver).send_keys_to_element(elem, "abc@xyz.com").perform()


why
https://github.com/mandeep/Travis-Encrypt/issues/16

centos:
In order to work equally well on Windows, Mac, and Linux, Pyperclip uses various mechanisms to do this. Currently, this error should only appear on Linux (not Windows or Mac). You can fix this by installing one of the copy/paste mechanisms:
sudo apt-get install xsel to install the xsel utility.
sudo apt-get install xclip to install the xclip utility.
pip install gtk to install the gtk Python module.
pip install pyqt5 to install the PyQt4 Python modul
pip3 install pygtk
dnf install python3-gobject gtk3 
xclip
pip3 install pycairo
pip3 install PyGObject

python下有两个库可以实现这个功能：pyperclip 和 clipboard。
两个库都是跨平台的剪贴板操作库，目前都可用（2022年4月10日）。
只不过，clipboard库年久失修，只提供了两个函数：copy()、paste()

pyperclip 这个方式在centos 平台不行，换个方式\
yum install gtk3-devel
https://stackoverflow.com/questions/34106832/error-when-install-gtk-3-0-5-on-centos
上面方式也不行

https://www.testim.io/blog/selenium-sendkeys/

解决该问题了
how



### ChromeDriver was unable to send the emoji signal through send_keys() method

https://www.youtube.com/watch?v=FS4xa7z2fDI
https://stackoverflow.com/questions/25583641/set-value-of-input-instead-of-sendkeys-selenium-webdriver-nodejs

https://qavalidation.com/2021/01/execute-javascript-using-selenium-webdriver-in-python.html/


https://www.emojiall.com/zh-hans/code/1F917

 How to input "Hot dog" emoji using Python Selenium send_keys
https://github.com/SeleniumHQ/selenium/issues/3257

https://stackoverflow.com/questions/45330640/python-selenium-send-keys-emoji-support

https://github.com/SeleniumHQ/selenium/issues/3257
https://github.com/SeleniumHQ/selenium/issues/3257
Full Emoji List, v15.0
https://www.unicode.org/emoji/charts/full-emoji-list.html
### 启动报错 pass

selenium.common.exceptions.WebDriverException: 
Message: unknown error: ChromeDriver only supports characters in the BMP      
(Session info: chrome=114.0.5735.199)

分析：
查看方式：chromedriver --version 和  google-chrome --version 要是版本不一致引起的问题，可以重新安装成匹配的版本

chrome://version/
Google Chrome	114.0.5735.199 (正式版本) （64 位） (cohort: Stable)

https://chromedriver.chromium.org/downloads
ChromeDriver 114.0.5735.90
Supports Chrome version 114

pycharm 如下载requests
https://www.cnblogs.com/k4nz/p/14397322.html

//版本是正确的
https://stackoverflow.com/questions/59138825/chromedriver-only-supports-characters-in-the-bmp-error-while-sending-emoji-with%20 

https://9to5answer.com/chromedriver-only-supports-characters-in-the-bmp-error-while-sending-emoji-with-chromedriver-chrome-using-selenium-python-to-tkinter-39-s-label-textbox

### 写下面句子，要求 每个开头 添加emoji 



### Python- 如何import导入统级目录下的文件

https://zhuanlan.zhihu.com/p/64893308
 统计文件：

### 如何免费查询天气预报?done

高德地图天气 API 接入极简教程

​     https://lbs.amap.com/api/webservice/guide/api/weatherinfo



天气查询是一个简单的HTTP接口，根据用户输入的adcode，查询目标区域当前/未来的天气情况，数据来源是中国气象局。

使用API前您需先[申请Key](https://lbs.amap.com/dev/key/app)，若无高德地图API账号需要先申请账号。

## 使用说明

第一步，申请”web服务 API”密钥（Key）；

第二步，拼接HTTP请求URL，第一步申请的Key需作为必填参数一同发送；

第三步，接收HTTP请求返回的数据（JSON或XML格式），解析数据。

如无特殊声明，接口的输入参数和输出数据编码全部统一为UTF-8。

~~~
https://restapi.amap.com/v3/weather/weatherInfo?key=0a0bb34d7214a2caebb4cb2fe6471f9f&city=110105
~~~

https://lbs.amap.com/api/webservice/guide/tools/weather-code/

