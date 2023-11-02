import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('model.h5')


def predict_frame(img):
    img = tf.keras.preprocessing.image.smart_resize(img, (250, 250), interpolation='bilinear')
    img_array = tf.keras.utils.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    prediction = (model.predict(img_batch) > 0.5).astype('int32')
    if prediction[0][0] == 0:
        return 'Terjadi kecelakaan'
    else:
        return 'Normal'
