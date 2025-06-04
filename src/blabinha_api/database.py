from alembic import command
from alembic.config import Config
from sqlmodel import SQLModel, create_engine
import blabinha_api.config as config


class DatabaseConfig:
    def __init__(self):
        self._engine = create_engine(config.DATABASE_URL)

    @property
    def engine(self):
        return self._engine

    def migrate(self, script_location="src/migrations", config_file="alembic.ini", revision="head"):
        try:
            config = Config(config_file)
            config.set_main_option("script_location", script_location)

            command.upgrade(config, revision)
            print("Migrations completed.")
        except Exception as e:
            print(f"Migrations failed. An error occured during execution: {e}")

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def drop_tables(self):
        SQLModel.metadata.drop_all(self.engine)
