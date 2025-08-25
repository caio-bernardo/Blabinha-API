from datetime import datetime as dt
from zoneinfo import ZoneInfo

from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
import uuid

if TYPE_CHECKING:
    from blabinha_api.apps.chats.models import Chat



class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(max_length=127, unique=True)
    hashed_password: str
    is_admin: bool = Field(default=False)

    chats: list["Chat"] = Relationship(back_populates="owner", cascade_delete=True)

    created_at: dt = Field(
        default_factory=lambda: dt.now(ZoneInfo("America/Sao_Paulo"))
    )
    updated_at: dt = Field(
        default_factory=lambda: dt.now(ZoneInfo("America/Sao_Paulo")),
        sa_column_kwargs={"onupdate": lambda: dt.now(ZoneInfo("America/Sao_Paulo"))},
    )
