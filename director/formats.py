from . import logger
from behave import register_type
import parse
from enum import Enum


class RelativePosition(Enum):
    Left = 0
    Right = 1
    Above = 2
    Below = 3


@parse.with_pattern(r"(\w|\s|\d|.)*")
def parse_string(text):
    logger.debug(f"Parsing Text pattern: {text}")
    return text


@parse.with_pattern(r"\d+")
def parse_number(text):
    logger.debug(f"Parsing Number pattern: {text}")
    return int(text)


@parse.with_pattern(r"left of|right of|above|below")
def parse_relative_position(text):
    logger.debug(f"Parsing RelativePosition pattern: {text}")
    if text == "left of":
        return RelativePosition.Left
    elif text == "right of":
        return RelativePosition.Right
    elif text == "above":
        return RelativePosition.Above
    elif text == "below":
        return RelativePosition.Below
    return None # not reached


def register_formats():
    logger.debug("registering Text pattern")
    register_type(Text=parse_string)
    logger.debug("registering Number pattern")
    register_type(Number=parse_number)
    logger.debug("registering RelativePosition pattern")
    register_type(RelativePosition=parse_relative_position)
