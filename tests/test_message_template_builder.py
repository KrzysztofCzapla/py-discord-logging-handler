from discord_logging_handler.message_template_builder import (
    ErrorMessageTemplateBuilder,
    BaseMessageTemplateBuilder,
)


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
        # TODO - need to make it so subclass has an error without the implementation of the abstract method
        class CustomMessageTemplateBuilder(BaseMessageTemplateBuilder):
            pass
