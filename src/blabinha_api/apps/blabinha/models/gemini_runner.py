import getpass
import os
import time
from typing import Any, Dict, List
from types import SimpleNamespace
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage

# Configura API key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

# Inicializa o LLM com LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def call(messages: List[Dict[str, Any]]) -> SimpleNamespace:
    """
    Chama o modelo via LangChain ChatGoogleGenerativeAI e retorna um objeto
    compatível com OpenAI ChatCompletion.
    """
    print(messages)

    # Verifica se existe alguma mensagem com role "user"
    has_user_message = any(m.get("role") == "user" for m in messages)

    # Se não houver, insere uma mensagem "user" genérica após a system
    if not has_user_message:
        # Encontra o índice da última mensagem "system"
        last_system_idx = -1
        for i, m in enumerate(messages):
            if m.get("role") == "system":
                last_system_idx = i
        # Insere uma mensagem "user" genérica logo depois
        generic_user_msg = {
            "role": "user",
            "content": "Ok! Pode seguir com a instrução acima."
        }
        messages.insert(last_system_idx + 1, generic_user_msg)

    # Converte para mensagens LangChain
    lc_msgs = []
    for m in messages:
        role = m.get("role")
        content = m.get("content", "")
        if role == "system":
            lc_msgs.append(SystemMessage(content=content))
        elif role == "user":
            lc_msgs.append(HumanMessage(content=content))
        # Ignora assistant

    # Chama o modelo
    result = llm.generate([lc_msgs])
    text = result.generations[0][0].text

    # Monta a resposta no formato OpenAI ChatCompletion
    resp_id = f"gemini-{int(time.time())}"
    message = SimpleNamespace(role="assistant", content=text)
    choice = SimpleNamespace(index=0, finish_reason="stop", logprobs=None, message=message)
    usage = SimpleNamespace(prompt_tokens=0, completion_tokens=0, total_tokens=0)
    completion = SimpleNamespace(
        id=resp_id,
        object="chat.completion",
        created=int(time.time()),
        model=llm.model,
        choices=[choice],
        usage=usage
    )
    return completion
