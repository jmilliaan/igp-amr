import numpy as np

"""
Data format: {theta_0:r_0, theta_1:r_1, .... theta_359: r_359}
"""

theta_list_deg = np.arange(360)
theta_list_rad = np.radians(theta_list_deg)
cosine_list = np.cos(theta_list_rad)
sine_list = np.sin(theta_list_rad)

def generate_cartesian(lidar_data):
    distances = np.array(list(lidar_data.values()))
    x_coords = distances * cosine_list * 10
    y_coords = distances * sine_list * 10
    return x_coords, y_coords

def generate_boolean_spacemap(x_coords, y_coords, map_size=(100_000, 100_000)):
    x_coordinates = np.round(x_coords).astype(int)
    y_coordinates = np.round(y_coords).astype(int)
    spacemap = np.zeros(map_size, dtype=bool)
    spacemap[y_coordinates, x_coordinates] = 1
    return spacemap
