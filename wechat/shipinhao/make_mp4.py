#!/usr/bin/python
# -*-coding:utf-8 -*-
import time
import os
import math
import subprocess


def cut_video(input_path, output_path, header_time_str, footer_time_str):
    
    #todo 片头长度
    header_time=header_time_str.split(":")
    header_time=int(header_time[0])*3600+int(header_time[1])*60+int(header_time[2])
    print ("header_time",header_time)
    
    #todo 片尾长度
    footer_time=footer_time_str.split(":")
    footer_time=int(footer_time[0])*3600+int(footer_time[1])*60+int(footer_time[2])
    print ("footer_time",footer_time)
    
    # 构建 ffmpeg 命令
    command = [
        "ffmpeg",
        "-i", input_path,
        "-ss", header_time_str,
        "-to", footer_time_str,
        "-vcodec", "copy",
        "-acodec", "copy",
        output_path
    ]

    # 执行 ffmpeg 命令
    subprocess.run(command, check=True)
    
    

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
  # 
  # ffmpeg -i test.mp4 -ss 1 -f image2 -vframes 1 out.jpg
if __name__ == '__main__':
   
    input_path = r"D:\mp4\db\万国志\[P11]11 兵无常势水无常形.mp4"  # 输入视频文件路径
    output_path = r"D:\mp4\db\万国志\P11.mp4"  # 输出视频文件路径
    pic_path =r"D:\mp4\db\万国志\p01.jpg"
    start_time = "00:03:18"  # 开始剪辑的时间点，格式为 HH:MM:SS
    end_time = "00:18:22"  # 结束剪辑的时间点，格式为 HH:MM:SS
    move_water_path = r"D:\mp4\db\万国志\noP01.mp4"
    cut_video(input_path,output_path,start_time,end_time)
    #find_water(output_path,600,300,384,300)
    #get_pic(output_path,pic_path)
    #get_info(output_path)
    #move_water(output_path,move_water_path)
 