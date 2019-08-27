# just use the built in voronoi objects

import matplotlib.pyplot as plt
from scipy.spatial  import Voronoi, voronoi_plot_2d
import numpy as np
import random


points = np.array([[0,0]])
for x in range(10):
    a = random.randint(1,11)
    b = random.randint(1,11)
    print(a,b)
    tmp = [a,b]
    np.concatenate((points[0], tmp))


points_working = np.array([[0.5, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],[2, 0], [2, 1], [2, 2]])

print(points)
print(points_working)

vor = Voronoi(points)
fig = voronoi_plot_2d(vor)
plt.show()
