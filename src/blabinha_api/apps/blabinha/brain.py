import importlib
import sys
from typing import Any, Dict, List

# Mapeamento entre nome dado pelo usuário e módulo correspondente
MODEL_MODULES = {
    'gpt':    'blabinha_api.apps.blabinha.models.gpt_runner',
    'llama':  'blabinha_api.apps.blabinha.models.llama_runner',
    'qwen':   'blabinha_api.apps.blabinha.models.qwen_runner',
    'gemini': 'blabinha_api.apps.blabinha.models.gemini_runner',
}

# Módulo selecionado em tempo de execução
_selected_module = None


def select_model(model_name: str) -> None:
    """
    Seleciona o módulo do modelo escolhido e armazena-o em _selected_module.
    """
    global _selected_module
    module_path = MODEL_MODULES.get(model_name.lower())
    if not module_path:
        raise ValueError(
            f"Modelo '{model_name}' não suportado. Escolha entre: {', '.join(MODEL_MODULES.keys())}"
        )
    try:
        module = importlib.import_module(module_path)
    except ImportError as e:
        raise ImportError(f"Falha ao importar o módulo para '{model_name}': {e}")

    if not hasattr(module, 'call') or not callable(module.call):
        raise AttributeError(
            f"O módulo '{module_path}' deve definir uma função 'call(messages: List[Dict])'."
        )

    _selected_module = module
    print("Modelo selecionado2:", _selected_module)


def call(messages: List[Dict[str, Any]]) -> str:
    """
    Encaminha a lista de mensagens para o modelo selecionado e retorna a resposta em texto puro.

    messages: lista de dicionários no formato padrão de conversa,
              ex: [{"role": "user", "content": "Olá"}, ...]
    Retorna sempre uma string com o conteúdo da resposta do modelo.
    """
    if _selected_module is None:
        raise RuntimeError(
            "Nenhum modelo selecionado. Chame select_model(nome) antes de usar call()."
        )

    # Chama o runner do modelo
    raw_response = _selected_module.call(messages)


    print(raw_response)
    print("test1", raw_response.choices[0].message.content)
    return raw_response

#função 'main' somente para caso queira testar os modelos antes de integrá-los na Blabinha
if __name__ == '__main__':
    # Uso via CLI para teste rápido
    if len(sys.argv) >= 2:
        choice = sys.argv[1]
    else:
        choice = input("Escolha o modelo (Chatgpt, Llama, Qwen, Gemini): ")

    select_model(choice)
    print(f"Modelo '{choice}' selecionado. Digite suas mensagens (ou 'sair' para encerrar).\n")

    convo: List[Dict[str, str]] = []
    while True:
        user_msg = input("Você: ")
        if user_msg.lower() in ('sair', 'quit', 'exit'):
            break
        convo.append({"role": "user", "content": user_msg})

        response = call(convo)
        print (response)
        print(f"{choice}: {response}\n")
        convo.append({"role": "assistant", "content": response})        
