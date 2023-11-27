import time
from flask import Flask, Response, request, render_template
import cv2
import threading
import queue
import numpy as np
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Initialize metrics exporter
metrics = PrometheusMetrics(app) # export metrics to /metrics endpoint
metrics.info('app_info', 'Application info', version='1.0.3', app_name='app_api_streaming')

@app.get('/health')
def health():
    return {"status" : "UP"}

# Queue to store frames
frame_queue = queue.Queue(maxsize=50)  # Adjust maxsize based on your needs

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file'].read()
    nparr = np.frombuffer(file, np.uint8)  # Convert buffer to numpy array
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Decode image

    # Resize the frame to SD resolution
    sd_frame = cv2.resize(frame, (640, 480))

    # Process the resized frame as needed
    # ...

    # Example: Add resized frame to a queue for streaming
    if not frame_queue.full():
        frame_queue.put(sd_frame)
    else:
        print("Dropping frame as the buffer is full")

    return 'Frame received', 200


def capture_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if not frame_queue.full():
            frame_queue.put(frame)
        else:
            print("Dropping frame as the buffer is full")

def clear_buffer():
    while True:
        time.sleep(10)  # Increase the sleep time to avoid clearing too frequently
        while not frame_queue.empty():
            frame_queue.get()

def gen_frames():
    frame_rate = 10  # Adjust frame rate if needed
    last_frame_time = 0

    while True:
        while frame_queue.empty():
            time.sleep(0.01)

        current_time = time.time()
        if (current_time - last_frame_time) < 1.0 / frame_rate:
            continue

        frame = frame_queue.get()
        resized_frame = cv2.resize(frame, (640, 480))
        ret, buffer = cv2.imencode('.jpg', resized_frame)
        if not ret:
            continue

        last_frame_time = current_time
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n'
               b'Cache-Control: no-cache, no-store, must-revalidate\r\n'
               b'Pragma: no-cache\r\n'
               b'Expires: 0\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html', cache_buster=time.time())

if __name__ == '__main__':
    app.run(debug=True, threaded=True,host='0.0.0.0', port=5000)
    buffer_clear_thread = threading.Thread(target=clear_buffer, daemon=True)
    buffer_clear_thread.start()
    frame_capture_thread = threading.Thread(target=capture_frames, daemon=True)
    frame_capture_thread.start()
