# Description: Helper functions for the API
import json
from typing import Any, Dict

from api_types import APIBodyRequest, APIException


def handle_exception(e):
    if isinstance(e, APIException):
        return {
            "statusCode": e.status_code,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"error": e.message}),
        }

    return {
        "statusCode": 500,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({"error": "Internal server error"}),
    }


def parse_body(body: Dict[str, Any]) -> APIBodyRequest:
    """
    Parse the body of the request and return a dict with the required fields

    Args:
        body (Dict[str, Any]): Body of the request

    Returns:
        APIBodyRequest: Dict with the required fields

    Raises:
        APIException: If the body is not valid
    """
    try:
        return {
            "bucket": body["bucket"],
            "imageName": body["imageName"],
        }
    except Exception as e:
        print(e)
        raise APIException(
            400, "Error parsing body. Required fields: bucket, imageName"
        )
