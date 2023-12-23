# Accident Detection Inference API

## How to run

1. Create a file named `.flaskenv` in the root directory, put the following content in it:
    ```
    FLASK_APP=cctv.py
    FLASK_ENV=development
    FLASK_DEBUG=1
    AWS_ACCESS_KEY_ID=<your AWS access key>
    AWS_SECRET_ACCESS_KEY=<your AWS secret access key>
    BUCKET_NAME=<your bucket name>
    ```
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

The predicted frame is stored in AWS S3 bucket. It'll automatically create directory based on the predicted class, e.g. `accident` or `normal`.

## Example

![Example](https://github.com/zeerafle/cctv-inference/blob/master/example.gif)

## TODO

- [x] Store the predicted frames
- [ ] Write test
- [x] Connect to cloud bucket storage
- [ ] Actually deploy it


