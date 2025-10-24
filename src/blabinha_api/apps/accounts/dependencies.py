from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session
import jwt

from blabinha_api.apps.auth.dependencies import oauth2_scheme
from blabinha_api.apps.auth.schemas import TokenData
from blabinha_api.apps.core.dependencies import get_db_session
from blabinha_api.config import settings

from .services import UserService
from .models import User
from fastapi import HTTPException, status


def get_user_service(session: Annotated[Session, Depends(get_db_session)]) -> UserService:
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
        payload = jwt.decode(token, settings.access_token_secret_key, algorithms=[settings.hash_algorithm])
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

async def get_admin_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Check if the current user has admin privileges. If not, raise an HTTP 403 Forbidden exception.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
