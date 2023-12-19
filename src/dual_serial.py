import threading
import multiprocessing
import PyLidar3
from serial_communication import SerialCommunication
import time
import glob

def check_port_connection():
    connections = {"lidar":"", "arduino":""}
    n_connections = len(connections.keys())
    
    ports = glob.glob("/dev/ttyUSB*")
    n_ports = len(ports)
    end_connection = False
    print(ports)
    if n_ports >= n_connections:    
        print("connection flag")
        for i in range(n_ports):
            print(f"port: {ports[i]} | ", end=" ")
            other_idx = not i
            try_lidar = PyLidar3.YdLidarX4(port=ports[i])
            try_lidar.Connect()
            device_info = try_lidar.GetDeviceInfo()
            print(device_info["model_number"], type(device_info["model_number"]))
            
            if device_info["model_number"] != '0':
                print(f"port {ports[i]} is lidar")
                connections["lidar"] = ports[i]
                connections["arduino"] = ports[other_idx]
                end_connection = True
                time.sleep(0.2)
                break
            try_lidar.Disconnect()

        if end_connection:
            try_lidar.Disconnect()

        return (True, connections)
    else:
        print(f"At least {str(n_connections - n_ports)} device(s) is not connected!")
        return (False, connections)

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
    connection_check = check_port_connection()
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