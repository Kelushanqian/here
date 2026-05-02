# extract_frames.py 本地版

import os
import cv2
from datetime import datetime
from database import insert_image, update_status, fetch_image_id_by_path
from processing import process_image_file
from config import ORIGINAL_DIR, PROCESSED_DIR

def extract_and_upload(video_path, interval_seconds=5, drone_id="drone_unknown", x=0, y=0):
    os.makedirs(ORIGINAL_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"打不开视频：{video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_seconds)

    frame_index = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % frame_interval == 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{timestamp}_f{frame_index}.jpg"

            original_path = os.path.join(ORIGINAL_DIR, filename)
            cv2.imwrite(original_path, frame)

            # insert_image(drone_id, x, y, datetime.now().isoformat(), original_path)

            processed = process_image_file(original_path)
            if processed is not None:
                processed_path = os.path.join(PROCESSED_DIR, filename)
                cv2.imwrite(processed_path, processed)
                # image_id = fetch_image_id_by_path(original_path)
                # if image_id:
                #     update_status(image_id, "done", processed_path)
                saved += 1
                print(f"第 {frame_index} 帧处理完成（第 {saved} 张）")
            else:
                print(f"第 {frame_index} 帧处理失败")

        frame_index += 1

    cap.release()
    print(f"完成，共处理 {saved} 张")