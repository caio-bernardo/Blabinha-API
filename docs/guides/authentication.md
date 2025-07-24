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

Você receberá um _token de acesso_, um _token de recuperação_ e o tipo desses tokens.

```json
{
  "access_token": "your-access-token",
  "refresh_token": "your-refresh-token",
  "token_type": "bearer"
}
```

## Usando tokens de acesso

Uma vez com seu token de acesso, tudo que você precisa fazer é inclui-lo no header `Authorization` a cada requisição como um token do tipo `bearer` Veja abaixo:

**Examplo:**

```bash
curl -X GET -H "Authorization: Bearer your-access-token" http://localhost:8000/users/me
```

Esse token tem um tempo de vida curto (certa de algumas dezenas de minutos), isso é uma medida de segurança. Caso esse token seja comprometido, ele se tornará inútil depois de certo tempo. Para renovar o seu token de acesso é preciso do outro token, o de recuperação.

## Recuperando o token de acesso

Quando o seu token de acesso expira, você pode utilizar o token de recuperação para obter um novo sem precisar logar novamente.

Para recuperar seu token, faça uma requisição POST para `/auth/refresh` com o seu token de recuperação.

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

Agora que estamos autenticados, vamos para o próximo capítulo: [Chats e Diálogos](./chat-and-dialogs.md)
