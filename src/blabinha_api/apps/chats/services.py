from typing import List
import uuid
from fastapi import HTTPException
from sqlmodel import Session, select

from blabinha_api.apps.accounts.models import User
from .models import Chat
from .schemas import ChatCreate, ChatUpdate
from uuid import UUID
from blabinha_api.apps.blabinha import brain as br


class ChatService:

    def __init__(self, session: Session):
        self.session = session

    async def is_owned_by(self, chat: Chat, user: User) -> bool:
        return chat.user_id == user.id



    async def get_one(self, id: UUID) -> Chat:
        return self.session.get_one(Chat, id)  # TODO: await with Async Session

    async def get_one_from(self, user: User, id: UUID) -> Chat:
        # Admin users can access any chat
        if user.is_admin:
            return self.session.exec(select(Chat).where(Chat.id == id)).one()
        # Regular users can only access their own chats
        return self.session.exec(select(Chat).where(Chat.id == id, Chat.user_id == user.id)).one()

    async def get_all(self) -> list[Chat]:
        return list(self.session.exec(select(Chat)).all())

    async def get_all_for_user(self, user: User) -> list[Chat]:
        # Admin users can access all chats
        if user.is_admin:
            return list(self.session.exec(select(Chat)).all())
        # Regular users can only access their own chats
        return list(self.session.exec(select(Chat).where(Chat.user_id == user.id)).all())


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
        # Allow admin users to update any chat
        if not user.is_admin and dbchat.user_id != user.id:
            raise HTTPException(status_code=403, detail="Operation not allowed")
        chat_data = props.model_dump(exclude_unset=True)

        dbchat.sqlmodel_update(chat_data)
        self.session.add(dbchat)
        self.session.commit()
        self.session.refresh(dbchat)
        return dbchat


    async def delete(self, id: uuid.UUID, user: User) -> None:
        chat = self.session.get_one(Chat, id)
        # Allow admin users to delete any chat
        if not user.is_admin and chat.user_id != user.id:
            raise HTTPException(status_code=403, detail="Operation not allowed")
        self.session.delete(chat)
        self.session.commit()


    async def enviaResultados(self, respostas) -> List[str]:
        perguntas = []
        for r in respostas:
            content = r.choices[0].message.content
            if content:
                for linha in content.strip().split("\n"):
                    linha = linha.strip()
                    perguntas.append(linha)
        return perguntas


    async def get_suggestions(self, id: uuid.UUID, user: User, api_key: str) -> List[str]:
        # get_one_from already handles admin access
        chat = await self.get_one_from(user, id)
        historico = ""
        for dialog in chat.dialogs:
            historico += f"Usuário: {dialog.input}\nAssistente: {dialog.answer}\n"

        prompt = (
            "Você é um assistente inteligente especializado na Amazônia Azul. "
            "Com base na conversa abaixo, gere uma lista com 4 perguntas (nem mais, nem menos) curtas, "
            "com no máximo 45 caracteres (contados com espaços e pontuação), que ainda não foram feitas. Exemplo de pergunta curta: O que é Amazônia Azul?\n\n"
            "As perguntas devem ser direcionadas ao assistente da conversa passada, "
            "estar dentro do tema da Amazônia Azul, e ser relevantes ao contexto da conversa. "
            "Evite repetir perguntas já feitas anteriormente. "
            "Responda apenas com as perguntas, uma por linha, sem explicações ou numeração.\n\n"
            f"{historico}\n"
            "Sugestões:"
        )

        br.select_model(chat.model or "gpt-3.5-turbo")
        response = br.call([{"role": "user", "content": prompt}])
        perguntas = await self.enviaResultados([response])  # passa como lista

        print("Perguntas geradas:", perguntas)
        return perguntas
