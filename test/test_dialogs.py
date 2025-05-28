from fastapi.testclient import TestClient
from .fixtures import *  # noqa: F403

def create_chat_for_dialog(client: TestClient):
    # Helper to create a chat, required for dialog creation
    res = client.post(
        "/chats/",
        json={
            "model": "gpt-4o",
            "strategy": "one-shot"
        }
    )
    assert res.status_code == 201
    return res.json()["id"]

def test_create_dialog(client: TestClient):
    chat_id = create_chat_for_dialog(client)
    dialog_data = {
        "chat_id": chat_id,
        "input": "Hello, how are you?"
    }
    res = client.post("/dialogs/", json=dialog_data)
    assert res.status_code == 201, f"Assertion Failed: {res.json()}"
    data = res.json()
    assert data["input"] == "Hello, how are you?"
    assert data["chat"]["id"] == chat_id
    assert "answer" in data
    assert "created_at" in data
    assert "id" in data
