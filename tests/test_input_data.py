import pytest

from discord_logging_handler import DiscordHandlerInputData
from discord_logging_handler.enums import DiscordLoggingHandlerLevel
from discord_logging_handler.message_template_builder import ErrorMessageTemplateBuilder
from discord_logging_handler.models import ErrorContentData


class TestInputData:
    def test_valid_input_data(self):
        name = "whatever"
        data = DiscordHandlerInputData(app_name=name)
        assert data.app_name == name
        assert data.add_additional_data_to_content is True
        assert data.content_dataclass_type == ErrorContentData
        assert data.logging_level == DiscordLoggingHandlerLevel.ERROR
        assert data.message_template_builder_type == ErrorMessageTemplateBuilder
        assert not data.content_dataclass_additional_fields

    def test_input_data_no_app_name(self):
        with pytest.raises(ValueError):
            DiscordHandlerInputData(app_name=None)
