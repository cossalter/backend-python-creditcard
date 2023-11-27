import base64


def base64_encode(number: str) -> str:
    return base64.b64encode(number.encode("ascii")).decode("ascii")


def base64_decode(number: str) -> str:
    return base64.b64decode(number.encode("ascii")).decode("ascii")
