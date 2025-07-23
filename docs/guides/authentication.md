# Autenticação

A Blabinha API usa autenticação baseada em tokens para proteger suas rotas. Para acessar um recurso, é preciso obter um token de acesso e inclui-lo no _header_ `Authorization` em cada requisição. Se quiser saber mais sobr o modelo de auteticação [clique aqui](https://fastapi.tiangolo.com/tutorial/security/first-steps/).

## Criando um usuário

Antes de obtermos nosso token precisamos criar um usuário. Vá para o endpoint `/users/register` e faça uma requisição POST passado um email e uma senha:

**Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/users/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "********",
  "confirm_password": "********"
}'
```

**Response:**
```json
{
  "email": "user@example.com",
  "created_at": "2025-07-23T21:54:18.774Z",
  "updated_at": "2025-07-23T21:54:18.774Z",
  "chats": []
}
```

## Obtendo um token de autenticação

Agora, para obter o token, é necessário fazer uma requisição POST para `/auth/token` com o email e senha do usuário recém criado.

**Request:**

```bash
curl -X 'POST' \
    'http://localhost:8000/auth/token' \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d '{
        "username": "your-username",
        "password": "your-password" \
    }'
```

**Response:**

```json
{
  "access_token": "your-access-token",
  "refresh_token": "your-refresh-token",
  "token_type": "bearer"
}
```

## Using the Access Token

Once you have an access token, you need to include it in the `Authorization` header of your requests as a bearer token.

**Example:**

```bash
curl -X GET -H "Authorization: Bearer your-access-token" http://localhost:8000/users/me
```

## Refreshing the Access Token

Access tokens have a limited lifetime. When an access token expires, you can use a refresh token to obtain a new access token without having to re-enter your credentials.

To refresh your access token, send a POST request to the `/auth/refresh` endpoint with your refresh token.

**Request:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"refresh_token": "your-refresh-token"}' http://localhost:8000/auth/refresh
```

**Response:**

```json
{
  "access_token": "your-new-access-token",
  "refresh_token": "your-refresh-token",
  "token_type": "bearer"
}
```
