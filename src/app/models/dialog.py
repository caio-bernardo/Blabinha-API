import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .chat import Chat, ChatPublic


class Dialog(SQLModel, table=True):
    """Dialog database model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    input: str = Field(default="")
    answer: str = Field(default="")
    turn: int = Field(default=100)
    tokens: int = Field(default=0)
    chat_id: Optional[int] = Field(default=None, foreign_key="chat.id")
    chat: Optional["Chat"] = Relationship(back_populates="dialogs")

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class DialogCreate(SQLModel, table=False):
    """Dialog creation model"""

    chat_id: int  # TODO: think about using a chat name instead to keep id secret
    input: str


class DialogPublic(SQLModel, table=False):
    """Dialog public model (without sensitive fields)"""

    id: int
    input: str
    answer: str
    turn: int = Field(default=100)
    tokens: int = Field(default=0)
    chat: Optional["ChatPublic"] = Relationship(back_populates="dialogs")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
