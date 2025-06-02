import matplotlib.pyplot as plt
import numpy as np

def linear_function(x, m, b):
    """
    1차 함수를 나타내는 함수: y = mx + b
    """
    return m * x + b

# 함수의 기울기(slope)와 y-절편(intercept) 설정
slope = 2
intercept = 3

# x 값의 범위 설정
x_values = np.linspace(-10, 10, 100)  # -10에서 10까지 100개의 점으로 나눈 범위

# 각 x 값에 대한 y 값을 계산
y_values = linear_function(x_values, slope, intercept)

# 그래프 그리기
plt.plot(x_values, y_values, label=f'y = {slope}x + {intercept}')
plt.title('1차 함수 그래프')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()  # 범례 표시

# 그래프 보여주기
plt.grid(True)
plt.sh()
