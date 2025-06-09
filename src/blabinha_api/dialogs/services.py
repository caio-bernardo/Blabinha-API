import uuid
from sqlmodel import Session, select

from ..blabinha.Blab import Blab, Variaveis
from ..chats.schemas import ChatState
from ..chats.services import get_one

from .models import Dialog
from .schemas import DialogCreate


async def interact(session: Session, props: DialogCreate, api_key: str) -> Dialog:
    dialog = Dialog.model_validate(props)
    chat = await get_one(session, props.chat_id)

    blab = Blab(api_key, chat, session)
    herofeatures = chat.heroFeatures.split("||")
    variaveis = Variaveis(
        section=chat.current_section,
        input=dialog.input,
        bonus=chat.bonusQnt,
        stars=chat.stars,
        repetition=chat.repetition,
        heroFeatures=herofeatures,
        username=chat.username,
    )
    resposta = blab.escolheParte(variaveis)

    chat.current_section = resposta.section
    chat.totalTokens += resposta.tokens
    chat.bonusQnt = resposta.bonus
    chat.heroFeatures = "||".join(resposta.heroFeatures)
    chat.stars = resposta.stars
    chat.repetition = resposta.repetition
    chat.username = resposta.username
    if resposta.section >= 371:
        chat.state = ChatState.CLOSE

    dialog.answer = resposta.answer
    dialog.section = resposta.section
    dialog.tokens = resposta.tokens

    session.add(dialog)
    session.add(chat)
    session.commit()
    session.refresh(dialog)
    session.refresh(chat)
    return dialog


async def create(session: Session, props: DialogCreate) -> Dialog:
    dbdialog = Dialog.model_validate(props)
    session.add(dbdialog)
    session.commit()
    session.refresh(dbdialog)
    return dbdialog


def get_all_part_two(session: Session, chat_id: uuid.UUID) -> list[Dialog]:
    statement = select(Dialog).where(
        Dialog.chat_id == chat_id, Dialog.section >= 200, Dialog.section < 300
    )
    return list(session.exec(statement))
