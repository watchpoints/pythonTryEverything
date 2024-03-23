"""This module provides 习惯培养卡"""
from datetime import datetime
import platform
import requests



class GetupHabit:
    """This class provides a way to do something."""
    def __init__(self,input_path:str):
        self.input_path = input_path
        print("create GetupHabit")

    def get_txt_content(self):
        """
        目标养成计划 emoji 表情作为目标的例子：

        """
        content = ""
        # 遍历目录下的所有文件  
        for filename in os.listdir(self.input_path):  
            if filename.endswith('.txt'):  # 确保只读取txt文件  
                # 打开文件并读取内容  
                with open(os.path.join(directory, filename), encoding='UTF-8','r') as file:  
                    lines = file.readlines()  # 按行读取文件内容  
                    for line in lines:  
                        content += (line.strip()) + "\r\n"
        content += "🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉" + "\r\n"
        
        return content
        
    def get_content(self):
        """
        目标养成计划
        """
        #第几天
        difference_in_days = (datetime.now() - datetime(2023, 12, 1)).days

        temp_habit_name = "#日拱一卒" + "第" + str(difference_in_days) + "天"
        txt_content = self.get_txt_content(self.input_path)
        return temp_habit_name,data

 
def interface_read_note(input_path):
    """
    获取每日英语单词

    Returns:
        tuple[str, str, Any]: 包含单词、释义和相关图片路径的元组
    Python Return Multiple Values  How to Return a Tuple, List, or Dictionary
    https://www.freecodecamp.org/news/python-returns-multiple-values-how-to-return-a-tuple-list-dictionary/
    """
    sys = platform.system()
    mynote = DailyNote(input_path) 
    temp_habit_name,temp_habit_detail = mynote.get_content()
    return getup.save_picture_path, temp_habit_name,temp_habit_detail

if __name__ == '__main__':
    input_path = r"D:\mp4\dail_note"
    habit_name,habit_detail = interface_read_note(input_path)
    print(habit_name)
    print(habit_detail)
