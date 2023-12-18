import picamera

class RaspberryPiCamera:
    def __init__(self, resolution=(1280, 720), framerate=30):
        """
        Initialize the Raspberry Pi camera with specified resolution and framerate.

        Args:
            resolution (tuple): Resolution of the captured image/video (width, height).
            framerate (int): Frames per second for video capture.
        """
        self.camera = picamera.PiCamera(resolution=resolution, framerate=framerate)

    def capture_continuous(self, callback_function):
        """
        Capture frames continuously and call the provided callback function for each frame.

        Args:
            callback_function: Function to be called with each captured frame as an argument.
        """
        # Start capturing frames
        for frame in self.camera.capture_continuous(format="bgr", use_video_port=True):
            # Pass the frame to the callback function
            callback_function(frame)

    def adjust_camera_settings(self, **kwargs):
        """
        Adjust camera settings like ISO, contrast, saturation, etc.

        Args:
            **kwargs: Key-value pairs of camera settings and their values to adjust.
        """
        for key, value in kwargs.items():
            self.camera.brightness = value if key == "brightness" else getattr(self.camera, key, value)

    def preview_stream(self, window_name="Raspberry Pi Camera Stream"):
        
        cv2.namedWindow(window_name)
        while True:
            frame = self.camera.capture_continuous(use_video_port=True)
            frame = next(frame.frames)
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cv2.destroyAllWindows()

    def close_camera(self):
        """
        Release resources and close the camera.
        """
        self.camera.close()

# Example usage
def process_frame(frame):
    # Implement your frame processing logic here
    # For example, perform object detection, track motion, etc.
    # (This example simply displays the frame size)
    print(f"Frame size: {frame.array.shape[:2]}")

camera = RaspberryPiCamera()

# Start continuous capture and use your custom processing function
camera.preview_stream()
