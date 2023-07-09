import datetime
import requests
import traceback
import platform
# 获取发表内容
from kernel import mymonitor


def DailyGetUpEvent():
    task = ''
    try:
        task = get_up_everyday()
    except Exception as e:
        print(e)
        traceback.print_exc()
        mymonitor.sendEmail("DailyGetUpEvent failed")
    return task


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
def output_str(emoji_str, saying, city, wea_dict):
    # 获取日期
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # 格式化字符串
    format_str = "%s \npython every day\n %s \n————————————  \n |日期：%s \n |坐标： %s\n |天气： %s\n |温度：%s\n |风力：%s"
    # 解析天气信息
    wea_type = wea_dict['type']
    wind = wea_dict['fengli'].split('CDATA[')[1][:2]
    temp = wea_dict['low'] + '~' + wea_dict['high']
    out = format_str % (saying, date, city, wea_type, temp, wind)
    return out


def read_get_up_from_txt(path: str):
    content = ''
    content += "\r\n"
    # 获取金山词霸每日一句

    with open(path, encoding='UTF-8') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if len(line.strip()) == 0:
                continue
            if i % 3 == 0:
                # content += (line.strip() + " 😊") + "\r\n"
                content += (line.strip()) + "\r\n"
            elif i % 3 == 1:
                content += (line.strip()) + "\r\n"
            else:
                content += (line.strip()) + "\r\n"
    # content += "😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊😊" + "\r\n"
    return content


# 定义通过城市获取天气信息的函数
def get_weather():
    url = 'https://restapi.amap.com/v3/weather/weatherInfo?parameters'
    # params_realtime = {
    #     'key':'0a0bb34d7214a2caebb4cb2fe6471f9f',
    #     'city':'110105', # 从城市编码里获取的a丢包code
    #     'extensions':'base' # 获取实时天气
    # }
    params_estimate = {
        'key': '0a0bb34d7214a2caebb4cb2fe6471f9f',
        'city': '110105',
        'extensions': 'all'  # 获取预报天气
    }

    res = requests.get(url=url, params=params_estimate)  # 预报天气
    # res2 = requests.get(url=url,params=params_realtime) # 实时天气
    tianqi = res.json()
    # print(tianqi)
    # tianqi2 = res2.json()
    # print(tianqi2)

    # print(tianqi.get('forecasts'))
    # province = tianqi.get('forecasts')[0].get("province") # 获取省份
    province = tianqi['forecasts'][0]["province"]  # 获取省份
    city = tianqi.get('forecasts')[0].get("city")  # 获取城市
    adcode = tianqi.get('forecasts')[0].get("adcode")  # 获取城市编码
    reporttime = tianqi.get('forecasts')[0].get("reporttime")  # 获取发布数据时间
    date = tianqi.get('forecasts')[0].get("casts")[0].get('date')  # 获取日期
    week = tianqi.get('forecasts')[0].get("casts")[0].get('week')  # 获取星期几
    dayweather = tianqi.get('forecasts')[0].get("casts")[0].get('dayweather')  # 白天天气现象
    nightweather = tianqi.get('forecasts')[0].get("casts")[0].get('nightweather')  # 晚上天气现象
    daytemp = tianqi.get('forecasts')[0].get("casts")[0].get('daytemp')  # 白天温度
    nighttemp = tianqi.get('forecasts')[0].get("casts")[0].get('nighttemp')  # 晚上温度
    daywind = tianqi.get('forecasts')[0].get("casts")[0].get('daywind')  # 白天风向
    nightwind = tianqi.get('forecasts')[0].get("casts")[0].get('nightwind')  # 晚上风向
    daypower = tianqi.get('forecasts')[0].get("casts")[0].get('daypower')  # 白天风力
    nightpower = tianqi.get('forecasts')[0].get("casts")[0].get('nightpower')  # 晚上风力

    # print("省份:",province)
    # print("城市:",city)
    # print("城市编码:",adcode)
    # print("发布数据时间:",reporttime)
    # print("日期:",reporttime)
    # print("星期:",week)
    # print("白天天气现象:",dayweather)
    # print("晚上天气现象:",nightweather)
    # print("白天温度:",daytemp)
    # print("晚上温度:",nighttemp)
    # print("白天风向:",daywind)
    # print("晚上风向:",nightwind)
    # print("白天风力:",daypower)
    # print("晚上风力:",nightpower)

    weather = ''
    weather += '✅ 天气:' + dayweather + "\r\n"
    weather += '✅  温度:' + "低温 " + nighttemp + "℃ ~高温 " + daytemp + " ℃\r\n"
    weather += '✅ 风力:' + daypower + "级\r"
    return weather


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
    path = ''
    sys = platform.system()
    if sys == "Windows":
        path = r"D:\golang\money\src\github.com\watchpoints\pythonTryEverything\config\01_get_up.txt"
    else:
        path = '/root/code/python/config/01_get_up.txt'
    # https://www.emojiall.com/zh-hans
    myday = '✅日期:'
    myday += datetime.datetime.now().strftime('%Y-%m-%d') + "\r\n"
    myday += "✅坐标：北京 "
    myday += "\r\n"
    weather = get_weather()
    myday += weather + "\r\n"
    myday += "✅ 早安提醒："
    saying = get_every_word()
    myday += saying + "\r"
    myday += "✅ 日课:" + "\r"
    task = read_get_up_from_txt(path)
    myday += str(task)
    print(myday)

    return myday


if __name__ == '__main__':
    get_up_everyday()
