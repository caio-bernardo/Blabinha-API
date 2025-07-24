# Rodando com o Swagger UI

O FastAPI vem com uma documentação integrada do _Swagger UI_ que espelha as ferramentas da aplicação. Você pode confir-la no endpoint `/docs`. Essa documentação é **interativa**, então você rodar os comandos vistos nas outras seções de modo mais **amigável**.

## Autenticando

Procure pela seção `users` e clique na rota `/users/register`, e então aperte o botão `Try it out`. Preencha o campo json, com um email e senhas, e clique em `Execute`, veja o resultado no campo `Responses`. Se tudo ocorreu bem, suba para o inicio da tela. Então clique no botão com um cadeado escrito `Authorize` (ou clique em qualquer cadeado das rotas). Preencha o email e senha que você acabou de criar. Pronto, você está logado! Pode usar as outras rotas normalmente.

## Criando chats e diálogos

Vá para a seção `chats` e clique no endpoint `POST /chats` (também marcado com 'Create chats'). Aperte em `Try it Out`, preencha a seção em json e clique em `Execute`. Isto devolverá um json contendo o ID do seu chat, salve ele em algum lugar.

Para criar um diálogo, repita as etapas anteriores e procure por `POST /dialogs`, `Try it out`, preencha no json o ID do seu Chat e a mensagem, clique em `Execute`. Essa resposta demorará um pouco mais. Espere e você terá sua resposta, continue escrevendo mensagens e enviando-as até encerrar a conversa.
