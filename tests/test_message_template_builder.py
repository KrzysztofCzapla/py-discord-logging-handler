import pytest

from py_discord_logging_handler.message_template_builder import (
    ErrorMessageTemplateBuilder,
    BaseMessageTemplateBuilder,
)
from py_discord_logging_handler.models import BaseContentData


class TestMessageTemplateBuilder:
    def test_error_message_template_builder(self, error_content_data):
        builder = ErrorMessageTemplateBuilder()
        parts = builder.build_message_parts(error_content_data)
        assert isinstance(parts, list)
        for part in parts:
            assert isinstance(part, str)

    def test_custom_message_template_builder(
        self, custom_content_data, custom_message_template_builder
    ):
        parts = custom_message_template_builder.build_message_parts(custom_content_data)
        assert isinstance(parts, list)
        for part in parts:
            assert isinstance(part, str)

    def test_custom_message_template_builder_no_build_message_parts(
        self, custom_content_data
    ):
        class CustomMessageTemplateBuilderNoAbstractMethod(
            BaseMessageTemplateBuilder[BaseContentData]
        ):
            pass

        with pytest.raises(TypeError) as error_info:
            CustomMessageTemplateBuilderNoAbstractMethod()

        assert "build_message_parts" in str(error_info)
