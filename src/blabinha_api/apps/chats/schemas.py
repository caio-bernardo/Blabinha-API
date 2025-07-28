from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID
from sqlmodel import Field
from sqlmodel.main import SQLModel

if TYPE_CHECKING:
    from blabinha_api.apps.dialogs.schemas import DialogPublic
    from blabinha_api.apps.accounts.schemas import UserPublic

class StrategyEnum(str, Enum):
    zero_shot = "zero-shot"
    one_shot = "one-shot"
    few_shot = "few-shot"
    step_by_step = "step-by-step"
    chain_of_thought = "chain-of-thought"
    self_consistency = "self-consistency"

class ChatState(Enum):
    OPEN = True
    CLOSE = False


class ChatBase(SQLModel):
    model: str = Field(default="gpt-4o")
    strategy: StrategyEnum = Field(default=StrategyEnum.zero_shot)
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
    model: str = "gpt-3.5-turbo"
    strategy: StrategyEnum = StrategyEnum.one_shot
    init_section: int = 100


class ChatPublic(ChatBase):
    id: UUID
    owner: Optional["UserPublic"] = None
    created_at: datetime
    updated_at: datetime


class ChatPublicWithDialogs(ChatPublic):
    dialogs: list["DialogPublic"] = []


class ChatUpdate(SQLModel):
    model: str | None = None
    strategy: StrategyEnum | None = None
    current_section: int | None = None
    bonusQnt: int | None = None
    stars: int | None = None
    heroFeatures: str | None = None
    username: str | None = None
    image: str |  None = None
