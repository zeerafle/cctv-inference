from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from app.utils.prediction import predict

import cv2
import json

cap = {}
app = FastAPI()


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
def read_sse(cctv_id: str):
    return StreamingResponse(predict(cap[cctv_id]), media_type="text/event-stream")
