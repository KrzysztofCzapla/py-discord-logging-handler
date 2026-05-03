import logging
import traceback as tb

from discord_logging_handler.content_manager import ContentManager
from discord_logging_handler.discord_api_adapter import DiscordAPIAdapter
from discord_logging_handler.enums import DiscordLoggingHandlerLevel
from discord_logging_handler.models import (
    BaseContentData,
    DiscordAPIJSONData,
)
from discord_logging_handler.input_data import DiscordHandlerInputData


def _core_handler(content_data: BaseContentData, input_data: DiscordHandlerInputData):
    content = ContentManager.create_content_message(
        data=content_data,
        template_builder=input_data.message_template_builder_type,
        add_additional_info=input_data.add_additional_data_to_content,
    )
    discord_json_data = DiscordAPIJSONData(
        content=content,
        username=input_data.username,
        avatar_url=input_data.avatar_url,
    )
    DiscordAPIAdapter.send_webhook(
        body=discord_json_data,
        webhook_url=input_data.webhook_url,
        webhook_id=input_data.webhook_id,
        webhook_token=input_data.webhook_token,
    )


class _DefaultHandler(logging.Handler):
    def __init__(self, input_data: DiscordHandlerInputData):
        super().__init__()
        self.input_data = input_data

    def emit(self, record: logging.LogRecord):
        message = record.getMessage()
        file = record.pathname
        traceback = None
        if record.exc_info:
            traceback = "".join(tb.format_exception(*record.exc_info))

        additional_attributes = {}
        for attr in self.input_data.content_dataclass_additional_fields:
            if (value := getattr(record, attr, None)) is not None:
                additional_attributes[attr] = value

        content_data = self.input_data.content_dataclass_type(
            app_name=self.input_data.app_name,
            file=file,
            message=message,
            **additional_attributes,
        )
        content_data.traceback = traceback
        _core_handler(content_data, self.input_data)


def _discord_loguru_handler_wrapper(input_data: DiscordHandlerInputData):
    def _discord_loguru_handler(message):
        record = message.record
        message = record["message"]
        file = record["file"].path
        exc = record["exception"]
        traceback = str(exc) if exc else None

        additional_attributes = {}
        extra = record["extra"]
        for attr in input_data.content_dataclass_additional_fields:
            if (value := extra.get(attr)) is not None:
                additional_attributes[attr] = value

        content_data = input_data.content_dataclass_type(
            app_name=input_data.app_name,
            file=file,
            message=message,
            **additional_attributes,
        )
        content_data.traceback = traceback
        _core_handler(content_data, input_data)

    return _discord_loguru_handler


def _discord_structlog_processor_wrapper(input_data: DiscordHandlerInputData):
    def _discord_structlog_processor(logger, method_name, event_dict):
        logging_level = input_data.logging_level
        legal_levels = DiscordLoggingHandlerLevel.get_current_and_higher_level_name(
            logging_level.value
        )
        if method_name not in [level.lower() for level in legal_levels]:
            return event_dict

        message = event_dict.get("event")
        file = event_dict.get("pathname")
        traceback = None
        exc_info = event_dict.get("exc_info")
        if exc_info:
            traceback = "".join(tb.format_exception(*exc_info))

        additional_attributes = {}
        for attr in input_data.content_dataclass_additional_fields:
            if (value := event_dict.get(attr)) is not None:
                additional_attributes[attr] = value

        content_data = input_data.content_dataclass_type(
            app_name=input_data.app_name,
            file=file,
            message=message,
            **additional_attributes,
        )
        content_data.traceback = traceback
        _core_handler(content_data, input_data)

        return event_dict

    return _discord_structlog_processor
