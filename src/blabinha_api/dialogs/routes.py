from fastapi import APIRouter, status
from fastapi import Depends
from sqlmodel import Session
from starlette.exceptions import HTTPException

from blabinha_api.dependencies import db_session
from . import services
from .schemas import DialogCreate, DialogPublicWithChat
from ..chats.schemas import ChatPublic  # noqa: F401

DialogPublicWithChat.model_rebuild()

router = APIRouter(prefix="/dialogs", tags=["dialogs"])

@router.post("/", response_model=DialogPublicWithChat, status_code=status.HTTP_201_CREATED)
async def create_dialog(props: DialogCreate, session: Session = Depends(db_session)):
    try:
        return await services.create(session, props)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
