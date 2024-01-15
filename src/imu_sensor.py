import mpu6050
import time
import numpy as np

mpu6050 = mpu6050.mpu6050(0x68)

def round_dict_values(input_dict):
    return {key: round(value, 3) for key, value in input_dict.items()}


# Define a function to read the sensor data
def read_sensor_data():
    accelerometer_data = round_dict_values(mpu6050.get_accel_data())
    gyroscope_data = round_dict_values(mpu6050.get_gyro_data())
    temperature = round(mpu6050.get_temp(), 2)
    return accelerometer_data, gyroscope_data, temperature

def calibrate_gyro(n_iter, interval):
    print("starting IMU...")
    time.sleep(2)
    print(f"IMU Initialized!\nExpected Duration: {n_iter * interval}s\nStarting calibration process...")
    time.sleep(0.2)
    start = time.time()
    np_sum = [0, 0, 0]
    for i in range(n_iter):
        gyro_data = mpu6050.get_gyro_data()
        gyro_arr = np.array([gyro_data["x"], gyro_data["y"], gyro_data["z"]])
        print(gyro_arr)
        np_sum += gyro_arr
        time.sleep(interval)
    calibration_value = np_sum / n_iter
    end = time.time() - start
    print(f"X, Y, Z Calibration Value: {calibration_value}")
    print(f"Duration: {end}s")

calibrate_gyro(100, 0.2)
