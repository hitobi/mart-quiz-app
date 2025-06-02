import cv2
import os

# 동영상 파일 경로
video_path = 'your_video.mp4'
cap = cv2.VideoCapture(video_path)

# 저장할 디렉토리 생성
output_dir = 'frames'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_path = os.path.join(output_dir, f'frame_{frame_count:04d}.jpg')
    cv2.imwrite(frame_path, frame)
    frame_count += 1

cap.release()