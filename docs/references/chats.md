# Chats API

This section provides a detailed reference for the Chats API endpoints.

## `GET /chats`

Retrieves a list of the authenticated user's chats.

- **Authorization:** Bearer Token
- **Response Body:**
  ```json
  [
    {
      "id": "chat_id",
      "name": "My First Chat",
      "user_id": "user_id"
    }
  ]
  ```

## `GET /chats/{id}`

Retrieves a specific chat by its ID.

- **Authorization:** Bearer Token
- **Path Parameter:** `id` (string, required)
- **Response Body:**
  ```json
  {
    "id": "chat_id",
    "name": "My First Chat",
    "user_id": "user_id",
    "dialogs": []
  }
  ```

## `POST /chats`

Creates a new chat.

- **Authorization:** Bearer Token
- **Request Body:**
  ```json
  {
    "name": "My First Chat"
  }
  ```
- **Response Body:**
  ```json
  {
    "id": "chat_id",
    "name": "My First Chat",
    "user_id": "user_id",
    "dialogs": []
  }
  ```

## `PATCH /chats/{id}`

Updates a chat's information.

- **Authorization:** Bearer Token
- **Path Parameter:** `id` (string, required)
- **Request Body:**
  ```json
  {
    "name": "My Updated Chat"
  }
  ```
- **Response Body:**
  ```json
  {
    "id": "chat_id",
    "name": "My Updated Chat",
    "user_id": "user_id"
  }
  ```

## `DELETE /chats/{id}`

Deletes a chat.

- **Authorization:** Bearer Token
- **Path Parameter:** `id` (string, required)
- **Successful Response:** `204 No Content`

## `GET /chats/{id}/suggestions`

Retrieves conversation suggestions for a chat.

- **Authorization:** Bearer Token
- **Path Parameter:** `id` (string, required)
- **Response Body:**
  ```json
  [
    "Suggestion 1",
    "Suggestion 2"
  ]
  ```
