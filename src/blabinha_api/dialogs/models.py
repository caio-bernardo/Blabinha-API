from datetime import datetime as dt
from zoneinfo import ZoneInfo
from typing import TYPE_CHECKING, Optional
import uuid

from sqlmodel import Field, Relationship
from .schemas import DialogBase

if TYPE_CHECKING:
    from chats.models import Chat


class Dialog(DialogBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    chat_id: uuid.UUID | None = Field(foreign_key="chat.id")
    chat: Optional["Chat"] = Relationship(back_populates="dialogs")
    created_at: dt = Field(
        default_factory=lambda: dt.now(ZoneInfo("America/Sao_Paulo"))
    )
