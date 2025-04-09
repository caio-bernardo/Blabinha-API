from pydantic import ValidationError
from starlette import status
from starlette.exceptions import HTTPException
from src.app.models.dialog import DialogCreate, DialogPublic
from src.app.repositories.dialog_repo import DialogRepository


class DialogController:
    """Controls request interaction with Database"""

    def __init__(self, repo: DialogRepository) -> None:
        self.repo = repo

    async def get_dialog(self, dialog_id: int) -> DialogPublic:
        try:
            dialog = self.repo.get(dialog_id)
            if dialog is None:
                raise TypeError(f"dialog: {id}, not found.")
            return DialogPublic.model_validate(dialog)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_dialog(self, dialog_props: DialogCreate) -> DialogPublic:
        try:
            dialog = self.repo.create(dialog_props)
            return DialogPublic.model_validate(dialog)
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
