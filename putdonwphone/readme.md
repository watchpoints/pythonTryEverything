帮助自己远离手机，
就是让他人代替你完成手机上做的事情



# 需求调研

## 第一步：搜集资料，写逐字稿 

## 第二步：优化





### 对视频进行处理

- 视频处理流程
   
   分割：大小限制 

   文字水印：版权限制



## 第三步：自动上传

### 图文支持平台
- 快手
- 小红书
- douyin
- 头条号
- 知乎 [UserAgent]

- 不支持：百家号 界面太花哨--个人反感 不作 一次需要传输多个图片 反人类 浪费太多时间 终止 
- 不支持 公众号  做了一层封装 太麻烦来了 不执行 浪费太多时间 终止 

### mp4
- shipinhao  可视化可用


# 技术栈

- Chrome + ChromeDriver
- playwright

- Pylint extension for Visual Studio Code

-  MoviePy是一个用于视频编辑的Python模块， [太慢 舍去]
   它可被用于一些基本操作（如剪切、拼接、插入标题）、视频合成（即非线性编辑）、视频处理和创建高级特效。
   它可对大多数常见视频格式进行读写，包括GIF。
  https://github.com/Zulko/moviepy
  https://moviepy.readthedocs.io/en

opencv
opencv也是我们最常用的视频读写库，但是opencv很明显，不太适合简单的视频剪辑，而更适合视频处理的用户，比如完成运动目标检测，运动目标跟踪等等。


## 安装依赖

### https://imagemagick.org/script/download.php#google_vignette
   D:\tools\python3\Lib\site-packages\moviepy
   pip3 install moviep
   




### vscode +python 
  https://stackoverflow.com/questions/68832892/why-cant-i-import-requests-in-vs-code

 Type python intepreter in the command palette and select it.

 - pylint


playwright -V
Version 1.31.1
python -m playwright install
playwright 默认会下载 chromium,firefox 和 webkit 三个浏览器

- playwright install --force chrome
ERROR: cannot install on centos distribution - only Ubuntu is supported



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


