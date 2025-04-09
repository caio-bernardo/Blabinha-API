from src.app.models.dialog import DialogCreate, DialogPublic
from src.app.repositories.chat_repo import ChatRepository
from src.app.repositories.dialog_repo import DialogRepository


class BlabinhaController:

    def __init__(
        self, chat_repo: ChatRepository, dialog_repo: DialogRepository
    ) -> None:
        self.chat_repo = chat_repo
        self.dialog_repo = dialog_repo

    # FIXME: solve this
    async def create_dialog(self, props: DialogCreate, api_key: str) -> DialogPublic:
        # Call blabinha

        # Save updates of chat, and dialog
        # Return a new public dialog
        ...
