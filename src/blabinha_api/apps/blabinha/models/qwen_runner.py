import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Any, Dict, List
from types import SimpleNamespace
import torch
try:
    device = "cuda" if torch.cuda.is_available() else "cpu"
except AssertionError:
    device = "cpu"


model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct",
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct")


def call(messages: List[Dict[str, Any]]) -> SimpleNamespace:
    """
    Chama diretamente o modelo Qwen e retorna um objeto compatível com OpenAI ChatCompletion,
    permitindo acessar response.choices[0].message.content
    """
    print(messages)
    # Prepara o prompt a partir das mensagens
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Tokeniza e move para o device
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    # Gera tokens
    generated_ids = model.generate(
        model_inputs.input_ids,
        attention_mask=model_inputs.attention_mask,
        max_new_tokens=512,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id
    )

    # Remove tokens de entrada
    output_ids = [
        output[len(inp):] for inp, output in zip(model_inputs.input_ids, generated_ids)
    ]

    # Decodifica resposta
    content = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]

    # Monta objetos para compatibilidade com ChatCompletion
    resp_id = f"Qwen-{int(time.time())}"
    model_name = getattr(model, 'name_or_path', 'Qwen-model')
    finish_reason = 'stop'

    message = SimpleNamespace(
        role='assistant',
        content=content
    )
    choice = SimpleNamespace(
        index=0,
        finish_reason=finish_reason,
        logprobs=None,
        message=message
    )
    usage = SimpleNamespace(
        prompt_tokens=len(model_inputs.input_ids[0]),
        completion_tokens=len(output_ids[0]),
        total_tokens=len(model_inputs.input_ids[0]) + len(output_ids[0])
    )
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
