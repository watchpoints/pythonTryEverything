import os
import random

def get_random_jpg_files(target_dir, count=3):
    """
    随机获取指定目录下的 count 个 JPG 文件。
    
    :param dir_path: 目录路径。
    :param count: 要获取的文件数量，默认为 3。
    :return: 一个包含文件路径的列表。
    """
   # 获取目录下所有文件
    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]

    # 过滤出jpg文件
    jpg_files = [f for f in files if f.endswith('.jpg')]

    # 随机选择三个jpg文件
    random_jpg_files = random.sample(jpg_files, min(3, len(jpg_files)))
    
    # 返回完整的文件路径
    return [os.path.join(dir_path, f) for f in random_jpg_files]

# 使用示例
dir_path = r"D:\mp4\2024\01"  # 替换为你的目录路径
random_files = get_random_jpg_files(dir_path)
for file_path in random_files:
    print(file_path)
