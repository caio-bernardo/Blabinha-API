"""
Configuration and Settings of the application.

Including env variables.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    app_name: str
    database_url: str

    hash_algorithm: str
    access_token_secret_key: str
    access_token_expire_minutes: int
    refresh_token_secret_key: str
    refresh_token_expire_minutes: int

    openai_api_key: str
    model_config = SettingsConfigDict(env_file=".env")

config = Settings()
