import os
import cv2
import subprocess

# 父資料夾路徑
parent_content_folder = r'/mnt/HDD7/miayan/hw/CV/input_frames/origin'
parent_qrcode_folder = r'/mnt/HDD7/miayan/hw/CV/QR_frames/without_seg'
output_parent_dir = r'./output_videos/Origin_QR'  # 所有影片輸出的父資料夾
fps = 10  # 每秒幀數 (FPS)

# 確保輸出資料夾存在
os.makedirs(output_parent_dir, exist_ok=True)

# 處理每個子資料夾
content_subfolders = sorted([f for f in os.listdir(parent_content_folder) if os.path.isdir(os.path.join(parent_content_folder, f))])

for subfolder in content_subfolders:
    print(f"Processing video: {subfolder}")
    print(subfolder)
    # if int(subfolder )== 286:
    #     continue
    # 定義對應的資料夾與輸出路徑
    content_image_dir = os.path.join(parent_content_folder, subfolder)
    qrcode_image_dir = os.path.join(parent_qrcode_folder, subfolder)
    output_dir = os.path.join(output_parent_dir, subfolder)
    video_output_path = os.path.join(output_parent_dir, f"{subfolder}_output_video.mp4")

    # 確保當前影片的輸出資料夾存在
    os.makedirs(output_dir, exist_ok=True)

    # 獲取所有影格圖片檔案
    frame_files = sorted([f for f in os.listdir(content_image_dir) if f.endswith(('.jpg', '.png'))])
    qr_files = sorted([f for f in os.listdir(qrcode_image_dir) if f.endswith(('.jpg', '.png'))])

    # 確保影格數量一致
    if len(frame_files) != len(qr_files):
        print(f"Warning: Frame count mismatch in {subfolder}. Skipping this video.")
        continue
    print(content_image_dir)
    # 遍歷每個影格並執行指令
    for i, (frame, qr) in enumerate(zip(frame_files, qr_files)):
        content_image_path = os.path.join(content_image_dir, frame)
        # qrcode_image_path = os.path.join(qrcode_image_dir, qr)
        qrcode_image_path = './QR_frames/plain_qrcode.png'  # for original qrcode guidance
        print(content_image_path)
        print(qrcode_image_path)
        # print(i)
        output_path = os.path.join(output_dir, f"output_{i:04d}.jpg")
        print(output_path)
        # 組建指令
        command = [
            "python", "generate_aesthetic_qrcode.py",
            "--qrcode_image_path", qrcode_image_path,
            "--content_image_path", content_image_path,
            "--style_image_path", content_image_path,
            "--output_path", output_path
        ]

        # 執行指令
        print(f"Processing frame {i+1}/{len(frame_files)} in video {subfolder}.")
        subprocess.run(command)

    print(f"All frames for {subfolder} have been processed successfully!")

    # 將輸出的圖片合併成影片
    def create_video_from_images(image_folder, video_output, fps):
        images = sorted([img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")])
        if not images:
            print(f"No images found in {image_folder} to create a video.")
            return

        # 獲取圖片尺寸
        first_image_path = os.path.join(image_folder, images[0])
        frame = cv2.imread(first_image_path)
        h, w, _ = frame.shape

        # 初始化 VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 mp4v 編碼
        out = cv2.VideoWriter(video_output, fourcc, fps, (w, h))

        print(f"Creating video for {video_output}...")
        for img_name in images:
            img_path = os.path.join(image_folder, img_name)
            frame = cv2.imread(img_path)
            out.write(frame)  # 寫入影格

        out.release()
        print(f"Video saved at: {video_output}")

    # 呼叫影片合成函數
    create_video_from_images(output_dir, video_output_path, fps)

print("All videos have been processed successfully!")