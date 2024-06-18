import base64
from typing import TypeVar, Type

T = TypeVar('T')

Separators = (tuple[str] | tuple[str, str] | tuple[str, str, str] | tuple[str, str, str, str]
              | tuple[str, str, str, str, str])
ParseResult = T | list[T | list[T | list[T | list[T | list[T]]]]]


def parse_string(string: str, separators: Separators, target_type: Type[T]) -> ParseResult[T]:
    r"""
    Parse a string (split by separators and convert to the given type).

    The string will be split by the given separators. The amount of separators will determine the dimension of the list.
    For example, if separators = ("\\n", ","), the content will be split by newline and each resulting substring will be
    split by comma, forming a two-dimensional list.
    The substrings will then be converted to the given type (default: str) and returned.
    The function can handle any number of separators/dimensions, but since recursive typing is not widely supported,
    the type hinting is limited to five dimensions.

    :param string: The string to parse.
    :param separators: The separators to split the content by.
    :param target_type: The type to convert the content to.
    :return: The result of the parsing and conversion.
    """
    processed_data: ParseResult = string

    if not separators:
        if target_type != str:
            processed_data = target_type(processed_data)
        return processed_data

    if separators[0] == "":
        processed_data = list(processed_data)
    else:
        processed_data = processed_data.split(separators[0])

    return [parse_string(substr, separators=separators[1:], target_type=target_type) for substr in processed_data]


def parse_file_content(filename: str, separators: Separators, target_type: type[T]) -> ParseResult[T]:
    r"""
    Read file content and parse it (split by separators and convert to the given type).

    The string will be read from the file with the given filename.
    The string will be split by the given separators. The amount of separators will determine the dimension of the list.
    For example, if separators = ("\\n", ","), the content will be split by newline and each resulting substring will be
    split by comma, forming a two-dimensional list.
    The substrings will then be converted to the given type (default: str) and returned.
    The function can handle any number of separators/dimensions, but since recursive typing is not widely supported,
    the type hinting is limited to five dimensions.

    :param filename: The name of the file to read the content from.
    :param separators: The separators to split the content by.
    :param target_type: The type to convert the content to.
    :return: The result of the parsing and conversion.
    """
    if target_type is None:
        target_type = str

    with open(filename) as file:
        file_content = file.read()

    return parse_string(file_content, separators, target_type)


def b64encode(text: str, times_to_encode: int = 1) -> str:
    """
    Encode the given text using base64 encoding.
    :param text: The text to encode.
    :param times_to_encode: The number of times to encode the text.
    :return: The encoded text.
    """
    for _ in range(times_to_encode):
        text = base64.b64encode(text.encode("utf-8")).decode("utf-8")

    return text


def b64decode(text: str, times_to_decode: int = 1) -> str:
    """
    Decode the given text using base64 encoding.
    :param text: The text to decode.
    :param times_to_decode: The number of times to decode the text.
    :return: The decoded text.
    """
    for _ in range(times_to_decode):
        text = base64.b64decode(text).decode("utf-8")

    return text
