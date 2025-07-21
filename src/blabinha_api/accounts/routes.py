from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr
from sqlmodel import Session

from blabinha_api.config import config
from blabinha_api.core.dependencies import db_session

from .dependencies import get_current_user
from .models import User
from .services import TokenService, UserService
from .schemas import Token, UserPublicWithChats, UserCreatePayload, UserPublic
from blabinha_api.chats.schemas import ChatPublic

router = APIRouter(tags=["Users"])

ChatPublic.model_rebuild()
UserPublicWithChats.model_rebuild()

def get_user_service(session: Annotated[Session, Depends(db_session)]) -> UserService:
    return UserService(session)

def get_token_service() -> TokenService:
    return TokenService()

@router.get("/users/me", response_model=UserPublicWithChats)
async def read_own_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_own_user(current_user: Annotated[User, Depends(get_current_user)], userservice: Annotated[UserService, Depends(get_user_service)]):
    await userservice.delete_user(current_user)

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
    access_token_expires = timedelta(minutes=config.access_token_expire_minutes)
    access_token = tokenservice.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=config.refresh_token_expire_minutes)
    refresh_token = tokenservice.create_refresh_token(
        data={"sub": user.email},
        expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@router.post("/auth/refresh")
async def refresh_token(
    refresh_token: str,
    userservice: Annotated[UserService, Depends(get_user_service)],
    tokenservice: Annotated[TokenService, Depends(get_token_service)]
):
    sub = await tokenservice.verify_refresh_token(refresh_token, userservice)
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.access_token_expire_minutes)
    access_token = tokenservice.create_access_token(
        data={"sub": sub.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
