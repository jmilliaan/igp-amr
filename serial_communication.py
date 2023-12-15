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
    start = time.time()
    while True:
        if not command_set:
            command = int(input("Enter command: "))
            command_set = True
        com.write(command)
        duration = time.time() - start
        if duration >= interval:
            start = time.time()
            command_set = False
            command = 1
            com.write(1)