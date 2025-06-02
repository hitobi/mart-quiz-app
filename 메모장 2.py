import cv2
from skimage.metrics import structural_similarity as ssim

img1 = cv2.imread("KakaoTalk_20250528_195212982_01.jpg", cv2.IMREAD_GRAYSCALE)  # 기준 이미지
img2 = cv2.imread("KakaoTalk_20250528_195212982_01.jpg", cv2.IMREAD_GRAYSCALE)  # 비교 이미지

if img1 is None or img2 is None:
    print("Error: 이미지를 불러올 수 없습니다. 파일이 존재하는지 확인하세요.")
    exit()

img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

score, diff = ssim(img1, img2, full=True)
print(f"SSIM 유사도: {score:.4f}")