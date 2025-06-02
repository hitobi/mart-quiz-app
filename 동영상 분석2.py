import cv2
import numpy as np

def mark_leftmost_point_on_object(image_path):
    # 이미지 로드
    image = cv2.imread(image_path)
    
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 흰색 영역 찾기 위한 임계값 설정
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    
    # 윤곽선 찾기
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 각 윤곽의 왼쪽 끝점 찾기
    if contours:
        leftmost = None
        for contour in contours:
            # 각 윤곽의 왼쪽 끝점 계산
            contour_leftmost = tuple(contour[contour[:,:,0].argmin()][0])
            
            # 가장 왼쪽 점 업데이트
            if leftmost is None or contour_leftmost[0] < leftmost[0]:
                leftmost = contour_leftmost
        
        # 왼쪽 끝점에 초록색 점 찍기
        if leftmost:
            cv2.circle(image, leftmost, 5, (0, 255, 0), -1)
    
    # 이미지를 저장하거나 출력
    output_path = image_path.replace('.jpeg', '_marked.jpeg')
    cv2.imwrite(output_path, image)
    return output_path

# 함수 실행
image_path = '/Users/hitobi/Library/CloudStorage/SynologyDrive-업무/정승환/파이썬/image.jpeg'
output_image_path = mark_leftmost_point_on_object(image_path)
output_image_path