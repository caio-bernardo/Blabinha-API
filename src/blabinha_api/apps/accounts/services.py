from pydantic import SecretStr
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from .models import User
from .schemas import UserCreatePayload
from typing import List

class UserService:

    def __init__(self, session: Session):
        self.session = session

    async def authenticate(self, username: str, password: SecretStr) -> User | None:
        user = await self.read_user(username)
        if not user:
            return None

        # Import here to avoid circular imports
        from blabinha_api.apps.auth.services import TokenService
        if not TokenService().verify_password(password, SecretStr(user.hashed_password)):
            return None
        return user

    async def create_user(self, payload: UserCreatePayload, is_admin: bool = False):
        if payload.password != payload.confirm_password:
            raise ValueError("Passwords do not match")
        # Import here to avoid circular imports
        from blabinha_api.apps.auth.services import TokenService
        user = User(
            email=payload.email,
            hashed_password=TokenService().get_password_hash(payload.password).get_secret_value(),
            is_admin=is_admin
        )

        try:

            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except IntegrityError:
            self.session.rollback()
            raise ValueError("User with this unique identifier already exists")

    async def read_user(self, username: str) -> User | None:
        user = self.session.exec(select(User).where(User.email == username)).first()
        return user

    async def read_all_users(self) -> List[User]:
        """Return all users. Should only be used by admin users."""
        users = self.session.exec(select(User)).all()
        return list(users)

    async def get_user_by_id(self, user_id) -> User | None:
        """Get a user by ID. Should only be used by admin users."""
        return self.session.exec(select(User).where(User.id == user_id)).first()

    async def update_user(self, user: User, data: dict):
        """Update user data including admin status."""
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    async def set_admin_status(self, user: User, is_admin: bool):
        """Set a user's admin status."""
        user.is_admin = is_admin
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    async def delete_user(self, user: User):
        self.session.delete(user)
        self.session.commit()
        self.session.refresh(user)
