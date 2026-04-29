from dataclasses import dataclass
from discord_logging_handler.constants import DISCORD_WEBHOOK_URL_PREFIX


@dataclass
class DiscordJSONData:
    content: str


class DiscordAPIAdapter:
    @staticmethod
    def send_webhook(
        body: DiscordJSONData,
    ):
        pass

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

    @staticmethod
    def _construct_webhook_url_from_id_and_token(webhook_id: str, webhook_token: str):
        return f"{DISCORD_WEBHOOK_URL_PREFIX}{webhook_id}/{webhook_token}"

    @staticmethod
    def _verify_webhook_url(webhook_url: str) -> str:
        if not webhook_url.startswith(DISCORD_WEBHOOK_URL_PREFIX):
            raise ValueError("Received wrong URL for the discord webhook.")
        return webhook_url
