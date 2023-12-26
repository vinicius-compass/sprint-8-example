# Description: This file contains the functions to interact with S3
from contextlib import closing

import boto3
from api_types import APIException, S3Object


def get_obj(bucket_name: str, key: str) -> S3Object:
    """
    Get an object from S3

    Args:
        bucket_name (str): Name of the bucket
        key (str): Key of the object

    Returns:
        S3Object: Object from S3

    Raises:
        APIException: Error getting object from S3 bucket
    """
    s3 = boto3.client("s3")
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        object_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
        body = b""
        with closing(response["Body"]) as f:
            body = f.read()
        return {
            "url_to_image": object_url,
            "created_image": response["LastModified"].strftime("%d-%m-%Y %H:%M:%S"),
            "body": body,
        }
    except Exception as e:
        print(e)
        raise APIException(500, "Error getting object from S3 bucket")
