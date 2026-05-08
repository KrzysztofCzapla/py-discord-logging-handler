from py_discord_logging_handler.constants import (
    DEFAULT_ADDITIONAL_DATA_TEXT,
    DISCORD_MAX_CHARS_LIMIT,
    DEFAULT_TRUNCATION_ENDING,
)
from py_discord_logging_handler.content_manager import ContentManager
from py_discord_logging_handler.models import ErrorContentData


class TestContentManager:
    def test_assemble_parts_smoke(self):
        parts = [
            "Life in the big city",
            "Drinking wine from burger king cup",
            "This guys was interior decorator?",
        ]
        concatenation_char = "\n"
        limit = 1000
        truncation_ending = "..."
        assembled = ContentManager._assemble_parts(
            parts, concatenation_char, limit, truncation_ending
        )
        assert len(assembled) < limit

    def test_assemble_parts_small_limit(self):
        parts = [
            "Life in the big city",
            "Drinking wine from burger king cup",
            "This guys was interior decorator?",
        ]
        concatenation_char = "\n"
        limit = 10
        truncation_ending = "..."
        assembled = ContentManager._assemble_parts(
            parts, concatenation_char, limit, truncation_ending
        )
        assert len(assembled) == len(truncation_ending)

    def test_assemble_parts_medium_limit(self):
        parts = [
            "Life in the big city",
            "Drinking wine from burger king cup",
            "This guys was interior decorator?",
        ]
        concatenation_char = "\n"
        limit = 30
        truncation_ending = "..."
        assembled = ContentManager._assemble_parts(
            parts, concatenation_char, limit, truncation_ending
        )
        assert len(assembled) <= limit

    def test_truncate_fields(self):
        message = "this is a test message"
        error_content_data = ErrorContentData(
            app_name="whatever",
            file="py-discord-logging-handler/tests/temp_e2e_test.py",
            message=message,
        )
        limits = {"file": 10, "message": 200}
        truncation_ending = "..."
        truncated_fields = ContentManager._truncate_fields(
            error_content_data, limits, truncation_ending
        )
        assert error_content_data.message == message
        assert truncation_ending in error_content_data.file
        assert len(truncated_fields) == 1

    def test_create_content_message_smoke(self, error_content_data):
        content = ContentManager.create_content_message(error_content_data)
        assert len(content) < DISCORD_MAX_CHARS_LIMIT

    def test_create_content_message_truncated_fields(self):
        message = "this is a test message" * 100
        error_content_data = ErrorContentData(
            app_name="whatever",
            file="py-discord-logging-handler/tests/temp_e2e_test.py",
            message=message,
        )
        content = ContentManager.create_content_message(error_content_data)
        truncated_fields = DEFAULT_ADDITIONAL_DATA_TEXT.format(
            truncated_fields="['message']"
        )
        assert truncated_fields in content
        assert len(content) < DISCORD_MAX_CHARS_LIMIT

    def test_create_content_message_truncated_fields_no_additional_info(self):
        message = "this is a test message" * 100
        error_content_data = ErrorContentData(
            app_name="whatever",
            file="py-discord-logging-handler/tests/temp_e2e_test.py",
            message=message,
        )
        content = ContentManager.create_content_message(
            error_content_data, add_additional_info=False
        )
        truncated_fields = DEFAULT_ADDITIONAL_DATA_TEXT.format(
            truncated_fields="['message']"
        )
        assert truncated_fields not in content
        assert len(content) < DISCORD_MAX_CHARS_LIMIT

    def test_create_content_message_truncated_fields_custom_template_builder(
        self, custom_content_data, custom_message_template_builder
    ):
        content = ContentManager.create_content_message(
            custom_content_data,
            custom_message_template_builder,
            add_additional_info=False,
        )
        assert "custom_field" in content
        assert DEFAULT_TRUNCATION_ENDING in content
        assert "custom field value" not in content

    def test_create_content_message_truncated_fields_custom_template_builder_no_field_limits(
        self, custom_content_data, custom_message_template_builder
    ):
        custom_message_template_builder.FIELD_LENGTH_LIMITS = {}
        content = ContentManager.create_content_message(
            custom_content_data,
            custom_message_template_builder,
            add_additional_info=False,
        )
        assert "custom_field" in content
        assert DEFAULT_TRUNCATION_ENDING not in content
        assert "custom field value" in content
