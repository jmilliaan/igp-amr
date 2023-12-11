import PyLidar3

lidar = PyLidar3.YdLidarX4(port="COM8")
lidar.Connect()

for i in range(1000):
    print(lidar.StartScanning())
lidar.Disconnect()