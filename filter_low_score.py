# python filter_low_score.py input output score
import os
import sys
import json
import shutil
from glob import glob

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def should_copy(json_path, threshold=0.75):
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON: {json_path}")
            return False

        shapes = data.get("shapes", [])

        # 空标注，直接复制
        if not shapes:
            print(f"[INFO] Empty shapes, copying: {json_path}")
            return True

        # 检查是否有任何一个 score 小于阈值
        for shape in shapes:
            score = shape.get("score")
            if score is not None:
                if score < threshold:
                    print(f"[INFO] Low score {score:.4f} found in: {json_path}")
                    return True

    return False

def find_image(base_path):
    # 尝试不同的图片后缀
    for ext in [".jpg", ".JPG", ".jpeg", ".JPEG"]:
        img_path = base_path + ext
        if os.path.exists(img_path):
            return img_path
    return None

def main(src_dir, dst_dir, threshold):
    ensure_dir(dst_dir)
    json_files = glob(os.path.join(src_dir, "*.json"))
    count = 0

    for json_file in json_files:
        if should_copy(json_file, threshold):
            base_name = os.path.splitext(os.path.basename(json_file))[0]
            img_path = find_image(os.path.join(src_dir, base_name))

            # 复制 JSON
            shutil.copy(json_file, os.path.join(dst_dir, os.path.basename(json_file)))
            print(f"[COPY] JSON: {json_file}")

            # 复制图片
            if img_path:
                shutil.copy(img_path, os.path.join(dst_dir, os.path.basename(img_path)))
                print(f"[COPY] IMG:  {img_path}")
            else:
                print(f"[WARN] Image not found for: {base_name}")

            count += 1

    print(f"\n✅ Done. Total files copied (json+image pairs): {count}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python filter_low_score.py <source_dir> <target_dir> <score_threshold>")
        sys.exit(1)

    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    
    try:
        score_threshold = float(sys.argv[3])
    except ValueError:
        print("[ERROR] <score_threshold> must be a float, e.g., 0.75")
        sys.exit(1)

    main(source_dir, target_dir, score_threshold)
