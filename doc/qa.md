

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

