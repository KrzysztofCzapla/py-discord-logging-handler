from dataclasses import dataclass
from typing import Dict, List, Type

from discord_logging_handler.constants import (
    DEFAULT_ADDITIONAL_DATA_TEXT,
    DEFAULT_TRUNCATION_ENDING,
    DISCORD_MAX_CHARS_LIMIT,
)
from discord_logging_handler.message_template_builder import (
    BaseMessageTemplateBuilder,
    ErrorMessageTemplateBuilder,
)
from discord_logging_handler.models import ContentDataType


@dataclass
class ContentManager:
    @staticmethod
    def create_content_message(
        data: ContentDataType,
        template_builder: Type[
            BaseMessageTemplateBuilder
        ] = ErrorMessageTemplateBuilder,
        add_additional_info: bool = True,
    ) -> str:
        truncated_fields = ContentManager._truncate_fields(
            data, template_builder.FIELD_LENGTH_LIMITS, DEFAULT_TRUNCATION_ENDING
        )
        if add_additional_info:
            data.additional_info = DEFAULT_ADDITIONAL_DATA_TEXT.format(
                truncated_fields=truncated_fields
            )
        content_message = ContentManager._assemble_parts(
            parts=template_builder.build_message_parts(data),
            concatenation_char=template_builder.PARTS_CONCATENATION_CHARACTER,
            limit=DISCORD_MAX_CHARS_LIMIT,
            truncation_ending=DEFAULT_TRUNCATION_ENDING,
        )
        return content_message

    @staticmethod
    def _truncate_fields(
        data: ContentDataType, limits: Dict[str, int], truncation_ending: str
    ) -> List[str]:
        truncated_fields = []
        for field_name, limit in limits.items():
            attr = getattr(data, field_name, None)
            if not attr or not isinstance(attr, str):
                continue
            if len(attr) > limit:
                setattr(
                    data,
                    field_name,
                    truncation_ending
                    + attr[len(attr) - limit - len(truncation_ending) :],
                )
                truncated_fields.append(field_name)
        return truncated_fields

    @staticmethod
    def _assemble_parts(
        parts: List[str], concatenation_char: str, limit: int, truncation_ending: str
    ) -> str:
        result = ""
        for part in parts:
            if not part:
                continue
            if len((new_result := result + concatenation_char + part)) < limit:
                result = new_result
            else:
                if len(result) + len(truncation_ending) < limit:
                    result += truncation_ending
                else:
                    result = result[: -len(truncation_ending)] + truncation_ending
                break
        return result
