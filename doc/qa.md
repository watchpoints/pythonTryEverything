
### ChromeDriver was unable to send the emoji signal through send_keys() method

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

