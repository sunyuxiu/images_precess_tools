# import os
# import sys
# import random
# import shutil

# def main(input_dir, output_dir, percent):
#     # 支持的图片后缀
#     img_exts = [".jpg", ".jpeg", ".png", ".bmp"]

#     # 创建输出目录
#     os.makedirs(output_dir, exist_ok=True)

#     # 获取所有图片文件
#     all_imgs = [f for f in os.listdir(input_dir) if os.path.splitext(f)[1].lower() in img_exts]

#     if not all_imgs:
#         print("❌ 输入目录下没有找到任何图片！")
#         return

#     # 随机挑选 percent%
#     num_to_select = max(1, int(len(all_imgs) * percent / 100))
#     selected_imgs = random.sample(all_imgs, num_to_select)

#     print(f"总共 {len(all_imgs)} 张图片，随机挑选 {num_to_select} 张 ({percent}%)。")

#     for img_file in selected_imgs:
#         img_path = os.path.join(input_dir, img_file)
#         shutil.copy(img_path, output_dir)

#         # 找对应的 JSON 文件（假设 json 和图片同名）
#         json_file = os.path.splitext(img_file)[0] + ".json"
#         json_path = os.path.join(input_dir, json_file)
#         if os.path.exists(json_path):
#             shutil.copy(json_path, output_dir)
#         else:
#             print(f"⚠️ 没找到对应的 JSON: {json_file}")

# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print("用法: python xxx.py <input_dir> <output_dir> <percent>")
#         sys.exit(1)

#     input_dir = sys.argv[1]
#     output_dir = sys.argv[2]
#     percent = float(sys.argv[3])  # 可以输入 10 或 10.5

#     main(input_dir, output_dir, percent)



import os
import sys
import shutil

def main(input_dir, output_dir, percent):
    img_exts = [".jpg", ".jpeg", ".png"]  # 只保留 jpg 和 png
    os.makedirs(output_dir, exist_ok=True)

    # 获取所有图片并排序（保证顺序稳定）
    all_imgs = sorted([f for f in os.listdir(input_dir) if os.path.splitext(f)[1].lower() in img_exts])

    if not all_imgs:
        print("❌ 输入目录下没有找到任何 jpg/png 图片！")
        return

    num_to_select = max(1, int(len(all_imgs) * percent / 100))
    selected_imgs = all_imgs[:num_to_select]

    print(f"总共 {len(all_imgs)} 张图片，顺序挑选 {num_to_select} 张 ({percent}%)。")

    for img_file in selected_imgs:
        shutil.copy(os.path.join(input_dir, img_file), output_dir)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python xxx.py <input_dir> <output_dir> <percent>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    percent = float(sys.argv[3])

    main(input_dir, output_dir, percent)
