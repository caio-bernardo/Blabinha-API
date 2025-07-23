# Blabinha API

Documentação para a _Blabinha API_, uma API para o chatbot Blabinha construído com [FastAPI](https://https://fastapi.tiangolo.com/ ).

## Guias
Segue alguns guias para ações básicas na API.
- [Começando](./guides/getting-started.md)
- [Autenticação](./guides/authentication.md)
- [Chats e Diálogos](./guides/chat-and-dialogs.md)
- [Extra: usando o Swagger UI para testar a API](../guides/run-with-swaggerui.md)

## Arquitetura

A Blabinha API segue um arquitetura modular, onde diferentes serviços são organizados em módulos separados, a fim de manter uma melhor separação de funcionalidades. Uma inspiração do sistema de aplicações do [Django (reusable apps)](https://docs.djangoproject.com/en/5.2/intro/reusable-apps/).

Além disso, todos os recursos seguem um formato MVC(_Model View Controller_), contando com modelos para a base de dados, controlodores para acessar esses dados - nesse projeto iremos nos referir a eles como _serviços_ - e rotas para a API como _views_.

## Tecnologias
Abaixo, uma lista das tecnologias e ferramentas utilizadas.

- [**FastAPI**](https://fastapi.tiangolo.com/): Framework para desenvolvimento de APIs.
- [**SQLModel**](https://sqlmodel.tiangolo.com/): ORM, modelos e esquemas para a base de dados.
- [**Alembic**](https://alembic.sqlalchemy.org/en/latest/): Organização e execução de migrações
- [**SQLite**](https://sqlite.org/index.html): Base de dados.
- [**UV package manager**](https://docs.astral.sh/uv/): Gerenciador de dependências do projeto.
