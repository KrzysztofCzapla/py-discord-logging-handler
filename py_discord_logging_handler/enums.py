from enum import IntEnum


class DiscordLoggingHandlerLevel(IntEnum):
    """
    Custom ENUM for logging level.

    Built-in logging and loguru uses the int values, while structlog uses lower-cased `.name` of each attribute.
    """

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    @classmethod
    def get_current_and_higher_level_name(cls, value):
        return [member.name for member in cls if member.value >= value]
