<img width="100%" height="150" alt="Blabinha_API_@_2 0" src="https://github.com/user-attachments/assets/bb817cc5-b0ea-4ceb-9b15-0892dc8ad597" />

---
<p align=center><strong>Web API para o chatbot Blabinha.</strong></p>

## Sobre
Um servidor HTTP REST, que expõe o chat-bot Blabinha através da rede, como um serviço de API, permitindo a criação de conversas utilizando diferentes modelos de LLMs e estratégias de prompt. Ligado ao projeto _Blabinha 2.0: um agente conversacional baseado em inteligência artificial generativa, especialista na Amazônia Azul_, do laboratório _Center for Artificial Intelligence_ (C4AI) da Universidade de São Paulo.

## _Features_

- Criar chats: sessões permanentes entre requisições;
- Criar diálogos (_dialogs_): uma seção de conversa com um chat (pergunta e resposta);
- Recuperar dados sobre chats ou diálogos anteriores;
- Editar e apagar dados referentes a chats e diálogos.

## Tecnologias utilizadas

- [FastAPI](https://fastapi.tiangolo.com/), para desenvolver os endpoints e o servidor _HTTP_;
- [SQLModel](https://sqlmodel.tiangolo.com/), para modelar a base de dados e validar as requisições;
- [Alembic](https://alembic.sqlalchemy.org/en/latest/), para organizar e rodar as migrações da base de dados;
- [SQLite](https://sqlite.org/index.html), a base de dados, para armazenar as interações com a Blabinha e armazenar _logs_;
- [UV package manager](https://docs.astral.sh/uv/), para genrenciar e instalar as dependências do projeto.

## Como usar a API

1. Crie um chat com `POST URL/chats`, com o modelo de LLM desejad e a estratégia de prompt preferida, e - opcionalmente - a seção que se deseja começar, para iniciar do 'zero' o valor padrão é `100`. A resposta será em _json_ no _schema_ `Chat`, contendo o atributo `id`. **Armazene esse id** para referênciar o chat nas próximas interações;
2. Interaja com o chat por meio de diálogos, com requisições do tipo `POST URL/dialogs`, enviando o **id do chat** e o **input desejado**, bem como a chave de API do modelo de LLM escolhido, através do _headers_ no campo `Authorization`, com o formato _Bearer_. A resposta será em _json_, no esquema `Dialog`, que contém a resposta gerada por IA, informações sobre aquela seção, e o `Chat` pertencente atualizado.

Veja um exemplo:

- Criando um chat
```bash
curl -X POST http://localhost:8000/chats -d '{"model": "gpt-4o"}' -H 'Content-Type: application/json'
```
- Criando dialogs
```bash
curl -X POST http://localhost:8000/dialogs -d '{"chat_id": X, "input": "Oi"}' -H 'Content-Type: application/json' -H 'Authorization: Bearer XXXXXXXX'
```

Para mais informações refira-se à documentação em `URL/docs`.

> `URL` refere-se ao endereço da que API está rodando, se ela estiver localmente, será algo como `http://localhost:8000`, ou similar. Em produção o endereço será fornecido pelo provedor.

### Windows

Antes de tudo verifique se o comando utilitário `curl` está instalado:
```bash
curl --version
```
Se sim, tudo está certo :smile, você pode seguir os exemplos anteriores. Caso contrário, siga este [link](https://curl.se/windows/), e instale o `curl` na sua máquina.

Ou utilize uma aplicação de software que testem requisições HTTP, como [Postman](https://www.postman.com/downloads/) ou [Insomnia](https://insomnia.rest/download).

## Como rodar a API

1. Clone este repositório: `git clone git@github.com:caio-bernardo/Blabinha2-API.git`;
1.2. **Recomenda-se fortemenete** o uso do package manager `uv`, a instalação é simples: `pip install uv`, se deseja mais informações [clique aqui](https://docs.astral.sh/uv/);
2. Crie um arquivo chamado `.env` seguindo o exemplo em `.env.example`. Preencha as variaveis de ambiente.
3. Crie a base de dados com o comando `uv run task migrate`. Verifique se um arquivo `db.sqlite3` foi criado na raíz do projeto.
3. Rode a API com o seguinte comando `uv run task run`

> Na primeira vez que você executar o _uv_ ele irá instalar todos os pacotes necessários e criar uma pasta _.venv_ na raíz do seu projeto. Essa pasta pode ser usada como ambiente virtual, e ativada com `source ./.venv/bin/activate` (e sua versão do Windows). Se decidir iniciar o ambiente virtual, pode executar todos os comandos demonstrados sem a necessidade do `uv run`.

## Desenvolvendo a API

1. Siga as instruções do tópico anterior
1. Para rodar a aplicação em **modo de desenvolvimento**, execute `uv run task dev`

> Lembre-se de criar uma nova _branch_, quando for fazer alterações ao código.

### Fazendo migrações

Ao fazer alterações nos modelos que representam tabelas, é preciso atualizar a base de dados, chamamos isso de **migrações**.
Para fazer isso é preciso executar o comando `alembic`. Veja o exemplo:

Para fazer uma migração:
```bash
alembic revision --autogenerate -m "campo adicionado na tabela x"
alembic upgrade head
```

Para reverter alterações:
```bash
alembic downgrade -1
```
