# Dialogs API

This section provides a detailed reference for the Dialogs API endpoints.

## `POST /dialogs`

Creates a new dialog (sends a message) in a chat.

- **Authorization:** Bearer Token
- **Request Body:**
  ```json
  {
    "chat_id": "your_chat_id",
    "message": "Hello, Blabinha!"
  }
  ```
- **Response Body:**
  ```json
  {
    "id": "dialog_id",
    "message": "Hello, Blabinha!",
    "response": "Hello! How can I help you today?",
    "chat_id": "your_chat_id"
  }
  ```
