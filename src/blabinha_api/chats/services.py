from typing import List
import uuid
from openai import OpenAI
from sqlmodel import Session, select
from .models import Chat
from .schemas import ChatCreate, ChatUpdate
from uuid import UUID


async def get_one(session: Session, id: UUID) -> Chat:
    return session.get_one(Chat, id)  # TODO: await with Async Session


async def get_all(session: Session) -> list[Chat]:
    return list(session.exec(select(Chat)).all())


async def get_history(session: Session, id: uuid.UUID) -> list[str]:
    raise NotImplementedError("needs dialog relationship")


async def get_heroFeatures(session: Session, id: uuid.UUID) -> list[str]:
    raise NotImplementedError("needs dialog relationship")


async def create(session: Session, props: ChatCreate) -> Chat:
    dbchat = Chat.model_validate(props)
    session.add(dbchat)
    session.commit()
    session.refresh(dbchat)
    return dbchat


async def update(session: Session, id: uuid.UUID, props: ChatUpdate) -> Chat:
    dbchat = session.get_one(Chat, id)
    chat_data = props.model_dump(exclude_unset=True)
    dbchat.sqlmodel_update(chat_data)
    session.add(dbchat)
    session.commit()
    session.refresh(dbchat)
    return dbchat


async def delete(session: Session, id: uuid.UUID) -> None:
    chat = session.get_one(Chat, id)
    session.delete(chat)
    session.commit()

async def get_suggestions(session: Session, id: uuid.UUID, api_key: str) -> List[str]:
    chat = session.get_one(Chat, id)
    client = OpenAI(api_key=api_key)
    historico = ""
    for dialog in chat.dialogs:
        historico += f"Usuário: {dialog.input}\nAssistente: {dialog.answer}\n"

    prompt = (
        "Você é um assistente inteligente especializado na Amazônia Azul. "
        "Com base na conversa abaixo, gere uma lista com 4 perguntas (nem mais, nem menos) curtas, "
        "com no máximo 45 caracteres, que ainda não foram feitas. "
        "As perguntas devem ser direcionadas ao assistente da conversa passada, "
        "estar dentro do tema da Amazônia Azul, e ser relevantes ao contexto da conversa. "
        "Evite repetir perguntas já feitas anteriormente. "
        "Responda apenas com as perguntas, uma por linha, sem explicações ou numeração.\n\n"
        f"{historico}\n"
        "Sugestões:"
    )

    response = client.chat.completions.create(
        model=chat.model,
        messages=[
            {"role": "system", "content": "Você é um assistente que sugere perguntas curtas baseadas em um diálogo."},
            {"role": "user", "content": prompt},
        ],
    )

    content = response.choices[0].message.content
    if content:
        perguntas = [linha.strip() for linha in content.strip().split("\n") if linha.strip()]
        perguntas = [p for p in perguntas if len(p) <= 45]
        return perguntas

    return []
