from typing import Any

from py_discord_logging_handler.constants import (
    NO_LOGGER_SET_ERROR_MESSAGE,
    LOGGER_NOT_SUPPORTED_ERROR_MESSAGE,
    NO_INPUT_DATA_ERROR_MESSAGE,
    STRUCTLOG_WRONG_FUNCTION_ERROR_MESSAGE,
    DEFAULT_LOGGER_METHOD,
    LOGURU_METHOD,
    STRUCTLOG_METHOD,
)
from py_discord_logging_handler.handlers import (
    DiscordLoggingHandler,
    discord_loguru_handler_wrapper,
)
from py_discord_logging_handler.input_data import DiscordHandlerInputData


def add_discord_logging_handler(logger: Any, input_data: DiscordHandlerInputData):
    """
    Main function for interaction with the py-discord-logging-handler package.

    It takes the inputted logger and data and adds a handler to the logger with the context of that data.
    You don't need to set any handlers yourself, it works out of the box.

    Currently supported loggers via this method:
        - Built-in Logging.logger
        - loguru's logger

    If you want to use structlog - you need to import `discord_structlog_processor_wrapper` and set it up manually.

    :param logger:
        either a built-in Logging logger or loguru. Otherwise, raises an exception
    :param input_data:
        DiscordHandlerInputData, you can just add a DiscordHandlerInputData(app_name="your_app_name") and it will work.
        To customize the handler further, you can edit other fields.
    :return:
        None
    """
    if not logger:
        raise ValueError(NO_LOGGER_SET_ERROR_MESSAGE)
    if not input_data:
        raise ValueError(NO_INPUT_DATA_ERROR_MESSAGE)
    level = input_data.logging_level
    if hasattr(logger, DEFAULT_LOGGER_METHOD):
        # default logger
        handler = DiscordLoggingHandler(input_data)
        handler.setLevel(int(level))
        logger.addHandler(handler)
    elif hasattr(logger, LOGURU_METHOD):
        # loguru logger
        logger.add(discord_loguru_handler_wrapper(input_data), level=level.name)
    elif hasattr(logger, STRUCTLOG_METHOD):
        # structlog logger
        raise ValueError(STRUCTLOG_WRONG_FUNCTION_ERROR_MESSAGE)
    else:
        raise ValueError(LOGGER_NOT_SUPPORTED_ERROR_MESSAGE)
