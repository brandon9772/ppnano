import numpy as np


a = np.round(343333.0000009945, 4) % 1

x = 1153235.534645
half = 56/2

x_max = np.round(x + half, 4)
x_min = np.round(x - half, 4)

print(x_min)
print(x_max)

print(x_max - x_min)


poly = 'POLYGON ((524311.95 196190.35, 524317.6 196190, 524317.8 196192.85, 524316.95 196192.9, 524312.2 196193.2, 524311.95 196190.35))'
