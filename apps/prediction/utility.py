import requests
import tensorflow as tf
import numpy as np
import cv2

from bs4 import BeautifulSoup
from flask import current_app
from selenium import webdriver

import json

from apps.saving.uploads import save_frame

model = tf.keras.models.load_model("model.h5", compile=False)
CCTV_BASE_URL = "https://diskominfo.samarindakota.go.id/api/cctv/"
with open("stream_url.json") as f:
    stream_urls = json.load(f)


def write_stream_url(identifier, stream_url):
    stream_urls[identifier] = stream_url
    with open("stream_url.json", "w") as f:
        json.dump(stream_urls, f)


def make_stream_url(identifier):
    if stream_urls.get(identifier) is not None and stream_urls[identifier]:
        return stream_urls[identifier]
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(CCTV_BASE_URL + identifier)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    stream_url = soup.find("video")["src"]
    driver.quit()
    write_stream_url(identifier, stream_url)
    return stream_url


def predictions(identifier):
    req = requests.get(CCTV_BASE_URL + identifier)
    if req.status_code != 200:
        yield "CCTV not found"
    cap = cv2.VideoCapture(make_stream_url(identifier))
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        result = predict_frame(frame)
        with current_app.app_context():
            current_app.task_queue.enqueue(
                save_frame,
                frame,
                result,
                identifier,
                current_app.config["BUCKET_NAME"],
                current_app.config["AWS_ACCESS_KEY_ID"],
                current_app.config["AWS_SECRET_ACCESS_KEY"],
            )
        print(result)
        yield f"data: {result}\n\n"


def predict_frame(img):
    img = tf.keras.preprocessing.image.smart_resize(
        img, (250, 250), interpolation="bilinear"
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    prediction = (model.predict(img_batch) > 0.5).astype("int32")
    if prediction[0][0] == 0:
        return "accident"
    else:
        return "normal"
