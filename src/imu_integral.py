import mpu6050
import time
import numpy as np

mpu6050 = mpu6050.mpu6050(0x68)
# Calibration Value (15 Jan 2024, 100 iteration, 200ms Interval)
gyro_calibration = np.array([13.6311, -51.4285, 96.8577])
accel_calibration = (-0.3906, 2.2161)


def accel():
    accel_data = mpu6050.get_accel_data()
    accel_arr = np.array([accel_data["x"], accel_data["y"], accel_data["z"]])
    return accel_arr

def gyro():
    gyro_data = mpu6050.get_gyro_data()
    gyro_arr =  np.array([gyro_data["x"], gyro_data["y"], gyro_data["z"]])
    return gyro_arr + gyro_calibration

def realtime_v(interval=0.02):
    a_prev = accel()
    v = np.zeros(3)
    try:
        while True:
            a_current = accel()
            v += (a_current + a_prev) * interval / 2
            print(f"V current = {v}")
            a_prev = a_current
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopped")

if __name__ == "__main__":
    realtime_v()