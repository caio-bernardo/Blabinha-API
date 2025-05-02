from ..models.chat import Chat, ChatCreate, ChatState
from ..models.dialog import DialogCreate, Dialog
from sqlmodel import Session


class ChatRepository:

    def __init__(self, engine):
        self._engine = engine

    def create(self, chat_props: ChatCreate) -> Chat:
        with Session(self._engine) as session:
            new_chat = Chat.model_validate(chat_props)
            session.add(new_chat)
            session.commit()
            session.refresh(new_chat)
            return new_chat

    def get(self, chat_id: int) -> Chat | None:
        with Session(self._engine) as session:
            return session.get(Chat, chat_id)

    def get_dialogs(self, chat_id: int) -> list[Dialog]:
        with Session(self._engine) as session:
            chat = session.get(Chat, chat_id)
            if chat:
                return chat.dialogs
            return []

    def get_part2_dialogs(self, chat_id: int) -> list[Dialog]:
        with Session(self._engine) as session:
            chat = session.get(Chat, chat_id)
            if chat:
                return [d for d in chat.dialogs if d.turn >= 200 ]
            return []

    def get_history(self, chat_id: int) -> list[str]:
        with Session(self._engine) as session:
            chat = session.get(Chat, chat_id)
            if chat:
                return [dial.answer for dial in chat.dialogs]
            return []

    def delete(self, chat_id: int) -> None:
        with Session(self._engine) as session:
            chat = session.get(Chat, chat_id)
            if chat:
                session.delete(chat)
                session.commit()
                session.refresh(chat)

    def update(self, chat: Chat) -> None:
        with Session(self._engine) as session:
            session.add(chat)
            session.commit()
            session.refresh(chat)


if __name__ == "__main__":
    from sqlmodel import create_engine, SQLModel
    from ..models import *

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)
    chat_repo = ChatRepository(engine)

    chat_props = chat.ChatCreate()
    chat = chat_repo.create(chat_props)
    print("Chat: ", chat)
    chat.totalTokens += 10

    chat_repo.update(chat)

    print("Chat: ", chat)
