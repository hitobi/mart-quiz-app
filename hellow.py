import matplotlib.pyplot as plt

def logistic_map(r, x0, num_iterations):
    results = [x0]
    for _ in range(num_iterations - 1):
        x0 = r * x0 * (1 - x0)
        results.append(x0)
    return results

def plot_logistic_map(r_values, x0, num_iterations):
    for r in r_values:
        solution = logistic_map(r, x0, num_iterations)
        plt.plot([r] * num_iterations, solution, 'b.', markersize=1)

    plt.xlabel('r')
    plt.ylabel('Xn+1')
    plt.title('Logistic Map')
    plt.show()

# 매개변수 설정
r_values = [i / 1000 for i in range(10, 4000)]  # r 값 범위 (0.5에서 1.0 사이로 변경 가능)
initial_value = 0.8  # 초기값 (원하는 값으로 변경 가능)
iterations = 50  # 반복 횟수 (원하는 값으로 변경 가능)

# 로지스틱 맵 시각화
plot_logistic_map(r_values, initial_value, iterations)
