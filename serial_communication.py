import serial
import time

class SerialCommunication:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.connection = serial.Serial(
            port=self.port, 
            baudrate = self.baud_rate, 
            timeout = 1)
        
    def write(self, data):
        data_to_send = str(data)
        self.connection.write(data_to_send.encode())

    def send_integer(self):
        for i in range(20):
            self.write(i)
            time.sleep(1)
    
    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    com = SerialCommunication("/dev/ttyUSB0", 9600)
    time.sleep(2)
    com.send_integer()
    time.sleep(0.5)
    print("done")
    time.sleep(0.5)
    com.close_connection()
    