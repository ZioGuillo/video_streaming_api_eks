import cv2
import requests
import threading
import time
from requests.exceptions import RequestException

# Configuration
endpoint_base = "http://endpoint:port"
api_endpoint = f"{endpoint_base}/upload"
max_retries = 5
retry_delay = 1  # seconds in between retries

# Global flags
streaming = False
exit_flag = False

def camera_thread():
    global streaming, exit_flag
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit_flag = True
        return

    while not exit_flag:
        if not streaming:
            time.sleep(1)
            continue

        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        _, jpeg = cv2.imencode('.jpg', frame)

        for attempt in range(max_retries):
            try:
                response = requests.post(api_endpoint, files={'file': jpeg.tobytes()}, timeout=5)
                if response.status_code == 200:
                    print("Frame sent successfully")
                    break
            except RequestException as e:
                print(f"An error occurred: {e}")
                print(f"Attempting to reconnect... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
        else:
            print("Failed to reconnect after several attempts.")
            break

        cv2.waitKey(200)

    cap.release()
    print("Camera and streaming stopped.")

def control_thread():
    global streaming, exit_flag
    while not exit_flag:
        command = input("Enter command (start, stop, exit): ").strip().lower()
        if command == "start":
            streaming = True
            print("Streaming started.")
        elif command == "stop":
            streaming = False
            print("Streaming stopped.")
        elif command == "exit":
            streaming = False
            exit_flag = True
            print("Exiting...")

if __name__ == "__main__":
    # Start the camera and control threads
    threading.Thread(target=camera_thread, daemon=True).start()
    control_thread()
