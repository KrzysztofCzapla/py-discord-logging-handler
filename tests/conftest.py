from dataclasses import dataclass
from typing import List
from unittest.mock import MagicMock

import pytest

from discord_logging_handler import DiscordHandlerInputData
from discord_logging_handler.constants import DISCORD_LOGGING_HANDLER_WEBHOOK_URL
from discord_logging_handler.message_template_builder import BaseMessageTemplateBuilder
from discord_logging_handler.models import (
    ErrorContentData,
    BaseContentData,
    DiscordAPIJSONData,
)


@pytest.fixture(autouse=True)
def mock_urllib(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("urllib.request.urlopen", mock)
    return mock


@pytest.fixture
def set_url_env_variable(monkeypatch):
    monkeypatch.setenv(
        DISCORD_LOGGING_HANDLER_WEBHOOK_URL,
        "https://discord.com/api/webhooks/adadada/dadadad",
    )
    yield
    monkeypatch.delenv(DISCORD_LOGGING_HANDLER_WEBHOOK_URL, raising=False)


@pytest.fixture
def default_input_data():
    return DiscordHandlerInputData(app_name="test_app_name")


@pytest.fixture
def error_content_data():
    return ErrorContentData(
        app_name="whatever",
        file="discord-logging-handler/tests/temp_e2e_test.py",
        message="this is a test message",
    )


@pytest.fixture
def custom_content_data():
    @dataclass
    class CustomContentData(BaseContentData):
        custom_field: str

    return CustomContentData(
        app_name="whatever",
        file="discord-logging-handler/tests/temp_e2e_test.py",
        message="this is a test message",
        custom_field="custom field value",
    )


@pytest.fixture
def custom_message_template_builder(custom_content_data):
    class CustomMessageTemplateBuilder(BaseMessageTemplateBuilder):
        FIELD_LENGTH_LIMITS = {
            "traceback": 1000,
            "file": 200,
            "message": 500,
            "custom_field": 10,
        }

        # typing: the CustomContentData comes as an object so we can only get its type in runtime,
        # for better readability and maintenance, the typing will not be ideal in tests
        @staticmethod
        def build_message_parts(data) -> List[str]:
            """Parts are ordered by importance"""
            return [
                f"{data.alert_emoji} {data.ping} {data.alert_emoji}",
                f"{f'-# **Additional Info:** `{data.additional_info}`' if data.additional_info else ''}",
                f":ringed_planet: **APP:** `{data.app_name}`",
                f":page_facing_up: **FILE:** `{data.file}`",
                f":custom_field: **ERROR:** `{data.custom_field}`",
            ]

    return CustomMessageTemplateBuilder


@pytest.fixture
def discord_api_json_data():
    return DiscordAPIJSONData(content="blalblalbalbalbalalbalbalalb")
