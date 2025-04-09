from src.app.models.dialog import DialogCreate, Dialog
from sqlmodel import Session


class DialogRepository:
    def __init__(self, engine):
        self._engine = engine

    def create(self, dialog_props: DialogCreate) -> Dialog:
        # TODO: implement proper creation with Blabinha
        with Session(self._engine) as session:
            dialog = Dialog.model_validate(dialog_props)
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
