"""This module provides 习惯培养卡1"""
from datetime import datetime
import platform
import requests
import random
import os

class GetupHabit1:
    """This class provides a way to do something."""
    def __init__(self, save_picture_path: str, default_picture_path: str, get_up_path:str):
        self.save_picture_path = save_picture_path
        self.default_picture_path = default_picture_path
        self.get_up_path = get_up_path
        print("create GetupHabit")

    def get_weather(self):
        """定义通过城市获取天气信息的函数."""
        print(self.save_picture_path)
        url: str = 'https://restapi.amap.com/v3/weather/weatherInfo?parameters'
        params_estimate1 = {
            'key': '0a0bb34d7214a2caebb4cb2fe6471f9f',
            'city': '110105',
            'extensions': 'all'  # 获取预报天气
        }

        res = requests.get(url=url, params=params_estimate1)  # 预报天气
        # res2 = requests.get(url=url,params=params_realtime) # 实时天气
        data_json = res.json()
        province = data_json['forecasts'][0]["province"]  # 获取省份
        city = data_json.get('forecasts')[0].get("city")  # 获取城市
        adcode = data_json.get('forecasts')[0].get("adcode")  # 获取城市编码
        reporttime = data_json.get('forecasts')[0].get("reporttime")  # 获取发布数据时间
        date = data_json.get('forecasts')[0].get("casts")[0].get('date')  # 获取日期
        week = data_json.get('forecasts')[0].get("casts")[0].get('week')  # 获取星期几
        dayweather = data_json.get('forecasts')[0].get("casts")[0].get('dayweather')  # 白天天气现象
        #nightweather = data_json.get('forecasts')[0].get("casts")[0].get('nightweather')  # 晚上天气现象
        daytemp = data_json.get('forecasts')[0].get("casts")[0].get('daytemp')  # 白天温度
        nighttemp = data_json.get('forecasts')[0].get("casts")[0].get('nighttemp')  # 晚上温度
        #daywind = data_json.get('forecasts')[0].get("casts")[0].get('daywind')  # 白天风向
        daypower = data_json.get('forecasts')[0].get("casts")[0].get('daypower')  # 白天风力

        weather = ''
        weather += '👋:' + week + "\r\n"
        weather += '✅ 天气:' + dayweather + "\r\n"
        weather += '✅  温度:' + "低温 " + nighttemp + "℃ ~高温 " + daytemp + " ℃\r\n"
        weather += '✅ 风力:' + daypower + "级\r"
        return weather
    # 获取金山词霸每日一句
    def get_every_word(self):
        """
        目标养成计划
        """
        print(self.save_picture_path)
        return requests.get("https://open.iciba.com/dsapi/").json()

    def read_get_up_from_txt(self,path: str):
        """
        目标养成计划 emoji 表情作为目标的例子：

        """
        content = ""
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
        content += "🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉" + "\r\n"
        return content

    def down_picture(self, image_url: str):
        """
        目标养成计划
        """
        # 发送 GET 请求获取图片内容
        response = requests.get(image_url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 获取图片内容
            image_content = response.content
            # 保存图片到本地
            with open(self.save_picture_path, "wb") as file:
                file.write(image_content)
                print(f"Image downloaded and saved to {self.save_picture_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            self.save_picture_path = self.default_picture_path

    def interface_get_up(self):
        """
        目标养成计划
        """
        # Current date
        current_date = datetime.now()
        # Specific date (2023-12-10)
        target_date = datetime(2023, 12, 1)
        # Calculate the difference in days
        difference_in_days = (current_date - target_date).days

        temp_habit_name = "挑战早睡早起100天" + "第" + str(difference_in_days) + "天"
        data = self.get_every_word()
        title = "#挑战早睡早起100天" + "\r\n"
        title += data['content'] + "\r\n"
        title += data['note'] + "\r\n"
        print(str(data['fenxiang_img']))
        self.down_picture(data['fenxiang_img'])
        title += datetime.now().strftime('%Y-%m-%d') + "\r\n"
        weather = self.get_weather()
        title += weather + "\r\n"
        title += "\r\n"
        title += self.read_get_up_from_txt(self.get_up_path)
        return temp_habit_name,title

 
def interface_get_daily_englis_word():
    """
    获取每日英语单词

    Returns:
        tuple[str, str, Any]: 包含单词、释义和相关图片路径的元组
    Python Return Multiple Values  How to Return a Tuple, List, or Dictionary
    https://www.freecodecamp.org/news/python-returns-multiple-values-how-to-return-a-tuple-list-dictionary/
    """
    sys = platform.system()
    if sys == "Windows":
        save_picture_path = r"D:\mp4\etc\temp.png"
        default_picture_path = r"D:\mp4\etc\ZfCYoSG1BE_small.jpg"
        get_up_path = r"D:\mp4\etc\01_get_up.txt"
    elif sys == "Darwin":
        save_picture_path = r"/Users/wangchuanyi/mp4/etc/temp.png"
        default_picture_path = r"/Users/wangchuanyi/mp4/etc/ZfCYoSG1BE_small.jpg"
        get_up_path = r"/Users/wangchuanyi/mp4/etc/01_get_up.txt"
    else:
        save_picture_path = r"/root/code/python/putdonwphone/upload/temp.png"
        default_picture_path = r"/root/code/python/putdonwphone/upload/ZfCYoSG1BE_small.jpg"
        get_up_path = '/root/code/python/config/01_get_up.txt'

    getup = GetupHabit1(save_picture_path, default_picture_path, get_up_path) 
    temp_habit_name,temp_habit_detail = getup.interface_get_up()
    return getup.save_picture_path, temp_habit_name,temp_habit_detail
def interface_get_daily_englis_word_pic2():
    """
    interface_get_daily_englis_word_pic
    """
    sys = platform.system()
    if sys == "Windows":
        save_picture_path = r"D:\mp4\etc\temp.png"
        default_picture_path = r"D:\mp4\etc\ZfCYoSG1BE_small.jpg"
        get_up_path = r"D:\mp4\etc\01_get_up.txt"
        pic_path = r"D:\mp4\action_card"
    else:
        save_picture_path = r"/root/code/python/putdonwphone/upload/temp.png"
        default_picture_path = r"/root/code/python/putdonwphone/upload/ZfCYoSG1BE_small.jpg"
        get_up_path = '/root/code/python/config/01_get_up.txt'
        pic_path = r"D:\mp4\action_card"
    #temp_file_list = read_pic_rand_two(pic_path)
    return None,None,None
def interface_get_daily_englis_word_pic11():
    """
    interface_get_daily_englis_word_pic
    """
    sys = platform.system()
    if sys == "Windows":
        save_picture_path = r"D:\mp4\etc\temp.png"
        default_picture_path = r"D:\mp4\etc\ZfCYoSG1BE_small.jpg"
        get_up_path = r"D:\mp4\etc\01_get_up.txt"
        pic_path = r"D:\mp4\action_card"
    else:
        save_picture_path = r"/root/code/python/putdonwphone/upload/temp.png"
        default_picture_path = r"/root/code/python/putdonwphone/upload/ZfCYoSG1BE_small.jpg"
        get_up_path = '/root/code/python/config/01_get_up.txt'
        pic_path = r"D:\mp4\action_card"
    temp_file_list = read_pic_rand_two3(pic_path)
    getup = GetupHabit1(save_picture_path, default_picture_path, get_up_path)
    temp_file_list.append(getup.save_picture_path)
    temp_habit_name,temp_habit_detail = getup.interface_get_up()
    return temp_file_list, temp_habit_name,temp_habit_detail

def read_pic_rand_two3(input_path):
    """
    read_pic_rand_two
    """
    file_list = []
    count = 0
    while True:
        index = random.randint(0,73)
        print(index)
        name = str(index)  + ".jpg"
        temp_file_path = os.path.join(input_path, name)
        if not os.path.exists(temp_file_path):
            continue
        file_list.append(temp_file_path)
        # print("add" + temp_file_path)
        count += 1
        if 2 == count:
            break
    # print("read_pic_rand_two" + str(file_list))
    return file_list
if __name__ == '__main__':
    file_path_list, habit_name,habit_detail = interface_get_daily_englis_word_pic1()
    print("------------")
    print(file_path_list)
  
