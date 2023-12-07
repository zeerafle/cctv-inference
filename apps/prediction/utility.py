import tensorflow as tf
import numpy as np
import cv2
from bs4 import BeautifulSoup
from selenium import webdriver

model = tf.keras.models.load_model('model.h5', compile=False)
CCTV_BASE_URL = 'https://diskominfo.samarindakota.go.id/api/cctv/'


def make_stream_url(identifier):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.get(CCTV_BASE_URL + identifier)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    stream_url = soup.find('video')['src']
    driver.quit()
    return stream_url


def predictions(identifier):
    cap = cv2.VideoCapture(make_stream_url(identifier))
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        result = predict_frame(frame)
        print(result)
        yield f'data: {result}\n\n'


def predict_frame(img):
    img = tf.keras.preprocessing.image.smart_resize(img, (250, 250), interpolation='bilinear')
    img_array = tf.keras.utils.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    prediction = (model.predict(img_batch) > 0.5).astype('int32')
    if prediction[0][0] == 0:
        return 'Terjadi kecelakaan'
    else:
        return 'Normal'
