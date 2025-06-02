import matplotlib.pyplot as plt
import numpy as np

def calculate_next_value(current_value, r):
        next_value = r * current_value * (1 - current_value)
        return next_value

finally_r = 4
x = np.arange(0.9, finally_r, 0.01)

for r in x:
    initial_value = 0.4
# initial_value_list = [initial_value]
# r = 1.0

    num_iterations = 10000

    current_value = initial_value
    value_map = []
    for _ in range(num_iterations):
        current_value = calculate_next_value(current_value, r)
        value_map.append(current_value)
    Y_value = value_map
    X_value = range(num_iterations)

    X1000_999 = value_map[num_iterations - 100:]
    plt.scatter([r] * 100, X1000_999, s=1, c='black')

plt.show()
## r에 따른 X1000_999의 점을 찍음