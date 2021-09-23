from . import logger
from behave import register_type
import parse


@parse.with_pattern(r"(\w|\s|\d|.)*")
def parse_string(text):
    logger.debug(f"Parsing Text pattern: {text}")
    return text


@parse.with_pattern(r"\d+")
def parse_number(text):
    logger.debug(f"Parsing Number pattern: {text}")
    return int(text)


def register_formats():
    logger.debug("registering Text pattern")
    register_type(Text=parse_string)
    logger.debug("registering Number pattern")
    register_type(Number=parse_number)
