from abc import ABC, abstractmethod
from typing import Generic, Dict, List

from discord_logging_handler.constants import (
    CONTENT_DATA_TRACEBACK,
    CONTENT_DATA_FILE,
    CONTENT_DATA_MESSAGE,
)
from discord_logging_handler.models import ErrorContentData, ContentDataType


class BaseMessageTemplateBuilder(ABC, Generic[ContentDataType]):
    FIELD_LENGTH_LIMITS: Dict[str, int] = {}
    PARTS_CONCATENATION_CHARACTER: str = "\n\n"

    """
    Abstract class for creating message templates.

    Message templates are formattable strings that will be used to send to discord API as the `content` param.

    Every subclass must implement `build_message_parts` method.
    """

    @staticmethod
    @abstractmethod
    def build_message_parts(data: ContentDataType) -> List[str]:
        """
        Builds a string message based on provided data and other params.

        Args:
            data: (BaseContentData subclasses): data from which we will take information to put in the returned content string

        Returns:
            str: a content message ready to be sent to the API
        """


class ErrorMessageTemplateBuilder(BaseMessageTemplateBuilder[ErrorContentData]):
    FIELD_LENGTH_LIMITS = {
        CONTENT_DATA_TRACEBACK: 900,
        CONTENT_DATA_FILE: 200,
        CONTENT_DATA_MESSAGE: 400,
    }

    @staticmethod
    def build_message_parts(data: ErrorContentData) -> List[str]:
        """Parts are ordered by importance"""
        return [
            f"{data.alert_emoji} {data.ping} {data.alert_emoji}",
            f"{f'-# **Additional Info:** `{data.additional_info}`' if data.additional_info else ''}",
            f":ringed_planet: **APP:** `{data.app_name}`",
            f":page_facing_up: **FILE:** `{data.file}`",
            f":warning: **ERROR:** `{data.message}`",
            f"{f':printer: **TRACEBACK:** ```{data.traceback}```' if data.traceback else ''}",
        ]
