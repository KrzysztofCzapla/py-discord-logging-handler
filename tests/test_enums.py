from discord_logging_handler.enums import DiscordLoggingHandlerLevel


class TestDiscordHandlerLoggingLevel:
    def test_method(self):
        error = DiscordLoggingHandlerLevel.ERROR
        current_and_higher = (
            DiscordLoggingHandlerLevel.get_current_and_higher_level_name(error.value)
        )

        for name in current_and_higher:
            assert getattr(DiscordLoggingHandlerLevel, name) >= error

        debug = DiscordLoggingHandlerLevel.DEBUG
        current_and_higher = (
            DiscordLoggingHandlerLevel.get_current_and_higher_level_name(debug.value)
        )

        for name in current_and_higher:
            assert getattr(DiscordLoggingHandlerLevel, name) >= debug
