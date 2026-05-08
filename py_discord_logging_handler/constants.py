DISCORD_WEBHOOK_URL_PREFIX = "https://discord.com/api/webhooks/"
DISCORD_MAX_CHARS_LIMIT = 2000
DISCORD_DEFAULT_REQUEST_METHOD = "POST"

# ENV Variables
DISCORD_LOGGING_HANDLER_WEBHOOK_URL = "DISCORD_LOGGING_HANDLER_WEBHOOK_URL"
DISCORD_LOGGING_HANDLER_WEBHOOK_TOKEN = "DISCORD_LOGGING_HANDLER_WEBHOOK_TOKEN"
DISCORD_LOGGING_HANDLER_WEBHOOK_ID = "DISCORD_LOGGING_HANDLER_WEBHOOK_ID"

# Error Messages
DEFAULT_ERROR_MESSAGE_PREFIX = "DiscordLoggingHandlerException: "
WRONG_WEBHOOK_URL_ERROR_MESSAGE = (
    f"{DEFAULT_ERROR_MESSAGE_PREFIX}Received wrong URL for the discord webhook."
)
NO_WEBHOOK_URL_SET_ERROR_MESSAGE = f"""{DEFAULT_ERROR_MESSAGE_PREFIX}Could not get the webhook URL to send to Discord API.

You must set it in one of those ways:
1) pass `webhook_url` argument in the main handler function
2) pass `webhook_id` and `webhook_token` arguments in the main handler function
3) Set the `DISCORD_LOGGING_HANDLER_WEBHOOK_URL` environmental variable
4) Set the `DISCORD_LOGGING_HANDLER_WEBHOOK_TOKEN` and `DISCORD_LOGGING_HANDLER_WEBHOOK_ID` environmental variables
"""
NO_LOGGER_SET_ERROR_MESSAGE = f"{DEFAULT_ERROR_MESSAGE_PREFIX}Specified Logger is None."
NO_INPUT_DATA_ERROR_MESSAGE = f"{DEFAULT_ERROR_MESSAGE_PREFIX}input_data is None."
NO_APP_NAME_ERROR_MESSAGE = f"{DEFAULT_ERROR_MESSAGE_PREFIX}App Name parameter is None"
LOGGER_NOT_SUPPORTED_ERROR_MESSAGE = (
    f"{DEFAULT_ERROR_MESSAGE_PREFIX}Specified Logger is not supported"
)
DISCORD_JSON_CONTENT_VALUE_ABOVE_LIMIT_ERROR_MESSAGE = f"{DEFAULT_ERROR_MESSAGE_PREFIX}The `content` value inside DiscordAPIJSONData is above {DISCORD_MAX_CHARS_LIMIT} characters."
STRUCTLOG_WRONG_FUNCTION_ERROR_MESSAGE = f"{DEFAULT_ERROR_MESSAGE_PREFIX}Structlog configuration should be done during logging initialization. Use `discord_structlog_processor_wrapper` processor wrapper instead of `add_discord_logging_handler`"


# Requests
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "python-requests/2.31.0",
    "Accept": "*/*",
    "Connection": "keep-alive",
}
DEFAULT_ENCODING = "utf-8"

# Message Template Builders
DEFAULT_PING = "@everyone"
DEFAULT_EMOJI = ":rotating_light:"
DEFAULT_TRUNCATION_ENDING = "..."

DEFAULT_ADDITIONAL_DATA_TEXT = "Truncated Fields: {truncated_fields}"

# Loggers Attributes
DEFAULT_LOGGER_METHOD = "addHandler"
LOGURU_METHOD = "add"
STRUCTLOG_METHOD = "get_config"

# Handlers Constants
LOGURU_MESSAGE = "message"
LOGURU_FILE = "file"
LOGURU_EXTRA = "extra"

STRUCTLOG_EVENT = "event"
STRUCTLOG_MESSAGE = "message"
STRUCTLOG_PATHNAME = "pathname"

# ContentData Attributes
CONTENT_DATA_TRACEBACK = "traceback"
CONTENT_DATA_FILE = "file"
CONTENT_DATA_MESSAGE = "message"
