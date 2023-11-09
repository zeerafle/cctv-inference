from flask import Blueprint, Response, render_template, stream_with_context
from apps.prediction.utility import predictions

prediction = Blueprint('prediction', __name__, template_folder='templates/prediction')


@prediction.route('/')
def home():
    return render_template('index.html')


@prediction.route('/sse')
def sse():
    return Response(stream_with_context(predictions()), mimetype='text/event-stream')


@prediction.app_errorhandler(404)
def page_not_found(e):
    return '404 Not Found', 404
