

from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from blabinha_api.chats.dependencies import get_chat_service
from blabinha_api.chats.services import ChatService
from blabinha_api.core.dependencies import db_session
from blabinha_api.dialogs.services import DialogService


def get_dialog_service(
    session: Annotated[Session, Depends(db_session)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)]
) -> DialogService:
    return DialogService(session, chat_service)
