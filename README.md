# Accident Detection Inference API

## How to run

1. Install requirements (or create a virtual environment beforehand), e.g.:
    ```bash
    pip install -r requirements.txt
    ```
2. Prepare your own model, put it in root directory and name it `model.h5`
3. Open terminal, run the inference server:
    ```bash
    flask run
    ```
4. Go to your inference server's URL, e.g. `http://localhost:5000`, follow the instruction there to test the API.

Currently, the predicted frame is stored in local directory. Create a directory named `data` in the root directory.
Inside it, create directories `normal` and `accident` to store the predicted frames.

## Example

![Example](https://github.com/zeerafle/cctv-inference/blob/master/example.gif)

## TODO

- [x] Store the predicted frames
- [ ] Write test
- [ ] Connect to cloud bucket storage
- [ ] Actually deploy it


