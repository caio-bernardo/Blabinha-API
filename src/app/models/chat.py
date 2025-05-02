import datetime
from enum import Enum
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from .dialog import Dialog, DialogPublic


class ChatState(Enum):
    """Represent possible states of a chat: either open or closed"""

    OPEN = "open"
    CLOSED = "closed"


class Chat(SQLModel, table=True):
    """Chat database model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    dialogs: List["Dialog"] = Relationship(
        back_populates="chat",
        cascade_delete=True,
        sa_relationship_kwargs={"lazy": "joined"},
    )

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

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.datetime.utcnow},
    )


class ChatPublic(SQLModel, table=False):
    """Public Chat model (without sensitive fields)"""

    id: int

    # TODO: update this to a enum of models
    model: str = Field(description="Model of the LLM used by Blabinha")
    # TODO: update this to a enum of strategies
    strategy: str = Field(description="Prompt strategy used by Blabinha")
    state: ChatState = Field(description="Current state of the chat. A closed chat won't accept dialogs")
    bonusQnt: int = Field(description="Quantity of bonus since last dialog")
    stars: int = Field(description="Quantity of stars since last dialog")
    repetition: int = Field(description="How many time current section has been repeated")
    heroFeature: str = Field(description="all features of the hero joined by '||'")

    totalTokens: int = Field(description="How many tokens this chat has consumed (sum of all dialog tokens)")

    created_at: datetime.datetime = Field(description="time of creation")
    updated_at: datetime.datetime = Field(description="time of last update")


class ChatPublicWithDialogs(ChatPublic):
    """Public model of chat with a list of all dialogs owned by the chat"""
    dialogs: List["DialogPublic"] = Field(default=[], description="List of all dialogs owned by this chat")


class ChatCreate(SQLModel, table=False):
    """Chat creation model (necessary for creation) but most field are optional"""

    # TODO: update this to a enum of models
    model: Optional[str] = Field(default="gpt-4o", description="LLM model to be used by Blabinha")
    # TODO: update this to a enum of strategies
    strategy: Optional[str] = Field(default="one-shot", description="Prompt strategy to be used by Blabinha")
    turn: Optional[int] = Field(default=100, description="To be the initial section of conversation")
