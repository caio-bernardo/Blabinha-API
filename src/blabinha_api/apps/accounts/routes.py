from typing import Annotated
from fastapi import APIRouter, Depends, status

from blabinha_api.apps.chats.schemas import ChatPublic

from .dependencies import get_user_service, get_current_user
from .models import User
from .services import UserService
from .schemas import UserPublicWithChats, UserCreatePayload, UserPublic  # noqa: F401

router = APIRouter(tags=["users"], prefix="/users")

ChatPublic.model_rebuild()
UserPublicWithChats.model_rebuild()

@router.get("/me", response_model=UserPublicWithChats)
async def read_own_user(current_user: Annotated[User, Depends(get_current_user)]):
    """Retorna o usuário logado"""
    return current_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_own_user(
    current_user: Annotated[
        User, Depends(get_current_user)],
        userservice: Annotated[UserService, Depends(get_user_service)
    ]
):
    """Deleta o usuário logado"""
    await userservice.delete_user(current_user)

@router.post("/register", response_model=UserPublicWithChats)
async def create_user(payload: UserCreatePayload, userservice: Annotated[UserService, Depends(get_user_service)]):
    """Cria um novo usuário"""
    user = await userservice.create_user(payload)
    return user
