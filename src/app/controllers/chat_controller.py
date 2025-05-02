from src.app.models.chat import Chat, ChatCreate, ChatPublic, ChatPublicWithDialogs
from src.app.models.dialog import Dialog, DialogPublic, DialogPublicWithChat
from src.app.repositories.chat_repo import ChatRepository
from fastapi import HTTPException, status
from typing import List

DialogPublic.model_rebuild()
ChatPublicWithDialogs.model_rebuild()


class ChatController:
    """Controls requests interaction with the database"""

    def __init__(self, repo: ChatRepository):
        self.repo = repo

    async def create_chat(self, chat: ChatCreate) -> ChatPublicWithDialogs:
        try:
            new_chat = self.repo.create(chat)
            dialogs = self.repo.get_dialogs(new_chat.id or -1)
            # INDO: precisa montar manualmente para que dialogs seja carregado na sessão
            # da base de dados (ou algo assim, so sei nao funciona com .model_validate())
            return ChatPublicWithDialogs(
                id=new_chat.id or -1,
                model=new_chat.model,
                strategy=new_chat.strategy,
                state=new_chat.state,
                bonusQnt=new_chat.bonusQnt,
                stars=new_chat.stars,
                repetition=new_chat.repetition,
                heroFeature=new_chat.heroFeature,
                totalTokens=new_chat.totalTokens,
                created_at=new_chat.created_at,
                updated_at=new_chat.updated_at,
                dialogs=[],
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_chat(self, chat_id: int) -> ChatPublicWithDialogs:
        try:
            chat = self.repo.get(chat_id)
            if chat is None:
                raise TypeError(f"chat: {chat_id}, not found")
            else:
                dialogs = self.repo.get_dialogs(chat_id)
                return ChatPublicWithDialogs(
                    id=chat_id,
                    model=chat.model,
                    strategy=chat.strategy,
                    state=chat.state,
                    bonusQnt=chat.bonusQnt,
                    stars=chat.stars,
                    repetition=chat.repetition,
                    heroFeature=chat.heroFeature,
                    totalTokens=chat.totalTokens,
                    created_at=chat.created_at,
                    updated_at=chat.updated_at,
                    dialogs=[DialogPublic.model_validate(d) for d in dialogs],
                )
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
