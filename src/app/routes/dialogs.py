from typing import Annotated
from fastapi import APIRouter, status, HTTPException
from fastapi.param_functions import Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic.type_adapter import TypeAdapter

from src.app.controllers.blabinha_controller import BlabinhaController
from src.app.controllers.dialog_controller import DialogController
from src.app.dependencies import get_blabinha_controller, get_dialog_controller
from src.app.models.dialog import DialogCreate, DialogPublic, DialogPublicWithChat

router = APIRouter()


@router.get(
    "/dialogs/{id}",
    description="Gets an existing dialog with it owner chat",
    response_model=DialogPublicWithChat,
    status_code=status.HTTP_200_OK,
    tags=["dialogs"],
)
async def get_dialog(
    id: int, controller: DialogController = Depends(get_dialog_controller)
):
    res = await controller.get_dialog(id)
    return res


api_key_header = HTTPBearer()


@router.post(
    "/dialogs",
    description="Makes a interaction with Blabinha in a specific chat context, returning the response and the update state of the chat",
    response_model=DialogPublicWithChat,
    status_code=status.HTTP_201_CREATED,
    tags=["dialogs"],
)
async def create_dialog(
    props: DialogCreate,
    api_key: Annotated[HTTPAuthorizationCredentials, Depends(api_key_header)],
    controller: BlabinhaController = Depends(get_blabinha_controller),
):
    res = await controller.create_dialog(props, api_key.credentials)
    return res


@router.delete("/dialogs/{id}", status_code=status.HTTP_200_OK, tags=["dialogs"])
async def delete_dialog(
    id: int, controller: DialogController = Depends(get_dialog_controller)
):
    res = await controller.delete_dialog(id)
    return res
