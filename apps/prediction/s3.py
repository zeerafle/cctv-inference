import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


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
    s3_client = boto3.client("s3", config=config)
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        # logging.error(e)
        print(e)
        return False
    return True
