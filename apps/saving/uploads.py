import os
import tempfile
from datetime import datetime
import random

import cv2

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


def upload_file(file_name, bucket, access_key, secret_key, object_name=None):
    """Upload a file to an S3 bucket.

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param access_key: AWS access key
    :param secret_key: AWS secret key
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
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        # logging.error(e)
        print(e)
        return False
    return True


def save_frame(frame, result, identifier, bucket_name, access_key, secret_key):
    try:
        now = datetime.now()
        now = now.strftime("%d-%m-%Y_%H-%M-%S")
        unique_id = random.randint(1, 1000)
        filename = f"{identifier}_{str(now)}_{unique_id}.jpg"
        temp_filename = os.path.join(tempfile.gettempdir(), filename)
        # Save the frame to a temporary file
        cv2.imwrite(temp_filename, frame)
        # Upload the temporary file to S3
        # with current_app.app_context():
        upload_file(
            temp_filename,
            bucket_name,
            access_key,
            secret_key,
            f"{result}/{filename}",
        )
        print(bucket_name)
        # Remove the temporary file
        os.remove(temp_filename)
    except Exception as e:
        print(e)
