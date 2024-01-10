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
2. Install requirements (or create a virtual environment beforehand), e.g.:
    ```bash
    pip install -r requirements.txt
    ```
3. Get the model [here](https://drive.google.com/file/d/1bxNL3AA9Ku66ZRkgReVMpAsNnD1OuTEB/view?usp=drive_link)
4. Install [docker](https://docs.docker.com/get-docker/) or [podman](https://podman.io/getting-started/installation)
5. Run redis server via docker/podman:
   ```bash
   docker run -d -p 6379:6379 redis
   ```
   For podman, follow instructions [here](https://computingforgeeks.com/how-to-run-redis-in-podman-docker-container/)
6. Run redis worker:
   ```bash
   rq worker saving-tasks
   ```
7. Open another terminal, run the inference server:
    ```bash
    flask run
    ```
8. Go to your inference server's URL, e.g. `http://localhost:5000`, follow the instruction there to test the API.

The predicted frame is stored in AWS S3 bucket.

## Example

![Example](https://github.com/zeerafle/cctv-inference/blob/master/example.gif)

## TODO

- [x] Store the predicted frames
- [ ] Write test
- [x] Connect to cloud bucket storage
- [x] Use redis worker to queue the upload to cloud storage process
- [ ] Actually deploy it


