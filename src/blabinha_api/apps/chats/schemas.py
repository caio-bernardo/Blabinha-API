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
    ZERO_SHOT = "zero_shot"
    ONE_SHOT = "one_shot"
    FEW_SHOT = "few_shots"
    STEP_BY_STEP = "step_by_step"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    SELF_CONSISTENCY = "self_consistency"


class ModelEnum(str, Enum):
    GPT = 'gpt'
    LLAMA = 'llama'
    QWEN = 'qwen'
    GEMINI = 'gemini'


class ChatState(Enum):
    OPEN = True
    CLOSE = False


class ChatBase(SQLModel):
    model: ModelEnum = Field(default=ModelEnum.GPT)
    strategy: StrategyEnum = Field(default=StrategyEnum.ONE_SHOT)
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
    model: ModelEnum = ModelEnum.GPT
    strategy: StrategyEnum = StrategyEnum.ONE_SHOT
    init_section: int = 100


class ChatPublic(ChatBase):
    id: UUID
    owner: Optional["UserPublic"] = None
    created_at: datetime
    updated_at: datetime


class ChatPublicWithDialogs(ChatPublic):
    dialogs: list["DialogPublic"] = []


class ChatUpdate(SQLModel):
    model: ModelEnum | None = None
    strategy: StrategyEnum | None = None
    current_section: int | None = None
    bonusQnt: int | None = None
    stars: int | None = None
    heroFeatures: str | None = None
    username: str | None = None
    image: str |  None = None
