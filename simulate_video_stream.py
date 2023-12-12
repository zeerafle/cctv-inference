import time

from flask import (
    Flask,
    Response,
    stream_with_context,
)

app = Flask(__name__)


def stream_video():
    # dummy video to serve as stream
    video_path = "Car accident Caught CCTV India _2.mp4"
    with open(video_path, "rb") as video_file:
        while True:
            chunk: bytes = video_file.read(1024)
            if not chunk:
                break
            yield chunk
            time.sleep(0.04)


@app.route("/")
def index():
    return "Stream Video API"


@app.route("/api/video_feed")
def video_feed():
    return Response(stream_with_context(stream_video()), mimetype="video/mp4")


if __name__ == "__main__":
    app.run(debug=True)
