
import datetime

import requests
import json
import random


def get_every_word():
      # 获取金山词霸每日一句
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = ''
    day1 = r.json()['content']
    day2 = r.json()['note']
    content += day2  
    content += "\r\n"
    
    content += day1  
    content += "\r\n"
    return content
    
# 填入我们的格式化字符串中
def output_str(emoji_str,saying,city,wea_dict):
    # 获取日期
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # 格式化字符串
    format_str = "%s \npython every day\n %s \n————————————  \n |日期：%s \n |坐标： %s\n |天气： %s\n |温度：%s\n |风力：%s"
    # 解析天气信息
    wea_type = wea_dict['type']
    wind = wea_dict['fengli'].split('CDATA[')[1][:2]
    temp = wea_dict['low'] + '~' + wea_dict['high']
    out = format_str % (saying, date, city, wea_type, temp,wind)
    return out


def read_get_up_from_txt(path:str):
    content = ''
    content += "\r\n"
    # 获取金山词霸每日一句


    with open(path, encoding='UTF-8') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if len(line.strip()) == 0:
                continue
            if i % 3 == 0:
                #content += (line.strip() + " 😊") + "\r\n"
                content += (line.strip() ) + "\r\n"
            elif i % 3 == 1:
                 content += (line.strip() ) + "\r\n"
            else:
                content +=(line.strip() ) + "\r\n"
    content +=  "😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊" + "\r\n"
    print(content)
            
# 定义通过城市获取天气信息的函数
def get_weather(city):
    url = 'http://wthrcdn.etouch.cn/weather_mini?city='+city
    web = requests.get(url)
    wea_dict = json.loads(web.text)
    return wea_dict['data']['forecast'][0]
        
def get_up_everyday():
    
    """
    描述:
        自动获取当前地理位置，天气，以及名人名言
        输出每日一句
    参数:
    
    生活的道路一旦选定，就要勇敢地走到底，决不回头。
    ————————————
    |日期：2021-03-20
    |坐标： 北京
    |天气： 晴
    |温度：低温 2℃~高温 15℃
    |风力：3级
    
    """
    #saying =  read_get_up_from_txt(r"D:\golang\money\src\github.com\watchpoints\pythonTryEverything\config\01_get_up.txt")
    myday ="日期: "
    myday += datetime.datetime.now().strftime('%Y-%m-%d') + "\r\n"
    myday +="坐标：北京 "
    myday +="\r\n"
    myday +="早安："
    
    
    saying =  get_every_word()
    myday += saying  + "\r\n"
    print(saying)
    wea_dict= get_weather('北京')
    print(wea_dict)
    # 免费的天气预报接口 https://zhuanlan.zhihu.com/p/540939924
    #out = output_str(saying,'北京',wea_dict)
    print(myday)
    return myday
   
    
    

if __name__ == '__main__':
    get_up_everyday()