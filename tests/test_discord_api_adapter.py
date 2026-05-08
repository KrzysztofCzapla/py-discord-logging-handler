import pytest

from py_discord_logging_handler.constants import (
    DISCORD_LOGGING_HANDLER_WEBHOOK_URL,
    DISCORD_LOGGING_HANDLER_WEBHOOK_ID,
    DISCORD_LOGGING_HANDLER_WEBHOOK_TOKEN,
)
from py_discord_logging_handler.discord_api_adapter import DiscordAPIAdapter


class TestDiscordAPIAdapter:
    adapter = DiscordAPIAdapter()
    good_url = "https://discord.com/api/webhooks/adadada/dadadad"
    webhook_id = "abc"
    webhook_token = "123"
    webhook_from_id_and_token = "https://discord.com/api/webhooks/abc/123"

    def test_verify_webhook_url(self):
        self.adapter._verify_webhook_url(self.good_url)

        bad_url = "https://discord.com/api/adadada/dadadad"
        with pytest.raises(ValueError):
            self.adapter._verify_webhook_url(bad_url)

    def test_construct_webhook(self):
        url = self.adapter._construct_webhook_url_from_id_and_token(
            self.webhook_id, self.webhook_token
        )

        assert url == self.webhook_from_id_and_token

    def test_get_webhook_with_url(self):
        url = self.adapter._get_webhook_url(webhook_url=self.good_url)
        assert url == self.good_url

    def test_get_webhook_with_id_and_token(self):
        assert (
            self.adapter._get_webhook_url(
                webhook_id=self.webhook_id, webhook_token=self.webhook_token
            )
            == self.webhook_from_id_and_token
        )

    def test_get_webhook_environ_url(self, monkeypatch):
        monkeypatch.setenv(DISCORD_LOGGING_HANDLER_WEBHOOK_URL, self.good_url)
        assert self.adapter._get_webhook_url() == self.good_url

    def test_get_webhook_environ_id_and_token(self, monkeypatch):
        monkeypatch.delenv(DISCORD_LOGGING_HANDLER_WEBHOOK_URL, raising=False)
        monkeypatch.setenv(DISCORD_LOGGING_HANDLER_WEBHOOK_ID, self.webhook_id)
        monkeypatch.setenv(DISCORD_LOGGING_HANDLER_WEBHOOK_TOKEN, self.webhook_token)
        assert self.adapter._get_webhook_url() == self.webhook_from_id_and_token

    def test_get_webhook_nothing_specified(self, monkeypatch):
        monkeypatch.delenv(DISCORD_LOGGING_HANDLER_WEBHOOK_ID, raising=False)
        monkeypatch.delenv(DISCORD_LOGGING_HANDLER_WEBHOOK_TOKEN, raising=False)
        with pytest.raises(ValueError):
            self.adapter._get_webhook_url()

    def test_send_webhook(self, monkeypatch, discord_api_json_data):
        # `urllib.request.urlopen` should be mocked from the autorun fixture
        self.adapter.send_webhook(discord_api_json_data, webhook_url=self.good_url)
