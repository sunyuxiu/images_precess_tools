# v1.0
# import os
# import shutil
# input_folder='/data/nofar/person_behavior/labeled_data/labeling_rule_v2.0.0/20250729/subdataset/person_behavior/trainval/val.txt'
# target_folder='/data/nofar/person_behavior/labeled_data/labeling_rule_v2.0.0/20250729/subdataset/person_behavior/val_images_temp/'
# if not os.path.exists(target_folder):
# 	os.makedirs(target_folder)
# with open(input_folder) as f:
#     a = f.readlines()
#     # print(a)
#     for b in a:
#         # print(b)
#         b = b.split('\n')[0]
#         # print(b)
#         shutil.copy(b, target_folder)


# v2.0，可以使用python xxx.py /data/nofar/person_behavior/labeled_data/labeling_rule_v2.0.0/20250729/subdataset/person_behavior/trainval/val.txt /data/nofar/person_behavior/labeled_data/labeling_rule_v2.0.0/20250729/subdataset/person_behavior/val_images_temp/
# 这种结构来运行
import os
import shutil
import sys

def copy_files_flat(input_txt, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_txt, 'r') as f:
        lines = f.readlines()

    for line in lines:
        src_path = line.strip()
        if not src_path:
            continue

        if not os.path.isfile(src_path):
            print(f"Warning: file not found: {src_path}")
            continue

        filename = os.path.basename(src_path)
        dst_path = os.path.join(output_dir, filename)

        shutil.copy(src_path, dst_path)
        print(f"Copied: {src_path} -> {dst_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python xxx.py input_txt output_folder")
        sys.exit(1)

    input_txt = sys.argv[1]
    output_dir = sys.argv[2]
    copy_files_flat(input_txt, output_dir)
