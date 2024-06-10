from fastapi import FastAPI, Request, BackgroundTasks, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from app.model.invocation import InvocationRequest
from app.utils.model import load_model
from app.utils.prediction import predict

import cv2
import json
import logging

app = FastAPI()

cap = {}
processor = None
model = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
def invocations(
    request: Request, invocation: InvocationRequest, background_tasks: BackgroundTasks
):
    identifier = invocation.identifier
    return StreamingResponse(
        predict(
            request, processor, model, cap[identifier], identifier, background_tasks
        ),
        status_code=status.HTTP_200_OK,
        media_type="text/event-stream",
    )
