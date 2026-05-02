import cv2
import requests

def extract_and_upload(video_path, interval_seconds=5, drone_id="drone_unknown", x=0, y=0):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"打不开视频：{video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_seconds)  # 每隔多少帧取一次
    
    frame_index = 0
    uploaded = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % frame_interval == 0:
            # 把帧编码成 jpg，直接发给 ingest 接口
            success, buffer = cv2.imencode('.jpg', frame)
            if not success:
                frame_index += 1
                continue

            files = {'file': ('frame.jpg', buffer.tobytes(), 'image/jpeg')}
            data = {'drone_id': drone_id, 'x': x, 'y': y}

            try:
                resp = requests.post("http://localhost:5001/api/ingest", files=files, data=data)
                if resp.status_code == 200:
                    uploaded += 1
                    print(f"第 {frame_index} 帧上传成功（第 {uploaded} 张）")
                else:
                    print(f"第 {frame_index} 帧上传失败：{resp.text}")
            except Exception as e:
                print(f"第 {frame_index} 帧请求出错：{e}")

        frame_index += 1

    cap.release()
    print(f"完成，共上传 {uploaded} 张")