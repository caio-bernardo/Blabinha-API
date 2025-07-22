from typing import Annotated, List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import NoResultFound

from blabinha_api.config import config
from blabinha_api.accounts.dependencies import get_current_user
from blabinha_api.accounts.models import User
from blabinha_api.chats.dependencies import get_chat_service

from . import services
from .schemas import ChatCreate, ChatPublic, ChatPublicWithDialogs, ChatUpdate
from ..dialogs.schemas import DialogPublic  # noqa: F401
from ..accounts.schemas import UserPublic # noqa: F401

import uuid

ChatPublicWithDialogs.model_rebuild()

router = APIRouter(prefix="/chats", tags=["chats"])


@router.get(
    "/", response_model=list[ChatPublic], status_code=status.HTTP_200_OK
)
async def list_chat(*,
    user: Annotated[User, Depends(get_current_user)] ,
):
    return user.chats

@router.get(
    "/{id}", response_model=ChatPublicWithDialogs, status_code=status.HTTP_200_OK
)
async def get_chat(id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    chat_service: Annotated[services.ChatService, Depends(get_chat_service)],
):
    try:
        return await chat_service.get_one_from(user, id)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "/", response_model=ChatPublicWithDialogs, status_code=status.HTTP_201_CREATED
)
async def create_chat(props: ChatCreate,
    user: Annotated[User, Depends(get_current_user)],
    chat_service: Annotated[services.ChatService, Depends(get_chat_service)],
):
    try:
        return await chat_service.create(props, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch("/{id}", response_model=ChatPublic, status_code=status.HTTP_200_OK)
async def update_chat(
    id: uuid.UUID, props: ChatUpdate,
    user: Annotated[User, Depends(get_current_user)],
    chat_service: Annotated[services.ChatService, Depends(get_chat_service)],
):
    try:
        return await chat_service.update(id, props, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    chat_service: Annotated[services.ChatService, Depends(get_chat_service)],
):
    try:
        await chat_service.delete(id, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

@router.get(
    "/{id}/suggestions", response_model=List[str], status_code=status.HTTP_200_OK
)
async def get_suggestions(
    id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    chat_service: Annotated[services.ChatService, Depends(get_chat_service)],
):
    try:
        return await chat_service.get_suggestions(id, user, config.openai_api_key)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
