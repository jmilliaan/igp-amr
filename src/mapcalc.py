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
    x_coords = distances * cosine_list
    y_coords = distances * sine_list
    return x_coords, y_coords

def generate_boolean_spacemap(x_coords, y_coords, map_size=(12_000, 12_000)):
    x_coordinates = np.round(x_coords).astype(int)
    y_coordinates = np.round(y_coords).astype(int)

    x_coordinates = np.clip(x_coordinates, 0, map_size[1] - 1)
    y_coordinates = np.clip(y_coordinates, 0, map_size[0] - 1)

    spacemap = np.zeros(map_size, dtype=bool)
    spacemap[y_coordinates, x_coordinates] = 1
    return spacemap
