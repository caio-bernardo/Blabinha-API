from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Field
from sqlmodel.main import SQLModel

if TYPE_CHECKING:
    from src.chats.schemas import ChatPublic


class DialogBase(SQLModel):
    input: str = Field()
    answer: str = Field(default="")
    section: int = Field(default=100)
    tokens: int = Field(default=0)


class DialogPublic(DialogBase):
    id: uuid.UUID
    created_at: datetime


class DialogPublicWithChat(DialogPublic):
    chat: Optional["ChatPublic"] = None


class DialogCreate(SQLModel):
    chat_id: uuid.UUID
    input: str
