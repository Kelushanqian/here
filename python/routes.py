# routes.py
# 接口。

import os
import time
import numpy as np
import cv2
from flask import Blueprint, jsonify, request, send_from_directory
from database import insert_image, fetch_all_images
from config import ORIGINAL_DIR
from extract_frames import extract_and_upload
import threading

bp = Blueprint('main', __name__)

# POST /api/ingest 接收上传的图片，存档并写入数据库
@bp.route('/api/ingest', methods=['POST'])
def ingest():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400

    file = request.files['file']
    drone_id = request.form.get('drone_id', 'drone_unknown')
    x = request.form.get('x', 0)
    y = request.form.get('y', 0)

    in_memory = file.read()
    nparr = np.frombuffer(in_memory, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return jsonify({'error': 'Invalid image'}), 400

    filename = f"{int(time.time() * 1000)}.jpg"
    original_path = os.path.join(ORIGINAL_DIR, filename)
    cv2.imwrite(original_path, img)

    insert_image(drone_id, x, y, time.strftime("%Y-%m-%d %H:%M:%S"), original_path)
    return jsonify({'status': 'ok', 'filename': filename})

# GET /api/images 返回所有图片记录（含处理状态）
@bp.route('/api/images', methods=['GET'])
def get_images():
    rows = fetch_all_images()
    result = []
    for r in rows:
        d = dict(r)
        d['original_filename'] = os.path.basename(d['original_path']) if d['original_path'] else None
        d['processed_filename'] = os.path.basename(d['processed_path']) if d['processed_path'] else None
        result.append(d)
    return jsonify(result)

# GET /images/<folder>/<filename> 直接访问原始或处理后的图片文件
@bp.route('/images/<folder>/<filename>')
def serve_image(folder, filename):
    directory = os.path.join("images", folder)
    return send_from_directory(directory, filename)

@bp.route('/api/ingest_video', methods=['POST'])
def ingest_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    drone_id = request.form.get('drone_id', 'drone_unknown')
    x = request.form.get('x', 0)
    y = request.form.get('y', 0)
    interval_seconds = float(request.form.get('interval_seconds', 5))

    # 先把视频存到本地
    filename = f"{int(time.time() * 1000)}.mp4"
    video_path = os.path.join("videos", filename)
    os.makedirs("videos", exist_ok=True)
    file.save(video_path)

    # 丢给后台线程处理，不阻塞请求
    threading.Thread(
        target=extract_and_upload,
        args=(video_path, interval_seconds, drone_id, x, y),
        daemon=True
    ).start()

    return jsonify({'status': 'ok', 'video': filename})