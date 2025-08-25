from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from blabinha_api.apps.chats.schemas import ChatPublic
from blabinha_api.apps.core.dependencies import get_db_session

from .dependencies import get_user_service, get_current_user
from .models import User
from .services import UserService
from .schemas import UserPublicWithChats, UserCreatePayload, UserPublic, UserAdminCreate  # noqa: F401

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
    try:
        user = await userservice.create_user(payload)
        return user
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/initialize", response_model=UserPublicWithChats)
async def create_first_admin(
    payload: UserAdminCreate,
    db_session: Annotated[Session, Depends(get_db_session)],
    userservice: Annotated[UserService, Depends(get_user_service)]
):
    """
    Creates the first admin user if no admin users exist in the system.
    This endpoint becomes inaccessible once any user is created.
    """
    # Check if any users exist
    user_count = db_session.exec(select(User).where(User.is_admin)).first()
    if user_count:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System already initialized with users"
        )

    try:
        # Force admin status to be true for the first user
        payload.is_admin = True
        user = await userservice.create_user(payload, is_admin=True)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
