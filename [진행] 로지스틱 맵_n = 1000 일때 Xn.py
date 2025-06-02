def calculate_next_value(current_value, r):
    next_value = r * current_value * (1 - current_value)
    return next_value

initial_value = 0.4
# initial_value_list = [initial_value]
r = 1.0

num_iterations = 1000

current_value = initial_value
value_map = []
for _ in range(num_iterations):
    current_value = calculate_next_value(current_value, r)
    value_map.append(current_value)
Y_value = value_map
X_value = range(num_iterations)

X1000_999 = value_map[num_iterations - 2:]

print(X1000_999)
## r에 따른 X1000_999의 점을 찍음