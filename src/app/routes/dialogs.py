from re import A
from fastapi import APIRouter, status, HTTPException
from fastapi.param_functions import Depends
from fastapi.security.api_key import APIKeyHeader

from src.app.controllers.blabinha_controller import BlabinhaController
from src.app.controllers.dialog_controller import DialogController
from src.app.dependencies import get_blabinha_controller, get_dialog_controller
from src.app.models.dialog import DialogCreate, DialogPublic

router = APIRouter()


@router.get(
    "/dialogs/{id}",
    response_model=DialogPublic,
    status_code=status.HTTP_200_OK,
    tags=["dialogs"],
)
async def get_dialog(
    id: int, controller: DialogController = Depends(get_dialog_controller)
):
    res = await controller.get_dialog(id)
    return res


api_key_header = APIKeyHeader(name="Model-API-Key", auto_error=False)


@router.post(
    "/dialogs",
    response_model=DialogPublic,
    status_code=status.HTTP_201_CREATED,
    tags=["dialogs"],
)
async def create_dialog(
    props: DialogCreate,
    api_key: str | None = Depends(api_key_header),
    controller: BlabinhaController = Depends(get_blabinha_controller),
):
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
            headers={"WWW-Authenticate": "Model-API-Key"},
        )
    res = await controller.create_dialog(props, api_key)
    return res


@router.delete("/dialogs/{id}", status_code=status.HTTP_200_OK, tags=["dialogs"])
async def delete_dialog(
    id: int, controller: DialogController = Depends(get_dialog_controller)
):
    res = await controller.delete_dialog(id)
    return res
