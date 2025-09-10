import os
import json

# 设置 JSON 文件所在目录
json_dir = r"D:\datasets\datasets_check\OBB\part2backup"  # 替换为你的实际路径

# 1750238406721_143.json

# 前胜桃酥

# 用于保存匹配到的文件名
matched_files = []

# 遍历目录下所有 JSON 文件
for filename in os.listdir(json_dir):
    if filename.endswith(".json"):
        file_path = os.path.join(json_dir, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for shape in data.get("shapes", []):
                    if shape.get("label") == "d":
                        matched_files.append(filename)
                        break  # 找到一个就可以停止这个文件的查找
        except Exception as e:
            print(f"读取出错: {file_path}, 错误: {e}")

# 输出所有包含 label="d" 的 JSON 文件
print("包含 label='d' 的文件有：")
for f in matched_files:
    print(f)
