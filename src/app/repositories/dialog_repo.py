from src.app.models.chat import Chat
from src.app.models.dialog import DialogCreate, Dialog
from sqlmodel import Session


class DialogRepository:
    def __init__(self, engine):
        self._engine = engine

    def create(self, dialog_props: DialogCreate) -> Dialog:
        with Session(self._engine) as session:
            dialog = Dialog.model_validate(dialog_props)
            chat_owner = session.get(Chat, dialog.chat_id)
            if chat_owner is None:
                raise Exception("chat id of new dialog not found")
            dialog.chat = chat_owner
            session.add(dialog)
            session.commit()
            session.refresh(dialog)
            return dialog

    def update(self, dialog: Dialog) -> None:
        with Session(self._engine) as session:
            session.merge(dialog)
            session.commit()
            session.refresh(dialog)

    def delete(self, dialog_id: int) -> None:
        with Session(self._engine) as session:
            dialog = session.get(Dialog, dialog_id)
            if dialog:
                session.delete(dialog)
                session.commit()
                session.refresh(dialog)

    def get(self, dialog_id: int) -> Dialog | None:
        with Session(self._engine) as session:
            return session.get(Dialog, dialog_id)

    def get_chat(self, chat_id: int) -> Chat:
        with Session(self._engine) as session:
            chat = session.get(Chat, chat_id)
            if chat is None:
                raise ValueError("Invalid chat id passed to the function")
            return chat


if __name__ == "__main__":
    from sqlmodel import create_engine, SQLModel
    from src.app.repositories.chat_repo import ChatRepository
    from ..models import *

    engine = create_engine("sqlite://", echo=True)
    SQLModel.metadata.create_all(engine)
    dialog_repo = DialogRepository(engine)
    chat_repo = ChatRepository(engine)

    chat = chat_repo.create(chat.ChatCreate())
    props = dialog.DialogCreate(chat_id=chat.id or -1, input="Oi")
    dialog = dialog_repo.create(props)
    print(dialog)
    print(f"chat: {dialog.chat}")
