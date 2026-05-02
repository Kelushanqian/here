# app2.py
# 服务端直接处理Potato leaf late blight图片的脚本
# 处理流程：复制原始图片 -> 数据库记录 -> 图像处理 -> 保存结果 -> 更新状态

import os
import shutil
import time
from datetime import datetime
import cv2
from database import insert_image, update_status, fetch_image_id_by_path
from processing import process_image_file
from config import ORIGINAL_DIR, PROCESSED_DIR
from extract_frames2 import extract_and_upload

def process_potato_leaf_images():
    # 确保目标目录存在
    os.makedirs(ORIGINAL_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # 源目录
    source_dir = "test"

    # 检查源目录是否存在
    if not os.path.exists(source_dir):
        print(f"源目录不存在: {source_dir}")
        return

    # 获取所有图片文件
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    image_files = [
        f for f in os.listdir(source_dir)
        if f.lower().endswith(image_extensions)
    ]

    if not image_files:
        print(f"源目录中没有找到图片文件: {source_dir}")
        return

    print(f"找到 {len(image_files)} 张图片需要处理...")

    # 处理每张图片
    total_images = len(image_files)
    for i, filename in enumerate(image_files, 1):
        try:
            # 源文件路径
            source_path = os.path.join(source_dir, filename)

            # 复制到original目录
            original_dest = os.path.join(ORIGINAL_DIR, filename)
            shutil.copy2(source_path, original_dest)

            # 生成元数据
            drone_id = "drone_A"
            x = 0  # 固定坐标
            y = 0  # 固定坐标
            capture_time = datetime.now().isoformat()

            # 插入数据库记录
            # insert_image(drone_id, x, y, capture_time, original_dest)

            # 处理图片
            processed_img = process_image_file(original_dest)
            if processed_img is None:
                raise ValueError("图片处理失败")

            # 保存处理后的图片
            processed_path = os.path.join(PROCESSED_DIR, filename)
            cv2.imwrite(processed_path, processed_img)

            # 更新数据库状态
            # image_id = fetch_image_id_by_path(original_dest)
            # if image_id:
                # update_status(image_id, "done", processed_path)
            # else:
                # print(f"  警告: 无法找到数据库记录")

        except Exception as e:
            print(f"  处理失败 {filename}: {e}")

            # 尝试更新数据库状态为failed
            try:
                # 查找可能已经插入的记录
                original_dest = os.path.join(ORIGINAL_DIR, filename)
                if os.path.exists(original_dest):
                    image_id = fetch_image_id_by_path(original_dest)
                    if image_id:
                        update_status(image_id, "failed")
            except Exception as db_error:
                print(f"  无法更新数据库状态: {db_error}")

    print("所有图片处理完成。")

if __name__ == '__main__':
    print("开始处理Potato leaf late blight图片...")
    process_potato_leaf_images()
    print(f"处理完成。")