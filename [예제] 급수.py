import matplotlib.pyplot as plt

def function(x,n):
    a=1
    b=1
    for _ in range(1,n+1):
        a*=x * (x + 1)
        b+=a
    return b

x=1
n = range(1, 10)
y = []
for c in n:
    y.append(function(x, c))

plt.plot(n, y)
plt.show()