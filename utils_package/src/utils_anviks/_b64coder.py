import base64


def b64encode(text: str, times_to_encode: int = 20) -> str:
    """
    Encode the given text using base64 encoding.
    :param text: The text to encode.
    :param times_to_encode: The number of times to encode the text.
    :return: The encoded text.
    """
    for _ in range(times_to_encode):
        text = base64.b64encode(text.encode("utf-8")).decode("utf-8")

    return text


def b64decode(text: str, times_to_decode: int = 20) -> str:
    """
    Decode the given text using base64 encoding.
    :param text: The text to decode.
    :param times_to_decode: The number of times to decode the text.
    :return: The decoded text.
    """
    for _ in range(times_to_decode):
        text = base64.b64decode(text).decode("utf-8")

    return text
