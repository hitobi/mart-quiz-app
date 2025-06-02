import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
import matplotlib.font_manager as fm

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'  # Mac OS용 한글 폰트
plt.rcParams['axes.unicode_minus'] = False   # 마이너스 기호 깨짐 방지

# 그래프 설정
fig = plt.figure(figsize=(12, 14))  # 세로 크기 증가
ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=4)  # 단위원 크기 더 증가
ax2 = plt.subplot2grid((8, 1), (4, 0), rowspan=2)  # sin 그래프
ax3 = plt.subplot2grid((8, 1), (6, 0), rowspan=1)  # 차이 그래프
ax_slider = plt.subplot2grid((8, 1), (7, 0))
plt.subplots_adjust(hspace=0.5)

# 단위원 그리기
circle = plt.Circle((0, 0), 1, fill=False, linewidth=2)  # 원 선 굵기 증가
ax1.add_artist(circle)
ax1.set_xlim(-1.8, 1.8)  # 여백 증가
ax1.set_ylim(-1.8, 1.8)  # 여백 증가
ax1.grid(True)
ax1.set_aspect('equal')
ax1.set_title('단위원에서의 sin 값', pad=15, fontsize=14)  # 제목 크기 증가

# sin 그래프 설정
x = np.linspace(0, np.pi, 500)  # π까지로 변경
line, = ax2.plot(x, np.sin(x))
point, = ax2.plot([], [], 'ro')
ax2.set_xlim(0, np.pi)  # π까지로 변경
ax2.set_ylim(-1.5, 1.5)
ax2.grid(True)
ax2.set_title('sin 그래프')
ax2.set_xlabel('각도 (라디안)')
ax2.set_ylabel('sin 값')

# x축에 π 단위로 눈금 표시
xticks = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
xtick_labels = ['0', 'π/4', 'π/2', '3π/4', 'π']
ax2.set_xticks(xticks)
ax2.set_xticklabels(xtick_labels)

# 차이 그래프 설정
x_diff = np.linspace(0.01, np.pi, 500)  # 0 제외, π까지로 변경
y_diff = -((np.sin(x_diff) - x_diff) / x_diff) * 100  # 부호 반전
diff_line, = ax3.plot(x_diff, y_diff)
diff_point, = ax3.plot([], [], 'ro')
ax3.set_xlim(0, np.pi)  # π까지로 변경
ax3.grid(True)
ax3.set_title('라디안 값과 sin 값의 차이')
ax3.set_xlabel('각도 (라디안)')
ax3.set_ylabel('차이 (%)')

# x축에 π 단위로 눈금 표시
ax3.set_xticks(xticks)
ax3.set_xticklabels(xtick_labels)

# 단위원의 각도를 보여주는 선과 점
angle_line, = ax1.plot([], [], 'r-', linewidth=3)  # 선 굵기 증가
circle_point, = ax1.plot([], [], 'ro', markersize=10)  # 점 크기 증가
sin_line, = ax1.plot([], [], 'b--', linewidth=3)  # 선 굵기 증가
sin_point, = ax1.plot([], [], 'bo', markersize=10)  # 점 크기 증가

# 텍스트 표시 (위치 조정 및 크기 증가)
angle_text = ax1.text(-1.7, 1.6, '', fontsize=14)
sin_text = ax1.text(-1.7, 1.4, '', fontsize=14)
diff_text = ax1.text(-1.7, 1.2, '', fontsize=14)

# 슬라이더 생성
slider = Slider(
    ax=ax_slider,
    label='각도 (라디안)',
    valmin=0,
    valmax=np.pi,  # π까지로 변경
    valinit=0,
)

# 애니메이션 상태
animation_running = True

def update(theta):
    # 단위원 위의 점 좌표
    x = np.cos(theta)
    y = np.sin(theta)
    
    # 단위원에서의 요소들 업데이트
    angle_line.set_data([0, x], [0, y])
    circle_point.set_data([x], [y])
    sin_line.set_data([x, x], [0, y])
    sin_point.set_data([x], [y])
    
    # sin 그래프에서의 점 업데이트
    point.set_data([theta], [y])
    
    # 차이 그래프에서의 점 업데이트
    if theta > 0:
        diff_val = -((y - theta) / theta) * 100  # 부호 반전
    else:
        diff_val = 0
    diff_point.set_data([theta], [diff_val])
    
    # 텍스트 업데이트
    angle_text.set_text(f'라디안: {theta:.3f} rad')
    sin_text.set_text(f'sin({theta:.3f}) = {y:.3f}')
    if theta > 0:
        diff_text.set_text(f'차이: {diff_val:.3f}%')
    else:
        diff_text.set_text('차이: 0.000%')
    
    fig.canvas.draw_idle()

def animate(frame):
    if animation_running:
        theta = (frame / 100) * np.pi  # π까지로 변경
        slider.set_val(theta)
    return angle_line, circle_point, sin_line, sin_point, point, diff_point, angle_text, sin_text, diff_text

# 슬라이더 값 변경 시 호출되는 함수
def slider_update(val):
    update(val)

# 애니메이션 시작/정지 버튼
ax_button = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(ax_button, '시작/정지')

def button_clicked(event):
    global animation_running
    animation_running = not animation_running

button.on_clicked(button_clicked)
slider.on_changed(slider_update)

# 애니메이션 생성
anim = FuncAnimation(fig, animate, frames=100, interval=20, blit=True)  # 프레임 수 조정

plt.show() 