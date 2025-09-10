# import os.path as osp
# from glob import glob
# import os
# import shutil


# root_path = "/data/nofar/material/liandongUgu/2025-06-10/frame/"
# target_dir1 = "zyw"
# target_dir2 = "yc"
# os.makedirs(target_dir1, exist_ok=True)
# os.makedirs(target_dir2, exist_ok=True)
# img_dirs = sorted(glob(osp.join(root_path, "*.jpg")))
# json_dirs = sorted(glob(osp.join(root_path, "*.json")))
# n = int(len(img_dirs)//2)

# for idx in range(len(img_dirs)):
#     if idx < n:
#         target_dir = target_dir1
#     else:
#         target_dir = target_dir2
#     shutil.copy(json_dirs[idx], target_dir)
#     shutil.copy(img_dirs[idx], target_dir)

# split jpgs and jsons average for everyone.

# import os
# import os.path as osp
# from glob import glob
# import shutil

# def split_and_copy_files(root_path, target_dirs):
#     """
#     将 root_path 中的 jpg 和 json 文件按顺序平均分配到多个目标目录中。

#     Args:
#         root_path (str): 原始文件目录，包含 .jpg 和 .json。
#         target_dirs (list): 目标目录完整路径列表，例如 ["/path/zyw", "/path/yc", "/path/aa"]。
#     """
#     os.makedirs(root_path, exist_ok=True)

#     img_files = sorted(glob(osp.join(root_path, "*.jpg")))
#     json_files = sorted(glob(osp.join(root_path, "*.json")))

#     assert len(img_files) == len(json_files), "图片和 JSON 文件数量不一致！"

#     total = len(img_files)
#     num_dirs = len(target_dirs)

#     # 创建目标目录
#     for dir_path in target_dirs:
#         os.makedirs(dir_path, exist_ok=True)

#     for idx in range(total):
#         dir_idx = idx * num_dirs // total
#         target_dir = target_dirs[dir_idx]
#         shutil.copy(img_files[idx], target_dir)
#         shutil.copy(json_files[idx], target_dir)

# # === 设置路径 ===
# root_path = "/data/nofar/material/liandongUgu/2025-06-26/frame"
# output_root = "/data/nofar/material/liandongUgu/2025-06-26/"
# target_dirs = [osp.join(output_root, name) for name in ["zyw", "yc"]]

# finish_dir1=os.makedirs(os.path.join(output_root,'zyw_finish'),exist_ok=True)
# finish_dir2=os.makedirs(os.path.join(output_root,'yc_finish'),exist_ok=True)
# split_and_copy_files(root_path, target_dirs)

#v2.0,加上了参数，可以通过python script.py /data/nofar/material/liandongUgu/2025-06-26/frame /data/nofar/material/liandongUgu/2025-06-26 zyw yc执行，会生成yc_finish等
import os
import os.path as osp
from glob import glob
import shutil
import sys

def split_and_copy_files(root_path, target_dirs):
    """
    将 root_path 中的图像（支持 jpg, jpeg, bmp, png）和 json 文件按顺序平均分配到多个目标目录中。
    
    Args:
        root_path (str): 原始文件目录，包含图像和 json。
        target_dirs (list): 目标目录完整路径列表，例如 ["/path/zyw", "/path/yc"]。
    """
    if not osp.exists(root_path):
        raise FileNotFoundError(f"原始路径不存在: {root_path}")

    # 支持多种图像格式
    image_extensions = ["*.jpg", "*.jpeg", "*.bmp", "*.png"]
    img_files = []
    for ext in image_extensions:
        img_files.extend(glob(osp.join(root_path, ext)))
    img_files = sorted(img_files)

    json_files = sorted(glob(osp.join(root_path, "*.json")))

    assert len(img_files) == len(json_files), f"图片（{len(img_files)}）和 JSON（{len(json_files)}）数量不一致！"

    total = len(img_files)
    num_dirs = len(target_dirs)

    # 创建目标目录
    for dir_path in target_dirs:
        os.makedirs(dir_path, exist_ok=True)

    # 平均分配
    for idx in range(total):
        dir_idx = idx * num_dirs // total
        target_dir = target_dirs[dir_idx]
        shutil.copy(img_files[idx], target_dir)
        shutil.copy(json_files[idx], target_dir)

def main():
    if len(sys.argv) < 4:
        print("用法: python script.py <root_path> <output_root> <target_dir1> [<target_dir2> ...]")
        sys.exit(1)

    root_path = sys.argv[1]
    output_root = sys.argv[2]
    dir_names = sys.argv[3:]

    target_dirs = [osp.join(output_root, name) for name in dir_names]

    # 可选：创建 *_finish 文件夹
    for name in dir_names:
        finish_dir = osp.join(output_root, f"{name}_finish")
        os.makedirs(finish_dir, exist_ok=True)

    split_and_copy_files(root_path, target_dirs)

if __name__ == "__main__":
    main()

