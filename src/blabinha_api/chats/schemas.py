from datetime import datetime
import enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID
from sqlmodel import Field
from sqlmodel.main import SQLModel

if TYPE_CHECKING:
    from blabinha_api.dialogs.schemas import DialogPublic
    from blabinha_api.accounts.schemas import UserPublic


class ChatState(enum.Enum):
    OPEN = True
    CLOSE = False


class ChatBase(SQLModel):
    model: str = Field(default="gpt-4o")
    strategy: str = Field(default="one-shot")
    state: ChatState = Field(default=ChatState.OPEN)
    current_section: int = Field(default=100)
    bonusQnt: int = Field(default=0)
    stars: int = Field(default=0)
    repetition: int = Field(default=0)
    heroFeatures: str = Field(default="")
    totalTokens: int = Field(default="0")
    username: str = Field(default="")
    image: str = Field(default="")


class ChatCreate(SQLModel):
    model: str
    strategy: str | None = None
    init_section: int | None = None


class ChatPublic(ChatBase):
    id: UUID
    owner: Optional["UserPublic"] = None
    created_at: datetime
    updated_at: datetime


class ChatPublicWithDialogs(ChatPublic):
    dialogs: list["DialogPublic"] = []


class ChatUpdate(SQLModel):
    model: str | None = None
    strategy: str | None = None
    current_section: int | None = None
    bonusQnt: int | None = None
    stars: int | None = None
    heroFeatures: str | None = None
    username: str | None = None
    image: str |  None = None
