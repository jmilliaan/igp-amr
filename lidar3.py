import PyLidar3

lidar = PyLidar3.YdLidarX4(port="/dev/ttyUSB0")
lidar.Connect()

for i in range(1000):
    data = lidar.StartScanning()
    print(data)
lidar.Disconnect()