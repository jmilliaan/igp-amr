import mpu6050
import time

# Create a new Mpu6050 object
mpu6050 = mpu6050.mpu6050(0x68)

def round_dict_values(input_dict):
    return {key: round(value, 2) for key, value in input_dict.items()}


# Define a function to read the sensor data
def read_sensor_data():
    accelerometer_data = round_dict_values(mpu6050.get_accel_data())
    gyroscope_data = round_dict_values(mpu6050.get_gyro_data())
    temperature = round(mpu6050.get_temp(), 2)
    return accelerometer_data, gyroscope_data, temperature


while True:
    accelerometer_data, gyroscope_data, temperature = read_sensor_data()
    print("Accelerometer data:", accelerometer_data)
    print("Gyroscope data:", gyroscope_data)
    print("Temp:", temperature, 2)
    print()
    # Wait for 1 second
    time.sleep(0.5)