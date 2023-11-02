from flask import Flask, jsonify, request, render_template, Response
from apps.prediction.views import prediction


def create_app():
    app = Flask(__name__)

    # register blueprint
    prediction.register_blueprint(prediction)

    return app


if __name__ == '__main__':
    create_app().run()
