# py-discord-logging-handler

Out of the box, highly customizable, discord logging handler that supports multiple logger libraries.

![CI](https://img.shields.io/github/actions/workflow/status/KrzysztofCzapla/py-discord-logging-handler/.github/workflows/publish.yaml)
![PyPI](https://img.shields.io/pypi/v/py-discord-logging-handler)

---

py-discord-logging-handler is a package that helps you save your logs as discord messages.
It uses Discord's API to send webhooks with a nicely formatted logging information.

This is a perfect package if you need a simple error logging for your side project.

The key features are:

- **Fast and no dependencies:** Because there are no dependencies and the code is simple the handlers work super fast
- **Out of the box usage:** No need to waste time setting it up. You can just start using it.
- **Third parties loggers support:** The package supports built-in logging module as well as loguru and structlog
- **Highly customizable:** You can customize the data and the format of the final logging message

This package is not an official product by Discord Inc.

---

## Installation

```bash
$ pip install py_discord_logging_handler
```

## Quickstart

Code:
```python
from py_discord_logging_handler import add_discord_logging_handler, DiscordHandlerInputData
from logging import getLogger

logger = getLogger(__file__)
input_data = DiscordHandlerInputData(
    app_name="my_app_name",
    webhook_url="https://discord.com/api/webhooks/my_id/my_token"
)
add_discord_logging_handler(logger, input_data)

try:
    x = 1/0
except Exception as e:
    logger.error(f"this is my error messsage: {e}")
```
Result:
// put image here

## Usage Guide

stuff: 1) Default 2) Loguru 3) Structlog 4) General input fields + ENV variables 5) Custom Builder and data type 6) Django integration

## Future Development

Future features/plans include:
- Supporting more loggers
- Improving message formatting
- 