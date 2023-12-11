import time
import PyLidar3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

lidar = PyLidar3.YdLidarX4(port="COM8")
lidar.Connect()

angles = np.array([])
distances = np.array([])
x_coords = np.array([])
y_coords = np.array([])

fig, ax = plt.subplots()
sc = ax.scatter([], [], s=2, marker='o')

ax.set_xlim(-4000, 4000)
ax.set_ylim(-4000, 4000)
ax.xaxis.set_major_locator(plt.MaxNLocator(10))
ax.yaxis.set_major_locator(plt.MaxNLocator(10))
ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.5)

def update_plot(frame, data_stream):
    global angles, distances, x_coords, y_coords
    data = next(data_stream)
    angles = np.radians(np.array(list(data.keys())))
    distances = np.array(list(data.values()))
    x_coords = distances * np.cos(angles)
    y_coords = distances * np.sin(angles)
    sc.set_offsets(np.column_stack((x_coords, y_coords)))
    return sc, 

animation = FuncAnimation(fig, update_plot, fargs=(lidar.StartScanning(),), frames=None, interval=20, blit=True)
plt.show()