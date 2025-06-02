import matplotlib.pyplot as plt
import numpy as np

area_wide = list(range(100, 1000))
area_Y = []
for basic_wide in area_wide:

    def linear_function(x, a, b):
        return a * x + b

    slope = 1
    intercept = 0


    last_x = 20
    # basic_wide = 10
    divide = last_x / basic_wide

    wide = list(range(0, (basic_wide + 1)))
    real_list = []
    for num in wide:
        real_list.append(num * divide)

    real_array = np.array(real_list)


    Y_value = linear_function(real_array, slope, intercept)

    area = 0
    for i in (Y_value * divide):
        area += i

    area_Y.append(area)

array_area_wide = np.array(area_wide)
array_area_Y = np.array(area_Y)

plt.plot(array_area_wide, array_area_Y)
plt.grid(True)
plt.show()