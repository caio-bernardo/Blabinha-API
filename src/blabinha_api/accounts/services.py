from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from passlib.context import CryptContext
from pydantic import SecretStr
from sqlmodel import Session, select
from blabinha_api import config
import jwt

from blabinha_api.accounts.models import User
from blabinha_api.accounts.schemas import UserCreatePayload

class UserService:

    def __init__(self, session: Session):
        self.session = session

    async def authenticate(self, username: str, password: SecretStr) -> User | None:
        user = await self.read_user(username)
        if not user:
            return None
        if not TokenService().verify_password(password, SecretStr(user.hashed_password)):
            return None
        return user

    async def create_user(self, payload: UserCreatePayload):
        if payload.password != payload.confirm_password:
            raise ValueError("Passwords do not match")
        user = User(
            email=payload.email,
            hashed_password=TokenService().get_password_hash(payload.password).get_secret_value()
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    async def read_user(self, username: str) -> User | None:
        user = self.session.exec(select(User).where(User.email == username)).first()
        return user

    async def update_user(self):
        pass

    async def delete_user(self):
        pass

class TokenService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(ZoneInfo("America/Sao_Paulo")) + expires_delta
        else:
            expire = datetime.now(ZoneInfo("America/Sao_Paulo")) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
        return encoded_jwt

    def verify_password(self, plain_password: SecretStr, hashed_password: SecretStr):
        return self.pwd_context.verify(plain_password.get_secret_value(), hashed_password.get_secret_value())

    def get_password_hash(self, password: SecretStr) -> SecretStr:
        return SecretStr(self.pwd_context.hash(password.get_secret_value()))
