"""This module provides mp4"""
import os
import platform
import logging
import subprocess
import traceback
import time




def trim_video(input_file, output_file, start_time, end_time):
    command = "ffmpeg -i {} -ss {} -to {}  -c copy  -y  {}".format(input_file,start_time,end_time,output_file)
    print(command)
    #command = ['ffmpeg', '-i', input_file, '-ss', start_time, '-to', end_time, '-c', 'copy','-y',output_file]
    subprocess.run(command)

def trim_and_encode_video(input_file, output_file, start_time, end_time):
    command = ['ffmpeg', '-ss', start_time, '-i', input_file, '-to', end_time, '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', output_file]
    subprocess.run(command)
    

# 获取一个图片
def get_pic(mp4_path, pic_path):
    cmd = "ffmpeg  -i  {} -ss 11 -f image2 -vframes 1 {}".format(mp4_path,pic_path)
    os.system(cmd)
# 3750 267 424 184
# https://zhuanlan.zhihu.com/p/145592911
def move_water(input_path,output_path):
    
     cmd = "ffmpeg -i {} -c:a copy -vf delogo=x=3250:y=500:w=437:h=158:show=0 {}".format(input_path,output_path)
     print(cmd)
     os.system(cmd)
     
def get_info(input_path):
     cmd = "ffprobe -print_format json -show_streams -i {}".format(input_path)
     print(cmd)
     os.system(cmd)


    
    

if __name__ == '__main__':
    input_path = r"D:\mp4\input\2.mp4"  # 输入视频文件路径
    output_path = r"D:\mp4\input\23.mp4"  # 输出视频文件路径
    pic_path =r"D:\mp4\db\万国志\p01.jpg"
    start_time = "00:36:11"  # 开始剪辑的时间点，格式为 HH:MM:SS
    end_time = "00:47:18"  # 结束剪辑的时间点，格式为 HH:MM:SS
    trim_video(input_path,output_path,start_time,end_time)
