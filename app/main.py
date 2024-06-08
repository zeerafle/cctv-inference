from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from app.utils.prediction import predict, predict_frame

import cv2
import json

import psutil

app = FastAPI()

cap = {}
origins = [
    "http://localhost",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Function to initialize the video capture object
@app.on_event("startup")
async def start_video_stream():
    global cap
    with open("app/stream_url.json") as f:
        stream_urls = json.load(f)
    for identifier, stream_url in stream_urls.items():
        cap[identifier] = cv2.VideoCapture(stream_url)


@app.get("/")
def main():
    return {"message": "CCTV Accident Inference API is running!"}


@app.get("/prediction/sse/{cctv_id}")
def read_sse(cctv_id: str, background_tasks: BackgroundTasks):
    return StreamingResponse(predict(cap[cctv_id], cctv_id, background_tasks), media_type="text/event-stream")


@app.get("/monitor/idle")
def monitor_idle():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    return {"CPU Usage": cpu_usage, "RAM Usage": ram_usage}


def simulate_request(cap, num_frames=10):
    for _ in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            continue
        result = predict_frame(frame)
        print(result)


@app.get("/monitor/request")
def monitor_request():
    # Simulate a request by predicting a certain number of frames
    simulate_request(cap["simpang-antasari-siradj-salman"])

    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    return {"CPU Usage": cpu_usage, "RAM Usage": ram_usage}
