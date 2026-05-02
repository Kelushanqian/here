import os
import shutil
import cv2
import numpy as np
import re

base = r"C:\Users\Oui\Desktop\deeplearning"

target = "train"
# target = "val"
# target = "test"

target_img = os.path.join(base, target, "images")
target_lbl = os.path.join(base, target, "labels")

def get_stem(fname):
    return os.path.splitext(fname)[0]

def read_label(path):
    with open(path, "r") as f:
        return f.readlines()

def write_label(path, lines):
    with open(path, "w") as f:
        f.writelines(lines)

def flip_labels(lines, flip_code):
    """水平翻转：x_center = 1 - x_center；垂直翻转：y_center = 1 - y_center"""
    new_lines = []
    for line in lines:
        parts = line.strip().split()
        cls, x, y, w, h = parts[0], float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
        if flip_code == 1:   # 水平
            x = 1.0 - x
        elif flip_code == 0: # 垂直
            y = 1.0 - y
        new_lines.append(f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
    return new_lines

imgs = [f for f in os.listdir(target_img) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
imgs.sort(key=lambda f: int(re.search(r'\d+', f).group()))

for fname in imgs:
    stem = get_stem(fname)
    img_path = os.path.join(target_img, fname)
    lbl_path = os.path.join(target_lbl, stem + ".txt")

    img = cv2.imread(img_path)
    lines = read_label(lbl_path) if os.path.exists(lbl_path) else []

    augments = []

    # 1. 垂直翻转 + 模糊
    vflip = cv2.flip(img, 0)
    vflip_blur = cv2.GaussianBlur(vflip, (11, 11), 0)
    augments.append((vflip_blur, flip_labels(lines, 0), "1"))

    # 2. 变亮 + 噪声
    bright = cv2.convertScaleAbs(img, alpha=1.0, beta=90)
    noise = np.random.normal(0, 15, bright.shape).astype(np.int16)
    bright_noisy = np.clip(bright.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    augments.append((bright_noisy, lines, "2"))

    # 3. 变暗 + 模糊 + 噪声
    dark = cv2.convertScaleAbs(img, alpha=1.0, beta=-90)
    dark_blur = cv2.GaussianBlur(dark, (11, 11), 0)
    noise2 = np.random.normal(0, 15, dark_blur.shape).astype(np.int16)
    dark_blur_noisy = np.clip(dark_blur.astype(np.int16) + noise2, 0, 255).astype(np.uint8)
    augments.append((dark_blur_noisy, lines, "3"))

    for aug_img, aug_lines, tag in augments:
        new_fname = f"{stem}_{tag}.jpg"
        cv2.imwrite(os.path.join(target_img, new_fname), aug_img)
        if aug_lines:
            write_label(os.path.join(target_lbl, f"{stem}_{tag}.txt"), aug_lines)

print("扩充完成！")