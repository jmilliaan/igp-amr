import time
import PyLidar3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

lidar = PyLidar3.YdLidarX4(port="COM8")
lidar.Connect()

for i in range(1000):
    print(lidar.StartScanning())
lidar.Disconnect()