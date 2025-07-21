from typing import Generator
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer
from .database import DatabaseConfig

db = DatabaseConfig()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def db_session() -> Generator[Session, None, None]:
    with Session(db.engine) as session:
        yield session
