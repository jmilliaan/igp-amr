from PyLidar3 import YdLidarX4
import numpy as np

theta_list_deg = np.arange(360)
theta_list_rad = np.radians(theta_list_deg)
cosine_list = np.cos(theta_list_rad)
sine_list = np.sin(theta_list_rad)

class LIDAR:
    def __init__(self, port, type="YdLidarX4"):
        self.port = port
        self.type = type
        self.lidar = YdLidarX4(self.port)
        self.lidar.Connect()

    def get_info(self):
        return self.lidar.GetDeviceInfo()
    
    def get_lidar_scan(self):
        return self.lidar.StartScanning()
        
    def stop_motor(self):
        self.lidar.stop_motor()
    

def generate_cartesian(lidar_data):
    distances = np.array(list(lidar_data.values()))
    x_coords = distances * cosine_list
    y_coords = distances * sine_list
    return x_coords, y_coords

def generate_boolean_spacemap(x_coords, y_coords, map_size):
    x_coordinates = np.round(x_coords).astype(int)
    y_coordinates = np.round(y_coords).astype(int)

    x_coordinates = np.clip(x_coordinates, 0, map_size[1] - 1)
    y_coordinates = np.clip(y_coordinates, 0, map_size[0] - 1)

    spacemap = np.zeros(map_size, dtype=bool)
    spacemap[y_coordinates, x_coordinates] = 1
    return spacemap


if __name__ == '__main__':
    lidar = YdLidarX4('COM4')
    lidar.Connect()
    if lidar._is_connected:
        print("Lidar is connected")
        # print(lidar.GetHealthStatus())
        distdict = lidar.StartScanning()
        for item in distdict:
            print(item)
            lidar.Disconnect()