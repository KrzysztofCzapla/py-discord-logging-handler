from unittest.mock import MagicMock


def get_mock_urllib_json_body(mock_urllib: MagicMock) -> str:
    return str(mock_urllib.call_args[0][0].data)
