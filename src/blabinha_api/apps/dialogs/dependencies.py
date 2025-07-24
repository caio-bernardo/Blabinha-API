from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from blabinha_api.apps.chats.dependencies import get_chat_service
from blabinha_api.apps.chats.services import ChatService
from blabinha_api.apps.core.dependencies import get_db_session
from blabinha_api.apps.dialogs.services import DialogService


def get_dialog_service(
    session: Annotated[Session, Depends(get_db_session)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)]
) -> DialogService:
    """Provides a DialogService instance as a dependency.
        Args:
            session: The database session dependency.
            chat_service: The chat service dependency.

        Returns:
            An instance of DialogService.
        """
    return DialogService(session, chat_service)
