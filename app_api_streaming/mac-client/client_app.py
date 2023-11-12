import cv2
import requests
from requests.exceptions import RequestException
import time

cap = cv2.VideoCapture(0)
api_endpoint = 'http://127.0.0.1:5000/upload'
max_retries = 5
retry_delay = 1  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    _, jpeg = cv2.imencode('.jpg', frame)

    for attempt in range(max_retries):
        try:
            response = requests.post(api_endpoint, files={'file': jpeg.tobytes()}, timeout=5)
            if response.status_code == 200:
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
