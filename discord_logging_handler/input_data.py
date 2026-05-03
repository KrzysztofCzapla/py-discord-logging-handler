from dataclasses import dataclass, field
from typing import Type, List

from discord_logging_handler.constants import NO_APP_NAME_ERROR_MESSAGE
from discord_logging_handler.enums import DiscordLoggingHandlerLevel
from discord_logging_handler.message_template_builder import (
    BaseMessageTemplateBuilder,
    ErrorMessageTemplateBuilder,
)
from discord_logging_handler.models import BaseContentData, ErrorContentData


@dataclass
class DiscordHandlerInputData:
    app_name: str
    webhook_url: str | None = None
    webhook_id: str | None = None
    webhook_token: str | None = None
    username: str | None = None
    avatar_url: str | None = None
    add_additional_data_to_content: bool = True
    content_dataclass_type: Type[BaseContentData] = ErrorContentData
    content_dataclass_additional_fields: List[str] = field(default_factory=list)
    message_template_builder_type: Type[BaseMessageTemplateBuilder] = (
        ErrorMessageTemplateBuilder
    )
    logging_level: DiscordLoggingHandlerLevel = DiscordLoggingHandlerLevel.ERROR

    def __post_init__(self):
        if self.app_name is None:
            raise ValueError(NO_APP_NAME_ERROR_MESSAGE)
