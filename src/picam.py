import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

class PiCam:
    def __init__(self, resolution=(640, 480), framerate=15):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.raw_capture = PiRGBArray(self.camera, size=resolution)

    def show_image(self, save_to_png=False):
        self.camera.capture(self.raw_capture, format="bgr")
        image = self.raw_capture.array

        if save_to_png:
            cv2.imwrite("captured_image.png", image)

        cv2.imshow("Captured Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def show_live_stream(self):
        for frame in self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):
            image = cv2.flip(frame.array, 0)
            print(image[:4])
            # cv2.imshow("Live Stream", image)
            key = cv2.waitKey(1) & 0xFF

            # self.raw_capture.truncate(0)

            if key == ord("q"):
                break

    def __del__(self):
        self.camera.close()

