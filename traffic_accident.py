import tensorflow as tf
import cv2
import numpy as np

model = tf.keras.models.load_model(r"E:\Semester 7\Hackaton\Traffic Accident\model.h5")


def predict_frame(img):
    img_array = tf.keras.utils.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    prediction = (model.predict(img_batch) > 0.5).astype("int32")
    if prediction[0][0] == 0:
        return "Accident Detected"
    else:
        return "No Accident"


image = []
label = []
savepath = "prediction.mp4"

# c=1
i = 1
cap = cv2.VideoCapture(
    r"E:\Semester 7\Hackaton\Traffic Accident\Viral- Horrific Pedestrian accident caught on Camera - Cyberabad Traffic Police.mp4"
)
fourcc = cv2.VideoWriter_fourcc(*"H264")
out = cv2.VideoWriter(savepath, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))), 1)
while i < 1300:
    i += 1
    grabbed, frame = cap.read()
    # if c%30==0:
    # print(c)

    if not grabbed:
        continue
    resized_frame = tf.keras.preprocessing.image.smart_resize(
        frame, (250, 250), interpolation="bilinear"
    )
    # image.append(frame)
    # label.append(predict_frame(resized_frame))
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(
        frame, predict_frame(resized_frame), (50, 50), font, 2, (255, 255, 255), 2
    )

    out.write(frame)
    cv2.imshow("My Frame", frame)
    ch = cv2.waitKey(1)
    #     if(len(image)==75):
    #         break
    # c+=1

cap.release()
out.release()
