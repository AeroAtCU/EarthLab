# eventually, take x y tree crown centerpoints (pixel locations) and create a thiessen (voronoi) polygon from them for comparison to negative slope map
import matplotlib.pyplot as plt
from scipy.spatial  import Voronoi, voronoi_plot_2d
import numpy as np

points = np.array([[0.5, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],[2, 0], [2, 1], [2, 2]])

vor = Voronoi(points)
fig = voronoi_plot_2d(vor)
plt.show()
