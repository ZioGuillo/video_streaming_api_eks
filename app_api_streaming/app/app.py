import os, time
import asyncio
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
import aioredis

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Redis setup without decoding the responses
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'default_redis_password_if_not_set')
redis = aioredis.from_url(
    "redis://127.0.0.1:6379",
    password=REDIS_PASSWORD
    # Removed encoding and decode_responses
)

# Global frame id
frame_id = 0

async def store_frame_in_redis(frame_data):
    global frame_id
    key = f"frame:{frame_id}"
    await redis.set(key, frame_data)
    frame_id += 1
    return key

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    resized_frame = cv2.resize(frame, (640, 480))

    _, buffer = cv2.imencode('.jpg', resized_frame)
    await store_frame_in_redis(buffer.tobytes())

    return {"message": "Frame received"}

async def gen_frames():
    last_frame_id = -1

    while True:
        await asyncio.sleep(0.01)  # Prevent high CPU usage
        current_frame_id = frame_id - 1
        if current_frame_id != last_frame_id:
            frame_key = f"frame:{current_frame_id}"
            frame_data = await redis.get(frame_key)
            if frame_data:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
                last_frame_id = current_frame_id

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "cache_buster": time.time()})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
