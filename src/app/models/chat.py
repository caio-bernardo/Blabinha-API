import datetime
from enum import Enum
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .dialog import Dialog, DialogPublic


class ChatState(Enum):
    """Represent possible states of a chat"""

    OPEN = "open"
    CLOSED = "closed"


class Chat(SQLModel, table=True):
    """Chat database model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    dialogs: List["Dialog"] = Relationship(back_populates="chat", cascade_delete=True)

    # TODO: update this to a enum of models
    model: str = Field(default="gpt-4o")
    # TODO: update this to a enum of strategies
    strategy: str = Field(default="one-shot")

    state: ChatState = Field(default=ChatState.OPEN)
    current_turn: int = Field(default=100)
    bonusQnt: int = Field(default=0)
    stars: int = Field(default=0)
    repetition: int = Field(default=0)
    heroFeature: str = Field(default="")
    totalTokens: int = Field(default=0)
    history: str = Field(max_length=10000, default="")

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.datetime.utcnow},
    )


class ChatPublic(SQLModel, table=False):
    """Public Chat model (without sensitive fields)"""

    id: int
    dialogs: List["DialogPublic"] = Relationship(back_populates="chat")

    # TODO: update this to a enum of models
    model: str = Field(default="gpt-4o")
    # TODO: update this to a enum of strategies
    strategy: str = Field(default="one-shot")

    state: ChatState = Field(default=ChatState.OPEN)
    bonusQnt: int = Field(default=0)
    stars: int = Field(default=0)
    repetition: int = Field(default=0)
    heroFeature: str = Field(default="")

    history: str = Field(max_length=10000, default="")
    totalTokens: int = Field(default=0)

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.datetime.utcnow},
    )


class ChatCreate(SQLModel, table=False):
    """Chat creation model (necessary for creation)"""

    # TODO: update this to a enum of models
    model: str = Field(default="gpt-4o")
    # TODO: update this to a enum of strategies
    strategy: str = Field(default="one-shot")
    turn: int = Field(default=100)
