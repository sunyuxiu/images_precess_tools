import os

# 根目录
root_dir = "/data/nofar/material/liandongUgu"
keyword = "smoke"

# 存放找到的路径
matched_paths = []

# 递归遍历
for dirpath, dirnames, filenames in os.walk(root_dir):
    # 检查文件夹名
    for dirname in dirnames:
        if keyword in dirname:
            matched_paths.append(os.path.join(dirpath, dirname))
    # 检查文件名
    for filename in filenames:
        if keyword in filename:
            matched_paths.append(os.path.join(dirpath, filename))

# 输出结果
for path in matched_paths:
    print(path)

print(f"共找到 {len(matched_paths)} 个包含 '{keyword}' 的文件或文件夹。")
