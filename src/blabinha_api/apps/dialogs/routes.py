
from typing import Annotated
from fastapi import APIRouter, status
from fastapi import Depends
from starlette.exceptions import HTTPException

from blabinha_api.apps.accounts.dependencies import get_current_user
from blabinha_api.apps.accounts.models import User
from blabinha_api.apps.dialogs.dependencies import get_dialog_service
from blabinha_api.config import settings

from .services import DialogService
from .schemas import DialogCreate, DialogPublicWithChat
from ..chats.schemas import ChatPublic  # noqa: F401
from ..accounts.schemas import UserPublic #noqa: F401

# Reconstroi o modelo para evitar dependências circulares e outras falhas
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
    """Cria um novo diálogo dentro do contexto de um chat"""
    try:
        return await dialog_service.interact(props, settings.openai_api_key, current_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
