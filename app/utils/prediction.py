from dotenv import load_dotenv
import json

from starlette.requests import Request
import asyncio

from .saving import save_frame
import cv2
import torch

from fastapi import BackgroundTasks

load_dotenv()

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CONFIDENCE_TRESHOLD = 0.5


async def inference(processor, model, image):
    # load image and predict
    inputs = processor(images=image, return_tensors="pt").to(DEVICE)
    outputs = model(**inputs)

    # post-process
    target_sizes = torch.tensor([image.shape[:2]]).to(DEVICE)
    return processor.post_process_object_detection(
        outputs=outputs, threshold=CONFIDENCE_TRESHOLD, target_sizes=target_sizes
    )[0]


async def predict(
    request: Request,
    processor,
    model,
    cap,
    identifier,
    background_tasks: BackgroundTasks,
):
    should_continue = True

    # used to stop predict function when the client disconnects
    async def stop():
        nonlocal should_continue
        await request.is_disconnected()
        should_continue = False

    background_tasks.add_task(stop)

    while should_continue:
        ret, frame = cap.read()
        if not ret:
            continue
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = await inference(processor, model, rgb_frame)
        results_json = {
            key: value.tolist()
            for key, value in results.items()
            if isinstance(value, torch.Tensor)
        }

        print("transformer result", results_json)
        background_tasks.add_task(save_frame, frame, results_json, identifier)

        yield f"{json.dumps(results_json)}\n\n"

        await asyncio.sleep(0.1)
