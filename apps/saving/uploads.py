import os
import tempfile
from datetime import datetime
import random

import cv2

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from flask import current_app


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket.

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    config = Config(read_timeout=70, connect_timeout=70, retries={"max_attempts": 10})
    s3_client = boto3.client(
        "s3",
        config=config,
        aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
    )
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        # logging.error(e)
        print(e)
        return False
    return True


def save_frame(frame, result, identifier):
    try:
        now = datetime.now()
        now = now.strftime("%d-%m-%Y_%H-%M-%S")
        unique_id = random.randint(1, 1000)
        filename = f"{identifier}_{str(now)}_{unique_id}.jpg"
        temp_filename = os.path.join(tempfile.gettempdir(), filename)
        # Save the frame to a temporary file
        cv2.imwrite(temp_filename, frame)
        # Upload the temporary file to S3
        upload_file(
            temp_filename, current_app.config["BUCKET_NAME"], f"{result}/{filename}"
        )
        # Remove the temporary file
        print(current_app.config["BUCKET_NAME"])
        os.remove(temp_filename)
    except Exception as e:
        print(e)


def save_frame_task(frame, result, identifier):
    with current_app.app_context():
        len_q = len(current_app.task_queue)
        print(f"Task queue length: {len_q}")
        save_frame(frame, result, identifier)
