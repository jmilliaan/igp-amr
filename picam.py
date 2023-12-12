import picamera
import picamera.array
import cv2

def main():
    with picamera.PiCamera() as camera:
        # Set camera resolution (adjust as needed)
        camera.resolution = (640, 480)

        # Create an OpenCV window
        cv2.namedWindow("Raspberry Pi Camera", cv2.WINDOW_NORMAL)

        try:
            with picamera.array.PiRGBArray(camera) as stream:
                while True:
                    camera.capture(stream, format="bgr", use_video_port=True)
                    image = stream.array
                    cv2.imshow("Raspberry Pi Camera", image)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                    # Clear the stream buffer to prepare for the next frame
                    stream.truncate(0)

        finally:
            # Release resources when the script is terminated
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
