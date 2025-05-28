import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session
from fastapi.testclient import TestClient
from src.main import app_runner  # Adjust import based on actual app location
from blabinha_api.dependencies import (
    db_session,
)  # Adjust import based on actual db module location


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        # echo=True
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app_runner.dependency_overrides[db_session] = get_session_override

    client = TestClient(app_runner)
    yield client
    app_runner.dependency_overrides.clear()
