import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv


load_dotenv()


class DatabaseConfig:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "env var not found")
        self._engine = create_engine(self.database_url)

    @property
    def engine(self):
        return self._engine

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def drop_tables(self):
        SQLModel.metadata.drop_all(self.engine)


if __name__ == "__main__":
    from models import *

    dbconfig = DatabaseConfig()
    dbconfig.create_tables()
