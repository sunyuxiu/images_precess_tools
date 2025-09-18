import os
import re
import sys
from collections import defaultdict

def main():
    if len(sys.argv) != 2:
        print("用法: python xxx.py <model_dir>")
        sys.exit(1)

    base_dir = sys.argv[1]

    if not os.path.exists(base_dir):
        print(f"错误: 目录 {base_dir} 不存在")
        sys.exit(1)

    # Rockchip 存储结构: {model: [path1, path2]}
    rockchip_models = defaultdict(list)

    # Nvidia 存储结构: {model: {b16: path, b32: path, b64: path}}
    nvidia_models = defaultdict(lambda: {})

    # 遍历目录下文件
    for fname in sorted(os.listdir(base_dir)):
        fpath = os.path.join(base_dir, fname)

        # Rockchip 模型 (rknn)
        if fname.endswith(".rknn"):
            model_name = fname.split("_fp16.rknn")[0]
            rockchip_models[model_name].append(fpath)

        # Nvidia 模型 (bin)
        elif fname.endswith(".bin"):
            # 匹配 batch size: b16, b32, b64
            m = re.search(r"_(b\d+)_fp16\.bin$", fname)
            if not m:
                continue
            batch = m.group(1)
            model_name = fname.split(f"_{batch}_fp16.bin")[0]
            nvidia_models[model_name][batch] = fpath

    # -------- 打印 Rockchip --------
    print("rockchip\n")
    for model, files in rockchip_models.items():
        print(model)
        for f in files:
            print(f"  {f}")
        print()

    # -------- 打印 Nvidia --------
    print("nvidia\n")
    for model, batches in nvidia_models.items():
        print(model)
        for b in ["b16", "b32", "b64"]:
            if b in batches:
                print(f"  {b}: {batches[b]}")
        print()

if __name__ == "__main__":
    main()

