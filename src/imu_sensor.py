import mpu6050
import time
import numpy as np

mpu6050 = mpu6050.mpu6050(0x68)
# Calibration Value (15 Jan 2024, 100 iteration, 200ms Interval)
gyro_calibration = np.array([13.63114504, -51.42854962, 96.85770992])
accel_calibration = (-0.4018109322449511, 2.227213520018861)

def round_dict_values(input_dict):
    return {key: round(value, 3) for key, value in input_dict.items()}

def get_accel_calibrated(calibration_value):
    m = calibration_value[0]
    b = calibration_value[1]
    az = mpu6050.get_accel_data()["z"]
    az_offset = az * m + b
    az_calibrated = az - az_offset
    return az_calibrated

def read_sensor_data():
    accelerometer_data = round_dict_values(mpu6050.get_accel_data())
    gyroscope_data = round_dict_values(mpu6050.get_gyro_data())
    temperature = round(mpu6050.get_temp(), 2)
    return accelerometer_data, gyroscope_data, temperature

def get_linear_acceleration():
    ax=mpu6050.get_accel_data()["x"]
    ay=mpu6050.get_accel_data()["y"]
    az=mpu6050.get_accel_data()["z"]
    return ax, ay, az

def linear_calibration(calibration_time=5, axis=2):
    num_of_points = 0
    x_sum = 0
    y_sum = 0
    x_squared_sum = 0
    x_times_y_sum = 0
    print('-' * 50)
    print('Orient the axis upwards against gravity - Click Enter When Ready' )
    # Gravity should be 1g in this scenerio
    x = input()
    end_loop_time = time.time() + calibration_time
    print('Beginning to Calibrate Part 1 (Acceleration = 1g) for %d seconds' % calibration_time)
    # We end the loop once the calibration time has passed
    
    while end_loop_time > time.time():
        
        num_of_points += 1
        offset = get_linear_acceleration()[axis] - 1
        
        x_sum += 1
        y_sum += offset
        x_squared_sum += 1
        x_times_y_sum += 1 * offset

        if num_of_points % 100 == 0:
            print('Still Calibrating Gyro... %d points so far' % num_of_points)
            
    print('-' * 50)
    print('Orient the axis downwards against gravity - Click Enter When Ready' )
    # Gravity should be 1g in this scenerio
    x = input()
    end_loop_time = time.time() + calibration_time
    print('Beginning to Calibrate Part 2 (Acceleration = -1g) for %d seconds' % calibration_time)
    # We end the loop once the calibration time has passed

    while end_loop_time > time.time():
        
        num_of_points += 1
        offset = get_linear_acceleration()[axis] + 1
        # Because acceleration should be -1g
        x_sum += (-1 * 1)
        y_sum += offset
        x_squared_sum += (-1 * 1) * (-1 * 1)
        x_times_y_sum += (-1 * 1) * offset

        if num_of_points % 100 == 0:
            print('Still Calibrating Gyro... %d points so far' % num_of_points)
    
    print('-' * 50)
    print('Orient the axis perpendicular against gravity - Click Enter When Ready' )
    # Gravity should be 1g in this scenerio
    x = input()
    end_loop_time = time.time() + calibration_time
    print('Beginning to Calibrate Part 3 (Acceleration = 0g) for %d seconds' % calibration_time)
    # We end the loop once the calibration time has passed

    while end_loop_time > time.time():
        
        num_of_points += 1
        # Just showing the zero for consistency purposes
        offset = get_linear_acceleration()[axis] + 0
        # Because acceleration should be -1g
        x_sum += 0
        y_sum += offset
        x_squared_sum += (0) * (0)
        x_times_y_sum += (0) * offset

        if num_of_points % 100 == 0:
            print('Still Calibrating Gyro... %d points so far' % num_of_points)
            
    # now I just utilize the equation for m and b in least sqaures theory
    m = (num_of_points * x_times_y_sum - (x_sum * y_sum)) / ((num_of_points * x_squared_sum) - (x_sum)**2)
    b = (y_sum - (m * x_sum)) / num_of_points
    
    return m, b


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

if __name__ == "__main__":
    print(linear_calibration())