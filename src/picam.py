import picamera
import cv2

class RaspberryPiCamera:
    def __init__(self, resolution=(1280, 720), framerate=30):
        self.camera = picamera.PiCamera(resolution=resolution, framerate=framerate)

    def capture_image(self, filename="image.jpg"):
        self.camera.capture(filename)

    def start_recording(self, filename="video.h264"):
        self.camera.start_recording(filename)

    def stop_recording(self):
        self.camera.stop_recording()

    def adjust_camera_settings(self, **kwargs):
        for key, value in kwargs.items():
            self.camera.brightness = value if key == "brightness" else getattr(self.camera, key, value)

    def preview_stream(self, window_name="Raspberry Pi Camera Stream"):
        cv2.namedWindow(window_name)
        while True:
            frame = self.camera.capture_continuous(format="bgr", use_video_port=True).next()
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cv2.destroyAllWindows()

    def close_camera(self):
        self.camera.close()

# Check camera functionality if script is directly run
if __name__ == "__main__":
    # Create camera object
    camera = RaspberryPiCamera()

    # Preview camera stream for 5 seconds
    print("Previewing camera stream for 5 seconds...")
    camera.preview_stream()
    cv2.waitKey(5000)

    # Capture an image for confirmation
    print("Capturing test image...")
    camera.capture_image("camera_test.jpg")

    # Print success message and close camera
    print("Camera functionality test successful!")
    camera.close()
