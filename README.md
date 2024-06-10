# Accident Detection Inference API

## How to develop

0. Prepare an S3 bucket in AWS, and get your access key and secret access key. This is used to store the predicted frames.
1. Create a file named `.env` in the root directory, put the following content in it:
    ```
    AWS_ACCESS_KEY_ID=<your AWS access key>
    AWS_SECRET_ACCESS_KEY=<your AWS secret access key>
    BUCKET_NAME=<your bucket name>
    ```
2. Install conda environment:
    ```bash
    conda env create -f environment.yml 
    ```
7. Open terminal, run the inference server:
    ```bash
    fastapi dev
    ```
8. Go to your inference server's URL, e.g. `http://localhost:8000`. Open docs at `http://localhost:8000/docs` to see the API documentation.

The predicted frame is stored in AWS S3 bucket.

## Example

Live example is available at [https://8zgpur6pwv.ap-southeast-1.awsapprunner.com/](https://8zgpur6pwv.ap-southeast-1.awsapprunner.com/)

## TODO

- [x] Store the predicted frames
- [ ] Write test
- [x] Connect to cloud bucket storage
- [x] Actually deploy it
