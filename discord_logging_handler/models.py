from dataclasses import dataclass


@dataclass
class DiscordJSONData:
    # The actual message that is being sent
    content: str
    # with those you can override the default username and avatar of the webhook app
    username: str | None = None
    avatar_url: str | None = None


@dataclass
class DefaultDiscordMessageTemplate:
    """All Message Templates should inherit this"""

    pass
    # TODO - think whether the logic should be here and overriden or managed by the ocntent manager, or both?


@dataclass
class ErrorDiscordMessageTemplate(DefaultDiscordMessageTemplate):
    app_name: str
    file: str
    error_message: str
