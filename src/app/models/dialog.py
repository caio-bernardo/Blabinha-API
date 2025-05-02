import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from src.app.models.chat import ChatPublicWithDialogs

if TYPE_CHECKING:
    from .chat import Chat, ChatPublic


class Dialog(SQLModel, table=True):
    """Dialog database model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    input: str = Field(default="")
    answer: str = Field(default="")
    section: int = Field(default=100)
    tokens: int = Field(default=0)
    chat_id: Optional[int] = Field(default=None, foreign_key="chat.id")
    chat: Optional["Chat"] = Relationship(
        back_populates="dialogs", sa_relationship_kwargs={"lazy": "joined"}
    )

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class DialogCreate(SQLModel, table=False):
    """Dialog creation model"""

    chat_id: int = Field(description="Chat which the dialog will belong to") # TODO: think about using a chat name instead to keep id secret
    input: str = Field(description="Input to be send to Blabinha")


class DialogPublic(SQLModel, table=False):
    """Dialog public model (without sensitive fields)"""

    id: int
    input: str = Field(description="Input of the user")
    answer: str = Field(description="Answer given by Blabinha")
    section: int = Field(description="Section this dialog represents")
    tokens: int = Field(description="How much AI tokens were consumed by the response")
    created_at: datetime.datetime = Field(description="Time of creation")


class DialogPublicWithChat(DialogPublic):
    """Dialog public model with it owner chat"""
    chat: Optional["ChatPublic"] = Field(default=None, description="Chat owner of the dialog")
