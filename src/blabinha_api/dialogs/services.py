import uuid
from sqlmodel import Session, select

from blabinha_api.accounts.models import User

from ..blabinha.Blab import Blab, Variaveis
from ..chats.schemas import ChatState
from ..chats.services import ChatService

from .models import Dialog
from .schemas import DialogCreate


class DialogService:
    def __init__(self, session: Session, chat_service: ChatService):
        self.session = session
        self.chat_service = chat_service

    async def interact(self, props: DialogCreate, api_key: str, user: User) -> Dialog:
        dialog = Dialog.model_validate(props)
        chat = await self.chat_service.get_one_from(user, props.chat_id)

        blab = Blab(api_key, chat, self)
        herofeatures = chat.heroFeatures.split("||")
        variaveis = Variaveis(
            section=chat.current_section,
            input=dialog.input,
            bonus=chat.bonusQnt,
            stars=chat.stars,
            repetition=chat.repetition,
            heroFeatures=herofeatures,
            username=chat.username,
            emotion=dialog.emotion,
        )
        resposta = blab.escolheParte(variaveis)
        emocao = blab.detecta_emocao(resposta)
        dialog.emotion = emocao
        chat.current_section = resposta.section
        chat.totalTokens += resposta.tokens
        chat.bonusQnt = resposta.bonus
        chat.heroFeatures = "||".join(resposta.heroFeatures)
        chat.stars = resposta.stars
        chat.repetition = resposta.repetition
        chat.username = resposta.username
        chat.image = resposta.image
        if resposta.section >= 371:
            chat.state = ChatState.CLOSE

        dialog.answer = resposta.answer
        dialog.section = resposta.section
        dialog.tokens = resposta.tokens

        self.session.add(dialog)
        self.session.add(chat)
        self.session.commit()
        self.session.refresh(dialog)
        self.session.refresh(chat)
        return dialog


    async def create(self, props: DialogCreate) -> Dialog:
        dbdialog = Dialog.model_validate(props)
        self.session.add(dbdialog)
        self.session.commit()
        self.session.refresh(dbdialog)
        return dbdialog


    def get_all_part_two(self, chat_id: uuid.UUID) -> list[Dialog]:
        statement = select(Dialog).where(
            Dialog.chat_id == chat_id, Dialog.section >= 200, Dialog.section < 300
        )
        return list(self.session.exec(statement))
