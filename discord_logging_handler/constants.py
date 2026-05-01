DISCORD_WEBHOOK_URL_PREFIX = "https://discord.com/api/webhooks/"
DISCORD_MAX_CHARS = "2000"

# ENV Variables
DISCORD_LOGGING_HANDLER_WEBHOOK_URL = "DISCORD_LOGGING_HANDLER_WEBHOOK_URL"
DISCORD_LOGGING_HANDLER_WEBHOOK_TOKEN = "DISCORD_LOGGING_HANDLER_WEBHOOK_TOKEN"
DISCORD_LOGGING_HANDLER_WEBHOOK_ID = "DISCORD_LOGGING_HANDLER_WEBHOOK_ID"

# Error Messages
WRONG_WEBHOOK_URL_ERROR_MESSAGE = "Received wrong URL for the discord webhook."
NO_WEBHOOK_URL_SET_ERROR_MESSAGE = """
DiscordLoggingHandlerException: Could not get the webhook URL to send to Discord API.

You must set it in one of those ways:
1) pass `webhook_url` argument in the main handler function
2) pass `webhook_id` and `webhook_token` arguments in the main handler function
3) Set the `DISCORD_LOGGING_HANDLER_WEBHOOK_URL` environmental variable
4) Set the `DISCORD_LOGGING_HANDLER_WEBHOOK_TOKEN` and `DISCORD_LOGGING_HANDLER_WEBHOOK_ID` environmental variables
"""

# Requests
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "python-requests/2.31.0",
    "Accept": "*/*",
    "Connection": "keep-alive",
}

# Message Template Builders
DEFAULT_PING = "@everyone"
DEFAULT_EMOJI = ":rotating_light:"