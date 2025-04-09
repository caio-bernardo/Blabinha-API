from fastapi.param_functions import Depends
from src.app.controllers.blabinha_controller import BlabinhaController
from src.app.database import DatabaseConfig
from src.app.repositories.chat_repo import ChatRepository
from src.app.repositories.dialog_repo import DialogRepository

from src.app.controllers.chat_controller import ChatController
from src.app.controllers.dialog_controller import DialogController

dbconfig = DatabaseConfig()


def get_chat_repo():
    return ChatRepository(dbconfig.engine)


def get_dialog_repo():
    return DialogRepository(dbconfig.engine)


def get_chat_controller(connectorChat=Depends(get_chat_repo)):
    return ChatController(connectorChat)


def get_dialog_controller(connectorDialog=Depends(get_dialog_repo)):
    return DialogController(connectorDialog)


def get_blabinha_controller(
    connectorChat=Depends(get_chat_repo), connectorDialog=Depends(get_dialog_repo)
):
    # TODO: add api key
    return BlabinhaController(connectorChat, connectorDialog)
