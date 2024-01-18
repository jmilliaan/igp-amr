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
import adafruit_rplidar
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

def setup_serial_port():
    connections = {"lidar": None, "arduino": None}
    ports = glob.glob("/dev/ttyUSB*")
    n_ports = len(ports)
    print(f"SERIAL PORTS: {ports}")

    if n_ports >= 1:
        connections["arduino"] = ports[0]
        connections["lidar"] = ports[1] if n_ports > 1 else None

    if connections["lidar"]:
        try:
            test_conn = adafruit_rplidar.RPLidar(None, connections["lidar"], timeout=3)
            if isinstance(test_conn.health, tuple):
                pass
            else:
                connections["lidar"], connections["arduino"] = connections["arduino"], connections["lidar"]
            del test_conn
        except adafruit_rplidar.RPLidarException:
            connections["lidar"], connections["arduino"] = connections["arduino"], connections["lidar"]

    return connections["arduino"], connections["lidar"]


if __name__ == "__main__":
    arduino_port, lidar_port = setup_serial_port()
    print(arduino_port, lidar_port)
