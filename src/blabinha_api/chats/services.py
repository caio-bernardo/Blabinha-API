import uuid
from sqlmodel import Session, select
from .models import Chat
from .schemas import ChatCreate, ChatUpdate
from uuid import UUID

async def get_one(session: Session, id: UUID) -> Chat:
    return session.get_one(Chat, id) # TODO: await with Async Session

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
