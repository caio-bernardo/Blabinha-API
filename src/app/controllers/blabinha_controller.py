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

            blab = Blab(api_key, chat.model, self.chat_repo, chat.id or -1)

            herofeatures = chat.heroFeature.split("||")
            variaveis = Variaveis(
                turn=chat.current_turn,
                input=dialog.input,
                bonus=chat.bonusQnt,
                stars=chat.stars,
                repetition=chat.repetition,
                heroFeatures=herofeatures,
            )
            resposta = blab.escolheParte(variaveis)

            dialog_res = DialogPublicWithChat(
                id=dialog.id,
                input=resposta.input,
                answer=resposta.answer,
                turn=chat.current_turn,
                tokens=resposta.tokens,
                chat=ChatPublic.model_validate(chat),
                created_at=dialog.created_at,
            )
            chat.current_turn = resposta.turn
            chat.totalTokens += resposta.tokens
            chat.bonusQnt = resposta.bonus
            chat.heroFeature = "||".join(resposta.heroFeatures)
            chat.stars = resposta.stars
            chat.repetition = resposta.repetition
            if resposta.turn >= 371:
                chat.state = ChatState.CLOSED

            self.chat_repo.update(chat)

            return dialog_res
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}",
            )
