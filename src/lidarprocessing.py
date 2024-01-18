from adafruit_rplidar import RPLidar
import numpy as np
import time

theta_list_deg = np.arange(360)
theta_list_rad = np.radians(theta_list_deg)
cosine_list = np.cos(theta_list_rad)
sine_list = np.sin(theta_list_rad)

class LIDAR:
    def __init__(self, port):
        self.port = port
        self.lidar = RPLidar(None, self.port, timeout=3)
        self.max_distance = 3
    
    def stop_lidar(self):
        try:
            self.lidar.stop()
            self.lidar.disconnect()
            return True
        except:
            print("LIDAR Stop Failed")
            return False

    def scan_lidar(self):
        self.stop_lidar()
        time.sleep(0.5)
        self.lidar.connect()
        self.lidar.start_motor()
        time.sleep(0.5)
        try:
            for scan in self.lidar.iter_scans():
                print(len(scan))
                print(scan[:6])
                print()
        except:
            self.lidar.stop()
            self.lidar.disconnect()
            print("Stopping")
            return

        

def get_lidar_scan():
    return

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


# lidar = RPLidar('COM13')

# info = lidar.get_info()
# print(info) 

# health = lidar.get_health()
# print(health)

# for i, scan in enumerate(lidar.iter_scans()):
#     print('%d: Got %d measurments' % (i, len(scan)))
#     if i > 10:
#         break
# lidar.stop()
# lidar.stop_motor()
# lidar.disconnect()