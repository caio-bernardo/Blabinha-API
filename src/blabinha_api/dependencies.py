from typing import Generator
from sqlmodel import Session

from .database import DatabaseConfig

db = DatabaseConfig()


def db_session() -> Generator[Session, None, None]:
    with Session(db.engine) as session:
        yield session
