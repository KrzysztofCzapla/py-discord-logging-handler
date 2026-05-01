from dataclasses import dataclass
from typing import Generic

from discord_logging_handler.message_template_builder import BaseMessageTemplateBuilder, ErrorMessageTemplateBuilder
from discord_logging_handler.models import ContentDataType


@dataclass
class ContentManager(Generic[ContentDataType]):
    template_builder: BaseMessageTemplateBuilder = ErrorMessageTemplateBuilder

    def create_content_message(self, data: ContentDataType, ):
        """
        Notebook:
        The hardest part here is the truncation because of the max character
        """
