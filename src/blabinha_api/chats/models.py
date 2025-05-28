from datetime import datetime as dt
from zoneinfo import ZoneInfo
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship
from .schemas import ChatBase

if TYPE_CHECKING:
    from dialogs.models import Dialog


class Chat(ChatBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    dialogs: list["Dialog"] = Relationship(back_populates="chat", cascade_delete=True)

    created_at: dt = Field(default_factory=lambda: dt.now(ZoneInfo('America/Sao_Paulo')))
    updated_at: dt = Field(
        default_factory=lambda: dt.now(ZoneInfo('America/Sao_Paulo')),
        sa_column_kwargs={"onupdate": lambda: dt.now(ZoneInfo('America/Sao_Paulo'))},
    )
