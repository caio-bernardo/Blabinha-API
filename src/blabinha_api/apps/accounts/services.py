from pydantic import SecretStr
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from .models import User
from .schemas import UserCreatePayload

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

    async def create_user(self, payload: UserCreatePayload):
        if payload.password != payload.confirm_password:
            raise ValueError("Passwords do not match")
        # Import here to avoid circular imports
        from blabinha_api.apps.auth.services import TokenService
        user = User(
            email=payload.email,
            hashed_password=TokenService().get_password_hash(payload.password).get_secret_value()
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

    async def update_user(self):
        pass

    async def delete_user(self, user: User):
        self.session.delete(user)
        self.session.commit()
        self.session.refresh(user)
