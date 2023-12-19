import PyLidar3
from serial_communication import SerialCommunication

arduino_port = "/dev/ttyUSB0"
lidar_port = "/dev/ttyUSB3"

lidar = PyLidar3.YdLidarX4(
    port=lidar_port)

lidar.Connect()
print("lidar connected")
print("Device Info: ", end="")
print(lidar.GetDeviceInfo())
print("Health Info: ", end="")
print(lidar.GetHealthStatus())
lidar._Start_motor()

def lidar_data():
    try:
        scanning_generator = lidar.StartScanning()
        while True:
            scan_result = next(scanning_generator)
            print("Lidar Scan Result:", scan_result)
    except Exception as e:
        print(f"Lidar scanning error: {e}")
    finally:
        lidar.Disconnect()