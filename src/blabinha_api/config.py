"""
Configurações da aplicação

Incluindo variáveis de ambiente. Exporta um objeto singleton com as configurações do projeto.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    """Configurações do projeto. Carrega as variáveis de ambiente de mesmo nome (snake_case para SCREAM_CASE)"""
    app_name: str
    app_version: str = "1.0.0"
    database_url: str

    hash_algorithm: str
    access_token_secret_key: str
    access_token_expire_minutes: int
    refresh_token_secret_key: str
    refresh_token_expire_minutes: int

    openai_api_key: str
    model_config = SettingsConfigDict(env_file=".env")

# Declara um singleton para as configurações
# NOTE: pode ser que haja um warning de _missing arguments_,
# isso é por que o linter não entende que os atributos são carregados dinâmicamente
# Apenas ignore
settings = Settings()
