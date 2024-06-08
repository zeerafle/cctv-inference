import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model("model.h5", compile=False)


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


def predict(cap):
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        result = predict_frame(frame)
        # with current_app.app_context():
        #     current_app.task_queue.enqueue(
        #         save_frame,
        #         frame,
        #         result,
        #         identifier,
        #         current_app.config["BUCKET_NAME"],
        #         current_app.config["AWS_ACCESS_KEY_ID"],
        #         current_app.config["AWS_SECRET_ACCESS_KEY"],
        #     )
        print(result)
        yield f"data: {result}\n\n"
