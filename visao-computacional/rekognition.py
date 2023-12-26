# Description: Rekognition API calls
from typing import Any, Dict

import boto3
from api_types import (APIException, RekognitionFaceResponse,
                       RekognitionLabelResponse)


def get_labels_from_bytes(data: bytes) -> RekognitionLabelResponse:
    """
    Returns a list of labels and their confidence from a given image

    Args:
        data (bytes): image data

    Returns:
        RekognitionLabelResponse: list of labels and their confidence

    Raises:
        APIException: if there is an error with the Rekognition API
    """
    try:
        rekognition = boto3.client("rekognition")
        response = rekognition.detect_labels(
            Image={
                "Bytes": data,
            },
        )

        print(response)

        return {
            "labels": [
                {"name": label["Name"], "confidence": label["Confidence"]}
                for label in response["Labels"]
            ]
        }
    except Exception as e:
        print(e)
        raise APIException(500, "Rekognition error: could not get labels from bytes")


def get_labels_from_bucket(bucket_name: str, key: str) -> RekognitionLabelResponse:
    """
    Returns a list of labels and their confidence from a given Image

    Args:
        bucket_name (str): bucket name
        key (str): key of image in bucket

    Returns:
        RekognitionLabelResponse: list of labels and their confidence

    Raises:
        APIException: if there is an error with the Rekognition API
    """
    try:
        rekognition = boto3.client("rekognition")
        response = rekognition.detect_labels(
            Image={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": key,
                },
            },
        )

        print(response)

        return {
            "labels": [
                {"name": label["Name"], "confidence": label["Confidence"]}
                for label in response["Labels"]
            ]
        }
    except Exception as e:
        print(e)
        raise APIException(500, "Rekognition error: could not get labels from bucket")


def parse_faces_response(response: Dict[str, Any]) -> RekognitionFaceResponse:
    if len(response["FaceDetails"]) == 0:
        return {
            "faces": [
                {
                    "position": {
                        "Height": None,
                        "Left": None,
                        "Top": None,
                        "Width": None,
                    },
                    "classified_emotion": None,
                    "classified_emotion_confidence": None,
                }
            ]
        }
    return {
        "faces": [
            {
                "position": {
                    "Height": face["BoundingBox"]["Height"],
                    "Left": face["BoundingBox"]["Left"],
                    "Top": face["BoundingBox"]["Top"],
                    "Width": face["BoundingBox"]["Width"],
                },
                "classified_emotion": face["Emotions"][0]["Type"],
                "classified_emotion_confidence": face["Emotions"][0]["Confidence"],
            }
            for face in response["FaceDetails"]
        ]
    }


def get_faces_from_bytes(data: bytes) -> RekognitionFaceResponse:
    """
    Returns a list of faces and their emotions from a given image

    Args:
        data (bytes): image data

    Returns:
        RekognitionFaceResponse: list of faces and their emotions

    Raises:
        APIException: if there is an error with the Rekognition API
    """
    try:
        rekognition = boto3.client("rekognition")
        response = rekognition.detect_faces(
            Image={
                "Bytes": data,
            },
            Attributes=["EMOTIONS"],
        )

        print(response)

        return parse_faces_response(response)
    except Exception as e:
        print(e)
        raise APIException(500, "Rekognition error: could not get faces from bytes")


def get_faces_from_bucket(bucket_name: str, key: str) -> RekognitionFaceResponse:
    """
    Returns a list of faces and their emotions from a given image

    Args:
        bucket_name (str): bucket name
        key (str): key of image in bucket

    Returns:
        RekognitionFaceResponse: list of faces and their emotions

    Raises:
        APIException: if there is an error with the Rekognition API
    """
    try:
        rekognition = boto3.client("rekognition")
        response = rekognition.detect_faces(
            Image={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": key,
                }
            },
            Attributes=["EMOTIONS"],
        )

        print(response)

        return parse_faces_response(response)

    except Exception as e:
        print(e)
        raise APIException(500, "Rekognition error: could not get faces from bytes")
