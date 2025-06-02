import numpy as np

a = np.arange(1, 3)
e = []
for c in a:
    y = np.arange(1, 3, c)
    d = sum(y)
    e.append(d)
print(np.arange(1, 3, 2))
print(a)
print(e)

