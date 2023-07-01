from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from datetime import datetime


class IdName(BaseModel):
    id: PydanticObjectId
    name: str


class Message(Document):
    chat: IdName
    sender: IdName
    text: str
    datetime: datetime
    is_read: bool = False

    class Settings:
        name = "message"
