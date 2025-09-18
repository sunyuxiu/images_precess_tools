# # python filter_low_score.py input output score
# import os
# import sys
# import json
# import shutil
# from glob import glob

# def ensure_dir(path):
#     if not os.path.exists(path):
#         os.makedirs(path)

# def should_copy(json_path, threshold=0.75):
#     with open(json_path, 'r', encoding='utf-8') as f:
#         try:
#             data = json.load(f)
#         except json.JSONDecodeError:
#             print(f"[ERROR] Invalid JSON: {json_path}")
#             return False

#         shapes = data.get("shapes", [])

#         # 空标注，直接复制
#         if not shapes:
#             print(f"[INFO] Empty shapes, copying: {json_path}")
#             return True

#         # 检查是否有任何一个 score 小于阈值
#         for shape in shapes:
#             score = shape.get("score")
#             if score is not None:
#                 if score < threshold:
#                     print(f"[INFO] Low score {score:.4f} found in: {json_path}")
#                     return True

#     return False

# def find_image(base_path):
#     # 尝试不同的图片后缀
#     for ext in [".jpg", ".JPG", ".jpeg", ".JPEG"]:
#         img_path = base_path + ext
#         if os.path.exists(img_path):
#             return img_path
#     return None

# def main(src_dir, dst_dir, threshold):
#     ensure_dir(dst_dir)
#     json_files = glob(os.path.join(src_dir, "*.json"))
#     count = 0

#     for json_file in json_files:
#         if should_copy(json_file, threshold):
#             base_name = os.path.splitext(os.path.basename(json_file))[0]
#             img_path = find_image(os.path.join(src_dir, base_name))

#             # 复制 JSON
#             shutil.copy(json_file, os.path.join(dst_dir, os.path.basename(json_file)))
#             print(f"[COPY] JSON: {json_file}")

#             # 复制图片
#             if img_path:
#                 shutil.copy(img_path, os.path.join(dst_dir, os.path.basename(img_path)))
#                 print(f"[COPY] IMG:  {img_path}")
#             else:
#                 print(f"[WARN] Image not found for: {base_name}")

#             count += 1

#     print(f"\n✅ Done. Total files copied (json+image pairs): {count}")

# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print("Usage: python filter_low_score.py <source_dir> <target_dir> <score_threshold>")
#         sys.exit(1)

#     source_dir = sys.argv[1]
#     target_dir = sys.argv[2]
    
#     try:
#         score_threshold = float(sys.argv[3])
#     except ValueError:
#         print("[ERROR] <score_threshold> must be a float, e.g., 0.75")
#         sys.exit(1)

#     main(source_dir, target_dir, score_threshold)

import os
import json
import shutil
import sys

def move_files(source_dir, target_dir, score_threshold):
    os.makedirs(target_dir, exist_ok=True)

    # 遍历 source_dir 下所有文件，包括子文件夹
    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            if not filename.endswith(".json"):
                continue

            json_path = os.path.join(root, filename)
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"无法读取 {json_path}: {e}")
                continue

            if not data.get("shapes"):
                print(f"{filename} 是空白 JSON,跳过")
                continue
            for shape in data.get("shapes", []):
                try:
                    score = float(shape.get("score", 0))
                except:
                    score = 0
                print(f"{filename} score={score}")

            move_flag = any(shape.get("score", 0) > score_threshold for shape in data["shapes"])
            print(f"{filename} move_flag={move_flag}")

            if move_flag:
                # 计算目标路径（保持文件名不变）
                target_json_path = os.path.join(target_dir, filename)
                shutil.move(json_path, target_json_path)
                print(f"移动 JSON: {json_path} -> {target_json_path}")

                # 移动对应 JPG
                jpg_name = data.get("imagePath")
                if jpg_name:
                    jpg_path = os.path.join(root, jpg_name)
                    if os.path.exists(jpg_path):
                        target_jpg_path = os.path.join(target_dir, jpg_name)
                        shutil.move(jpg_path, target_jpg_path)
                        print(f"移动 JPG: {jpg_path} -> {target_jpg_path}")
                    else:
                        print(f"对应 JPG 不存在: {jpg_path}")

def main():
    if len(sys.argv) != 4:
        print("用法: python move_highscore.py <source_dir> <target_dir> <score_threshold>,score_threshold是小数,比如0.7")
        sys.exit(1)

    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    try:
        score_threshold = float(sys.argv[3])
    except ValueError:
        print("score_threshold 必须是数字")
        sys.exit(1)

    move_files(source_dir, target_dir, score_threshold)
    print("处理完成！")

if __name__ == "__main__":
    main()
