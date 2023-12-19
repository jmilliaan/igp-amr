import threading
import multiprocessing
import PyLidar3
from serial_communication import SerialCommunication

arduino_port = "/dev/ttyUSB1"
lidar_port = "/dev/ttyUSB0"


lidar = PyLidar3.YdLidarX4(
    port=lidar_port
    )
drive_comm = SerialCommunication(
    port=arduino_port, 
    baud_rate=9600
    )

lidar.Connect()

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

def send_data():
    drive_comm.send_repeating_data(2)

if __name__ == "__main__":
    lidar_thread = threading.Thread(target=lidar_data)
    sercomm_process = multiprocessing.Process(target=send_data)
    try:
        lidar_thread.start()
        sercomm_process.start()
        lidar_thread.join()
        sercomm_process.join()
    except KeyboardInterrupt:
        lidar_thread.join()
        sercomm_process.join()