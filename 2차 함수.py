import matplotlib.pyplot as plt
import numpy as np

def quadraric_function(x, a, b):
    return a * x * x + b

slope = 2
intercept = 0

x_values = np.linspace(-10, 10, 100)
y_values = quadraric_function(x_values, slope, intercept)

plt.plot(x_values, y_values, label='2차 함수')
plt.title('quadraric function')
plt. xlabel('x')
plt. ylabel('y')
plt. legend()

plt.grid(True)
plt.show()