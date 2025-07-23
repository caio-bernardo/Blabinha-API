# Auth API

This section provides a detailed reference for the Authentication API endpoints.

## `POST /auth/token`

Authenticates a user and returns an access token and a refresh token.

- **Request Body:**
  ```json
  {
    "username": "user@example.com",
    "password": "your_password"
  }
  ```
- **Response Body:**
  ```json
  {
    "access_token": "your_access_token",
    "refresh_token": "your_refresh_token",
    "token_type": "bearer"
  }
  ```

## `POST /auth/refresh`

Refreshes an expired access token using a refresh token.

- **Request Body:**
  ```json
  {
    "refresh_token": "your_refresh_token"
  }
  ```
- **Response Body:**
  ```json
  {
    "access_token": "your_new_access_token",
    "refresh_token": "your_refresh_token",
    "token_type": "bearer"
  }
  ```
