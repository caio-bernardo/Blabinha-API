from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from blabinha_api.chats.services import ChatService
from blabinha_api.core.dependencies import db_session


def get_chat_service(session: Annotated[Session, Depends(db_session)]) -> ChatService:
    return ChatService(session)
