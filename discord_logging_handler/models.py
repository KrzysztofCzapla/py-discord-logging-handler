from dataclasses import dataclass, field
from typing import TypeVar

from discord_logging_handler.constants import (
    DEFAULT_EMOJI,
    DEFAULT_PING,
    DISCORD_MAX_CHARS_LIMIT,
    DISCORD_JSON_CONTENT_VALUE_ABOVE_LIMIT_ERROR_MESSAGE,
)


@dataclass
class DiscordAPIJSONData:
    content: str
    username: str | None = None
    avatar_url: str | None = None

    def __post_init__(self):
        if len(self.content) > DISCORD_MAX_CHARS_LIMIT:
            raise ValueError(DISCORD_JSON_CONTENT_VALUE_ABOVE_LIMIT_ERROR_MESSAGE)


@dataclass
class BaseContentData:
    app_name: str
    file: str
    message: str
    traceback: str | None = field(default=None, init=False)
    alert_emoji: str = field(default=DEFAULT_EMOJI, init=False)
    ping: str = field(default=DEFAULT_PING, init=False)
    additional_info: str | None = field(default=None, init=False)


ContentDataType = TypeVar("ContentDataType", bound=BaseContentData)


@dataclass
class ErrorContentData(BaseContentData):
    pass
