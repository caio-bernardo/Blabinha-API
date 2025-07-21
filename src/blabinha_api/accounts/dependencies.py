from typing import Annotated
from fastapi import Depends, HTTPException, status
import jwt
from sqlmodel import Session

from blabinha_api.config import config
from .schemas import TokenData
from .services import UserService

from .models import User
from blabinha_api.core.dependencies import db_session, oauth2_scheme

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(db_session)]) -> User:
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
    user = await UserService(session).read_user(token_data.username)
    if user is None:
        print("User not found in db")
        raise credentials_exception()
    return user
