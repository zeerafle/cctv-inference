import redis
import rq
from flask import Flask, render_template

from apps.prediction import bp as prediction_bp
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.redis = redis.Redis()
    app.task_queue = rq.Queue("saving-tasks", connection=app.redis)

    # register blueprint
    app.register_blueprint(prediction_bp, url_prefix="/prediction")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
