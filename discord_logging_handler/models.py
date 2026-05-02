from dataclasses import dataclass, field
from typing import TypeVar

from discord_logging_handler.constants import DEFAULT_EMOJI, DEFAULT_PING


@dataclass
class DiscordJSONData:
    # The actual message that is being sent
    content: str
    # with those you can override the default username and avatar of the webhook app
    username: str | None = None
    avatar_url: str | None = None


@dataclass
class BaseContentData:
    additional_info: str | None = field(default=None, init=False)
    alert_emoji: str = field(default=DEFAULT_EMOJI, init=False)
    ping: str = field(default=DEFAULT_PING, init=False)


ContentDataType = TypeVar("ContentDataType", bound=BaseContentData)


@dataclass
class ErrorContentData(BaseContentData):
    app_name: str
    file: str
    error_message: str
    traceback: str | None = None
