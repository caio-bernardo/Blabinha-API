import uuid
from fastapi import status
from fastapi.testclient import TestClient
from blabinha_api.chats.schemas import ChatPublicWithDialogs, ChatState

from .fixtures import *  # noqa: F403


def test_get_all_chat(client: TestClient):

    res = client.post(
        "/chats/",
        json={
            "model": "gpt-4o",
            "strategy": "one-shot"
        }
    )
    res = client.get("/chats/")

    data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert len(data) == 1

def test_create_chat(client: TestClient):
    res = client.post(
        "/chats/",
        json={
            "model": "gpt-4o",
            "strategy": "one-shot"
        }
    )
    data = ChatPublicWithDialogs.model_validate(res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert data.model == "gpt-4o"
    assert data.bonusQnt == 0
    assert data.dialogs == []
    assert data.strategy == "one-shot"
    assert data.current_section == 100
    assert data.state == ChatState.OPEN
    assert data.stars == 0
    assert data.repetition == 0
    assert data.heroFeatures == ""
    assert data.totalTokens == 0
    assert data.id is not None
    assert data.created_at is not None
    assert data.updated_at is not None


def test_get_chat(client: TestClient):
    # First create a chat
    res_create = client.post(
        "/chats/",
        json={
            "model": "gpt-4o",
            "strategy": "one-shot"
        }
    )
    created_data = res_create.json()
    chat_id = created_data["id"]

    # Then get the chat by ID
    res_get = client.get(f"/chats/{chat_id}")
    assert res_get.status_code == status.HTTP_200_OK
    data = ChatPublicWithDialogs.model_validate(res_get.json())
    assert data.id == uuid.UUID(chat_id)
    assert data.model == "gpt-4o"
    assert data.strategy == "one-shot"


def test_update_chat(client: TestClient):
    # First create a chat
    res_create = client.post(
        "/chats/",
        json={
            "model": "gpt-4o",
            "strategy": "one-shot"
        }
    )
    created_data = res_create.json()
    chat_id = created_data["id"]

    # Update the chat
    update_data = {
        "model": "gpt-3.5-turbo",
        "current_section": 200,
        "bonusQnt": 2,
        "stars": 5,
        "heroFeatures": "brave,smart"
    }
    res_update = client.patch(f"/chats/{chat_id}", json=update_data)
    print(res_update.json())
    assert res_update.status_code == status.HTTP_200_OK

    updated_data = ChatPublicWithDialogs.model_validate(res_update.json())
    assert updated_data.id == uuid.UUID(chat_id)
    assert updated_data.model == "gpt-3.5-turbo"
    assert updated_data.current_section == 200
    assert updated_data.bonusQnt == 2
    assert updated_data.stars == 5
    assert updated_data.heroFeatures == "brave,smart"
    assert updated_data.strategy == "one-shot"  # This should remain unchanged


def test_delete_chat(client: TestClient):
    # First create a chat
    res_create = client.post(
        "/chats/",
        json={
            "model": "gpt-4o",
            "strategy": "one-shot"
        }
    )
    created_data = res_create.json()
    chat_id = created_data["id"]

    # Delete the chat
    res_delete = client.delete(f"/chats/{chat_id}")
    assert res_delete.status_code == status.HTTP_204_NO_CONTENT

    # Try to get the deleted chat
    res_get = client.get(f"/chats/{chat_id}")
    assert res_get.status_code == status.HTTP_404_NOT_FOUND
