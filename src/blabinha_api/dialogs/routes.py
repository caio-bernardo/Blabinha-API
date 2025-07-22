
from typing import Annotated
from fastapi import APIRouter, status
from fastapi import Depends
from starlette.exceptions import HTTPException

from blabinha_api.accounts.dependencies import get_current_user
from blabinha_api.accounts.models import User
from blabinha_api.dialogs.dependencies import get_dialog_service
from blabinha_api.config import config

from .services import DialogService
from .schemas import DialogCreate, DialogPublicWithChat
from ..chats.schemas import ChatPublic  # noqa: F401
from ..accounts.schemas import UserPublic #noqa: F401

DialogPublicWithChat.model_rebuild()

router = APIRouter(prefix="/dialogs", tags=["dialogs"])


@router.post(
    "/", response_model=DialogPublicWithChat, status_code=status.HTTP_201_CREATED
)
async def create_dialog(
    props: DialogCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    dialog_service: Annotated[DialogService, Depends(get_dialog_service)]
):
    try:
        return await dialog_service.interact(props, config.openai_api_key, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
