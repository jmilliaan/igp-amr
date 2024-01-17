'''
MAIN PROGRAM

This program integrates:
1. Camera interface (raspberry pi camera connection)
2. Lidar interface (serial communication)
3. Arduino interface (serial communication)
4. Web app interface (websocket)

Outputs the command to send to the arduino (movement commend)
'''


# import threading
# import multiprocessing
# import PyLidar3
from serial_communication import SerialCommunication
import time
import glob
# from picam import PiCam
# from mapcalc import Map
# from webapp_interface import WebInterface

manual_command = 5
web_to_serial_command = {
    1: 1,
    2: 2,
    3: 1,
    4: 5,
    5: 1,
    6: 4,
    7: 1,
    8: 3,
    9: 1,
}

# def check_port_connection():
#     connections = {"lidar":"", "arduino":""}
#     n_connections = len(connections.keys())
    
#     ports = glob.glob("/dev/ttyUSB*")
#     n_ports = len(ports)
#     end_connection = False
#     if n_ports >= n_connections:    
#         for i in range(n_ports):
#             other_idx = not i
#             try_lidar = PyLidar3.YdLidarX4(port=ports[i])
#             try_lidar.Connect()
#             device_info = try_lidar.GetDeviceInfo()
            
#             if device_info["model_number"] != '0':
#                 connections["lidar"] = ports[i]
#                 connections["arduino"] = ports[other_idx]
#                 end_connection = True
#                 time.sleep(0.2)
#                 break
#             try_lidar.Disconnect()

#         if end_connection:
#             try_lidar.Disconnect()

#         return (True, connections)
#     else:
#         print(f"At least {str(n_connections - n_ports)} device(s) is not connected!")
#         return (False, connections)

# # def lidar_data(lidar_obj:PyLidar3.YdLidarX4):
#     try:
#         scanning_generator = lidar_obj.StartScanning()
#         while True:
#             scan_result = next(scanning_generator)
#             cart = generate_cartesian(scan_result)
#             bool_map = generate_boolean_spacemap(cart[0], cart[1])
#             print(bool_map[0][:3])

#             del cart
#             del bool_map
            
#     except Exception as e:
#         print(f"Lidar scanning error: {e}")
#     finally:
#         lidar_obj.Disconnect()

def send_data(comm_obj:SerialCommunication):
    while True:
        comm_obj.write(1)

# def show_vision(cam_obj:PiCam, framerate):
#     delay = round(1 / framerate, 2)
#     while True:
#         frame = cam_obj.capture_frame()
#         print(f"Frame: {frame[0][0]}")
#         time.sleep(delay)

# def get_manual_command(web_obj:WebInterface):
#     global manual_command
#     while True:
#         cmd = int(web_obj.get_latest_message())
#         manual_command = web_to_serial_command[cmd]
#         print(cmd, end=" | ")
#         print(manual_command)
#         return manual_command

if __name__ == "__main__":

    web_url = "ws://192.168.29.219:8000"

    # connection_check = check_port_connection()
    # connection_status = connection_check[0]
    # lidar_port = connection_check[1]["lidar"]
    arduino_port = "/dev/ttyUSB1"
    drive_comm = SerialCommunication(
            port=arduino_port, 
            baud_rate=9600)
    drive_comm.send_repeating_data(1)
    # if connection_status:
    #     print(connection_check)
        
    #     drive_comm = SerialCommunication(
    #         port=arduino_port, 
    #         baud_rate=9600)
        
    #     camera = PiCam()
        
    #     interface = WebInterface(web_url)
    #     interface.start()

    #     lidar = PyLidar3.YdLidarX4(port=lidar_port)
    #     lidar.Connect()

    #     lidar_thread = threading.Thread(target=lidar_data, args=(lidar,))
    #     sercomm_process = multiprocessing.Process(target=send_data, args=(drive_comm,))
    #     vision_thread = threading.Thread(target=show_vision, args=(camera, 10, ))
    #     webcomm_thread = threading.Thread(target=get_manual_command, args=(interface, ))
        
    #     try:
    #         lidar_thread.start()
    #         sercomm_process.start()
    #         vision_thread.start()
    #         webcomm_thread.start()

    #         lidar_thread.join()
    #         sercomm_process.join()
    #         vision_thread.join()
    #         webcomm_thread.start()

    #     except KeyboardInterrupt:
    #         for i in range(4):
    #             drive_comm.write(1)
    #             time.sleep(0.1)

    #         lidar_thread.join()
    #         sercomm_process.join()
    #         vision_thread.join()

    #         lidar.Disconnect()
    #         drive_comm.close_connection()

    # else: 
    #     print("Bad port connection!")
    #     exit()
