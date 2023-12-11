import serial
import time
import re

port = "COM8"
baud_rate = 128000
data_bits = 8
stop_bits = 1
parity = serial.PARITY_NONE

lidar_command = {
    "start_scan":"A5 60", 
    "stop_scan":"A5 65", 
    "get_info":"A5 90", 
    "get_health":"A5 91", 
    "soft_restart":"A5 80", 
}

hex_re = re.compile(r'\s+')

class Lidar:
    def __init__(self):
        self.serial = False
        self.delimiter = "AA55"
        
    def connect(self, port, baud_rate, byte_size, parity, stop_bits, timeout):
        self.serial = serial.Serial(
            port, 
            baud_rate, 
            bytesize=byte_size, 
            parity=parity, 
            stopbits=stop_bits, 
            timeout=timeout)
        self.is_connected = True

    def send_command(self, command):
        if command in lidar_command:
            command_hex = lidar_command[command]
            data_bytes = bytes.fromhex(hex_re.sub('', command_hex))
            self.serial.write(data_bytes)
            response = self.serial.read_until().hex().upper()
            return response
        else:
            return None
    
    def split_response(self, response):    
        content_groups = re.findall(r'(?s)AA55(.*?)AA55', response)
        complete_groups = [group for group in content_groups if len(group) % 2 == 0]
        complete_groups_with_delimiter = ["AA55" + group for group in complete_groups]
        return complete_groups_with_delimiter
    
    def little_endian(self, split_response):
        bytes_list = [split_response[i:i+2] for i in range(0, len(split_response), 2)]
        little_endian_list = [bytes_list[i+1] + bytes_list[i] for i in range(0, len(bytes_list), 2)]
        result_str = ''.join(little_endian_list)
        return result_str
        
    def start_scan(self):
        while True: 
            raw_response = self.send_command("start_scan")
            split_response = self.split_response(raw_response)
            n = len(split_response)
            if n == 0: continue
            print(n, split_response)
            print()

if __name__ == "__main__":
    ydl = Lidar()
    ydl.connect(
        port=port, 
        baud_rate=baud_rate, 
        byte_size=data_bits, 
        parity=parity, 
        stop_bits=stop_bits, 
        timeout=1
    )
    ydl.start_scan()