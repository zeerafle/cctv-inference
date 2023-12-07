from flask import Blueprint, Response, render_template, stream_with_context

bp = Blueprint('prediction', __name__, template_folder='templates/prediction')

from apps.prediction import routes
