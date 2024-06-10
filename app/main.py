from fastapi import FastAPI, BackgroundTasks, Request, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from app.utils.model import load_model
from app.utils.prediction import predict

import cv2
import json
import logging

app = FastAPI()

cap = {}
processor = None
model = None
origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://master.diuxi4un1be14.amplifyapp.com/",
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
async def initialize():
    global cap, processor, model
    with open("app/stream_url.json") as f:
        stream_urls = json.load(f)
    for identifier, stream_url in stream_urls.items():
        cap[identifier] = cv2.VideoCapture(stream_url)
    logging.info("Video capture object created")
    processor, model = load_model()
    logging.info("Model loaded")


@app.get("/")
def main():
    return {"message": "CCTV Accident Inference API is running!"}


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.post("/invocations")
def invocations(request: Request, background_tasks: BackgroundTasks):
    cctv_id = request.query_params["identifier"]
    return StreamingResponse(
        predict(request, processor, model, cap[cctv_id], cctv_id, background_tasks),
        status_code=status.HTTP_200_OK,
        media_type="text/event-stream",
    )
