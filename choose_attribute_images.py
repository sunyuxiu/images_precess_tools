# # v1.0
# import os
# import shutil
# import json

# # 设置参数路径 后面可以直接从labeled_data里面找，避免重复复制
# # json_dir = "/data/nofar/person_attribute/person_attribute_v0.1.4/images"
# # xml_dir = "/data/nofar/person_attribute/person_attribute_v0.1.4/Annotations"
# # save_dir = "/data/nofar/person_attribute/0630/images/"
# # xml_save_dir = "/data/nofar/person_attribute/0630/Annotations"

# json_dir = "/home/lorenzo/test_chunk/labeling/chunk_0003"
# # xml_dir = "/data/nofar/person_attribute/person_attribute_v0.2.6/Annotations"
# save_dir = "/home/lorenzo/test_chunk/labeling/no_label"
# # xml_save_dir = "/data/nofar/person_attribute/sleep/Annotations"
# # shutil.copy('')

# # 需要筛选的标签
# target_labels = {"nomask", "nowf","fall","sleep","tx","wsf"}
# target_labels2 = {"fire", "smoke"}
# target_labels3 = {"person"}
# target_labels4 = {"sleep"}
# target_labels5 = {"no"}

# # 创建目标文件夹（如果不存在）
# os.makedirs(save_dir, exist_ok=True)
# # os.makedirs(xml_save_dir, exist_ok=True)

# # 遍历所有json文件
# for filename in os.listdir(json_dir):
#     if not filename.endswith(".json"):
#         continue

#     json_path = os.path.join(json_dir, filename)

#     # 解析json
#     with open(json_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)

#     # 检查是否有目标label
#     labels = [shape.get("label", "") for shape in data.get("shapes", [])]
#     if any(label in target_labels5 for label in labels):
#         # 拷贝json
#         shutil.move(json_path, os.path.join(save_dir, filename))

#         # 拷贝对应图片
#         base_name = os.path.splitext(filename)[0]
#         found_image = False
#         for ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
#             image_path = os.path.join(json_dir, base_name + ext)
#             if os.path.exists(image_path):
#                 shutil.move(image_path, os.path.join(save_dir, base_name + ext))
#                 found_image = True
#                 break
#         if not found_image:
#             print(f"[警告] 找不到图片文件: {base_name}")

#         # 拷贝对应xml
#         # xml_path = os.path.join(xml_dir, base_name + ".xml")
#         # if os.path.exists(xml_path):
#         #     shutil.copy(xml_path, os.path.join(xml_save_dir, base_name + ".xml"))
#         # else:
#         #     print(f"[警告] 找不到xml文件: {base_name}.xml")


# v2.0 传入参数 python filter_json.py no /home/lorenzo/test_chunk/labeling/chunk_0003 /home/lorenzo/test_chunk/labeling/no_label

import os
import shutil
import json
import sys

def main():
    if len(sys.argv) != 4:
        print("用法: python filter_json.py <label> <json_dir> <save_dir>")
        sys.exit(1)

    target_label = sys.argv[1]  # e.g., "no"
    json_dir = sys.argv[2]
    save_dir = sys.argv[3]

    # 检查路径是否存在
    if not os.path.isdir(json_dir):
        print(f"[错误] 输入目录不存在: {json_dir}")
        sys.exit(1)

    os.makedirs(save_dir, exist_ok=True)

    # 遍历所有json文件
    for filename in os.listdir(json_dir):
        if not filename.endswith(".json"):
            continue

        json_path = os.path.join(json_dir, filename)

        # 解析json
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"[错误] 解析 JSON 文件失败: {json_path}, 错误: {e}")
            continue

        # 检查是否有目标label
        labels = [shape.get("label", "") for shape in data.get("shapes", [])]
        if any(label == target_label for label in labels):
            # 移动json
            shutil.move(json_path, os.path.join(save_dir, filename))

            # 移动对应图片
            base_name = os.path.splitext(filename)[0]
            found_image = False
            for ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
                image_path = os.path.join(json_dir, base_name + ext)
                if os.path.exists(image_path):
                    shutil.move(image_path, os.path.join(save_dir, base_name + ext))
                    found_image = True
                    break
            if not found_image:
                print(f"[警告] 找不到图片文件: {base_name}")

if __name__ == "__main__":
    main()

