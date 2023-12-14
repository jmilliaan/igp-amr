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
    com = SerialCommunication("/dev/ttyUSB0", 9600)
    interval = 2
    while True:
        start = time.time()
        print("2: Forward, 3: Reverse, 4: Right, 5: Left")
        order = int(input("Enter direction: "))
        com.write(order)
        if time.time() - start >= interval:
            continue
