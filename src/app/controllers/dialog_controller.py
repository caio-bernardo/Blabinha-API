from fastapi import HTTPException, status
from pydantic import ValidationError
from src.app.models.chat import ChatPublic
from src.app.models.dialog import DialogCreate, DialogPublic, DialogPublicWithChat
from src.app.repositories.dialog_repo import DialogRepository

DialogPublicWithChat.model_rebuild()


class DialogController:
    """Controls request interaction with Database"""

    def __init__(self, repo: DialogRepository) -> None:
        self.repo = repo

    async def get_dialog(self, dialog_id: int) -> DialogPublicWithChat:
        try:
            dialog = self.repo.get(dialog_id)
            if dialog is None:
                raise TypeError(f"dialog: {id}, not found.")
            return DialogPublicWithChat(
                id=dialog.id or -1,
                answer=dialog.answer,
                chat=ChatPublic.model_validate(dialog.chat),
                input=dialog.input,
                tokens=dialog.tokens,
                section=dialog.section,
                created_at=dialog.created_at,
            )
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_dialog(self, dialog_props: DialogCreate) -> DialogPublicWithChat:
        try:
            dialog = self.repo.create(dialog_props)
            owner = self.repo.get_chat(dialog.chat_id or -1)
            assert owner
            return DialogPublicWithChat(
                id=dialog.id or -1,
                answer=dialog.answer,
                input=dialog.input,
                section=dialog.section,
                tokens=dialog.tokens,
                created_at=dialog.created_at,
                chat=ChatPublic.model_validate(owner),
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_dialog(self, dialog_id: int) -> None:
        try:
            self.repo.delete(dialog_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
