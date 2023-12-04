from flask import Flask, jsonify, request, render_template, Response
from apps.prediction.views import prediction


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Inference API. To view prediction, go to <a href="/prediction">/prediction</a>'

    # register blueprint
    app.register_blueprint(prediction, url_prefix='/prediction')

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
