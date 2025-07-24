from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from blabinha_api.apps.chats.services import ChatService
from blabinha_api.apps.core.dependencies import get_db_session


def get_chat_service(session: Annotated[Session, Depends(get_db_session)]) -> ChatService:
    return ChatService(session)
