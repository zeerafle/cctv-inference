from flask import Flask, jsonify, request, render_template, Response
from apps.prediction import bp as prediction_bp


def create_app():
    app = Flask(__name__)

    # register blueprint
    app.register_blueprint(prediction_bp, url_prefix='/prediction')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
