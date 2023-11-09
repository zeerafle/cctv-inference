from flask import Flask, jsonify, request, render_template, Response, stream_with_context
import time

app = Flask(__name__)


def stream_video():  # put application's code here
    # if 'video' not in request.files:
    #     return 'no file part'
    #
    # video_file = request.files['video']
    # if video_file.filename == '':
    #     return 'no selected file'
    #
    with open('Car accident Caught CCTV India _2.mp4', 'rb') as video_file:
        while True:
            chunk: bytes = video_file.read(1024)
            if not chunk:
                break
            yield chunk
            time.sleep(0.04)


@app.route('/')
def index():
    return 'Stream Video API'


@app.route('/api/video_feed')
def video_feed():
    return Response(stream_with_context(stream_video()),
                    mimetype='video/mp4')


if __name__ == '__main__':
    app.run(debug=True)
