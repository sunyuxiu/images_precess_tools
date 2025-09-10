import os
import shutil
from glob import glob

# 顶层路径
base_dir = "/data/nofar/material/liandongUgu/"

# 目标路径
dest_dir = "/data/nofar/all_facility_mp4/"
os.makedirs(dest_dir, exist_ok=True)

# 找到所有 facility 文件夹
facility_dirs = glob(os.path.join(base_dir, "*/facility/"))

for src in facility_dirs:
    for root, dirs, files in os.walk(src):
        for file in files:
            if file.lower().endswith(".mp4"):
                src_file = os.path.join(root, file)
                
                # 计算相对于根路径的完整路径
                rel_path = os.path.relpath(src_file, "/")  # 相对于根路径
                
                # 构建目标路径
                dest_file = os.path.join(dest_dir, rel_path)
                dest_folder = os.path.dirname(dest_file)
                os.makedirs(dest_folder, exist_ok=True)
                
                shutil.copy2(src_file, dest_file)

print("所有 mp4 文件已复制完成，且保留原始目录结构！")
