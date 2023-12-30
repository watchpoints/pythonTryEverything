"""This module provides mp4"""
import os
import shutil
import platform
import logging
import subprocess
import traceback
from moviepy.editor import VideoFileClip,TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip


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

def create_big_to_small(input_dir:str,output_dir:str,bak_dir:str):
    """
        功能：
        输出：
        输出：
    """
    print(create_big_to_small)
    for root,_,files in os.walk(input_dir):
        for file in files:
            # 拼接路径
            file_path = os.path.join(root,file)
            try:
                if file.endswith('.mp4'):
                    print(file_path)
                    bak_file_name = os.path.basename(file_path)
                    bak_file_name_path =os.path.join(bak_dir, bak_file_name)
                    duration, file_size = get_video_properties(file_path)
                    if  duration > 30*60 or  file_size /1024/1024  > 250:
                        if split_video(file_path,output_dir,60*5):
                            print(file_path)
                            print("done split_video")
                            if not os.path.exists(bak_file_name_path):
                                shutil.move(file_path, bak_dir)
                    else:
                        print("less")
                        if not os.path.exists(bak_file_name_path):
                            shutil.move(file_path, output_dir)
            except Exception as myunkonw:
                print(f"处理视频文件时出错: {str(myunkonw)}")
                if not os.path.exists(bak_file_name_path):
                            shutil.move(file_path, output_dir)
    
    return True
                    
                     
def split_video(input_file, output_dir, duration):
    """
        功能：
        输出：
        输出：
    """
    try:
        file_name = os.path.basename(input_file)
        file_name_without_ext = os.path.splitext(file_name)[0]

        clip = VideoFileClip(input_file)
        # 获取视频的总时长（以秒为单位）
        total_duration = int(clip.duration)
        if duration > total_duration:
            print("less")
            return
        print(total_duration)
        # 计算分割的段数
        num_segments = total_duration // duration
        # # 创建水印字幕 255, 255, 255表示的是白色
        # watermark_clip = TextClip("个人学习", font="Arial", color="white", fontsize=26)
        # watermark_clip = watermark_clip.set_position('center').set_duration(duration/2)
        
        # 制作文字，指定文字大小和颜色
        #watermark_clip = ( TextClip("个人学习",fontsize=50,color='red')
        #     .set_position('center')#水印内容居中
        #     .set_duration(60) )#水印持续时间

    
        # 对视频进行分割并保存到指定路径
        for i in range(num_segments):
            start = i * duration
            end = start + duration
            print(start)
            print(end)
            segment = clip.subclip(start, end)
            #segment = CompositeVideoClip([segment, watermark_clip])
            # 指定保存的文件名
            filename = f'{file_name_without_ext}_{i + 1}.mp4'
            #ffmepg -codecs
            segment.write_videofile(os.path.join(output_dir, filename),fps=clip.fps, threads=16,preset='ultrafast',codec="libx264")
    except Exception as myunkonw:
        print(f"处理视频文件时出错: {str(myunkonw)}")
        print("使用 traceback 输出异常: {}".format(traceback.format_exc()))
        return False    
    return True

# def split_video(input_path, output_path, duration):
#     # 获取视频总时长
#     command = f'ffprobe -i {input_path} -show_streams -v 0 -of json "%%{stream_type%%}%%{duration%%}"'
#     res = subprocess.run(command, capture_output=True, text=True)
#     total_duration = float(res.stdout.strip())

#     # 计算分割的份数
#     num_parts = total_duration // duration
#     if total_duration % duration != 0:
#         num_parts += 1

#     # 开始执行分割命令
#     part_index = 1
#     for i in range(num_parts):
#         start_time = i * duration
#         end_time = start_time + duration
#         part_path = f'{output_path}/{input_path[:-4]}-{part_index:03d}-{start_time}-{end_time}.mp4'
#         command = f'ffmpeg -i {input_path} -c:v copy -c:a copy -ss {start_time} -to {end_time} {part_path}'
#         subprocess.run(command)
#         part_index += 1

def check_file_exist(folder_path):
    """ 目录下有文件存在 """
    file_list = os.listdir(folder_path)
    if file_list:
        return True
    return False
def get_video_properties(video_path):
    """
        功能：
        输出：
        输出：
    """
    try:
        clip = VideoFileClip(video_path)
        duration = clip.duration
        file_size = os.path.getsize(video_path)
        print(f"视频文件的时长为 {duration} 秒")
        print(f"视频文件的大小为 {file_size/1024/1204} M")
        return duration, file_size
    except Exception as myunkonw:
       print(f"发生异常：{myunkonw}")




        # # 获取文件大小，单位为字节
        # video_size = os.path.getsize(video_path)
        # # 转换为MB单位
        # video_size_mb = video_size /1024 / 1024
        # print('视频文件大小为：%.2f MB' % video_size_mb)

        # cmd = f"ffprobe -select_streams v:0 -print_format json -show_streams -i {video_path}"
        # # https://superuser.com/questions/841235/how-do-i-use-ffmpeg-to-get-the-video-resolution
        # print(cmd)
        # result = subprocess.run(cmd, capture_output=True, text=True,check=False)

        # # 获取命令执行结果
        # output = result.stdout
        # error = result.stderr

        # # 打印输出结果
        # print(output)
        # # 打印错误结果
        # print(error)    

def add_text_watermark(input_video, output_video, watermark_text):
    """ 添加水印 """
    print(input_video)
    print(output_video)
    command = [
        'ffmpeg',
        '-i', input_video,
        '-vf', f'drawtext=text={watermark_text}:fontsize=24:fontcolor=white:x=(w-text_w-10):y=10',
        '-c:a', 'copy',
        output_video
    ]
    print(command)
    result = subprocess.run(command, capture_output=True,  text=True, check=True)
        # 判断命令是否执行成功
    if result.returncode == 0:
        print("命令执行成功")
    else:
        print("命令执行失败，返回值为：", result.returncode, result)
        
    
def bath_add_water_to_mp4(input_path:str, out_path:str):
    """ 批量添加水印 """
    for root,_,files in os.walk(input_path):
        for file in files:
            # 拼接路径
            file_path = os.path.join(root,file)
            if file.endswith('.mp4'):
                print(file_path)
                file_name = os.path.basename(file_path)
                wather_new_path = os.path.join(out_path, file_name)
                logging.info(file_name)
                logging.info(wather_new_path)
                if add_watermark_subtitle(file_path, wather_new_path, "学习使用","bottom_right"):
                    print(f"{wather_new_path} ok ")
                else:
                     print(f"{wather_new_path} failed ")
               
def add_watermark_subtitle(intp_mp4_path:str, output_file:str,
                           watermark_text:str, watermark_position:str):
    """ 批量添加水印 """
    # 读取视频文件
    print(" >>>>>>>>>>>>>>>>>>>>>>>>add_watermark_subtitle >>" + intp_mp4_path)
    video_clip = VideoFileClip(intp_mp4_path)

    # 创建水印字幕 255, 255, 255表示的是白色
    watermark_clip = TextClip(watermark_text, font="Arial", color="white", fontsize=26)

    # 设置水印字幕位置
    # https://www.cnblogs.com/zhike/p/14477977.html
    if watermark_position == "top_right":
        #watermark_clip = watermark_clip.set_position((video_clip.w - watermark_clip.w, 0))
        # https://zulko.github.io/moviepy/ref/VideoClip/VideoClip.html?#moviepy.video.VideoClip.VideoClip.set_position
        watermark_clip = watermark_clip.set_position(("right", "top")).set_duration(video_clip.duration/4)
    elif watermark_position == "bottom_right":
        #watermark_clip = watermark_clip.set_position((0.4,0.7), relative=True).set_duration(video_clip.duration/4)
        watermark_clip = watermark_clip.set_position('center').set_duration(video_clip.duration/4)

    else:
        raise ValueError("Invalid watermark position. Valid positions are 'top_right' and 'bottom_right'.")
    # 将文本水印与视频合并
    watermarked_video = CompositeVideoClip([video_clip, watermark_clip])


    # 保存水印视频
    watermarked_video.write_videofile(output_file, codec="libx264")
    # Close the video clips
    video_clip.close()
    watermarked_video.close()

    return True
    
#####################################################################

def interface_mp4_to_post():
    """
        功能：
        输出：
        输出：
    """
    print("interface_mp4_to_post")
    if platform.system() == "Windows":
        print("Windows")
        input_dir = r'D:\mp4\input'
        output_dir = r'D:\mp4\output'
        bak_dir = r"D:\mp4\bak"
    else:
        input_dir = r'/root/mp4/input'
        output_dir = r'/root/mp4/output'
        bak_dir = r'/root/mp4/bak'
        
    ret = create_big_to_small(input_dir,output_dir,bak_dir)
    if ret :
        print("create_big_to_small done")
    else:
        print("create_big_to_small failed")
    
    
    

if __name__ == '__main__':
    interface_mp4_to_post()
    # input_path = r"D:\mp4\ENG SUB《仙逆》Renegade Immortal EP01-EP09 合集 Full Version ｜ 腾讯视频 - 动漫 [6EGJSh-uqWE].mp4"  # 输入视频文件路径
    # output_path = r"D:\mp4\33.mp4"  # 输出视频文件路径
    # pic_path =r"D:\mp4\db\万国志\p01.jpg"
    # start_time = "01:50:00"  # 开始剪辑的时间点，格式为 HH:MM:SS
    # end_time = "02:30:00"  # 结束剪辑的时间点，格式为 HH:MM:SS
    # #move_water_path = r"D:\mp4\db\万国志\noP01.mp4"
    # #cut_video(input_path,output_path,start_time,end_time)
    # #find_water(output_path,600,300,384,300)
    # #get_pic(output_path,pic_path)
    # #get_info(output_path)
    # #move_water(output_path,move_water_path)
 
 # 不同平台数据相互搬运
 