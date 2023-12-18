import serial
import time

class SerialCommunication:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.connection = serial.Serial(
            port=self.port,
            baudrate=self.baud_rate,
            timeout=1)

    def write(self, data):
        print(data)
        data_to_send = str(data)
        self.connection.write(data_to_send.encode())

    def send_repeating_data(self, interval):
        data_sequence = [2, 3, 4, 5]
        for i in range(20):
            for data in data_sequence:
                self.write(data)
                time.sleep(interval)

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    com = SerialCommunication("/dev/ttyUSB1", 9600)
    interval = 3
    command_set = False
    for i in range(10):
        for j in range(4):
            command = j + 1
            print(command)
            com.write(command)
            time.sleep(3)
        print(i)


class Lidar:
    def __init__(self) -> None:
        pass