"""
Core dependecies for all apps
"""
from typing import Annotated, Generator
from fastapi import Depends
from sqlmodel import Session
from blabinha_api.database import DatabaseConfig


def get_db_session(db: Annotated[DatabaseConfig, Depends(DatabaseConfig)]) -> Generator[Session, None, None]:

    with Session(db.engine) as session:
        yield session
