from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from . import services
from .schemas import ChatCreate, ChatPublic, ChatPublicWithDialogs, ChatUpdate
from ..dependencies import db_session
from ..dialogs.schemas import DialogPublic # noqa: F401

import uuid

ChatPublicWithDialogs.model_rebuild()

router = APIRouter(prefix="/chats", tags=["chats"])

@router.get("/", response_model=list[ChatPublicWithDialogs], status_code=status.HTTP_200_OK)
async def list_chat(*, session: Session = Depends(db_session)):
    chats = await services.get_all(session)
    return chats

@router.get("/{id}", response_model=ChatPublicWithDialogs, status_code=status.HTTP_200_OK)
async def get_chat(id: uuid.UUID, session: Session = Depends(db_session)):
    try:
        return await services.get_one(session, id)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/", response_model=ChatPublicWithDialogs, status_code=status.HTTP_201_CREATED)
async def create_chat(props: ChatCreate, session: Session = Depends(db_session)):
    try:
        return await services.create(session, props)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/{id}", response_model=ChatPublic, status_code=status.HTTP_200_OK)
async def update_chat(id: uuid.UUID, props: ChatUpdate, session: Session = Depends(db_session)):
    try:
        return await services.update(session, id, props)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(id: uuid.UUID, session: Session = Depends(db_session)):
    try:
        await services.delete(session, id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
