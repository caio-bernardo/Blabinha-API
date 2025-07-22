from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo
from passlib.context import CryptContext
from pydantic import SecretStr

from .schemas import TokenData
from blabinha_api.config import config
from blabinha_api.accounts.services import UserService
import jwt


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

    async def verify_refresh_token(
        self, token: str,
        user_service: "UserService"
    ) -> Optional[TokenData]:
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
