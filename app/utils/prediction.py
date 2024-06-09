from dotenv import load_dotenv
import json

from .model import load_model
from .saving import save_frame
import cv2
import torch

from fastapi import BackgroundTasks

load_dotenv()

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
CONFIDENCE_TRESHOLD = 0.5
processor, model = load_model()


def inference(image):
    # load image and predict
    inputs = processor(images=image, return_tensors='pt').to(DEVICE)
    outputs = model(**inputs)

    # post-process
    target_sizes = torch.tensor([image.shape[:2]]).to(DEVICE)
    return processor.post_process_object_detection(
        outputs=outputs,
        threshold=CONFIDENCE_TRESHOLD,
        target_sizes=target_sizes
    )[0]


def predict(cap, identifier, background_tasks: BackgroundTasks):
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = inference(rgb_frame)
        results_json = {key: value.tolist() for key, value in results.items() if isinstance(value, torch.Tensor)}

        print("transformer result", results_json)
        # background_tasks.add_task(
        #     save_frame,
        #     frame,
        #     results,
        #     identifier
        # )
        yield f"data: {json.dumps(results_json)}\n\n"
