from fastapi import APIRouter, status
from fastapi.param_functions import Depends
from pydantic import TypeAdapter

from src.app import controllers
from src.app.controllers.chat_controller import ChatController
from src.app.dependencies import get_chat_controller
from src.app.models.chat import ChatCreate, ChatPublic, ChatPublicWithDialogs
from src.app.models.dialog import DialogPublic, DialogPublicWithChat

from typing import List

router = APIRouter()


@router.get(
    "/chats/{id}",
    response_model=ChatPublicWithDialogs,
    status_code=status.HTTP_200_OK,
    tags=["chats"],
)
async def get_chat(id: int, controller: ChatController = Depends(get_chat_controller)):
    res = await controller.get_chat(id)
    return res


@router.get(
    "/chats/{id}/dialogs",
    response_model=List[DialogPublic],
    status_code=status.HTTP_200_OK,
    tags=["chats"],
)
async def get_dialogs_of_chat(
    id: int, controller: ChatController = Depends(get_chat_controller)
):
    res = await controller.get_dialogs(id)
    return res


@router.post(
    "/chats",
    response_model=ChatPublicWithDialogs,
    status_code=status.HTTP_201_CREATED,
    tags=["chats"],
)
async def create_chat(
    props: ChatCreate, controller: ChatController = Depends(get_chat_controller)
):
    res = await controller.create_chat(props)
    return res


@router.delete("/chats/{id}", status_code=status.HTTP_200_OK, tags=["chats"])
async def delete_chat(
    id: int, controller: ChatController = Depends(get_chat_controller)
):
    res = await controller.delete(id)
    return res
