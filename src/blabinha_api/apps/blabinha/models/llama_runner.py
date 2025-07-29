import transformers
import torch
import time
from typing import Any, Dict, List
from types import SimpleNamespace

model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]


def call(messages: List[Dict[str, Any]]) -> SimpleNamespace:
    """
    Chama o pipeline de Llama com `model_id` pré-definido e retorna um objeto compatível
    com OpenAI ChatCompletion, permitindo usar response.choices[0].message.content
    """
    # Constrói o prompt de conversação
    text = transformers.tokenization_utils_base.BatchEncoding({})  # placeholder se necessário
    # Caso o pipeline não tenha método apply_chat_template, adapte:
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Gera texto
    outputs = pipeline(
        text,
        max_new_tokens=256,
        pad_token_id=tokenizer.eos_token_id
    )

    full_text = outputs[0]["generated_text"]
    generated = full_text[len(text):].strip()

    # Cria estrutura de resposta
    resp_id = f"llama-{int(time.time())}"
    model_name = model_id
    finish_reason = 'stop'

    message = SimpleNamespace(role='assistant', content=generated)
    choice = SimpleNamespace(
        index=0,
        finish_reason=finish_reason,
        logprobs=None,
        message=message
    )
    usage = SimpleNamespace(prompt_tokens=0, completion_tokens=0, total_tokens=0)
    completion = SimpleNamespace(
        id=resp_id,
        object='chat.completion',
        created=int(time.time()),
        model=model_name,
        choices=[choice],
        usage=usage
    )

    print("test", completion.choices[0].message.content)
    return completion
