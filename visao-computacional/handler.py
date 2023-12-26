import json

from rekognition import get_faces_from_bytes, get_labels_from_bytes
from s3 import get_obj
from utils import handle_exception, parse_body


def health(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "healthy"}),
    }


def v1_description(event, context):
    route_usage = """POST /v1/vision
{
    "bucket": "bucket-name",
    "imageName": "image-name"
}

Response:
{
    "url_to_image": "https://bucket-name.s3.amazonaws.com/image-name",
    "created_image": "https://bucket-name.s3.amazonaws.com/image-name",
    "labels": [
        {
            "Name": "Person",
            "Confidence": 99.99999237060547
        },
        {
            "Name": "Human",
            "Confidence": 99.99999237060547
        },
    ]
}"""
    return {"statusCode": 200, "body": route_usage}


def v2_description(event, context):
    route_usage = """POST /v2/vision 
{
    "bucket": "bucket-name",
    "imageName": "image-name"
}

Response:
{
    "url_to_image": "https://bucket-name.s3.amazonaws.com/image-name",
    "created_image": "https://bucket-name.s3.amazonaws.com/image-name",
    "faces": [
        {
            "position": {
                "Width": 0.2638888955116272,
                "Height": 0.35185185074806213,
                "Left": 0.3680555522441864,
                "Top": 0.29629629850387573
            },
            "classified_emotion": "HAPPY",
            "classified_emotion_confidence": 99.99999237060547
        },
        {
            "position": {
                "Width": 0.2638888955116272,
                "Height": 0.35185185074806213,
                "Left": 0.3680555522441864,
                "Top": 0.29629629850387573
            },
            "classified_emotion": "HAPPY",
            "classified_emotion_confidence": 99.99999237060547
        },
    ]
}"""
    return {
        "statusCode": 200,
        "body": route_usage,
    }


def v1(event, context):
    try:
        body = parse_body(json.loads(event.get("body", "{}")))
        obj = get_obj(body["bucket"], body["imageName"])
        labels = get_labels_from_bytes(obj["body"])

        response = {
            "statusCode": 200,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({
                "url_to_image": obj["url_to_image"],
                "created_image": obj["created_image"],
                "labels": labels["labels"],
            }),
        }

        return response
    except Exception as e:
        return handle_exception(e)


def v2(event, context):
    try:
        body = parse_body(json.loads(event.get("body", "{}")))
        obj = get_obj(body["bucket"], body["imageName"])
        faces = get_faces_from_bytes(obj["body"])

        response = {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "url_to_image": obj["url_to_image"],
                "created_image": obj["created_image"],
                "faces": faces["faces"],
            }),
        }

        return response
    except Exception as e:
        return handle_exception(e)
