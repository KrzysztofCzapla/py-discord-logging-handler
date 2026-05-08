from abc import ABC, abstractmethod
from typing import Generic, Dict, List

from discord_logging_handler.constants import (
    CONTENT_DATA_TRACEBACK,
    CONTENT_DATA_FILE,
    CONTENT_DATA_MESSAGE,
)
from discord_logging_handler.models import ErrorContentData, ContentDataType


class BaseMessageTemplateBuilder(ABC, Generic[ContentDataType]):
    """
    Abstract class for creating message templates that must be inherited.

    You can specify the content dataclass that will be used by the Builder to generate content like this:
    `class ErrorMessageTemplateBuilder(BaseMessageTemplateBuilder[ErrorContentData]):`
    This is done for typing purposes and can be skipped.

    Attributes:
        - FIELD_LENGTH_LIMITS - you can specify how long each attribute/field in the dataclass can be. This must be used
            smartly, since Discord allows only 2k characters per message.
        - PARTS_CONCATENATION_CHARACTER - the main method returns list of strings that later need to be concatenated.
            This param specifies which character concatenates those strings.


    Every subclass must implement `build_message_parts` method.
    """

    FIELD_LENGTH_LIMITS: Dict[str, int] = {}
    PARTS_CONCATENATION_CHARACTER: str = "\n\n"

    @staticmethod
    @abstractmethod
    def build_message_parts(data: ContentDataType) -> List[str]:
        """
        Builds a string message based on provided data and other params.

        Args:
            data: (BaseContentData subclasses): data from which we will take information to put in the returned content string

        Returns:
            List[str]: list of strings that will be later concatenated.
                *THEY MUST BE ORDERED BY IMPORTANCE DESCENDING*.
                This is because we will later cut them in case some of them cannot fit into the max chars allowed (2k)
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
