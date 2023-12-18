import picamera

def capture_single_frame(camera, filename="image.jpg"):
  """
  Captures a single frame from the Raspberry Pi camera and saves it to the specified filename.

  Args:
    camera: RaspberryPiCamera object initialized with desired resolution and settings.
    filename (str): Path and filename to save the captured image.
  """
  # Warm up the camera
  print("Warming up camera...")
  camera.start_preview()
  sleep(2)

  # Capture and save the frame
  print("Capturing frame...")
  camera.capture(filename)

  # Stop preview and close camera
  print("Cleaning up...")
  camera.stop_preview()
  camera.close()

# Example usage
camera = picamera.RaspberryPiCamera(resolution=(1280, 720))
capture_single_frame(camera, "captured_frame.jpg")

print("Frame captured successfully!")
