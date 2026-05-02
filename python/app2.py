import os
from extract_frames2 import extract_and_upload

def process_potato_leaf_videos():
    source_dir = "test"

    if not os.path.exists(source_dir):
        print(f"源目录不存在: {source_dir}")
        return

    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
    video_files = [
        f for f in os.listdir(source_dir)
        if f.lower().endswith(video_extensions)
    ]

    if not video_files:
        print(f"源目录中没有找到视频文件: {source_dir}")
        return

    print(f"找到 {len(video_files)} 个视频需要处理...")

    for filename in video_files:
        video_path = os.path.join(source_dir, filename)
        print(f"正在处理: {filename}")
        extract_and_upload(
            video_path=video_path,
            interval_seconds=1,
            drone_id="drone_A",
            x=0,
            y=0
        )
        print(f"完成: {filename}")

    print("所有视频处理完成。")

if __name__ == '__main__':
    print("开始处理Potato leaf late blight视频...")
    process_potato_leaf_videos()
    print("处理完成。")