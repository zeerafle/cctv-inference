from flask import render_template, Response, stream_with_context

from apps.prediction import utility
from apps.prediction import bp


@bp.route("/")
def index():
    return render_template("prediction.html")


@bp.route("/<identifier>")
def home(identifier):
    return render_template("prediction.html", identifier=identifier)


@bp.route("/sse/<identifier>")
def sse(identifier):
    return Response(
        stream_with_context(utility.predictions(identifier)),
        mimetype="text/event-stream",
    )


@bp.app_errorhandler(404)
def page_not_found(e):
    return "404 Not Found", 404
