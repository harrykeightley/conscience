from director import setup, logger


def before_feature(context, feature):
    context.under_test = context.config.under_test
    logger.debug("environment setup")
    setup()
