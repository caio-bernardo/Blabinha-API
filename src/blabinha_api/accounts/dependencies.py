from typing import Annotated
from fastapi import Depends, HTTPException, status
import jwt
from sqlmodel import Session

from blabinha_api import config
from blabinha_api.accounts.schemas import TokenData
from blabinha_api.accounts.services import UserService

from .models import User
from core.dependencies import db_session, oauth2_scheme

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(db_session)]) -> User:
    def credentials_exception(err):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {err}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception("username not in token")
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError as e:
        raise credentials_exception(e)
    assert token_data.username is not None, credentials_exception
    user = await UserService(session).read_user(token_data.username)
    if user is None:
        print("User not found in db")
        raise credentials_exception("user not found")
    return user
