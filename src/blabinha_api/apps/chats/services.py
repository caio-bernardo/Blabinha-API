from typing import List
import uuid
from fastapi import HTTPException
from openai import OpenAI
from sqlmodel import Session, select

from blabinha_api.apps.accounts.models import User
from .models import Chat
from .schemas import ChatCreate, ChatUpdate
from uuid import UUID


class ChatService:

    def __init__(self, session: Session):
        self.session = session

    async def is_owned_by(self, chat: Chat, user: User) -> bool:
        return chat.user_id == user.id



    async def get_one(self, id: UUID) -> Chat:
        return self.session.get_one(Chat, id)  # TODO: await with Async Session

    async def get_one_from(self, user: User, id: UUID) -> Chat:
        return self.session.exec(select(Chat).where(Chat.id == id, Chat.user_id == user.id)).one()

    async def get_all(self) -> list[Chat]:
        return list(self.session.exec(select(Chat)).all())


    async def get_history(self, id: uuid.UUID) -> list[str]:
        chat: Chat = await self.get_one(id)
        return [x.answer for x in chat.dialogs]


    async def get_heroFeatures(self, id: uuid.UUID) -> list[str]:
        chat: Chat = await self.get_one(id)
        return chat.heroFeatures.split("||")


    async def create(self, props: ChatCreate, owner: User) -> Chat:
        dbchat = Chat(
            user_id=owner.id,
            model=props.model,
            strategy=props.strategy,
            current_section=props.init_section
        )
        self.session.add(dbchat)
        self.session.commit()
        self.session.refresh(dbchat)
        return dbchat


    async def update(self, id: uuid.UUID, props: ChatUpdate, user: User) -> Chat:
        dbchat = self.session.get_one(Chat, id)
        if dbchat.user_id != user.id:
            raise HTTPException(status_code=403, detail="Operation not allowed")
        chat_data = props.model_dump(exclude_unset=True)

        dbchat.sqlmodel_update(chat_data)
        self.session.add(dbchat)
        self.session.commit()
        self.session.refresh(dbchat)
        return dbchat


    async def delete(self, id: uuid.UUID, user: User) -> None:
        chat = self.session.get_one(Chat, id)
        if chat.user_id != user.id:
            raise HTTPException(status_code=403, detail="Operation not allowed")
        self.session.delete(chat)
        self.session.commit()

    async def get_suggestions(self, id: uuid.UUID, user: User, api_key: str) -> List[str]:
        chat = await self.get_one_from(user, id)
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
