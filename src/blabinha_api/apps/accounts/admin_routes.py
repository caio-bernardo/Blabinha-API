from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from .dependencies import get_user_service, get_admin_user
from .models import User
from .services import UserService
from .schemas import UserPublicWithChats, AdminUserUpdatePayload, UserAdminCreate

router = APIRouter(tags=["admin"], prefix="/admin/users")


@router.get("", response_model=List[UserPublicWithChats])
async def get_all_users(
    admin_user: Annotated[User, Depends(get_admin_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Get all users in the system.
    Only accessible to admin users.
    """
    return await user_service.read_all_users()


@router.get("/{user_id}", response_model=UserPublicWithChats)
async def get_user_by_id(
    user_id: UUID,
    admin_user: Annotated[User, Depends(get_admin_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Get a specific user by ID.
    Only accessible to admin users.
    """
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("", response_model=UserPublicWithChats, status_code=status.HTTP_201_CREATED)
async def create_user_as_admin(
    payload: UserAdminCreate,
    admin_user: Annotated[User, Depends(get_admin_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Create a new user with optional admin status.
    Only accessible to admin users.
    """
    try:
        user = await user_service.create_user(payload, is_admin=payload.is_admin)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{user_id}", response_model=UserPublicWithChats)
async def update_user(
    user_id: UUID,
    payload: AdminUserUpdatePayload,
    admin_user: Annotated[User, Depends(get_admin_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Update a user's details.
    Only accessible to admin users.
    """
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Don't allow admin to revoke their own admin privileges
    if admin_user.id == user.id and payload.is_admin is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin users cannot revoke their own admin privileges"
        )
        
    data = payload.model_dump(exclude_unset=True)
    updated_user = await user_service.update_user(user, data)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    admin_user: Annotated[User, Depends(get_admin_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Delete a user.
    Only accessible to admin users.
    """
    # Don't allow admin to delete themselves
    if admin_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin users cannot delete themselves"
        )
    
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    await user_service.delete_user(user)