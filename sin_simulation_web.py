import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.font_manager as fm

# 페이지 설정
st.set_page_config(page_title="Sin 함수 시뮬레이션", layout="wide")

# 제목
st.title("Sin 함수 시뮬레이션")
st.markdown("각도(라디안)에 따른 sin 값의 변화를 시각화하는 도구입니다.")

# 사이드바에 각도 선택 슬라이더 추가
theta = st.sidebar.slider(
    "각도 (라디안)",
    min_value=0.0,
    max_value=float(np.pi),
    value=0.0,
    step=0.01,
    format="%.3f"
)

# 각도에 따른 값 계산
x = np.cos(theta)
y = np.sin(theta)

# 그래프 생성
fig = plt.figure(figsize=(15, 12))

# 1. 단위원 그래프
ax1 = plt.subplot2grid((3, 2), (0, 0), rowspan=2)
circle = Circle((0, 0), 1, fill=False, linewidth=2)
ax1.add_artist(circle)
ax1.plot([0, x], [0, y], 'r-', linewidth=3, label='각도')
ax1.plot([x, x], [0, y], 'b--', linewidth=3, label='sin 값')
ax1.plot(x, y, 'ro', markersize=10)
ax1.plot(x, y, 'bo', markersize=10)
ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-1.5, 1.5)
ax1.grid(True)
ax1.set_aspect('equal')
ax1.set_title('단위원에서의 sin 값')
ax1.legend()

# 2. sin 그래프
ax2 = plt.subplot2grid((3, 2), (0, 1), rowspan=2)
x_sin = np.linspace(0, np.pi, 500)
ax2.plot(x_sin, np.sin(x_sin), 'b-', label='sin(x)')
ax2.plot(theta, y, 'ro', markersize=10)
ax2.set_xlim(0, np.pi)
ax2.set_ylim(-1.5, 1.5)
ax2.grid(True)
ax2.set_title('sin 그래프')
xticks = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
xtick_labels = ['0', 'π/4', 'π/2', '3π/4', 'π']
ax2.set_xticks(xticks)
ax2.set_xticklabels(xtick_labels)
ax2.legend()

# 3. 차이 그래프
ax3 = plt.subplot2grid((3, 2), (2, 0), colspan=2)
x_diff = np.linspace(0.01, np.pi, 500)
y_diff = -((np.sin(x_diff) - x_diff) / x_diff) * 100
ax3.plot(x_diff, y_diff, 'g-', label='차이')
if theta > 0:
    diff_val = -((y - theta) / theta) * 100
    ax3.plot(theta, diff_val, 'ro', markersize=10)
ax3.set_xlim(0, np.pi)
ax3.grid(True)
ax3.set_title('라디안 값과 sin 값의 차이')
ax3.set_xlabel('각도 (라디안)')
ax3.set_ylabel('차이 (%)')
ax3.set_xticks(xticks)
ax3.set_xticklabels(xtick_labels)
ax3.legend()

plt.tight_layout()

# 그래프 표시
st.pyplot(fig)

# 현재 값들 표시
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("라디안", f"{theta:.3f}")
with col2:
    st.metric("sin 값", f"{y:.3f}")
with col3:
    if theta > 0:
        diff_val = -((y - theta) / theta) * 100
        st.metric("차이", f"{diff_val:.3f}%")
    else:
        st.metric("차이", "0.000%")

# 설명 추가
st.markdown("""
### 사용 방법
1. 왼쪽 사이드바의 슬라이더를 움직여 각도를 조절할 수 있습니다.
2. 상단의 단위원에서 빨간색 선은 각도를, 파란색 점선은 sin 값을 나타냅니다.
3. 우측 그래프는 sin 함수의 전체 모양을 보여줍니다.
4. 하단 그래프는 라디안 값과 sin 값의 차이를 퍼센트로 보여줍니다.

### 참고사항
- 각도는 0부터 π(약 3.142)까지 표시됩니다.
- 차이(%)는 (라디안 값 - sin 값) / 라디안 값 * 100으로 계산됩니다.
- 양수 차이는 라디안 값이 sin 값보다 큰 경우를 나타냅니다.
- 음수 차이는 sin 값이 라디안 값보다 큰 경우를 나타냅니다.
""") 