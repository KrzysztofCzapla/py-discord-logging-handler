from dataclasses import dataclass
from typing import TypeVar


@dataclass
class DiscordJSONData:
    # The actual message that is being sent
    content: str
    # with those you can override the default username and avatar of the webhook app
    username: str | None = None
    avatar_url: str | None = None


@dataclass
class BaseContentData:
    pass


ContentDataType = TypeVar("ContentDataType", bound=BaseContentData)


@dataclass
class ErrorContentData(BaseContentData):
    app_name: str
    file: str
    error_message: str
    traceback: str | None = None

