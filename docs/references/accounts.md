# Accounts API

This section provides a detailed reference for the Accounts API endpoints.

## `GET /users/me`

Retrieves the authenticated user's profile information.

- **Authorization:** Bearer Token
- **Response Body:**
  ```json
  {
    "id": "user_id",
    "email": "user@example.com",
    "is_active": true,
    "chats": []
  }
  ```

## `DELETE /users/me`

Deletes the authenticated user's account.

- **Authorization:** Bearer Token
- **Successful Response:** `204 No Content`

## `POST /users/register`

Creates a new user account.

- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "your_password"
  }
  ```
- **Response Body:**
  ```json
  {
    "id": "user_id",
    "email": "user@example.com",
    "is_active": true,
    "chats": []
  }
  ```
