from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr
from sqlmodel import Session

from blabinha_api import config
from blabinha_api.dependencies import db_session

from .dependencies import get_current_user
from .models import User
from .services import TokenService, UserService
from .schemas import Token, UserPublicWithChats, UserCreatePayload, UserPublic
from blabinha_api.chats.schemas import ChatPublic

router = APIRouter()

ChatPublic.model_rebuild()
UserPublicWithChats.model_rebuild()

def get_user_service(session: Annotated[Session, Depends(db_session)]) -> UserService:
    return UserService(session)

def get_token_service() -> TokenService:
    return TokenService()

@router.get("/users/me", response_model=UserPublicWithChats)
async def read_own_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/auth/register", response_model=UserPublicWithChats)
async def create_user(payload: UserCreatePayload, userservice: Annotated[UserService, Depends(get_user_service)]):
    user = await userservice.create_user(payload)
    return user


@router.post("/auth/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    userservice: Annotated[UserService, Depends(get_user_service)],
    tokenservice: Annotated[TokenService, Depends(get_token_service)]
) -> Token:
    user = await userservice.authenticate(form_data.username, SecretStr(form_data.password))
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = tokenservice.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
