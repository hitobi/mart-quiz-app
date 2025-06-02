import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.font_manager as fm
import platform
import os

# 페이지 설정
st.set_page_config(page_title="Sin 함수 시뮬레이션", layout="wide")

# CSS로 웹 폰트 적용
st.markdown("""
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500&display=swap");
        * {
            font-family: "Noto Sans KR", sans-serif !important;
        }
        .stTitle {
            font-size: 2rem !important;
            font-weight: 500 !important;
        }
        .stMarkdown {
            font-size: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# matplotlib 한글 폰트 설정
plt.style.use("default")  # seaborn 대신 기본 스타일 사용
plt.rcParams['font.family'] = 'DejaVu Sans'  # 기본 폰트 사용
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.dpi'] = 100
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

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
fig = plt.figure(figsize=(15, 4.5))

# 1. 단위원 그래프
ax1 = plt.subplot(1, 3, 1)
circle = Circle((0, 0), 1, fill=False, linewidth=1.5)
ax1.add_artist(circle)
ax1.plot([0, x], [0, y], "r-", linewidth=1.5, label="Angle")
ax1.plot([x, x], [0, y], "b--", linewidth=1.5, label="Sin")
ax1.plot(x, y, "ro", markersize=6)
ax1.plot(x, y, "bo", markersize=6)
ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-1.5, 1.5)
ax1.grid(True, alpha=0.3)
ax1.set_aspect("equal")
ax1.set_title("Unit Circle Sin Value")
ax1.legend(loc="upper right", fontsize="small")

# 2. sin 그래프
ax2 = plt.subplot(1, 3, 2)
x_sin = np.linspace(0, np.pi, 500)
ax2.plot(x_sin, np.sin(x_sin), "b-", label="sin(x)")
ax2.plot(theta, y, "ro", markersize=6)
ax2.set_xlim(0, np.pi)
ax2.set_ylim(-1.5, 1.5)
ax2.grid(True, alpha=0.3)
ax2.set_title("Sin Graph")
xticks = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
xtick_labels = ["0", "π/4", "π/2", "3π/4", "π"]
ax2.set_xticks(xticks)
ax2.set_xticklabels(xtick_labels)
ax2.legend(loc="upper right", fontsize="small")

# 3. 차이 그래프
ax3 = plt.subplot(1, 3, 3)
x_diff = np.linspace(0.01, np.pi, 500)
y_diff = -((np.sin(x_diff) - x_diff) / x_diff) * 100
ax3.plot(x_diff, y_diff, "g-", label="Difference")
if theta > 0:
    diff_val = -((y - theta) / theta) * 100
    ax3.plot(theta, diff_val, "ro", markersize=6)
ax3.set_xlim(0, np.pi)
ax3.grid(True, alpha=0.3)
ax3.set_title("Difference Between Radian and Sin")
ax3.set_xlabel("Angle (radian)")
ax3.set_ylabel("Difference (%)")
ax3.set_xticks(xticks)
ax3.set_xticklabels(xtick_labels)
ax3.legend(loc="upper right", fontsize="small")

plt.tight_layout(pad=2.0)

# 그래프를 반응형으로 표시
st.pyplot(fig, use_container_width=True)

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
with st.expander("사용 방법"):
    st.markdown("""
    1. 왼쪽 사이드바의 슬라이더를 움직여 각도를 조절할 수 있습니다.
    2. 왼쪽 그래프의 단위원에서 빨간색 선은 각도를, 파란색 점선은 sin 값을 나타냅니다.
    3. 가운데 그래프는 sin 함수의 전체 모양을 보여줍니다.
    4. 오른쪽 그래프는 라디안 값과 sin 값의 차이를 퍼센트로 보여줍니다.
    """)

with st.expander("참고사항"):
    st.markdown("""
    - 각도는 0부터 π(약 3.142)까지 표시됩니다.
    - 차이(%)는 (라디안 값 - sin 값) / 라디안 값 * 100으로 계산됩니다.
    - 양수 차이는 라디안 값이 sin 값보다 큰 경우를 나타냅니다.
    - 음수 차이는 sin 값이 라디안 값보다 큰 경우를 나타냅니다.
    """) 