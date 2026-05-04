from dataclasses import dataclass
from typing import List

import pytest

from discord_logging_handler.message_template_builder import BaseMessageTemplateBuilder
from discord_logging_handler.models import (
    ErrorContentData,
    BaseContentData,
    DiscordAPIJSONData,
)


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
        FIELD_LENGTH_LIMITS = {"traceback": 1000, "file": 200, "message": 500}

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
                f":warning: **ERROR:** `{data.custom_field}`",
            ]

    return CustomMessageTemplateBuilder()


@pytest.fixture
def discord_api_json_data():
    return DiscordAPIJSONData(content="blalblalbalbalbalalbalbalalb")
