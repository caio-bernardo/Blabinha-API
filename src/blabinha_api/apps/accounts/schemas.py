from datetime import datetime
from typing import TYPE_CHECKING, Optional
from pydantic import EmailStr, SecretStr
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from blabinha_api.apps.chats.schemas import ChatPublic


class UserCreatePayload(SQLModel):
    email: EmailStr = Field(..., title="Email", description="Email of the user")
    password: SecretStr = Field(..., title="Password", description="Password of the user")
    confirm_password: SecretStr = Field(..., title="Confirm Password", description="Confirm password of the user")


class UserAdminCreate(UserCreatePayload):
    is_admin: bool = Field(default=False, title="Is Admin", description="Flag indicating if the user has admin privileges")


class AdminUserUpdatePayload(SQLModel):
    email: Optional[EmailStr] = Field(None, title="Email", description="Email of the user")
    is_admin: Optional[bool] = Field(None, title="Is Admin", description="Flag indicating if the user has admin privileges")


class UserPublic(SQLModel):
    email: EmailStr = Field(..., title="Email", description="Email of the user")
    is_admin: bool = Field(default=False, title="Is Admin", description="Flag indicating if the user has admin privileges")
    created_at: datetime = Field(..., title="Created At", description="Date and time when the user was created")
    updated_at: datetime = Field(..., title="Updated At", description="Date and time when the user was last updated")


class UserPublicWithChats(UserPublic):
    chats: list["ChatPublic"] = []
