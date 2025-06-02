import matplotlib.pyplot as plt
import numpy as np

def quadraric_function(x, a, b):
    return a * x * x + b

slope = 1
intercept = 0


last_x = 10
basic_wide = 10
divide = last_x / basic_wide

wide = list(range(0, last_x + 1))
real_list = []
for num in wide:
    real_list.append(num / divide)

real_array = np.array(real_list)


Y_value = quadraric_function(real_array, slope, intercept)


print(real_list)


plt.plot(real_list, Y_value)
plt.grid(True)

plt.show()