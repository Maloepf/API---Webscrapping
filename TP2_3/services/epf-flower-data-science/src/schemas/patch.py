from src.schemas.camelcase import CamelCase
from typing import Any, Optional

class DatasetUpdate(CamelCase):
    name: Optional[str] = None
    url: Optional[str] = None

