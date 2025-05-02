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
    summary="Get a Chat",
    description="Gets a chat with a list of its dialogs",
    response_model=ChatPublicWithDialogs,
    status_code=status.HTTP_200_OK,
    tags=["chats"],
)
async def get_chat(id: int, controller: ChatController = Depends(get_chat_controller)):
    res = await controller.get_chat(id)
    return res


@router.get(
    "/chats/{id}/dialogs",
    summary="Get dialogs of a chat",
    description="Get all dialogs of a chat in a list format",
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
    summary="Create a Chat",
    description="Create a chat with optional model type, prompt strategy and initial section point",
    response_model=ChatPublicWithDialogs,
    status_code=status.HTTP_201_CREATED,
    tags=["chats"],
)
async def create_chat(
    props: ChatCreate, controller: ChatController = Depends(get_chat_controller)
):
    res = await controller.create_chat(props)
    return res


@router.delete("/chats/{id}",
    summary="Delete a chat",
    description="Deletes a chat, clean all the dialogs related to it",
    status_code=status.HTTP_200_OK,
    tags=["chats"])
async def delete_chat(
    id: int, controller: ChatController = Depends(get_chat_controller)
):
    res = await controller.delete(id)
    return res
