import datetime
from enum import Enum
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel
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
    dialogs: List['Dialog'] = Relationship(back_populates="chat", cascade_delete=True, sa_relationship_kwargs={"lazy": "joined"})

    # TODO: update this to a enum of models
    model: str = Field(default="gpt-4o")
    # TODO: update this to a enum of strategies
    strategy: str = Field(default="one-shot")

    state: ChatState = Field(default=ChatState.OPEN)
    current_turn: int = Field(default=100)
    bonusQnt: int = Field(default=0)
    stars: int = Field(default=0)
    repetition: int = Field(default=0) # qts vezes uma pergunta foi repetida
    heroFeature: str = Field(default="")
    totalTokens: int = Field(default=0)

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.datetime.utcnow},
    )


class ChatPublic(SQLModel, table=False):
    """Public Chat model (without sensitive fields)"""
    id: int

    # TODO: update this to a enum of models
    model: str
    # TODO: update this to a enum of strategies
    strategy: str
    state: ChatState
    bonusQnt: int
    stars: int
    repetition: int
    heroFeature: str

    totalTokens: int

    created_at: datetime.datetime
    updated_at: datetime.datetime

class ChatPublicWithDialogs(ChatPublic):
    dialogs: List["DialogPublic"] = []


class ChatCreate(SQLModel, table=False):
    """Chat creation model (necessary for creation)"""

    # TODO: update this to a enum of models
    model: Optional[str] = Field(default="gpt-4o")
    # TODO: update this to a enum of strategies
    strategy: Optional[str] = Field(default="one-shot")
    turn: Optional[int] = Field(default=100)
