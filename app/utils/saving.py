import json
import os
import tempfile
from datetime import datetime
import random
from dotenv import load_dotenv

import cv2

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

load_dotenv()
bucket = os.getenv("BUCKET_NAME")
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")


def upload_file(file_name, object_name=None):
    """Upload a file to an S3 bucket.

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param access_key: AWS access key
    :param secret_key: AWS secret key
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    print("uploading file")
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
        print(file_name, "uploaded")
    except ClientError as e:
        # logging.error(e)
        print(e)
        return False
    return True


async def save_frame(frame, result, identifier):
    try:
        now = datetime.now()
        now = now.strftime("%d-%m-%Y_%H-%M-%S")
        unique_id = random.randint(1, 1000)
        filename = f"{identifier}_{str(now)}_{unique_id}.jpg"
        temp_filename = os.path.join(tempfile.gettempdir(), filename)
        # Save the frame to a temporary file
        cv2.imwrite(temp_filename, frame)
        # Upload the temporary file to S3
        upload_file(temp_filename, f"frames{filename}")
        temp_annotation = os.path.join(tempfile.gettempdir(), f"{temp_filename}.json")
        with open(temp_annotation, "w") as f:
            json.dump(result, f)
            upload_file(temp_annotation, f"annotation/{filename.split('.')[0]}.json")
        # Remove the temporary file
        os.remove(temp_filename)
        os.remove(temp_annotation)
    except Exception as e:
        print(e)
