from fastapi import HTTPException, status
from src.app.blabinha import Blab, Variaveis
from src.app.models.chat import ChatPublic, ChatState
from src.app.models.dialog import (
    Dialog,
    DialogCreate,
    DialogPublic,
    DialogPublicWithChat,
)
from src.app.models.chat import Chat
from src.app.repositories.chat_repo import ChatRepository
from src.app.repositories.dialog_repo import DialogRepository


class BlabinhaController:
    """Controls request iteractions with Blabinha agent"""
    def __init__(
        self, chat_repo: ChatRepository, dialog_repo: DialogRepository
    ) -> None:
        self.chat_repo = chat_repo
        self.dialog_repo = dialog_repo

    async def create_dialog(
        self, props: DialogCreate, api_key: str
    ) -> DialogPublicWithChat:
        try:
            dialog: Dialog = self.dialog_repo.create(props)
            assert dialog.id is not None
            chat: Chat | None = self.chat_repo.get(dialog.chat_id or -1)
            assert chat

            # Envia para Blabinha
            blab = Blab(api_key, chat.model, self.chat_repo, chat.id or -1)

            herofeatures = chat.heroFeature.split("||")
            variaveis = Variaveis(
                section=chat.current_section,
                input=dialog.input,
                bonus=chat.bonusQnt,
                stars=chat.stars,
                repetition=chat.repetition,
                heroFeatures=herofeatures,
            )
            resposta = blab.escolheParte(variaveis)

            # Update database and create response
            dialog_res = DialogPublicWithChat(
                id=dialog.id,
                input=resposta.input,
                answer=resposta.answer,
                section=chat.current_section,
                tokens=resposta.tokens,
                chat=ChatPublic.model_validate(chat),
                created_at=dialog.created_at,
            )
            chat.current_section = resposta.section
            chat.totalTokens += resposta.tokens
            chat.bonusQnt = resposta.bonus
            chat.heroFeature = "||".join(resposta.heroFeatures)
            chat.stars = resposta.stars
            chat.repetition = resposta.repetition
            if resposta.section >= 371:
                chat.state = ChatState.CLOSED

            self.chat_repo.update(chat)
            self.dialog_repo.update(dialog)
            return dialog_res
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}",
            )
