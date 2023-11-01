from flask import Flask, jsonify, request, render_template, Response
import tensorflow as tf
import numpy as np
import cv2

model = tf.keras.models.load_model('model.h5')
pred_class = ''

app = Flask(__name__)

def predict_frame(img):
    img_array = tf.keras.utils.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    prediction = (model.predict(img_batch) > 0.5).astype('int32')
    if prediction[0][0] == 0:
        return 'Terjadi kecelakaan'
    else:
        return 'Normal'

def generate_prediction():  # put application's code here
    global pred_class
    # if 'video' not in request.files:
    #     return 'no file part'
    #
    # video_file = request.files['video']
    # if video_file.filename == '':
    #     return 'no selected file'
    #
    cap = cv2.VideoCapture('Car accident Caught CCTV India _2.mp4')
    while True:
        grabbed, frame = cap.read()
        if not grabbed:
            break

        resized_frame = tf.keras.preprocessing.image.smart_resize(frame, (250, 250), interpolation='bilinear')
        pred_class = predict_frame(resized_frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break
        yield b'--frame\r\n'
        yield b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n'
        # yield b'<p>' + prediction.encode('utf-8') + b'</p>\r\n'
        # yield f'prediction: {prediction}\r\n'
        # yield f'prediction: {prediction}'


def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_prediction(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/prediction_text')
# def prediction_text():
#     def generate():
#         yield pred_class
#     return Response(generate(), mimetype='text')

if __name__ == '__main__':
    app.run()
