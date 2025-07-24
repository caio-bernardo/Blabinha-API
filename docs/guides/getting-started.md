# Getting Started

Esse capítulo irá guiá-lo no processo de configurar e rodar localmente a Blabinha API para desenvolvimento e testes.

## Pré-requisitos

Antes de começar garante que esses sistemas estão instalados em sua máquina:

- **Python 3.12 ou maior**
- **Gerenciador de pacotes UV**:
Você instalá-lo através do `pip`:
```sh
pip install uv
```
Se estiver buscando adicionar novas dependências ou configurar o projeto, confira a documentação do `uv` aqui:
[uv astral](https://docs.astral.sh/uv/). Porém, vamos usar comandos mais simples.

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/caio-bernarndo/Blabinha-API.git
   cd blabinha2-api
   ```

2. **Instale as dependências:**
   ```bash
   uv sync
   ```
   Isto irá instalar as dependências do projeto e criar um ambiente virtual em `.venv`.
  > NOTA: Se você estiver no Windows talvez seja necessário instalar a biblioteca _tzdata_, execute o comando `uv add tzdata`.

3. **Configure as variáveis de ambiente:**
Crie um arquivo `.env` baseado no arquivo `.env.example`. Configure seus valores com o nome da base de dados, chaves de modelos de llms e outros. Veja exemplo:
```sh
DATABASE_URL=sqlite:///db.sqlite3

HASH_ALGORITHM=HS256
ACCESS_TOKEN_SECRET_KEY=senha-super-secreta
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_SECRET_KEY=outra-senha-super-secreta
# 2 dias mais ou menos
REFRESH_TOKEN_EXPIRE_MINUTES=2880

OPENAI_API_KEY=sua-chave-super-secreta
GEMINI_API_KEY=sua-outra-chave-super-secreta
```
**Recomenda-se**: não exponha essas chaves e secredos!

> Se estiver no linux o comando `openssl rand -hex 32` lhe dará uma sequência hexadecimal aleatória que serve como uma boa senha de segurança.

4. **(Opcional) Entre no ambiente virtual:**
Desse ponto em diante usaremos o prefixo `uv run` para executar migrar e rodar nossa aplicação, isso serve para rodar nossos scripts python dentro do ambiente virtual. Porém, você também pode iniciar o ambiente virtual dentro da sua shell: `source .venv/bin/activate`.

## Setup da base de dados

1. **Migre a base de dados:**

   ```bash
   uv run task migrate
   ```
   Esse comando vai criar a sua base de dados e criar as tabelas necessárias para rodar a API.

## Rodando a aplicação

1. **Inicie o server:**

   ```bash
   uv run task dev
   ```

  A API estará rodando no em `http://localhost:8000`. Você pode acessar o endpoint `http://localhost:8000/docs` para ver a documentação da API em tempo real.

Agora precisamos criar um usuário para utilizar os endpoints protegidos da API. Vá próximo capítulo: [Autenticação](./authentication.md).
