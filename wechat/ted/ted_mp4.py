#!/usr/bin/python
# -*-coding:utf-8 -*-
import time
import os
import math
import subprocess


def ted_to_mp4(mp4_path,mp3_path,english_subtitle_path,chine_subtitle_path,out_path):
    
     #cmd = "ffmpeg -i {}  -i {} -c:a copy  -c:v copy -vf 'subtitles={}, {}'  {} " \
     #      .format(mp4_path,mp3_path,english_subtitle_path, chine_subtitle_path, out_path)
           
     cmd = "ffmpeg -i {}  -i {} -vcodec copy -acodec copy   {} " \
              .format(mp4_path,mp3_path, out_path)
     print(cmd)
     os.system(cmd)
     

def add_text_watermark(input_video, output_video, watermark_text):
    command = [
        'ffmpeg',
        '-i', input_video,
        '-vf', f'drawtext=text={watermark_text}:fontsize=24:fontcolor=white:x=(w-text_w-10):y=10',
        '-c:a', 'copy',
        output_video
    ]

    subprocess.run(command)
    
def add_english_subtitles(input_video, english_subtitles, output_video):
    cmdLine = 'ffmpeg -i {} -vf subtitles={} -y {} '.format(input_video,english_subtitles, output_video)
    subprocess.call(cmdLine, shell=True)
    
    
if __name__ == '__main__':
   
    mp4_path = r"D:\mp4\english\p1.mp4"  # 输入视频文件路径
    mp3_path = r"D:\mp4\english\p1.mp3"  # 输出视频文件路径
    english_subtitle_path = "english.srt"
    chine_subtitle_path = r"D:\mp4\english\chine.srt"
    out_path = r"D:\mp4\english\为什么快乐是健康生活的秘诀.mp4"
    rst_out_path = r"D:\mp4\english\rst.mp4"
    ted_to_mp4(mp4_path,mp3_path,english_subtitle_path,chine_subtitle_path,out_path)
    #add_text_watermark(out_path,rst_out_path,"个人学习使用")
    #add_english_subtitles(rst_out_path,english_subtitle_path, out_path)
  
 #fffmpeg -i p1.mp4  -i p1.mp3  -c copy -c:s mov_text  -vf subtitles=english.srt  drawtext=text=only learn:fontsize=24:fontcolor=white:x=(w-text_w-10):y=10 -y 11.mp4
 
 
 
 # ffmpeg -i p1.mp4  -i p1.mp3 -vf "drawtext=text='个人学习使用':fontsize=24:fontcolor=white:x=(w-text_w-10):y=10,subtitles=english.srt" -c:a copy   333.mp4

