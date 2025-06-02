import matplotlib.pyplot as plt
import numpy as np

def linear_function(x, a, b):
    return a * x + b

slope = 1
intercept = 0

last_number_x = []
for number_x in np.linspace(2, 1000, 1000):
    start_x = 0
    finsh_x = 10

    x_value = np.linspace(start_x, finsh_x, number_x)
    y_value = linear_function(x_value, slope, intercept)

    dx = y_value[1] - y_value[0]

    sub_result = []
    for a in y_value:
        sub_result.append(dx * a)
    result = sum(sub_result)

last_x_vlaue = last_number_x
last_y_vlaue = result

plt.plot(last_x_vlaue, last_y_vlaue)

plt.grid(True)
plt.show()