import asyncio
import time
import cv2
import threading
import queue
import numpy as np
from fastapi import FastAPI, File, Request, UploadFile, Response
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
import aioredis

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Queue to store frames
frame_queue = queue.Queue(maxsize=50)

# Set up Redis for caching (adjust connection details as needed)
redis = aioredis.from_url("redis://redis-service:6379", encoding="utf-8", decode_responses=True)


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    sd_frame = cv2.resize(frame, (640, 480))

    # Process the resized frame as needed
    # ...

    if not frame_queue.full():
        frame_queue.put(sd_frame)
    else:
        print("Dropping frame as the buffer is full")

    return {"message": "Frame received"}


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
        time.sleep(10)
        while not frame_queue.empty():
            frame_queue.get()


async def gen_frames():
    frame_rate = 10
    last_frame_time = 0

    while True:
        while frame_queue.empty():
            await asyncio.sleep(0.01)

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


@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


@app.get("/")
async def index(request: Request):  # accept the request object as a parameter
    return templates.TemplateResponse("index.html", {"request": request, "cache_buster": time.time()})


if __name__ == "__main__":
    buffer_clear_thread = threading.Thread(target=clear_buffer, daemon=True)
    buffer_clear_thread.start()
    frame_capture_thread = threading.Thread(target=capture_frames, daemon=True)
    frame_capture_thread.start()
