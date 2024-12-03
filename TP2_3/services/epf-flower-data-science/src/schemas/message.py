from src.schemas.camelcase import CamelCase
from typing import Any


class MessageResponse(CamelCase):
    message: str
    data: Any
