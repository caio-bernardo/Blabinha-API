from datetime import datetime
from typing import TYPE_CHECKING
from pydantic import EmailStr, SecretStr
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from blabinha_api.apps.chats.schemas import ChatPublic


class UserCreatePayload(SQLModel):
    email: EmailStr = Field(..., title="Email", description="Email of the user")
    password: SecretStr = Field(..., title="Password", description="Password of the user")
    confirm_password: SecretStr = Field(..., title="Confirm Password", description="Confirm password of the user")


class UserPublic(SQLModel):
    email: EmailStr = Field(..., title="Email", description="Email of the user")
    created_at: datetime = Field(..., title="Created At", description="Date and time when the user was created")
    updated_at: datetime = Field(..., title="Updated At", description="Date and time when the user was last updated")


class UserPublicWithChats(UserPublic):
    chats: list["ChatPublic"] = []
