import threading
import multiprocessing
import PyLidar3
from serial_communication import SerialCommunication
import time
import glob


arduino_port = "/dev/ttyUSB1"
lidar_port = "/dev/ttyUSB0"

def check_port_connection():
    connections = {"lidar":"", "arduino":""}
    n_connections = len(connections.keys())
    
    ports = glob.glob("/dev/ttyUSB*")
    n_ports = len(ports)

    if n_ports >= n_connections:
        for port in ports:
            print(port)
    else:
        print(f"At least {str(n_ports - n_connections)} device(s) is not connected!")
        return
    return connections

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
    lidar = PyLidar3.YdLidarX4(
    port=lidar_port
    )
    drive_comm = SerialCommunication(
        port=arduino_port, 
        baud_rate=9600
        )
    check_port_connection()
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