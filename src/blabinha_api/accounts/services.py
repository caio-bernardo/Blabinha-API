from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from passlib.context import CryptContext
from pydantic import SecretStr
from sqlmodel import Session, select
from blabinha_api.config import config
import jwt

from .models import User
from .schemas import UserCreatePayload, TokenData

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

    async def delete_user(self, user: User):
        self.session.delete(user)
        self.session.commit()
        self.session.refresh(user)

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
        encoded_jwt = jwt.encode(to_encode, config.access_token_secret_key, algorithm=config.hash_algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(ZoneInfo("America/Sao_Paulo")) + expires_delta
        else:
            expire = datetime.now(ZoneInfo("America/Sao_Paulo")) + timedelta(minutes=1440)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.refresh_token_secret_key, algorithm=config.hash_algorithm)
        return encoded_jwt

    async def verify_refresh_token(self, token: str, user_service: UserService) -> TokenData | None:
        try:
            payload = jwt.decode(token, config.refresh_token_secret_key, algorithms=[config.hash_algorithm])
            username: str = payload.get("sub")
            if username is None:
                return None
            token_data = TokenData(username=username)
        except jwt.InvalidTokenError:
            return None
        user = await user_service.read_user(token_data.username)
        if user is None:
            return None
        return token_data

    def verify_password(self, plain_password: SecretStr, hashed_password: SecretStr):
        return self.pwd_context.verify(plain_password.get_secret_value(), hashed_password.get_secret_value())

    def get_password_hash(self, password: SecretStr) -> SecretStr:
        return SecretStr(self.pwd_context.hash(password.get_secret_value()))
