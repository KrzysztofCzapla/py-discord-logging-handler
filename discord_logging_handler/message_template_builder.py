from abc import ABC, abstractmethod
from typing import Generic

from discord_logging_handler.constants import DEFAULT_PING, DEFAULT_EMOJI
from discord_logging_handler.models import ErrorContentData, ContentDataType


class BaseMessageTemplateBuilder(ABC, Generic[ContentDataType]):
    """
    Abstract class for creating message templates.

    Message templates are formattable strings that will be used to send to discord API as the `content` param.

    Every subclass must implement `build_message_template` method.
    """

    @staticmethod
    @abstractmethod
    def build_message_template(data: ContentDataType, ping: str = DEFAULT_PING, alert_emoji: str = DEFAULT_EMOJI, additional_info: str | None = None) -> str:
        """
        Builds a string message based on provided data and other params.
        
        Args:
            data: (BaseContentData subclasses): data from which we will take information to put in the returned content string
            ping: (optional str): who to ping. Defaults to `@everyone`. Used as a param instead of hard-coding, so user can change it easily without creating new subclass
            alert_emoji: (optional str): Top emoji used. Defaults to `:rotating_light:`. Used as a param instead of hard-coding, so user can change it easily without creating new subclass
            additional_info: (optional bool): Additional information about the logging itself in the final message, i.e. what was truncated. Defaults to None.

        Returns:
            str: a content message ready to be sent to the API
        """


class ErrorMessageTemplateBuilder(BaseMessageTemplateBuilder[ErrorContentData]):
    @staticmethod
    def build_message_template(data: ErrorContentData, ping: str = DEFAULT_PING, alert_emoji: str = DEFAULT_EMOJI, additional_info: str | None = None) -> str:
        return f"""{alert_emoji} {ping} {alert_emoji}
:ringed_planet: **APP:** {data.app_name}
:page_facing_up: **FILE:** {data.file}
:warning: **ERROR:** {data.error_message}
{f':printer: **TRACEBACK:** {data.traceback}' if data.traceback else ''}
{f'-# **Additional Info** {additional_info}' if additional_info else ''}
"""