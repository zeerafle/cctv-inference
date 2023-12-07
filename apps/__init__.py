from flask import Flask, jsonify, request, render_template, Response
from apps.prediction import bp as prediction_bp


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Inference API. To view prediction, go to <a href="/prediction">/prediction</a>'

    # register blueprint
    app.register_blueprint(prediction_bp, url_prefix='/prediction')

    return app
