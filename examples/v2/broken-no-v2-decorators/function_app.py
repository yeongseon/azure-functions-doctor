"""This module intentionally does NOT use Azure Functions v2 decorators."""

import logging


def hello():
    logging.info("This is a plain Python function, not an Azure Functions v2 app.")
    return "hello"
