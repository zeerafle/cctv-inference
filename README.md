# Accident Detection Inference API

## How to run

1. Install requirements (or create a virtual environment beforehand), e.g.:
    ```bash
    pip install -r requirements.txt
    ```
2. Prepare your own model, put it in root directory and name it `model.h5`
3. Prepare your own dummy accident video, remember the path.
4. Open `simulate_video_stream.py`, and change the `video_path` variable to your own video path.
5. Run the dummy video stream server to simulate the real-time video stream:
    ```bash
    flask --app simulate_video_stream.py run
    ```
6. Open another terminal, run the inference server:
    ```bash
    flask run
    ```
7. Go to your inference server's URL, e.g. `http://localhost:5000`, append it with `/prediction`,
   e.g. `http://localhost:5000/prediction`, and you will see the inference result printed in the terminal and shown in
   the webpage as it streaming the video.


