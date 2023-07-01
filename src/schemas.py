from pydantic import BaseModel
from enum import Enum
from typing import Optional, List


class Event(Enum):
    FIRST = "first"
    NEXT = "next"


class First(BaseModel):
    channels: Optional[List[str]]


class PydanticMessage(BaseModel):
    channel: str
    sender: str
    text: str
    datetime: str
