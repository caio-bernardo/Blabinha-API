from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session
import jwt

from blabinha_api.auth.dependencies import oauth2_scheme
from blabinha_api.auth.schemas import TokenData
from blabinha_api.core.dependencies import db_session
from blabinha_api.config import config

from .services import UserService
from .models import User


def get_user_service(session: Annotated[Session, Depends(db_session)]) -> UserService:
    return UserService(session)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_service: Annotated[UserService, Depends(get_user_service)]) -> User:
    """
    Authenticate and retrieve the current user based on a JWT token.
    """
    def credentials_exception():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, config.access_token_secret_key, algorithms=[config.hash_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception()
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception()

    assert token_data.username is not None, credentials_exception
    user = await user_service.read_user(token_data.username)
    if user is None:
        raise credentials_exception()
    return user
