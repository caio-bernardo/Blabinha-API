from sqlmodel import SQLModel, create_engine
import blabinha_api.config as config


class DatabaseConfig:
    def __init__(self):
        self._engine = create_engine(config.DATABASE_URL)

    @property
    def engine(self):
        return self._engine

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def drop_tables(self):
        SQLModel.metadata.drop_all(self.engine)
