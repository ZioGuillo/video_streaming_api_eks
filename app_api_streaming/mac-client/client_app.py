import cv2
import requests
from requests.exceptions import RequestException
import time

# Configuration
endpoint_base = "http://endpoind:port"
api_endpoint = f"{endpoint_base}/upload"
max_retries = 5
retry_delay = 1  # seconds in between retries
streaming = False

def start_streaming():
    global streaming
    streaming = True

def stop_streaming():
    global streaming
    streaming = False

# Initialize the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Start streaming initially
start_streaming()

while True:
    if not streaming:
        print("Streaming is paused. Waiting to resume...")
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
        print("Failed to reconnect after several attempts. Exiting.")
        break

    cv2.waitKey(200)

cap.release()
