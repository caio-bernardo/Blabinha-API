
from typing import Annotated
from fastapi import APIRouter, status
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security.http import HTTPBearer
from starlette.exceptions import HTTPException

from blabinha_api.accounts.dependencies import get_current_user
from blabinha_api.accounts.models import User
from blabinha_api.dialogs.dependencies import get_dialog_service

from .services import DialogService
from .schemas import DialogCreate, DialogPublicWithChat
from ..chats.schemas import ChatPublic  # noqa: F401
from ..accounts.schemas import UserPublic #noqa: F401

DialogPublicWithChat.model_rebuild()

router = APIRouter(prefix="/dialogs", tags=["dialogs"])

api_key_header = HTTPBearer()

@router.post(
    "/", response_model=DialogPublicWithChat, status_code=status.HTTP_201_CREATED
)
async def create_dialog(props: DialogCreate, api_key: Annotated[HTTPAuthorizationCredentials, Depends(api_key_header)],
    current_user: Annotated[User, Depends(get_current_user)],
    dialog_service: Annotated[DialogService, Depends(get_dialog_service)]
):
    try:
        return await dialog_service.interact(props, api_key.credentials)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
