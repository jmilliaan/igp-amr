import threading
import multiprocessing
import PyLidar3
from serial_communication import SerialCommunication
import time
import glob

LIDAR_IDX = 0
ARDUINO_IDX = 1

def connect_lidar(port):
    lidar = PyLidar3.YdLidarX4(port=port)
    lidar.Connect()
    device_info = lidar.GetDeviceInfo()
    return lidar if device_info["model_number"] != '0' else None

def detect_connected_devices():
    connections = {"lidar": "", "arduino": ""}
    ports = glob.glob("/dev/ttyUSB*")

    if len(ports) >= len(connections):
        for i, port in enumerate(ports):
            other_idx = ARDUINO_IDX if i == LIDAR_IDX else LIDAR_IDX

            with connect_lidar(port) as lidar:
                if lidar:
                    connections["lidar"] = port
                    connections["arduino"] = ports[other_idx]
                    break

        return True, connections
    else:
        print(f"At least {len(connections) - len(ports)} device(s) is not connected!")
        return False, connections

def lidar_data(lidar_obj):
    try:
        scanning_generator = lidar_obj.StartScanning()
        while True:
            scan_result = next(scanning_generator)
            print("Lidar Scan Result:", scan_result)
    except Exception as e:
        print(f"Lidar scanning error: {e}")
    finally:
        lidar_obj.Disconnect()

def send_data(comm_obj):
    comm_obj.send_repeating_data(2)

if __name__ == "__main__":
    connection_check = detect_connected_devices()
    connection_status = connection_check[0]
    lidar_port = connection_check[1]["lidar"]
    arduino_port = connection_check[1]["arduino"]
    if connection_status:
        print(connection_check)
        # lidar = PyLidar3.YdLidarX4(port=lidar_port)
        # drive_comm = SerialCommunication(
        #     port=arduino_port, 
        #     baud_rate=9600)
    else: 
        print("Bad port connection!")
    # lidar.Connect()

    # lidar_thread = threading.Thread(target=lidar_data, args=(lidar,))
    # sercomm_process = multiprocessing.Process(target=send_data, args=(drive_comm,))
    # try:
    #     lidar_thread.start()
    #     sercomm_process.start()
    #     lidar_thread.join()
    #     sercomm_process.join()
    # except KeyboardInterrupt:
    #     for i in range(4):
    #         drive_comm.write(1)
    #         time.sleep(0.1)

    #     lidar_thread.join()
    #     sercomm_process.join()