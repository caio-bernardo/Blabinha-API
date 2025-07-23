from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr

from blabinha_api.apps.accounts.dependencies import get_user_service
from blabinha_api.apps.accounts.services import UserService
from blabinha_api.config import settings

from .services import TokenService
from .schemas import Token


router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    userservice: Annotated[UserService, Depends(get_user_service)],
    tokenservice: Annotated[TokenService, Depends(lambda: TokenService())]
) -> Token:
    """Login de usuário, cria token de acesso e de recuperação"""
    user = await userservice.authenticate(form_data.username, SecretStr(form_data.password))
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = tokenservice.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=settings.refresh_token_expire_minutes)
    refresh_token = tokenservice.create_refresh_token(
        data={"sub": user.email},
        expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@router.post("/refresh")
async def refresh_token(
    refresh_token: str,
    userservice: Annotated[UserService, Depends(get_user_service)],
    tokenservice: Annotated[TokenService, Depends(lambda: TokenService())]
):
    """Cria um novo token de acesso apartir de um token de recuperação"""
    sub = await tokenservice.verify_refresh_token(refresh_token, userservice)
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = tokenservice.create_access_token(
        data={"sub": sub.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
