from src.app.models.chat import ChatCreate, ChatPublic
from src.app.models.dialog import DialogPublic
from src.app.repositories.chat_repo import ChatRepository
from fastapi import HTTPException, status
from typing import List


class ChatController:
    """Controls requests interaction with the database"""

    def __init__(self, repo: ChatRepository):
        self.repo = repo

    async def create_chat(self, chat: ChatCreate) -> ChatPublic:
        try:
            new_chat = self.repo.create(chat)
            return ChatPublic.model_validate(new_chat)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_chat(self, chat_id: int) -> ChatPublic:
        try:
            chat = self.repo.get(chat_id)
            if chat is None:
                raise TypeError(f"chat: {chat_id}, not found")
            else:
                return ChatPublic.model_validate(chat)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_dialogs(self, chat_id: int) -> List[DialogPublic]:
        try:
            dialogs = self.repo.get_dialogs(chat_id)
            return [DialogPublic.model_validate(d) for d in dialogs]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete(self, chat_id: int) -> None:
        try:
            self.repo.delete(chat_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
