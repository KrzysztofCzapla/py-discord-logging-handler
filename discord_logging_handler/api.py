from typing import Any

from discord_logging_handler.constants import (
    NO_LOGGER_SET_ERROR_MESSAGE,
    LOGGER_NOT_SUPPORTED_ERROR_MESSAGE,
    NO_INPUT_DATA_ERROR_MESSAGE,
)
from discord_logging_handler.handlers import (
    _DefaultHandler,
    _discord_loguru_handler_wrapper,
    _discord_structlog_processor_wrapper,
)
from discord_logging_handler.input_data import DiscordHandlerInputData


def add_discord_logging_handler(logger: Any, input_data: DiscordHandlerInputData):
    if not logger:
        raise ValueError(NO_LOGGER_SET_ERROR_MESSAGE)
    if not input_data:
        raise ValueError(NO_INPUT_DATA_ERROR_MESSAGE)
    if hasattr(logger, "addHandler"):
        # default logger
        logger.addHandler(_DefaultHandler(input_data))
    elif hasattr(logger, "add"):
        # loguru logger
        logger.add(_discord_loguru_handler_wrapper(input_data), level="ERROR")
    elif hasattr(logger, "get_config"):
        # structlog logger
        config = logger.get_config()
        processors = config.get("processors", [])
        logger.configure(
            processers=processors + [_discord_structlog_processor_wrapper(input_data)]
        )
    else:
        raise ValueError(LOGGER_NOT_SUPPORTED_ERROR_MESSAGE)
    # TODO - handle logging level
