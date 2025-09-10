import os
import json

def find_rotation_jsons(directory):
    rotation_json_files = []

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for shape in data.get("shapes", []):
                        if shape.get("shape_type") == "rotation":
                            rotation_json_files.append(filename)
                            break  # 找到一个即可跳出
            except Exception as e:
                print(f"Failed to parse {filename}: {e}")

    return rotation_json_files

# 示例用法
json_directory = r"D:\datasets\datasets_check\images"  # 替换为你的路径
rotation_files = find_rotation_jsons(json_directory)

print("包含 rotation 的 JSON 文件:")
for file in rotation_files:
    print(file)



