from loguru import logger
from conscience import setup


def before_feature(context, feature):
    setup(context)
    logger.debug("environment setup")
