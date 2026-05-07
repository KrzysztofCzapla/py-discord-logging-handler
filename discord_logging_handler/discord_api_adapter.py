import urllib.request
from dataclasses import asdict
import os
import json
from discord_logging_handler.constants import (
    DISCORD_WEBHOOK_URL_PREFIX,
    DISCORD_LOGGING_HANDLER_WEBHOOK_URL,
    DISCORD_LOGGING_HANDLER_WEBHOOK_TOKEN,
    DISCORD_LOGGING_HANDLER_WEBHOOK_ID,
    NO_WEBHOOK_URL_SET_ERROR_MESSAGE,
    DEFAULT_HEADERS,
    WRONG_WEBHOOK_URL_ERROR_MESSAGE,
    DEFAULT_ENCODING,
    DISCORD_DEFAULT_REQUEST_METHOD,
)
from discord_logging_handler.models import DiscordAPIJSONData


class DiscordAPIAdapter:
    """
    Internal class for interaction with the Discord API.

    No need for detailed docstrings for now, since everything is straightforward and isolated from the rest of the package.
    """

    @staticmethod
    def send_webhook(
        body: DiscordAPIJSONData,
        webhook_url: str | None = None,
        webhook_id: str | None = None,
        webhook_token: str | None = None,
    ):
        webhook_url = DiscordAPIAdapter._get_webhook_url(
            webhook_url, webhook_id, webhook_token
        )
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(asdict(body)).encode(DEFAULT_ENCODING),
            headers=DEFAULT_HEADERS,
            method=DISCORD_DEFAULT_REQUEST_METHOD,
        )
        urllib.request.urlopen(req)

    @staticmethod
    def _get_webhook_url(
        webhook_url: str | None = None,
        webhook_id: str | None = None,
        webhook_token: str | None = None,
    ):
        if webhook_url:
            return DiscordAPIAdapter._verify_webhook_url(webhook_url)
        elif (
            isinstance(webhook_id, str)
            and webhook_id
            and isinstance(webhook_token, str)
            and webhook_token
        ):
            webhook_url = DiscordAPIAdapter._construct_webhook_url_from_id_and_token(
                webhook_id, webhook_token
            )
            return DiscordAPIAdapter._verify_webhook_url(webhook_url)
        elif webhook_url := os.environ.get(DISCORD_LOGGING_HANDLER_WEBHOOK_URL):
            return DiscordAPIAdapter._verify_webhook_url(webhook_url)
        elif (webhook_id := os.environ.get(DISCORD_LOGGING_HANDLER_WEBHOOK_ID)) and (
            webhook_token := os.environ.get(DISCORD_LOGGING_HANDLER_WEBHOOK_TOKEN)
        ):
            webhook_url = DiscordAPIAdapter._construct_webhook_url_from_id_and_token(
                webhook_id, webhook_token
            )
            return DiscordAPIAdapter._verify_webhook_url(webhook_url)
        raise ValueError(NO_WEBHOOK_URL_SET_ERROR_MESSAGE)

    @staticmethod
    def _construct_webhook_url_from_id_and_token(webhook_id: str, webhook_token: str):
        return f"{DISCORD_WEBHOOK_URL_PREFIX}{webhook_id}/{webhook_token}"

    @staticmethod
    def _verify_webhook_url(webhook_url: str) -> str:
        if not webhook_url.startswith(DISCORD_WEBHOOK_URL_PREFIX):
            raise ValueError(WRONG_WEBHOOK_URL_ERROR_MESSAGE)
        return webhook_url
