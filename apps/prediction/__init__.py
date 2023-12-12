from flask import Blueprint

bp = Blueprint("prediction", __name__, template_folder="../templates/prediction")

from apps.prediction import routes

# pylama:ignore=W0611
