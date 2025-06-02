# 프로그램 구현에 필요한 모듈 가져오기
import pandas as pd  # pandas 라는 모듈을 pd 라는 별칭(alias)으로 사용
import numpy as np  # numpy 라는 모듈을 np 라는 별명(alias)으로 사용
import matplotlib.pyplot as plt
import platform
# 여기서 as(alias) 하는 것은 일반적인 관례이지만, alias 기능을 사용하지 않아도 전혀 상관없음

dataframe = pd.read_excel("./LP-1-data.xlsx", sheet_name="Sheet1", header=None, index_col=None)
x축 = dataframe.iloc[0, 1:13].to_numpy()  # 선택한 행렬 데이터를 array 로 변환
y축2020 = dataframe.iloc[1, 1:13].to_numpy()
y축2021 = dataframe.iloc[2, 1:13].to_numpy()
y축2022 = dataframe.iloc[3, 1:13].to_numpy()
소비카테고리 = dataframe.iloc[5, 1:5].to_numpy()
이번달소비금액 = dataframe.iloc[6, 1:5].to_numpy()
이번달소비금액합계 = np.nansum(이번달소비금액, dtype="float16")
평균2020 = np.nanmean(y축2020, dtype="float16")
평균2021 = np.nanmean(y축2021, dtype="float16")
평균2022 = np.nanmean(y축2022, dtype="float16")

print(x축)
print(y축2020)
print(y축2021)
print(y축2022)
print(소비카테고리)
print(이번달소비금액)
print(이번달소비금액합계)
print(평균2020)
print(평균2021)
print(평균2022)

if platform.system() == "Darwin":
    plt.rc("font", family="AppleGothic")
else:
    plt.rc("font", family="Malgun Gothic")

plt.subplot(3, 1, 1)

plt.subplot(3, 1, 1)  # 가로 3칸, 세로 1칸 사이즈의 차트를 1번째로 그리기 시작하기
plt.title("지난 1년간 월별 카드값 사용 내역 (단위: 만)")  # 차트의 제목
plt.plot(x축, y축2020, marker="o", label="2020년")
plt.plot(x축, y축2021, marker="o", label="2021년")
plt.plot(x축, y축2022, marker="o", label="2022년")
plt.legend()  # 범례 표시
plt.xlabel("월")  # x축 레이블
plt.ylabel("카드사용금액")  # y축 레이블
plt.grid(True, axis="y")  # 그리드 선 표시

plt.show()  # 작성된 모든 plot 들을 표시