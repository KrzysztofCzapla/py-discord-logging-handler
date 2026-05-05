import logging

from discord_logging_handler import add_discord_logging_handler
from discord_logging_handler.handlers import discord_structlog_processor_wrapper
from tests.utils import get_mock_urllib_json_body
from loguru import logger as loguru_logger
import structlog


class TestDiscordLoggingHandlerAPI:
    def test_api_default_logging_smoke(
        self, default_input_data, mock_urllib, set_url_env_variable
    ):
        mock_urllib.reset_mock()
        logger = logging.getLogger("TestAPI")
        add_discord_logging_handler(logger, default_input_data)
        logger.info("info logggg")
        mock_urllib.assert_not_called()
        logger.error("error log")
        mock_urllib.assert_called_once()
        assert "traceback" not in get_mock_urllib_json_body(mock_urllib)

    def test_api_default_logging_traceback(
        self, default_input_data, mock_urllib, set_url_env_variable
    ):
        mock_urllib.reset_mock()
        logger = logging.getLogger("TestAPI2")
        add_discord_logging_handler(logger, default_input_data)
        try:
            1 / 0
        except Exception:
            logger.exception("exception log")
        assert "traceback" in get_mock_urllib_json_body(mock_urllib)
        mock_urllib.assert_called_once()

    def test_api_loguru_smoke(
        self, default_input_data, mock_urllib, set_url_env_variable
    ):
        mock_urllib.reset_mock()
        add_discord_logging_handler(loguru_logger, default_input_data)
        loguru_logger.info("info logggg")
        mock_urllib.assert_not_called()
        loguru_logger.error("error log")
        mock_urllib.assert_called_once()
        assert "traceback" not in get_mock_urllib_json_body(mock_urllib)

    def test_api_loguru_traceback(
        self, default_input_data, mock_urllib, set_url_env_variable
    ):
        mock_urllib.reset_mock()
        add_discord_logging_handler(loguru_logger, default_input_data)
        try:
            1 / 0
        except Exception as e:
            loguru_logger.exception(f"exception log: {e}")
        assert "traceback" in get_mock_urllib_json_body(mock_urllib)
        mock_urllib.assert_called_once()

    def test_api_structlog_smoke(
        self, default_input_data, mock_urllib, set_url_env_variable
    ):
        mock_urllib.reset_mock()
        structlog.configure(
            processors=[
                discord_structlog_processor_wrapper(default_input_data),
            ],
        )
        structlog_logger = structlog.get_logger()
        structlog_logger.info("info logggg")
        mock_urllib.assert_not_called()
        structlog_logger.error("error log")
        mock_urllib.assert_called_once()
        assert "traceback" not in get_mock_urllib_json_body(mock_urllib)

    def test_api_structlog_traceback(
        self, default_input_data, mock_urllib, set_url_env_variable
    ):
        mock_urllib.reset_mock()
        structlog.configure(
            processors=[
                discord_structlog_processor_wrapper(default_input_data),
            ],
        )
        structlog_logger = structlog.get_logger()
        structlog_logger.info("info logggg")
        mock_urllib.assert_not_called()
        try:
            1 / 0
        except Exception as e:
            structlog_logger.exception(f"error log {e}")
        mock_urllib.assert_called_once()
        assert "traceback" in get_mock_urllib_json_body(mock_urllib)
