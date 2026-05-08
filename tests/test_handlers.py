import logging
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from py_discord_logging_handler.handlers import (
    _core_handler,
    _DefaultHandler,
    _discord_loguru_handler_wrapper,
    discord_structlog_processor_wrapper,
)
from tests.utils import get_mock_urllib_json_body


class TestHandlers:
    message = "I Love Hotels Because I Hate My Life"

    def test_core_handler_smoke(
        self, error_content_data, default_input_data, set_url_env_variable, mock_urllib
    ):
        _core_handler(error_content_data, default_input_data)
        mock_urllib.assert_called_once()

    def test_core_handler_no_webhook(self, error_content_data, default_input_data):
        with pytest.raises(ValueError):
            _core_handler(error_content_data, default_input_data)

    def test_default_handler(
        self, default_input_data, set_url_env_variable, mock_urllib
    ):
        record = logging.LogRecord(
            name="abc",
            level=40,
            pathname=str(Path(__file__)),
            lineno=10,
            msg=self.message,
            args=None,
            exc_info=None,
        )

        handler = _DefaultHandler(default_input_data)
        handler.emit(record)
        mock_urllib.assert_called_once()

        # assert our message is somewhere inside the json body sent to the Discord API
        assert self.message in get_mock_urllib_json_body(mock_urllib)

    def test_loguru_handler(
        self, default_input_data, set_url_env_variable, mock_urllib
    ):
        handler_function = _discord_loguru_handler_wrapper(default_input_data)
        logging_message = SimpleNamespace(
            record={
                "message": self.message,
                "file": SimpleNamespace(path="my path"),
                "exception": ValueError("My Beautiful Dark Twisted Exception"),
                "extra": {},
            }
        )
        handler_function(logging_message)
        mock_urllib.assert_called_once()
        assert self.message in get_mock_urllib_json_body(mock_urllib)

    def test_structlog_processor(
        self, default_input_data, set_url_env_variable, mock_urllib
    ):
        handler_function = discord_structlog_processor_wrapper(default_input_data)
        logging_message = {"event": self.message, "pathname": "my path", "extra": {}}
        handler_function(MagicMock(), "error", logging_message)
        mock_urllib.assert_called_once()
        assert self.message in get_mock_urllib_json_body(mock_urllib)
