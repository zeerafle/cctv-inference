from flask import Blueprint
from prediction import predict_frame

prediction = Blueprint('prediction', __name__, template_folder='templates/prediction')


@prediction.route('/')
def home():
    return 'Prediction Home'


@prediction.route('/predict')
def predict():
    result = predict_frame()
    return result


@prediction.app_errorhandler(404)
def page_not_found(e):
    return '404 Not Found', 404
