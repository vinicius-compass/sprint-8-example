from typing import TypedDict


class APIException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class APIBodyRequest(TypedDict):
    bucket: str
    imageName: str


class S3Object(TypedDict):
    url_to_image: str
    created_image: str
    body: bytes


class Label(TypedDict):
    name: str
    confidence: float


class RekognitionLabelResponse(TypedDict):
    labels: list[Label]


class Position(TypedDict):
    Height: float | None
    Left: float | None
    Top: float | None
    Width: float | None


class Face(TypedDict):
    position: Position
    classified_emotion: str | None
    classified_emotion_confidence: float | None


class RekognitionFaceResponse(TypedDict):
    faces: list[Face]


class V1Response(TypedDict):
    url_to_image: str
    created_image: str
    labels: list[Label]


class V2Response(TypedDict):
    url_to_image: str
    created_image: str
    faces: list[Face]
