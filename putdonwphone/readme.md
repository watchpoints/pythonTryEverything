帮助自己远离手机，
就是让他人代替你完成手机上做的事情

# 支持平台

- 支持快手发布图文

# 功能

# 技术栈

- Chrome + ChromeDriver
- playwright

## 安装依赖
 
 pip3 install pyautogui
-

## 可能遇到问题

1. selenium 安装

chrome://version
 Google Chrome	120.0.6099.71

latest Chrome + ChromeDriver releases per release channel (Stable, Beta, Dev, Canary) are available 
 at the Chrome for Testing availability dashboard. 
 https://googlechromelabs.github.io/chrome-for-testing/


查看现有chromedriver版本
 win+r:打开cmd:输入 chromedriver --version 可查看chromedriver现版本
 ChromeDriver 117.0.5938.92
2. 如何通过文本获取内容
<div role="tab" aria-selected="true" class="ant-tabs-tab-btn" tabindex="0" id="rc-tabs-0-tab-2" aria-controls="rc-tabs-0-panel-2" data-immersive-translate-effect="1" data-immersive_translate_walked="b6fc5c97-b731-4509-9198-05c9c6c6a411">上传图文</div>


3.如果不上input按钮，如何上传图片 window 文件上传 selenium 无法自动选择文件？


-  对于 Linux 系统上的文件上传，Selenium 可能无法直接触发文件选择对话框。在这种情况下，
    可以考虑使用 pyautogui 等库，通过模拟键盘输入来实现文件上传。

- 在liunx 环境下    开启headless模式 Selenium 如何上传文件？ pyautogui  还能使用吗？

  https://stackoverflow.com/questions/39137476/is-it-possible-to-run-pyautogui-in-headless-mode
 https://abhishekvaid13.medium.com/pyautogui-headless-docker-mode-without-display-in-python-480480599fc4
 https://github.com/asweigart/pyautogui/issues/133

pyautogui 主要用于模拟鼠标和键盘输入，而不是直接与浏览器交互。在 headless 模式下，浏览器通常没有可见的图形界面，因此无法使用 pyautogui 模拟用户在图形界面上的交互。

无法解决--改为window



4. 点击编辑封面 有弹出一个页面  如何获取源码 如何selenium实现？


Is it possible to run PyAutoGUI in headless mode?

<button type="button" class="ant-btn ant-btn-primary"><span>发布</span></button>

<button type="button" class="ant-btn ant-btn-primary"><span>编辑封面</span></button>

Unable to run pyautogui scripts from remote headless server
https://github.com/asweigart/pyautogui/issues/87