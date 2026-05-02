import os
import shutil
import re

base = r"C:\Users\Oui\Desktop\deeplearning"
img_dir = os.path.join(base, "images")
lbl_dir = os.path.join(base, "labels")

# 建子目录
for split in ["train", "val", "test"]:
    for sub in ["images", "labels"]:
        os.makedirs(os.path.join(base, split, sub), exist_ok=True)

# 以图片文件名为基准
imgs = [f for f in os.listdir(img_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
imgs.sort(key=lambda f: int(re.search(r'\d+', f).group()))

n = len(imgs)
n_train = int(n * 0.7)
n_val   = int(n * 0.2)
# 剩余全给 test

splits = {
    "train": imgs[:n_train],
    "val":   imgs[n_train:n_train+n_val],
    "test":  imgs[n_train+n_val:],
}

for split, files in splits.items():
    for fname in files:
        stem = os.path.splitext(fname)[0]
        # 复制图片
        shutil.copy(
            os.path.join(img_dir, fname),
            os.path.join(base, split, "images", fname)
        )
        # 复制对应 label（.txt）
        lbl_fname = stem + ".txt"
        lbl_src = os.path.join(lbl_dir, lbl_fname)
        if os.path.exists(lbl_src):
            shutil.copy(lbl_src, os.path.join(base, split, "labels", lbl_fname))
        else:
            print(f"[警告] 找不到标注文件: {lbl_fname}")

print(f"完成！train={len(splits['train'])} val={len(splits['val'])} test={len(splits['test'])}")