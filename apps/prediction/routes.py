from flask import render_template, Response, stream_with_context

from apps.prediction import utility
from apps.prediction import bp

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/sse')
def sse():
    return Response(stream_with_context(utility.predictions()), mimetype='text/event-stream')

@bp.app_errorhandler(404)
def page_not_found(e):
    return '404 Not Found', 404