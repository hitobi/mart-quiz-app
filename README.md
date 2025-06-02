# Sin 함수 시뮬레이션

각도(라디안)에 따른 sin 값의 변화를 시각화하는 웹 애플리케이션입니다.

## 기능
- 단위원에서 sin 값의 기하학적 의미 시각화
- sin 함수 그래프 표시
- 라디안 값과 sin 값의 차이를 퍼센트로 표시
- 실시간 각도 조절 가능

## 사용 방법
1. 왼쪽 사이드바의 슬라이더를 움직여 각도를 조절할 수 있습니다.
2. 상단의 단위원에서 빨간색 선은 각도를, 파란색 점선은 sin 값을 나타냅니다.
3. 우측 그래프는 sin 함수의 전체 모양을 보여줍니다.
4. 하단 그래프는 라디안 값과 sin 값의 차이를 퍼센트로 보여줍니다.

## 설치 및 실행
```bash
# 필요한 패키지 설치
pip install -r requirements.txt

# 애플리케이션 실행
streamlit run sin_simulation_web.py
```

## 기술 스택
- Python
- Streamlit
- Matplotlib
- NumPy 