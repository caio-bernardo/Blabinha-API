# Chats and Dialogs

This guide explains how to use the chat and dialog endpoints to interact with the Blabinha API.

## Chats

Chats represent conversations between a user and the chatbot. You can create, retrieve, and manage your chats using the `/chats` endpoints.

### Creating a Chat

To create a new chat, send a POST request to the `/chats` endpoint.

**Request:**

```bash
curl -X POST -H "Authorization: Bearer your-access-token" -H "Content-Type: application/json" -d '{"name": "My First Chat"}' http://localhost:8000/chats
```

### Listing Your Chats

To list your chats, send a GET request to the `/chats` endpoint.

**Request:**

```bash
curl -X GET -H "Authorization: Bearer your-access-token" http://localhost:8000/chats
```

## Dialogs

Dialogs represent the individual messages within a chat. You can send messages and get suggestions using the `/dialogs` endpoints.

### Sending a Message

To send a message, send a POST request to the `/dialogs` endpoint with the chat ID and the message content.

**Request:**

```bash
curl -X POST -H "Authorization: Bearer your-access-token" -H "Content-Type: application/json" -d '{"chat_id": "your-chat-id", "message": "Hello, Blabinha!"}' http://localhost:8000/dialogs
```

### Getting Suggestions

To get suggestions for what to say next, send a GET request to the `/chats/{chat_id}/suggestions` endpoint.

**Request:**

```bash
curl -X GET -H "Authorization: Bearer your-access-token" http://localhost:8000/chats/your-chat-id/suggestions
```
