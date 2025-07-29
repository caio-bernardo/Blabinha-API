import getpass
import os
import time
from typing import Any, Dict, List
from types import SimpleNamespace

from langchain.chat_models import init_chat_model

# Inicializa a API key se não definida
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

# Inicializa o modelo (mude o nome conforme desejar)
model = init_chat_model("gpt-3.5-turbo", model_provider="openai")
print(f"[DEBUG] Iniciando modelo com nome: {model}")


def call(messages: List[Dict[str, Any]]) -> SimpleNamespace:
    """
    Chama LangChain e retorna um objeto compatível com OpenAI ChatCompletion,
    permitindo acessar response.choices[0].message.content.upper().
    """
    print(messages)
    # Invoca o modelo
    result = model.invoke(messages)

    # Extrai campos básicos
    content = getattr(result, 'content', None)
    if content is None:
        # Caso LangChain retorne outra estrutura
        content = str(result)
    resp_id = getattr(result, 'id', f"langchain-{int(time.time())}")
    model_name = getattr(result, 'model_name', None) or getattr(model, 'model_name', 'gpt-3.5-turbo')
    finish_reason = getattr(result, 'finish_reason', 'stop')
    print("model name", model_name)

    # Monta a estrutura de ChatCompletion
    message = SimpleNamespace(
        role="assistant",
        content=content
    )
    choice = SimpleNamespace(
        index=0,
        finish_reason=finish_reason,
        logprobs=None,
        message=message
    )
    usage = SimpleNamespace(
        prompt_tokens=getattr(result, 'input_tokens', 0),
        completion_tokens=getattr(result, 'output_tokens', 0),
        total_tokens=getattr(result, 'total_tokens', 0)
    )
    completion = SimpleNamespace(
        id=resp_id,
        object="chat.completion",
        created=int(time.time()),
        model=model_name,
        choices=[choice],
        usage=usage
    )
    print("test", completion.choices[0].message.content)
    return completion
