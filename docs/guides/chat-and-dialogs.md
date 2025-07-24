# Chats e Diálogos

Esse capítulo explica como usar chat e dialogs (diálogos) para interagir com a API.

> Nota: é preciso estar autenticado (logado) para usar as rotas a seguir, volte para o capítulo de [autenticação](./authentication.md) se estiver com dúvida de como fazer isso.

## Chats

Um chat representa uma conversa entre o usuário e o chatbot Blabinha. Você pode criar e gerenciar chats, no endpoint `/chats`.

### Criando um chat

Para cria um novo chat envie uma requisção POST para `/chats`. Configure o modelo do seu chat, e, opcionalmente, a estratégia de prompt e o turno inicial.

**Request:**

```bash
curl -X POST -H "Authorization: Bearer your-access-token" -H "Content-Type: application/json" -d '{"model": "gpt-4o", "strategy": "one-shot", "initial_section": 100}' http://localhost:8000/chats
```

### Listando chats

Para listar os chats do seu usuário, envie uma requisição GET para `/chats`.

**Request:**

```bash
curl -X GET -H "Authorization: Bearer your-access-token" http://localhost:8000/chats
```

## Dialogs (Diálogos)

Dialogs (diálogos) representam mensagens individuais de um chat.

### Enviando uma mensagem

Para enviar uma mensage, faça uma requisição POST para `/dialogs` com o ID do chat e o conteúdo da mensagem.

**Request:**

```bash
curl -X POST -H "Authorization: Bearer your-access-token" -H "Content-Type: application/json" -d '{"chat_id": "your-chat-id", "message": "Olá, Blabinha!"}' http://localhost:8000/dialogs
```

### Sugestões

Para ter sugestões de tópicos para conversar, envie uma requisição GET para o endpoint `/chats/{chat_id}/suggestions`.

**Request:**

```bash
curl -X GET -H "Authorization: Bearer your-access-token" http://localhost:8000/chats/your-chat-id/suggestions
```

**Response:**
```json
[
  "sugestao A",
  "sugestao B",
  "sugestao C"
]
```
